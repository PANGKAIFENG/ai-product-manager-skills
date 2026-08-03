#!/usr/bin/env python3
"""Check a brainstorming design spec for decision-ready sections."""

from __future__ import annotations

import argparse
from pathlib import Path


REQUIRED_TERMS = ["当前问题", "推荐方案", "不做范围", "主要风险", "待确认"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a design spec.")
    parser.add_argument("path")
    args = parser.parse_args()
    text = Path(args.path).read_text(encoding="utf-8")
    missing = [term for term in REQUIRED_TERMS if term not in text]
    if missing:
        print("Design spec warnings:")
        for term in missing:
            print(f"- missing:{term}")
        return 1
    print("Design spec shape looks complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
