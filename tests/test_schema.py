"""Schema validation tests — golden fixture + negative cases."""
from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest
import yaml

SCHEMA_PATH = Path(__file__).parent.parent / "generator" / "schema.json"
FIXTURES = Path(__file__).parent / "fixtures"


def load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def load_fixture(name: str) -> dict:
    return yaml.safe_load((FIXTURES / name).read_text(encoding="utf-8"))


def test_schema_valid_passes() -> None:
    schema = load_schema()
    entry = load_fixture("entry_valid.yaml")
    jsonschema.validate(entry, schema)  # raises if invalid


def test_schema_missing_required_endpoint_url_fails() -> None:
    schema = load_schema()
    entry = load_fixture("entry_missing_required.yaml")
    with pytest.raises(jsonschema.ValidationError) as exc:
        jsonschema.validate(entry, schema)
    assert "url" in str(exc.value)


def test_schema_bad_transport_enum_fails() -> None:
    schema = load_schema()
    entry = load_fixture("entry_bad_enum.yaml")
    with pytest.raises(jsonschema.ValidationError) as exc:
        jsonschema.validate(entry, schema)
    assert "transport" in str(exc.value).lower() or "ftp" in str(exc.value)
