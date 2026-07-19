"""xquik-mcp entry schema and metadata tests."""
from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).parent.parent
ENTRY_PATH = ROOT / "entries" / "xquik-mcp.yaml"


def load_entry() -> dict:
    return yaml.safe_load(ENTRY_PATH.read_text(encoding="utf-8"))


def test_xquik_entry_validates_against_schema() -> None:
    schema = json.loads((ROOT / "generator" / "schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(load_entry(), schema)


def test_xquik_filename_matches_id() -> None:
    assert load_entry()["id"] == "xquik-mcp"


def test_xquik_endpoint_matches_public_manifest() -> None:
    entry = load_entry()
    assert entry["endpoint"]["url"] == "https://xquik.com/mcp"
    assert entry["endpoint"]["transport"] == "streamable-http"
    assert entry["endpoint"]["auth"] == "oauth"


def test_xquik_tools_match_public_reference() -> None:
    entry = load_entry()
    assert entry["tools"] == ["explore", "xquik"]
    assert entry["tools_count"] == len(entry["tools"])
