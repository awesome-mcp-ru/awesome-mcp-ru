"""biziq-mcp seed entry — schema + filename↔id integrity."""
from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).parent.parent


def test_biziq_entry_validates_against_schema() -> None:
    schema = json.loads((ROOT / "generator" / "schema.json").read_text(encoding="utf-8"))
    entry = yaml.safe_load((ROOT / "entries" / "biziq-mcp.yaml").read_text(encoding="utf-8"))
    jsonschema.validate(entry, schema)


def test_biziq_filename_matches_id() -> None:
    entry = yaml.safe_load((ROOT / "entries" / "biziq-mcp.yaml").read_text(encoding="utf-8"))
    assert entry["id"] == "biziq-mcp"


def test_biziq_endpoint_uses_dedicated_subdomain() -> None:
    entry = yaml.safe_load((ROOT / "entries" / "biziq-mcp.yaml").read_text(encoding="utf-8"))
    # Spec §4.1 — Landing ≠ Endpoint pattern. biziq.ru/mcp is landing,
    # mcp.biziq.ru is the dedicated endpoint.
    assert entry["endpoint"]["url"] == "https://mcp.biziq.ru"


def test_biziq_tools_count_matches_array_length() -> None:
    entry = yaml.safe_load((ROOT / "entries" / "biziq-mcp.yaml").read_text(encoding="utf-8"))
    assert entry["tools_count"] >= len(entry["tools"])
    # tools array may be truncated к 50 max per schema; tools_count is the real total
