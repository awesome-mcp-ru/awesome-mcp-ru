"""build.py — README generation smoke tests."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent


def test_build_renders_readme(tmp_path):
    result = subprocess.run(
        [sys.executable, "-m", "generator.build", "--output", str(tmp_path / "README.md")],
        cwd=ROOT, capture_output=True, text=True
    )
    assert result.returncode == 0, f"stderr={result.stderr}"
    readme = (tmp_path / "README.md").read_text(encoding="utf-8")
    assert "awesome-mcp-ru" in readme
    assert "BizIQ MCP" in readme
    assert "Бизнес-разведка" in readme


def test_build_idempotent(tmp_path):
    out = tmp_path / "README.md"
    subprocess.run([sys.executable, "-m", "generator.build", "--output", str(out)], cwd=ROOT, check=True)
    first = out.read_text(encoding="utf-8")
    subprocess.run([sys.executable, "-m", "generator.build", "--output", str(out)], cwd=ROOT, check=True)
    second = out.read_text(encoding="utf-8")
    assert first == second


def test_build_includes_endpoint(tmp_path):
    out = tmp_path / "README.md"
    subprocess.run([sys.executable, "-m", "generator.build", "--output", str(out)], cwd=ROOT, check=True)
    readme = out.read_text(encoding="utf-8")
    assert "mcp.biziq.ru" in readme
