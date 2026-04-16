"""
CSV Logger for Test Validation Results.

This module provides utilities to log test data and validation results to CSV files.
Useful for tracking registration details, order details, and test outcomes.
"""

import csv
import os
from datetime import datetime
from pathlib import Path


class CSVLogger:
    """Logger for writing test validation results to CSV files."""
    
    def __init__(self, output_dir="reports/csv"):
        """
        Initialize CSV Logger.
        
        Args:
            output_dir: Directory to store CSV files (default: reports/csv)
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def log_registration(self, test_name, registration_data, status, error_message=""):
        """
        Log user registration details to CSV.
        
        Args:
            test_name: Name of the test
            registration_data: Dictionary with registration details
            status: Test status (PASS/FAIL)
            error_message: Error message if test failed
        """
        csv_file = self.output_dir / "registration_results.csv"
        
        # Check if file exists to determine if we need headers
        file_exists = csv_file.exists()
        
        # Prepare row data
        row = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Test Name": test_name,
            "Status": status,
            "First Name": registration_data.get("first_name", ""),
            "Last Name": registration_data.get("last_name", ""),
            "Email": registration_data.get("email", ""),
            "Phone": registration_data.get("phone", ""),
            "Address": registration_data.get("address", ""),
            "City": registration_data.get("city", ""),
            "Postcode": registration_data.get("postcode", ""),
            "Login Name": registration_data.get("login_name", ""),
            "Password": "***HIDDEN***",  # Never log actual passwords
            "Error Message": error_message
        }
        
        # Write to CSV
        with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=row.keys())
            
            # Write header if file is new
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(row)
        
        print(f"📝 Registration data logged to: {csv_file}")
        return csv_file
    
    def log_order(self, test_name, order_data, status, error_message=""):
        """
        Log order details to CSV.
        
        Args:
            test_name: Name of the test
            order_data: Dictionary with order details
            status: Test status (PASS/FAIL)
            error_message: Error message if test failed
        """
        csv_file = self.output_dir / "order_results.csv"
        
        file_exists = csv_file.exists()
        
        # Prepare row data
        row = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Test Name": test_name,
            "Status": status,
            "Order ID": order_data.get("order_id", "N/A"),
            "Customer Name": order_data.get("customer_name", ""),
            "Email": order_data.get("email", ""),
            "Product Name": order_data.get("product_name", ""),
            "Quantity": order_data.get("quantity", ""),
            "Unit Price": order_data.get("unit_price", ""),
            "Total Price": order_data.get("total_price", ""),
            "Payment Method": order_data.get("payment_method", ""),
            "Shipping Address": order_data.get("shipping_address", ""),
            "Order Status": order_data.get("order_status", ""),
            "Error Message": error_message
        }
        
        # Write to CSV
        with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=row.keys())
            
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(row)
        
        print(f"📝 Order data logged to: {csv_file}")
        return csv_file
    
    def log_cart_operation(self, test_name, cart_data, status, error_message=""):
        """
        Log shopping cart operations to CSV.
        
        Args:
            test_name: Name of the test
            cart_data: Dictionary with cart details
            status: Test status (PASS/FAIL)
            error_message: Error message if test failed
        """
        csv_file = self.output_dir / "cart_operations.csv"
        
        file_exists = csv_file.exists()
        
        row = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Test Name": test_name,
            "Status": status,
            "Operation": cart_data.get("operation", ""),  # add, remove, update
            "Product Name": cart_data.get("product_name", ""),
            "Quantity": cart_data.get("quantity", ""),
            "Price": cart_data.get("price", ""),
            "Cart Total": cart_data.get("cart_total", ""),
            "Items in Cart": cart_data.get("items_count", ""),
            "Error Message": error_message
        }
        
        with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=row.keys())
            
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(row)
        
        print(f"📝 Cart operation logged to: {csv_file}")
        return csv_file
    
    def log_validation(self, test_name, validation_type, expected, actual, status, notes=""):
        """
        Log validation results to CSV.
        
        Args:
            test_name: Name of the test
            validation_type: Type of validation (e.g., "Email Format", "Password Match")
            expected: Expected value
            actual: Actual value
            status: Validation status (PASS/FAIL)
            notes: Additional notes
        """
        csv_file = self.output_dir / "validation_results.csv"
        
        file_exists = csv_file.exists()
        
        row = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Test Name": test_name,
            "Validation Type": validation_type,
            "Expected": str(expected),
            "Actual": str(actual),
            "Status": status,
            "Notes": notes
        }
        
        with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=row.keys())
            
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(row)
        
        return csv_file
    
    def log_test_summary(self, test_name, test_type, duration, status, details=""):
        """
        Log test execution summary to CSV.
        
        Args:
            test_name: Name of the test
            test_type: Type of test (e.g., "Registration", "Checkout", "Cart")
            duration: Test execution duration in seconds
            status: Test status (PASS/FAIL)
            details: Additional details
        """
        csv_file = self.output_dir / "test_summary.csv"
        
        file_exists = csv_file.exists()
        
        row = {
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Test Name": test_name,
            "Test Type": test_type,
            "Duration (seconds)": duration,
            "Status": status,
            "Details": details
        }
        
        with open(csv_file, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=row.keys())
            
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(row)
        
        return csv_file
    
    def read_csv(self, filename):
        """
        Read CSV file and return data as list of dictionaries.
        
        Args:
            filename: Name of CSV file (e.g., "registration_results.csv")
        
        Returns:
            List of dictionaries containing CSV data
        """
        csv_file = self.output_dir / filename
        
        if not csv_file.exists():
            print(f"⚠️ CSV file not found: {csv_file}")
            return []
        
        with open(csv_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    
    def get_summary_stats(self, filename):
        """
        Get summary statistics from CSV file.
        
        Args:
            filename: Name of CSV file
        
        Returns:
            Dictionary with summary statistics
        """
        data = self.read_csv(filename)
        
        if not data:
            return {"total": 0, "passed": 0, "failed": 0}
        
        total = len(data)
        passed = sum(1 for row in data if row.get("Status", "").upper() == "PASS")
        failed = total - passed
        
        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": f"{(passed/total*100):.1f}%" if total > 0 else "0%"
        }


# Pytest fixture for CSV logging
def pytest_csv_logger():
    """Pytest fixture to provide CSV logger instance."""
    return CSVLogger()
