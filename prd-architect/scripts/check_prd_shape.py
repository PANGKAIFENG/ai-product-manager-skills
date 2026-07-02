#!/usr/bin/env python3
"""Lightweight PRD shape checks for prd-architect outputs."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


OVER_TECH_PATTERNS = [
    ("typescript_code_fence", re.compile(r"```(?:ts|typescript)\b", re.I)),
    ("json_code_fence", re.compile(r"```json\b", re.I)),
    ("ts_interface", re.compile(r"\binterface\s+[A-Z][A-Za-z0-9_]*\s*\{")),
    ("endpoint_focus", re.compile(r"\b(endpoint|api route|路由|接口路径)\b", re.I)),
    ("adapter_focus", re.compile(r"\b(adapter|适配器)\b", re.I)),
    ("metadata_focus", re.compile(r"\b(metadata|hidden context|隐藏上下文)\b", re.I)),
    ("schema_focus", re.compile(r"\b(schema|json schema)\b", re.I)),
    ("capability_registry", re.compile(r"\b(requiredCapabilities|capability registry|action_template_registry|能力注册)\b", re.I)),
]

REQUIRED_BY_TYPE = {
    "lite": ["功能目标", "用户场景", "关键交互", "验收标准", "待确认"],
    "standard": ["功能目标", "用户场景", "入口", "核心对象", "交互逻辑", "异常", "验收标准", "待确认"],
    "ai-native": ["模块定位", "功能目标", "用户场景", "双轨协作", "状态反馈", "人工", "异常", "验收标准", "待确认"],
}


def strip_handoff_appendix(text: str) -> str:
    markers = [
        r"^#+\s*开发\s*handoff",
        r"^#+\s*Development Handoff",
        r"^#+\s*附录",
        r"^#+\s*Handoff Appendix",
    ]
    for marker in markers:
        match = re.search(marker, text, flags=re.I | re.M)
        if match:
            return text[: match.start()]
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description="Check PRD shape and warn on over-technical drafts.")
    parser.add_argument("path", help="Path to a Markdown PRD")
    parser.add_argument("--type", choices=sorted(REQUIRED_BY_TYPE), default="standard", help="Expected PRD type")
    parser.add_argument("--allow-handoff", action="store_true", help="Allow technical schema details in the document")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2

    text = path.read_text(encoding="utf-8")
    body_to_check = text if args.allow_handoff else strip_handoff_appendix(text)
    warnings: list[str] = []

    for name, pattern in OVER_TECH_PATTERNS:
        if pattern.search(body_to_check):
            warnings.append(f"over_technical:{name}")

    for required in REQUIRED_BY_TYPE[args.type]:
        if required not in text:
            warnings.append(f"missing_expected_section:{required}")

    if "本期只解决" not in text and "本期只讲" not in text:
        warnings.append("missing_scope_sentence")

    if "待确认" not in text:
        warnings.append("missing_open_questions")

    if warnings:
        print("PRD shape warnings:")
        for warning in warnings:
            print(f"- {warning}")
        return 1

    print("PRD shape check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

