#!/usr/bin/env python3
"""Static checks for Concept Lens Dashboard HTML artifacts."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_SNIPPETS = {
    "Tailwind CSS CDN": "https://cdn.tailwindcss.com",
    "Alpine.js CDN": "alpinejs",
    "Alpine data binding": "x-data",
    "Concept Lens marker": "data-concept-lens",
    "Stage tabs marker": "data-stage-tabs",
    "Debt detector marker": "data-debt-detector",
    "Sources marker": "data-sources",
}

FORBIDDEN_PATTERNS = [
    re.compile(r"TODO|TBD|FIXME|PLACEHOLDER", re.IGNORECASE),
    re.compile(r"随着时代的发展"),
    re.compile(r"技术是一把双刃剑"),
]


def validate(path: Path) -> tuple[bool, list[str]]:
    issues: list[str] = []
    if not path.exists():
        return False, [f"File not found: {path}"]
    if path.suffix.lower() not in {".html", ".htm"}:
        issues.append("File extension should be .html or .htm")

    text = path.read_text(encoding="utf-8", errors="ignore")
    lower = text.lower()

    for label, snippet in REQUIRED_SNIPPETS.items():
        if snippet.lower() not in lower:
            issues.append(f"Missing required snippet: {label} ({snippet})")

    if not re.search(r"<html\b", text, flags=re.IGNORECASE):
        issues.append("Missing <html> tag")
    if not re.search(r"</html>", text, flags=re.IGNORECASE):
        issues.append("Missing closing </html> tag")
    if not re.search(r"<script\b", text, flags=re.IGNORECASE):
        issues.append("Missing <script> tag")
    if len(re.findall(r"https?://", text)) < 3:
        issues.append("Expected at least 3 source or CDN URLs")
    if not re.search(r"copy|复制|clipboard", text, flags=re.IGNORECASE):
        issues.append("Missing copy interaction hint")

    for pattern in FORBIDDEN_PATTERNS:
        match = pattern.search(text)
        if match:
            issues.append(f"Forbidden or unresolved text found: {match.group(0)}")

    return not issues, issues


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_html_artifact.py <dashboard.html>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1]).expanduser().resolve()
    ok, issues = validate(path)
    if ok:
        print(f"PASS: {path}")
        return 0

    print(f"FAIL: {path}")
    for issue in issues:
        print(f"- {issue}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
