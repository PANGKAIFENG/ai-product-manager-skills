#!/usr/bin/env python3
"""Check a UI wireframe package for the minimum structure-stage deliverables."""

from __future__ import annotations

import argparse
from pathlib import Path


REQUIRED = ["screen-inventory.md", "state-model.md", "ascii-layout.md"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a wireframe package.")
    parser.add_argument("path", help="Directory containing wireframe outputs")
    args = parser.parse_args()

    root = Path(args.path)
    missing = [name for name in REQUIRED if not (root / name).exists()]
    if missing:
        print("Wireframe package warnings:")
        for name in missing:
            print(f"- missing:{name}")
        return 1

    print("Wireframe package contains required structure-stage files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
