#!/usr/bin/env python3
"""Check a competitive-analysis Product Decision Brief."""

from __future__ import annotations

import argparse
from pathlib import Path


REQUIRED = ["Decision question", "Recommendation", "Confidence", "Evidence", "What to copy", "Next validation"]
ALT = {
    "Decision question": ["决策问题"],
    "Recommendation": ["建议", "推荐"],
    "Confidence": ["置信"],
    "Evidence": ["证据"],
    "What to copy": ["借鉴", "适配", "避免"],
    "Next validation": ["下一步验证", "验证动作"],
}


def has_term(text: str, term: str) -> bool:
    return term in text or any(option in text for option in ALT.get(term, []))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Product Decision Brief.")
    parser.add_argument("path")
    args = parser.parse_args()
    text = Path(args.path).read_text(encoding="utf-8")
    missing = [term for term in REQUIRED if not has_term(text, term)]
    if missing:
        print("Decision brief warnings:")
        for term in missing:
            print(f"- missing:{term}")
        return 1
    print("Decision brief shape looks complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
