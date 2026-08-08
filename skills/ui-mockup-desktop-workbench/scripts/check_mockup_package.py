#!/usr/bin/env python3
"""Check a UI mockup package for implementation-handoff deliverables."""

from __future__ import annotations

import argparse
from pathlib import Path


BASE_REQUIRED = ["ascii-layout.md", "screen-contract.md"]
IMPLEMENTATION_REQUIRED = ["component-map.md", "implementation-notes.md"]
STRUCTURE_REQUIRED = [
    "screen-inventory.md",
    "state-model.md",
    "ascii-layout.md",
    "wireframe-handoff.md",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a UI mockup package.")
    parser.add_argument("path", help="Directory containing mockup outputs")
    parser.add_argument("--implementation", action="store_true", help="Require implementation handoff files")
    parser.add_argument(
        "--structure-only",
        action="store_true",
        help="Validate structure-stage files without requiring a visual artifact",
    )
    args = parser.parse_args()

    root = Path(args.path)
    if args.structure_only:
        missing = [name for name in STRUCTURE_REQUIRED if not (root / name).exists()]
        if missing:
            print("Mockup structure package warnings:")
            for name in missing:
                print(f"- missing:{name}")
            return 1
        print("Mockup structure package contains required wireframe files.")
        return 0

    required = list(BASE_REQUIRED)
    if args.implementation:
        required.extend(IMPLEMENTATION_REQUIRED)

    has_artifact = any((root / name).exists() for name in ("mockup.html", "preview.md", "screenshots.md"))
    missing = [name for name in required if not (root / name).exists()]
    if not has_artifact:
        missing.append("mockup.html|preview.md|screenshots.md")

    if missing:
        print("Mockup package warnings:")
        for name in missing:
            print(f"- missing:{name}")
        return 1

    print("Mockup package contains required handoff files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
