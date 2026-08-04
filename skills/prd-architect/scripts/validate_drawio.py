#!/usr/bin/env python3
"""Validate a Draw.io .drawio file with lightweight structural checks."""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def fail(message: str) -> int:
    print(f"FAIL: {message}")
    return 1


def validate(path: Path) -> int:
    if not path.exists():
        return fail(f"file does not exist: {path}")
    if not path.is_file():
        return fail(f"path is not a file: {path}")

    try:
        tree = ET.parse(path)
    except ET.ParseError as error:
        return fail(f"XML parse error: {error}")

    root = tree.getroot()
    if root.tag != "mxfile":
        return fail(f"root element must be <mxfile>, got <{root.tag}>")

    diagrams = root.findall("diagram")
    if not diagrams:
        return fail("missing <diagram> element")

    cells = root.findall(".//mxCell")
    if not cells:
        return fail("missing mxCell elements")

    ids: set[str] = set()
    duplicates: list[str] = []
    missing_ids = 0

    for cell in cells:
        cell_id = cell.get("id")
        if not cell_id:
            missing_ids += 1
            continue
        if cell_id in ids:
            duplicates.append(cell_id)
        ids.add(cell_id)

    if missing_ids:
        return fail(f"{missing_ids} mxCell element(s) missing id")
    if duplicates:
        return fail(f"duplicate mxCell id(s): {', '.join(sorted(set(duplicates)))}")

    broken_edges: list[str] = []
    for cell in cells:
        if cell.get("edge") != "1":
            continue

        edge_id = cell.get("id", "<missing-id>")
        source = cell.get("source")
        target = cell.get("target")

        if source and source not in ids:
            broken_edges.append(f"{edge_id} source={source}")
        if target and target not in ids:
            broken_edges.append(f"{edge_id} target={target}")

    if broken_edges:
        return fail("edge endpoint(s) reference missing id(s): " + "; ".join(broken_edges))

    print(f"OK: {path} ({len(diagrams)} diagram(s), {len(cells)} mxCell(s))")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Draw.io mxfile XML structure.")
    parser.add_argument("path", help="Path to a .drawio file")
    args = parser.parse_args()
    return validate(Path(args.path).expanduser().resolve())


if __name__ == "__main__":
    sys.exit(main())
