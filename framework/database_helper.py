# framework/database_helper.py

"""
Database Query Helpers for various database backends.

Supports:
  - Generic SQL database queries via JDBC subprocess (Informix, Oracle, etc.)
  - Direct Python database connections (PostgreSQL, MySQL, SQLite)
  - Query result parsing to List[Dict]
  - Context manager support
  - Allure step integration

Usage:
    # JDBC-based (Informix, Oracle)
    db = JDBCDatabaseHelper(
        jdbc_url="jdbc:informix-sqli://host:1523/db:INFORMIXSERVER=server",
        driver_jar="path/to/jdbc-driver.jar",
        username="user", password="pass"
    )
    rows = db.query("SELECT * FROM orders WHERE status = 'pending'")

    # Direct Python (PostgreSQL, MySQL, SQLite)
    db = SQLDatabaseHelper(
        connection_string="postgresql://user:pass@host:5432/db"
    )
    rows = db.query("SELECT * FROM orders LIMIT 10")
"""

import json
import logging
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Any, Optional
import allure

logger = logging.getLogger(__name__)


class JDBCDatabaseHelper:
    """Database helper using JDBC via Java subprocess.

    Useful for databases without good Python drivers (Informix, some Oracle versions).
    Compiles a small Java class on first use, then shells out to Java for each query.
    """

    JAVA_RUNNER = """
import java.sql.*;
import java.util.*;

public class JDBCRunner {
    public static void main(String[] args) throws Exception {
        String url = args[0];
        String user = args[1];
        String pass = args[2];
        String sql = args[3];

        Connection conn = DriverManager.getConnection(url, user, pass);
        try {
            if (sql.trim().toUpperCase().startsWith("SELECT")) {
                Statement stmt = conn.createStatement();
                ResultSet rs = stmt.executeQuery(sql);
                ResultSetMetaData meta = rs.getMetaData();
                int cols = meta.getColumnCount();

                System.out.print("[");
                boolean first = true;
                while (rs.next()) {
                    if (!first) System.out.print(",");
                    System.out.print("{");
                    for (int i = 1; i <= cols; i++) {
                        if (i > 1) System.out.print(",");
                        String name = meta.getColumnLabel(i);
                        String val = rs.getString(i);
                        System.out.print("\\"" + name + "\\":");
                        if (val == null) System.out.print("null");
                        else System.out.print("\\"" + val.replace("\\\\", "\\\\\\\\").replace("\\"", "\\\\\\"") + "\\"");
                    }
                    System.out.print("}");
                    first = false;
                }
                System.out.println("]");
                rs.close();
                stmt.close();
            } else {
                Statement stmt = conn.createStatement();
                int affected = stmt.executeUpdate(sql);
                System.out.println("{\\"affected\\":" + affected + "}");
                stmt.close();
            }
        } finally {
            conn.close();
        }
    }
}
"""

    def __init__(self, jdbc_url: str = "", driver_jar: str = "",
                 username: str = "", password: str = "",
                 java_home: str = ""):
        """Initialize JDBC database helper.

        Args:
            jdbc_url: JDBC connection URL
            driver_jar: Path to JDBC driver JAR file
            username: Database username
            password: Database password
            java_home: Path to Java installation (auto-detected if empty)
        """
        self.jdbc_url = jdbc_url or os.environ.get("JDBC_URL", "")
        self.driver_jar = driver_jar or os.environ.get("JDBC_DRIVER_JAR", "")
        self.username = username or os.environ.get("DB_USERNAME", "")
        self.password = password or os.environ.get("DB_PASSWORD", "")
        self.java_home = java_home
        self._compiled = False
        self._temp_dir = tempfile.mkdtemp(prefix="jdbc_runner_")

    def _compile_runner(self):
        """Compile the Java JDBC runner class."""
        if self._compiled:
            return

        java_file = Path(self._temp_dir) / "JDBCRunner.java"
        java_file.write_text(self.JAVA_RUNNER)

        javac = "javac"
        if self.java_home:
            javac = str(Path(self.java_home) / "bin" / "javac")

        result = subprocess.run(
            [javac, "-cp", self.driver_jar, str(java_file)],
            capture_output=True, text=True, cwd=self._temp_dir
        )
        if result.returncode != 0:
            raise RuntimeError(f"Java compilation failed: {result.stderr}")

        self._compiled = True
        logger.info("JDBC runner compiled successfully")

    def _run_java(self, sql: str) -> str:
        """Execute SQL via Java subprocess.

        Args:
            sql: SQL query string

        Returns:
            Raw JSON output from Java
        """
        self._compile_runner()

        java = "java"
        if self.java_home:
            java = str(Path(self.java_home) / "bin" / "java")

        result = subprocess.run(
            [java, "-cp", f"{self.driver_jar}{os.pathsep}{self._temp_dir}",
             "JDBCRunner", self.jdbc_url, self.username, self.password, sql],
            capture_output=True, text=True, timeout=60
        )

        if result.returncode != 0:
            raise RuntimeError(f"JDBC query failed: {result.stderr}")

        return result.stdout.strip()

    @allure.step("JDBC Query: {sql}")
    def query(self, sql: str) -> List[Dict[str, Any]]:
        """Execute SELECT query and return rows as list of dicts.

        Args:
            sql: SELECT SQL query

        Returns:
            List of row dicts
        """
        logger.info(f"JDBC query: {sql[:200]}")
        output = self._run_java(sql)
        rows = json.loads(output)
        logger.info(f"JDBC returned {len(rows)} rows")
        return rows

    @allure.step("JDBC Execute: {sql}")
    def execute(self, sql: str) -> int:
        """Execute INSERT/UPDATE/DELETE and return affected row count.

        Args:
            sql: DML SQL statement

        Returns:
            Number of affected rows
        """
        logger.info(f"JDBC execute: {sql[:200]}")
        output = self._run_java(sql)
        result = json.loads(output)
        affected = result.get("affected", 0)
        logger.info(f"JDBC affected {affected} rows")
        return affected

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def close(self):
        """Cleanup temp files."""
        import shutil
        try:
            shutil.rmtree(self._temp_dir, ignore_errors=True)
        except Exception:
            pass


