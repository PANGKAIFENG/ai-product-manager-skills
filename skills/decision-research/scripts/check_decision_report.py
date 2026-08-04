#!/usr/bin/env python3
"""Check a decision-research report for minimum decision-ready structure."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_PATTERNS = {
    "decision_question": re.compile(r"decision_question|决策问题|核心决策", re.I),
    "competing_hypotheses": re.compile(r"competing_hypotheses|竞争假设|候选假设|H1", re.I),
    "evidence": re.compile(r"\[Evidence\]|\bL[1-4]\b|证据", re.I),
    "recommendation": re.compile(r"推荐|Recommendation", re.I),
    "excluded": re.compile(r"排除|不推荐|Excluded|Avoid", re.I),
    "confidence": re.compile(r"置信度|Confidence", re.I),
    "overturn": re.compile(r"颠覆条件|推翻条件|Overturn|Re-evaluate", re.I),
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a decision report shape.")
    parser.add_argument("path", help="Path to Markdown report")
    args = parser.parse_args()

    text = Path(args.path).read_text(encoding="utf-8")
    missing = [name for name, pattern in REQUIRED_PATTERNS.items() if not pattern.search(text)]

    if missing:
        print("Decision report warnings:")
        for name in missing:
            print(f"- missing:{name}")
        return 1

    print("Decision report shape looks complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
