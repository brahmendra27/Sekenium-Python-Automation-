"""Report ingester for parsing and storing pytest-json-report files."""

import json
import logging
from pathlib import Path

from dashboard.db import Database
from dashboard.models import IngestResult

logger = logging.getLogger(__name__)


class IngestionError(Exception):
    """Raised when report ingestion fails."""

    pass


class ReportIngester:
    """Parses pytest-json-report files and ingests them into the database."""

    def parse_report(self, file_path: str) -> dict:
        """Parse a pytest-json-report file and extract run/test data.

        Args:
            file_path: Path to the report JSON file.

        Returns:
            A dict with run-level and test-level data ready for DB insertion.

        Raises:
            IngestionError: If the file is missing, invalid, or malformed.
        """
        path = Path(file_path)
        if not path.exists():
            raise IngestionError(f"File not found: {file_path}")

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise IngestionError(f"Invalid JSON in {file_path}: {e}")

        # Validate required top-level fields
        for field in ("created", "summary", "tests"):
            if field not in data:
                raise IngestionError(f"Missing required field: {field}")

        summary = data["summary"]
        for field in ("passed", "failed", "skipped", "total"):
            if field not in summary:
                # pytest-json-report omits fields with 0 count
                summary[field] = 0

        # Extract test-level data
        tests = []
        for test_entry in data.get("tests", []):
            nodeid = test_entry.get("nodeid", "")
            outcome = test_entry.get("outcome", "skipped")
            call = test_entry.get("call", {})
            duration = call.get("duration", 0.0) if call else 0.0
            keywords = test_entry.get("keywords", [])
            error_message = None
            longrepr = None

            if call:
                crash = call.get("crash", {})
                if crash:
                    error_message = crash.get("message")
                longrepr = call.get("longrepr")

            tests.append({
                "nodeid": nodeid,
                "outcome": outcome,
                "duration": duration,
                "keywords": keywords,
                "error_message": error_message,
                "longrepr": longrepr,
            })

        return {
            "created": data["created"],
            "duration": data.get("duration", 0.0),
            "passed": summary["passed"],
            "failed": summary["failed"],
            "skipped": summary["skipped"],
            "total": summary["total"],
            "collected": summary.get("collected", summary["total"]),
            "root": data.get("root", ""),
            "source_path": str(file_path),
            "tests": tests,
        }

    def ingest(self, file_path: str, db: Database) -> IngestResult:
        """Parse and ingest a report file into the database.

        Args:
            file_path: Path to the report JSON file.
            db: Database instance to insert data into.

        Returns:
            IngestResult with run_id and summary counts.

        Raises:
            IngestionError: If parsing or insertion fails.
        """
        parsed = self.parse_report(file_path)

        # Check for duplicates
        if db.run_exists(parsed["created"], parsed["root"]):
            logger.warning(
                f"Duplicate report detected (created={parsed['created']}, "
                f"root={parsed['root']}). Skipping."
            )
            return IngestResult(
                run_id="duplicate",
                passed=parsed["passed"],
                failed=parsed["failed"],
                skipped=parsed["skipped"],
                total=parsed["total"],
                message="Duplicate report - already ingested",
            )

        try:
            run_id = db.insert_run(parsed)
        except Exception as e:
            raise IngestionError(f"Database write failure: {e}")

        return IngestResult(
            run_id=run_id,
            passed=parsed["passed"],
            failed=parsed["failed"],
            skipped=parsed["skipped"],
            total=parsed["total"],
            message=f"Successfully ingested run {run_id}",
        )
