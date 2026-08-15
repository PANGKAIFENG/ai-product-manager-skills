#!/usr/bin/env python3
"""Validate the canonical PRD version history block."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


VERSION_PATTERN = re.compile(r"^[Vv](\d+)\.(\d+)$")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
GENERIC_CHANGE_SUMMARIES = {
    "更新prd",
    "优化prd",
    "修改prd",
    "内容更新",
    "需求更新",
    "更新文档",
    "优化文档",
}


def canonical_heading(title: str) -> str:
    canonical = re.sub(r"^[`*_\s]+|[`*_\s]+$", "", title)
    canonical = re.sub(r"^\d+(?:\.\d+)*[.、)]?\s*", "", canonical)
    return canonical.strip()


def table_cells(line: str) -> list[str]:
    if not line.lstrip().startswith("|"):
        return []
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_separator_row(cells: list[str]) -> bool:
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def extract_version_rows(text: str) -> tuple[list[dict[str, str]], list[str]]:
    warnings: list[str] = []
    headings = list(re.finditer(r"^(#{1,6})\s+(.+?)\s*$", text, re.M))
    version_heading_index = next(
        (
            index
            for index, match in enumerate(headings)
            if canonical_heading(match.group(2)).lower() == "版本记录"
        ),
        None,
    )
    if version_heading_index is None:
        return [], ["missing_version_history"]

    version_heading = headings[version_heading_index]
    h2_headings = [match for match in headings if len(match.group(1)) == 2]
    if not h2_headings or h2_headings[0].start() != version_heading.start():
        warnings.append("version_history_not_at_top")

    end = len(text)
    heading_level = len(version_heading.group(1))
    for later in headings[version_heading_index + 1 :]:
        if len(later.group(1)) <= heading_level:
            end = later.start()
            break
    section_lines = text[version_heading.end() : end].splitlines()

    header_index = None
    for index, line in enumerate(section_lines):
        cells = table_cells(line)
        normalized = [re.sub(r"\s+", "", cell).lower() for cell in cells]
        if len(normalized) >= 3 and normalized[:3] == ["版本", "日期", "修改内容"]:
            header_index = index
            break
    if header_index is None:
        warnings.append("invalid_version_history_table")
        return [], warnings

    rows: list[dict[str, str]] = []
    for line in section_lines[header_index + 1 :]:
        cells = table_cells(line)
        if not cells:
            if rows:
                break
            continue
        if is_separator_row(cells):
            continue
        if len(cells) < 3:
            warnings.append("invalid_version_history_row")
            continue
        rows.append({"version": cells[0], "date": cells[1], "changes": cells[2]})

    if not rows:
        warnings.append("missing_version_history_rows")
    return rows, warnings


def validate_version_history(text: str) -> tuple[list[dict[str, str]], list[str]]:
    rows, warnings = extract_version_rows(text)
    parsed_versions: list[tuple[int, int]] = []

    for row in rows:
        version_match = VERSION_PATTERN.fullmatch(row["version"])
        if version_match is None:
            warnings.append(f"invalid_version:{row['version'] or '<empty>'}")
        else:
            parsed_versions.append((int(version_match.group(1)), int(version_match.group(2))))

        if DATE_PATTERN.fullmatch(row["date"]) is None:
            warnings.append(f"invalid_version_date:{row['date'] or '<empty>'}")

        normalized_changes = re.sub(r"[\s。；;，,]+", "", row["changes"]).lower()
        if not normalized_changes:
            warnings.append(f"empty_version_changes:{row['version'] or '<empty>'}")
        elif normalized_changes in GENERIC_CHANGE_SUMMARIES:
            warnings.append(f"generic_version_changes:{row['version'] or '<empty>'}")

    if len(parsed_versions) == len(rows) and rows:
        if len(set(parsed_versions)) != len(parsed_versions):
            warnings.append("duplicate_version_numbers")
        if any(current <= following for current, following in zip(parsed_versions, parsed_versions[1:])):
            warnings.append("version_history_not_newest_first")
        if parsed_versions[-1] != (1, 0):
            warnings.append("missing_v1_0_origin")
        elif "首次创建" not in rows[-1]["changes"]:
            warnings.append("v1_0_missing_initial_creation_summary")

    return rows, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a PRD version history table.")
    parser.add_argument("path", help="Path to a Markdown PRD")
    parser.add_argument("--json", action="store_true", help="Print structured validation output")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2

    rows, warnings = validate_version_history(path.read_text(encoding="utf-8"))
    if args.json:
        print(json.dumps({"valid": not warnings, "rows": rows, "warnings": warnings}, ensure_ascii=False))
    elif warnings:
        print("PRD version history warnings:")
        for warning in warnings:
            print(f"- {warning}")
    else:
        print(f"PRD version history check passed: {rows[0]['version']}")
    return 1 if warnings else 0


if __name__ == "__main__":
    raise SystemExit(main())