class SQLDatabaseHelper:
    """Database helper using Python's built-in database drivers.

    Supports PostgreSQL (psycopg2), MySQL (mysql-connector), SQLite.
    """

    def __init__(self, connection_string: str = "", db_type: str = "sqlite"):
        """Initialize SQL database helper.

        Args:
            connection_string: Database connection string or path
            db_type: Database type ('sqlite', 'postgresql', 'mysql')
        """
        self.connection_string = connection_string or os.environ.get(
            "SQL_CONNECTION_STRING", ":memory:"
        )
        self.db_type = db_type
        self.connection = None

    def connect(self):
        """Establish database connection."""
        if self.db_type == "sqlite":
            import sqlite3
            self.connection = sqlite3.connect(self.connection_string)
            self.connection.row_factory = sqlite3.Row
        elif self.db_type == "postgresql":
            import psycopg2
            import psycopg2.extras
            self.connection = psycopg2.connect(self.connection_string)
        elif self.db_type == "mysql":
            import mysql.connector
            self.connection = mysql.connector.connect(
                connection_string=self.connection_string
            )
        logger.info(f"Connected to {self.db_type} database")

    @allure.step("SQL Query: {sql}")
    def query(self, sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute SELECT query with parameterized values.

        Args:
            sql: SELECT SQL with ? or %s placeholders
            params: Query parameters (prevents SQL injection)

        Returns:
            List of row dicts
        """
        if not self.connection:
            self.connect()

        cursor = self.connection.cursor()
        cursor.execute(sql, params)
        columns = [desc[0] for desc in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.close()
        logger.info(f"SQL returned {len(rows)} rows")
        return rows

    @allure.step("SQL Execute: {sql}")
    def execute(self, sql: str, params: tuple = ()) -> int:
        """Execute INSERT/UPDATE/DELETE with parameterized values.

        Args:
            sql: DML SQL with ? or %s placeholders
            params: Query parameters (prevents SQL injection)

        Returns:
            Number of affected rows
        """
        if not self.connection:
            self.connect()

        cursor = self.connection.cursor()
        cursor.execute(sql, params)
        self.connection.commit()
        affected = cursor.rowcount
        cursor.close()
        logger.info(f"SQL affected {affected} rows")
        return affected

    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
