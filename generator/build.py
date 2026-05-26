"""Build README.md from entries/*.yaml.

Usage:
    python3 -m generator.build --output README.md

Idempotent — same input always produces same output.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

REPO_ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DIR = REPO_ROOT / "entries"
TEMPLATES_DIR = REPO_ROOT / "templates"
STANDARD_VERSION = "1.0.0-draft"

CATEGORIES = {
    "business-intel": {"emoji": "🏢", "ru": "Бизнес-разведка", "en": "Business Intelligence"},
    "ecommerce":      {"emoji": "🛒", "ru": "E-commerce", "en": "E-commerce"},
    "finance":        {"emoji": "💰", "ru": "Финансы и платежи", "en": "Banking & Payments"},
    "government":     {"emoji": "🏛", "ru": "Госданные и реестры", "en": "Government & Public Data"},
    "crm-saas":       {"emoji": "🤝", "ru": "CRM и SaaS", "en": "CRM & Business SaaS"},
    "communication":  {"emoji": "💬", "ru": "Коммуникации", "en": "Communication"},
    "cloud":          {"emoji": "☁️", "ru": "Cloud-инфраструктура", "en": "Cloud Infrastructure"},
    "ai-llm":         {"emoji": "🤖", "ru": "ИИ и LLM-шлюзы", "en": "AI & LLM Gateways"},
    "logistics":      {"emoji": "🚛", "ru": "Логистика и доставка", "en": "Logistics & Delivery"},
    "maps-geo":       {"emoji": "🗺", "ru": "Карты и геоданные", "en": "Maps & Geo"},
    "education":      {"emoji": "🎓", "ru": "Образование и знания", "en": "Education & Knowledge"},
    "devtools":       {"emoji": "💻", "ru": "Developer Tools", "en": "Developer Tools"},
    "other":          {"emoji": "📦", "ru": "Прочее", "en": "Other"},
}

BADGE_EMOJI = {
    "commercial":      "🏢",
    "ru-hosted":       "🇷🇺",
    "fz152-declared":  "🔐",
    "attribution":     "🤖",
    "osi-license":     "📜",
    "sbp-compatible":  "💳",
    "bilingual-tools": "🌐",
}


def load_entries() -> list[dict]:
    entries: list[dict] = []
    for path in sorted(ENTRIES_DIR.glob("*.yaml")):
        if path.name.startswith("."):
            continue
        entries.append(yaml.safe_load(path.read_text(encoding="utf-8")))
    return entries


def compute_badges(entry: dict) -> list[str]:
    badges: list[str] = []
    ver = entry.get("verification") or {}
    hosting = entry.get("hosting") or {}
    if (ver.get("ogrn") or {}).get("legal_entity"):
        badges.append("commercial")
    if hosting.get("country") == "RU":
        badges.append("ru-hosted")
    if hosting.get("fz152_pii_processing") == "declared":
        badges.append("fz152-declared")
    if (entry.get("attribution") or {}).get("utm_pattern"):
        badges.append("attribution")
    spdx = (entry.get("license") or {}).get("spdx")
    if spdx and spdx != "null":
        badges.append("osi-license")
    payment_methods = (entry.get("pricing") or {}).get("ru_payment_methods") or []
    if "sbp" in payment_methods:
        badges.append("sbp-compatible")
    if set(entry.get("tools_lang") or []) >= {"ru", "en"}:
        badges.append("bilingual-tools")
    return badges


def bucket_by_category(entries: list[dict]) -> dict:
    cats: dict = {k: {**v, "entries": []} for k, v in CATEGORIES.items()}
    for entry in entries:
        cat_id = entry.get("category", "other")
        if cat_id not in cats:
            cats[cat_id] = {**CATEGORIES.get(cat_id, CATEGORIES["other"]), "entries": []}
        cats[cat_id]["entries"].append(entry)
    # Hide `other` until ≥3 entries (per spec §8)
    if len(cats.get("other", {}).get("entries", [])) < 3:
        cats.pop("other", None)
    return cats


def render_readme(entries: list[dict]) -> str:
    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=select_autoescape(disabled_extensions=(".j2", ".md")),
        keep_trailing_newline=True,
    )

    def entry_url(entry: dict) -> str:
        return f"https://mcp.neuralgate.ru/entry/{entry['id']}/"

    def tier_badge(entry: dict) -> str:
        return "🥇 Tier 1" if entry.get("tier") == 1 else "🥈 Tier 2"

    def orthogonal_badges(entry: dict) -> str:
        return " ".join(BADGE_EMOJI.get(b, "") for b in compute_badges(entry))

    env.globals["entry_url"] = entry_url
    env.globals["tier_badge"] = tier_badge
    env.globals["orthogonal_badges"] = orthogonal_badges

    template = env.get_template("README.j2")
    cats = bucket_by_category(entries)
    return template.render(
        entries=entries,
        categories=cats,
        t1_count=sum(1 for e in entries if e.get("tier") == 1),
        t2_count=sum(1 for e in entries if e.get("tier") != 1),
        standard_version=STANDARD_VERSION,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build awesome-mcp-ru README from entries/")
    parser.add_argument("--output", "-o", default="README.md", help="Output path (default: README.md)")
    args = parser.parse_args(argv)
    entries = load_entries()
    out = render_readme(entries)
    Path(args.output).write_text(out, encoding="utf-8")
    print(f"Wrote {len(entries)} entries to {args.output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
