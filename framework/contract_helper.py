# framework/contract_helper.py

"""
API Contract Testing Helper.

Validates API responses against contracts (JSON Schema or snapshot).
Useful for Boomi middleware and Salesforce integration testing.

Supports:
  - JSON Schema contract validation
  - Response structure snapshot comparison
  - Field type validation
  - Required field checks
  - Contract versioning

Usage:
    contract = ContractHelper()
    contract.validate_response(response, "schemas/order_response.json")
    contract.assert_fields_present(data, ["id", "status", "total"])
    contract.assert_field_types(data, {"id": str, "total": (int, float)})
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Type, Union
import allure

logger = logging.getLogger(__name__)


class ContractHelper:
    """API contract validation helper."""

    def __init__(self, schemas_dir: str = "tests/test_data/schemas"):
        """Initialize with schemas directory.

        Args:
            schemas_dir: Path to directory containing JSON schema files
        """
        self.schemas_dir = Path(schemas_dir)

    @allure.step("Validate response against schema: {schema_name}")
    def validate_response(self, data: Any, schema_name: str) -> List[str]:
        """Validate response data against a JSON schema file.

        Args:
            data: Response data (dict or list)
            schema_name: Schema filename (relative to schemas_dir)

        Returns:
            List of validation errors (empty if valid)

        Raises:
            FileNotFoundError: If schema file doesn't exist
        """
        from framework.schema_validator import validate_schema, load_schema

        schema_path = self.schemas_dir / schema_name
        schema = load_schema(str(schema_path))
        errors = validate_schema(data, schema)

        if errors:
            logger.warning(f"Contract violations for {schema_name}: {errors}")
            allure.attach(
                json.dumps(errors, indent=2),
                name=f"contract_violations_{schema_name}",
                attachment_type=allure.attachment_type.JSON
            )
        else:
            logger.info(f"Contract valid: {schema_name}")

        return errors

    @allure.step("Assert response matches contract: {schema_name}")
    def assert_contract(self, data: Any, schema_name: str):
        """Assert response matches a JSON schema contract.

        Args:
            data: Response data
            schema_name: Schema filename

        Raises:
            AssertionError with violation details
        """
        errors = self.validate_response(data, schema_name)
        if errors:
            detail = "\n".join(f"  - {e}" for e in errors)
            raise AssertionError(
                f"Contract violation for {schema_name}:\n{detail}"
            )

    @allure.step("Assert required fields present")
    def assert_fields_present(self, data: Dict, required_fields: List[str]):
        """Assert all required fields are present in response.

        Args:
            data: Response dict
            required_fields: List of required field names

        Raises:
            AssertionError listing missing fields
        """
        missing = [f for f in required_fields if f not in data]
        if missing:
            raise AssertionError(
                f"Missing required fields: {missing}. "
                f"Present fields: {list(data.keys())}"
            )

    @allure.step("Assert field types")
    def assert_field_types(self, data: Dict,
                           type_map: Dict[str, Union[Type, Tuple[Type, ...]]]):
        """Assert fields have expected types.

        Args:
            data: Response dict
            type_map: Dict mapping field names to expected types
                e.g., {"id": str, "total": (int, float), "items": list}

        Raises:
            AssertionError listing type mismatches
        """
        mismatches = []
        for field, expected_type in type_map.items():
            if field not in data:
                mismatches.append(f"{field}: missing")
                continue
            if not isinstance(data[field], expected_type):
                actual_type = type(data[field]).__name__
                expected_name = (
                    expected_type.__name__ if isinstance(expected_type, type)
                    else str(expected_type)
                )
                mismatches.append(
                    f"{field}: expected {expected_name}, got {actual_type}"
                )

        if mismatches:
            detail = "\n".join(f"  - {m}" for m in mismatches)
            raise AssertionError(f"Field type mismatches:\n{detail}")

    @allure.step("Assert response structure matches snapshot")
    def assert_structure_matches(self, data: Dict,
                                 expected_structure: Dict):
        """Assert response has the same structure (keys) as expected.

        Does not check values, only that the same keys exist at each level.

        Args:
            data: Actual response dict
            expected_structure: Expected structure dict

        Raises:
            AssertionError with structural differences
        """
        differences = self._compare_structure(data, expected_structure)
        if differences:
            detail = "\n".join(f"  - {d}" for d in differences)
            raise AssertionError(
                f"Response structure mismatch:\n{detail}"
            )

    def _compare_structure(self, actual: Any, expected: Any,
                           path: str = "$") -> List[str]:
        """Recursively compare dict structures.

        Args:
            actual: Actual data
            expected: Expected structure
            path: Current JSON path

        Returns:
            List of difference descriptions
        """
        differences = []

        if isinstance(expected, dict) and isinstance(actual, dict):
            # Check for missing keys
            for key in expected:
                if key not in actual:
                    differences.append(f"{path}.{key}: missing in response")
                else:
                    differences.extend(
                        self._compare_structure(
                            actual[key], expected[key], f"{path}.{key}"
                        )
                    )
            # Check for extra keys
            for key in actual:
                if key not in expected:
                    differences.append(f"{path}.{key}: unexpected field")

        elif isinstance(expected, list) and isinstance(actual, list):
            if len(actual) > 0 and len(expected) > 0:
                differences.extend(
                    self._compare_structure(
                        actual[0], expected[0], f"{path}[0]"
                    )
                )

        elif type(actual) != type(expected):
            differences.append(
                f"{path}: type mismatch "
                f"(expected {type(expected).__name__}, "
                f"got {type(actual).__name__})"
            )

        return differences

    @allure.step("Save response as contract snapshot")
    def save_snapshot(self, data: Any, snapshot_name: str):
        """Save response structure as a contract snapshot.

        Args:
            data: Response data to snapshot
            snapshot_name: Snapshot filename
        """
        snapshot_dir = self.schemas_dir / "snapshots"
        snapshot_dir.mkdir(parents=True, exist_ok=True)

        snapshot_path = snapshot_dir / snapshot_name
        with open(snapshot_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)

        logger.info(f"Saved contract snapshot: {snapshot_path}")

    def load_snapshot(self, snapshot_name: str) -> Any:
        """Load a contract snapshot.

        Args:
            snapshot_name: Snapshot filename

        Returns:
            Snapshot data
        """
        snapshot_path = self.schemas_dir / "snapshots" / snapshot_name
        with open(snapshot_path) as f:
            return json.load(f)
