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

PUBLISH_CONTAMINATION_PATTERNS = [
    ("local_html_path", re.compile(r"(?<![\w-])[\w./~ -]+\.html\b|file://|localhost|127\.0\.0\.1", re.I)),
    ("local_image_path", re.compile(r"(?<![\w-])[\w./~ -]+\.(?:png|jpg|jpeg|webp)\b", re.I)),
    ("dingtalk_assets_path", re.compile(r"dingtalk-assets|\.dingtalk-assets", re.I)),
    ("artifact_section", re.compile(r"^#+\s*(?:关联产物|本地草稿附录)", re.M)),
    ("open_questions_section", re.compile(r"^#+\s*\d*\.?\s*待确认事项", re.M)),
    ("mock_link_field", re.compile(r"关联\s*mock|关联\s*Mock|Look up|lookup", re.I)),
]

MARKDOWN_IMAGE_PATTERN = re.compile(
    r"!\[[^\]\n]*\]\(\s*(?:<([^>\n]+)>|([^\s)\n]+))(?:\s+[\"'][^)\n]*[\"'])?\s*\)",
    re.I,
)
HTML_IMAGE_PATTERN = re.compile(r"<img\b[^>]*\bsrc\s*=\s*[\"']([^\"']+)[\"']", re.I)
NON_FEATURE_SECTION_PATTERN = re.compile(
    r"^(?:本地草稿附录|关联产物|local draft appendix|related artifacts?)\b",
    re.I,
)

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


def strip_non_feature_sections(text: str) -> str:
    """Remove appendix-style sections that cannot satisfy inline mockup evidence."""
    kept: list[str] = []
    excluded_level: int | None = None

    for line in text.splitlines(keepends=True):
        heading = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if heading:
            level = len(heading.group(1))
            title = heading.group(2).strip()
            if NON_FEATURE_SECTION_PATTERN.match(title):
                excluded_level = level
                continue
            if excluded_level is not None and level <= excluded_level:
                excluded_level = None

        if excluded_level is None:
            kept.append(line)

    return "".join(kept)


def extract_image_targets(text: str) -> list[str]:
    targets = [match.group(1) or match.group(2) for match in MARKDOWN_IMAGE_PATTERN.finditer(text)]
    targets.extend(match.group(1) for match in HTML_IMAGE_PATTERN.finditer(text))
    return targets


def missing_local_image_targets(prd_path: Path, targets: list[str]) -> list[str]:
    missing: list[str] = []
    for target in targets:
        clean_target = target.split("#", 1)[0].split("?", 1)[0]
        if not clean_target or re.match(r"^(?:https?:|data:)", clean_target, re.I):
            continue
        image_path = Path(clean_target)
        if not image_path.is_absolute():
            image_path = prd_path.parent / image_path
        if not image_path.exists():
            missing.append(target)
    return missing


def main() -> int:
    parser = argparse.ArgumentParser(description="Check PRD shape and warn on over-technical drafts.")
    parser.add_argument("path", help="Path to a Markdown PRD")
    parser.add_argument("--type", choices=sorted(REQUIRED_BY_TYPE), default="standard", help="Expected PRD type")
    parser.add_argument("--allow-handoff", action="store_true", help="Allow technical schema details in the document")
    parser.add_argument("--publish-ready", action="store_true", help="Check for online-publishing contamination such as local mock links")
    parser.add_argument(
        "--require-mockup-evidence",
        action="store_true",
        help="Require a real screenshot reference in a feature section, not only in a local appendix",
    )
    parser.add_argument(
        "--require-mockup-artifact",
        action="append",
        default=[],
        metavar="PATH",
        help="Require a generated HTML mockup artifact; may be passed more than once",
    )
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
        if args.publish_ready and required == "待确认":
            continue
        if required not in text:
            warnings.append(f"missing_expected_section:{required}")

    if "本期只解决" not in text and "本期只讲" not in text:
        warnings.append("missing_scope_sentence")

    if not args.publish_ready and "待确认" not in text:
        warnings.append("missing_open_questions")

    if args.publish_ready:
        for name, pattern in PUBLISH_CONTAMINATION_PATTERNS:
            if pattern.search(body_to_check):
                warnings.append(f"publish_contamination:{name}")

    if args.require_mockup_evidence:
        feature_text = strip_non_feature_sections(text)
        image_targets = extract_image_targets(feature_text)
        if not image_targets:
            warnings.append("missing_mockup_evidence")
        else:
            for target in missing_local_image_targets(path, image_targets):
                warnings.append(f"missing_mockup_file:{target}")

    for target in args.require_mockup_artifact:
        artifact_path = Path(target)
        if not artifact_path.is_absolute():
            artifact_path = path.parent / artifact_path
        if not artifact_path.is_file():
            warnings.append(f"missing_mockup_artifact:{target}")
            continue
        if artifact_path.suffix.lower() not in {".html", ".htm"}:
            warnings.append(f"invalid_mockup_artifact_type:{target}")
            continue
        artifact_text = artifact_path.read_text(encoding="utf-8", errors="ignore")
        if not re.search(r"<body\b[^>]*>.*\S.*</body>", artifact_text, re.I | re.S):
            warnings.append(f"empty_mockup_artifact:{target}")

    if warnings:
        print("PRD shape warnings:")
        for warning in warnings:
            print(f"- {warning}")
        return 1

    print("PRD shape check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
