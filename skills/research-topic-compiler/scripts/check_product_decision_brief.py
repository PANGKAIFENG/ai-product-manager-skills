#!/usr/bin/env python3
"""Check the deterministic shape of a product-research decision brief."""

from __future__ import annotations

import argparse
from pathlib import Path


REQUIRED = {
    "Decision question": ("决策问题",),
    "Direction": ("方向", "建议"),
    "Confidence": ("置信",),
    "Evidence": ("证据",),
    "Copy, Adapt, Avoid, Validate": ("借鉴", "适配", "避免", "验证"),
    "Next Validation": ("下一步验证", "验证动作"),
    "Final option selection owner": ("最终选型责任", "最终选择责任"),
}


def has_term(text: str, term: str, alternatives: tuple[str, ...]) -> bool:
    return term in text or any(value in text for value in alternatives)


def validate(text: str) -> list[str]:
    return [
        term
        for term, alternatives in REQUIRED.items()
        if not has_term(text, term, alternatives)
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Product Decision Brief.")
    parser.add_argument("path", help="Markdown brief to validate")
    args = parser.parse_args()
    text = Path(args.path).read_text(encoding="utf-8")
    missing = validate(text)
    if missing:
        print("Product decision brief warnings:")
        for term in missing:
            print(f"- missing:{term}")
        return 1
    print("Product decision brief shape looks complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
