"""JSON Schema validation helper for API response verification."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import ValidationError, validate


def validate_schema(data: Any, schema: dict) -> list[str]:
    """
    Validate data against a JSON schema.

    Returns:
        Empty list if valid, list of error messages if invalid.
    """
    errors = []
    try:
        validate(instance=data, schema=schema)
    except ValidationError as e:
        errors.append(f"{e.json_path}: {e.message}")
    return errors


def load_schema(schema_path: str) -> dict:
    """Load a JSON schema from file."""
    path = Path(schema_path)
    if not path.exists():
        raise FileNotFoundError(f"Schema file not found: {schema_path}")
    with open(path) as f:
        return json.load(f)


def assert_valid_schema(data: Any, schema: dict, message: str = ""):
    """Assert data matches schema. Raises AssertionError with details on failure."""
    errors = validate_schema(data, schema)
    if errors:
        error_detail = "\n".join(f"  - {e}" for e in errors)
        msg = message or "Schema validation failed"
        raise AssertionError(f"{msg}:\n{error_detail}")
