#!/usr/bin/env python3
"""Check a PRD-to-issues draft for minimum backlog structure."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED = {
    "issue_plan": re.compile(r"Issue Plan|Issue Breakdown|工单|Issue", re.I),
    "acceptance": re.compile(r"Acceptance criteria|验收标准|\[ \]", re.I),
    "verification": re.compile(r"Verification|验证", re.I),
    "coverage": re.compile(r"Coverage Matrix|覆盖矩阵", re.I),
    "afk_hitl": re.compile(r"AFK|HITL", re.I),
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an issue breakdown draft.")
    parser.add_argument("path")
    args = parser.parse_args()
    text = Path(args.path).read_text(encoding="utf-8")
    missing = [name for name, pattern in REQUIRED.items() if not pattern.search(text)]
    if missing:
        print("Issue plan warnings:")
        for name in missing:
            print(f"- missing:{name}")
        return 1
    print("Issue plan shape looks complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
