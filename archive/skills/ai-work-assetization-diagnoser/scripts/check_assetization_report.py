#!/usr/bin/env python3
"""Check an assetization diagnosis report."""

from __future__ import annotations

import argparse
from pathlib import Path


REQUIRED = ["Recommended layer", "Evidence", "Why", "Smallest Next Artifact", "Reuse Signal"]
ALT = {
    "Recommended layer": ["推荐层级"],
    "Evidence": ["证据"],
    "Why": ["为什么"],
    "Smallest Next Artifact": ["最小下一步"],
    "Reuse Signal": ["复用信号"],
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate assetization diagnosis.")
    parser.add_argument("path")
    args = parser.parse_args()
    text = Path(args.path).read_text(encoding="utf-8")
    missing = [
        term for term in REQUIRED if term not in text and not any(option in text for option in ALT.get(term, []))
    ]
    if missing:
        print("Assetization report warnings:")
        for term in missing:
            print(f"- missing:{term}")
        return 1
    print("Assetization report shape looks complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
