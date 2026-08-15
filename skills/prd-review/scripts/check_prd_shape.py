#!/usr/bin/env python3
"""Lightweight PRD shape checks for prd-architect outputs."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from check_prd_version_history import validate_version_history


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
MARKDOWN_TARGET_IMAGE_PATTERN = re.compile(
    r"!\[[^\]\n]*(?:目标态|目标状态)[^\]\n]*\]\(\s*(?:<([^>\n]+)>|([^\s)\n]+))(?:\s+[\"'][^)\n]*[\"'])?\s*\)",
    re.I,
)
HTML_IMAGE_TAG_PATTERN = re.compile(r"<img\b[^>]*>", re.I)

REQUIRED_CAPABILITIES = {
    "lite": {
        "context_and_scope": ("背景与目标", "功能目标"),
        "feature_modules": ("功能模块", "功能改动"),
        "open_questions": ("待确认", "待确认事项"),
    },
    "standard": {
        "context_and_scope": ("背景与目标", "功能目标"),
        "feature_modules": ("功能模块", "功能设计", "功能说明"),
        "open_questions": ("待确认", "待确认事项"),
    },
    "ai-native": {
        "context_and_scope": ("背景与目标", "功能目标"),
        "ai_collaboration": ("AI 协作边界", "AI 协作", "人机协作", "双轨协作"),
        "feature_modules": ("功能模块", "功能设计", "功能说明"),
        "open_questions": ("待确认", "待确认事项"),
    },
}

BASELINE_KINDS = {"frontend-repo", "design-system", "reference-html", "screenshot"}
LEGACY_PARALLEL_SECTIONS = {
    "用户场景",
    "入口",
    "入口与触发",
    "页面结构",
    "核心对象",
    "交互逻辑",
    "关键交互",
    "验收标准",
    "模块验收",
    "整体验收",
}
MODULE_DETAIL_SECTIONS = {
    "目标态 ui",
    "功能逻辑",
    "状态语义",
    "边界与异常",
    "模块验收",
}
MATURITY_ALIASES = {
    "草稿": "draft",
    "draft": "draft",
    "讨论中": "discussing",
    "discussing": "discussing",
    "已确认": "confirmed",
    "confirmed": "confirmed",
}


def heading_matches(title: str, alternatives: tuple[str, ...]) -> bool:
    canonical = canonical_heading(title).lower()
    return canonical in {alternative.lower() for alternative in alternatives}


def heading_titles(text: str) -> list[str]:
    return [match.group(1).strip() for match in re.finditer(r"^#{1,6}\s+(.+?)\s*$", text, re.M)]


def has_heading_capability(titles: list[str], alternatives: tuple[str, ...]) -> bool:
    return any(heading_matches(title, alternatives) for title in titles)


def canonical_heading(title: str) -> str:
    canonical = re.sub(r"^[`*_\s]+|[`*_\s]+$", "", title)
    canonical = re.sub(r"^\d+(?:\.\d+)*[.、)]?\s*", "", canonical)
    canonical = re.sub(r"\s*(?:（[^）]*）|\([^)]*\))\s*$", "", canonical)
    return canonical.strip()


def heading_sections(text: str) -> list[tuple[int, str, int, int]]:
    matches = list(re.finditer(r"^(#{1,6})\s+(.+?)\s*$", text, re.M))
    sections: list[tuple[int, str, int, int]] = []
    for index, match in enumerate(matches):
        level = len(match.group(1))
        end = len(text)
        for later in matches[index + 1 :]:
            if len(later.group(1)) <= level:
                end = later.start()
                break
        sections.append((level, match.group(2).strip(), match.start(), end))
    return sections


def extract_feature_modules(text: str, prd_type: str) -> list[tuple[str, str]]:
    sections = heading_sections(text)
    alternatives = REQUIRED_CAPABILITIES[prd_type]["feature_modules"]
    parent_index = next(
        (index for index, (_, title, _, _) in enumerate(sections) if heading_matches(title, alternatives)),
        None,
    )
    if parent_index is None:
        return []

    parent_level, _, parent_start, parent_end = sections[parent_index]
    candidates = [
        (level, title, start, end)
        for level, title, start, end in sections[parent_index + 1 :]
        if parent_start < start < parent_end and level > parent_level
    ]
    if not candidates:
        return []

    module_level = min(level for level, _, _, _ in candidates)
    modules: list[tuple[str, str]] = []
    module_candidates = [candidate for candidate in candidates if candidate[0] == module_level]
    for index, (_, title, start, _) in enumerate(module_candidates):
        canonical = canonical_heading(title).lower()
        if canonical in MODULE_DETAIL_SECTIONS:
            continue
        end = module_candidates[index + 1][2] if index + 1 < len(module_candidates) else parent_end
        modules.append((canonical_heading(title), text[start:end]))
    return modules


def module_has_logic_table(module_text: str, prd_type: str) -> bool:
    lines = module_text.splitlines()
    for line_index, line in enumerate(lines):
        if not line.lstrip().startswith("|"):
            continue
        cells = [re.sub(r"\s+", "", cell).lower() for cell in line.strip().strip("|").split("|")]
        condition_index = next((index for index, cell in enumerate(cells) if "条件" in cell or "状态" in cell), None)
        user_index = next((index for index, cell in enumerate(cells) if "用户操作" in cell or "用户动作" in cell), None)
        if prd_type == "ai-native":
            execution_index = next((index for index, cell in enumerate(cells) if "ai动作" in cell or "系统行为" in cell), None)
            feedback_index = next((index for index, cell in enumerate(cells) if "系统反馈" in cell or "ui反馈" in cell), None)
        else:
            execution_index = next((index for index, cell in enumerate(cells) if "系统行为" in cell), None)
            feedback_index = next((index for index, cell in enumerate(cells) if "ui反馈" in cell), None)
        required_indexes = (condition_index, user_index, execution_index, feedback_index)
        if any(index is None for index in required_indexes):
            continue

        for data_line in lines[line_index + 1 :]:
            if not data_line.strip():
                continue
            if not data_line.lstrip().startswith("|"):
                break
            data_cells = [cell.strip() for cell in data_line.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-{3,}:?", cell) for cell in data_cells):
                continue
            if all(index < len(data_cells) and data_cells[index] for index in required_indexes if index is not None):
                return True
    return False


def detect_maturity(text: str) -> str | None:
    first_section = re.search(r"^##\s+", text, re.M)
    preamble = text[: first_section.start()] if first_section else text
    explicit = re.search(r"(?:\*\*)?文档状态(?:\*\*)?\s*[：:]\s*(草稿|讨论中|已确认|draft|discussing|confirmed)\b", preamble, re.I)
    if explicit:
        return MATURITY_ALIASES[explicit.group(1).lower()]

    for _, title, start, end in heading_sections(text):
        if canonical_heading(title).lower() != "文档信息":
            continue
        section_text = text[start:end]
        explicit = re.search(r"(?:\*\*)?状态(?:\*\*)?\s*[：:]\s*(草稿|讨论中|已确认|draft|discussing|confirmed)\b", section_text, re.I)
        if explicit:
            return MATURITY_ALIASES[explicit.group(1).lower()]
        rows = [
            [part.strip().lower() for part in line.strip().strip("|").split("|")]
            for line in section_text.splitlines()
            if line.lstrip().startswith("|")
        ]
        for index, row in enumerate(rows):
            status_index = next((cell_index for cell_index, cell in enumerate(row) if cell in {"状态", "文档状态"}), None)
            if status_index is None:
                continue
            for value_row in rows[index + 1 :]:
                if all(re.fullmatch(r":?-{3,}:?", cell) for cell in value_row):
                    continue
                if status_index < len(value_row) and value_row[status_index] in MATURITY_ALIASES:
                    return MATURITY_ALIASES[value_row[status_index]]
                break
    return None


def extract_labeled_background(text: str) -> str | None:
    match = re.search(
        r"(?:^|\n)\s*(?:[-*]\s*)?(?:\*\*)?背景(?:\*\*)?\s*[：:]\s*(.+?)"
        r"(?=\n\s*(?:[-*]\s*)?(?:\*\*)?[^\n：:]+(?:\*\*)?\s*[：:]|\n#{1,6}\s|\Z)",
        text,
        re.S,
    )
    if not match:
        return None
    return match.group(1).strip()


def extract_background(text: str) -> tuple[bool, str | None]:
    labeled = extract_labeled_background(text)
    if labeled is not None:
        return True, labeled

    sections = heading_sections(text)
    has_combined_heading = False
    for _, title, start, end in sections:
        canonical = canonical_heading(title).lower()
        if canonical == "背景":
            heading_end = text.find("\n", start, end)
            content = text[heading_end + 1 : end].strip() if heading_end != -1 else ""
            content = re.split(
                r"(?m)^\s*(?:[-*]\s*)?(?:\*\*)?(?:本期只解决|本期只讲|成功标准|不做)(?:\*\*)?\s*[：:]",
                content,
                maxsplit=1,
            )[0].strip()
            return True, content or None
        if canonical == "背景与目标":
            has_combined_heading = True
    return has_combined_heading, None


def visible_character_count(text: str) -> int:
    without_links = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)
    without_markup = re.sub(r"[`*_>#|~-]", "", without_links)
    return len(re.sub(r"\s+", "", without_markup))


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


def extract_image_targets(text: str) -> list[str]:
    targets = [match.group(1) or match.group(2) for match in MARKDOWN_IMAGE_PATTERN.finditer(text)]
    targets.extend(match.group(1) for match in HTML_IMAGE_PATTERN.finditer(text))
    return targets


def extract_target_state_image_targets(text: str) -> list[str]:
    targets = [match.group(1) or match.group(2) for match in MARKDOWN_TARGET_IMAGE_PATTERN.finditer(text)]
    for tag_match in HTML_IMAGE_TAG_PATTERN.finditer(text):
        tag = tag_match.group(0)
        alt = re.search(r"\balt\s*=\s*[\"']([^\"']+)[\"']", tag, re.I)
        src = re.search(r"\bsrc\s*=\s*[\"']([^\"']+)[\"']", tag, re.I)
        if alt and src and re.search(r"目标态|目标状态", alt.group(1), re.I):
            targets.append(src.group(1))
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


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_path(path: Path) -> str:
    if path.is_file():
        return sha256_file(path)
    if not path.is_dir():
        return ""

    digest = hashlib.sha256()
    files = sorted(candidate for candidate in path.rglob("*") if candidate.is_file() and ".git" not in candidate.parts)
    for candidate in files:
        digest.update(candidate.relative_to(path).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(bytes.fromhex(sha256_file(candidate)))
    return digest.hexdigest()


def resolve_record_path(manifest_path: Path, value: object) -> Path | None:
    if not isinstance(value, str) or not value:
        return None
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = manifest_path.parent / path
    return path.resolve()


def resolved_image_targets(prd_path: Path, targets: list[str]) -> set[Path]:
    resolved: set[Path] = set()
    for target in targets:
        clean_target = target.split("#", 1)[0].split("?", 1)[0]
        if not clean_target or re.match(r"^(?:https?:|data:)", clean_target, re.I):
            continue
        image_path = Path(clean_target).expanduser()
        if not image_path.is_absolute():
            image_path = prd_path.parent / image_path
        resolved.add(image_path.resolve())
    return resolved


def git_output(repo: Path, *args: str) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def validate_mockup_manifest(manifest_path: Path, prd_path: Path, feature_text: str) -> list[str]:
    warnings: list[str] = []
    if not manifest_path.is_file():
        return [f"missing_mockup_manifest:{manifest_path}"]

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return [f"invalid_mockup_manifest:{manifest_path}"]

    if manifest.get("schema_version") != 1:
        warnings.append("invalid_mockup_manifest_schema")

    workflow = manifest.get("workflow")
    if not isinstance(workflow, dict) or workflow.get("stage") != "prd_embedded":
        warnings.append("invalid_mockup_workflow_stage")

    baseline = manifest.get("baseline")
    if not isinstance(baseline, dict) or baseline.get("kind") not in BASELINE_KINDS:
        warnings.append("invalid_mockup_baseline")
    else:
        if not isinstance(baseline.get("note"), str) or not baseline.get("note", "").strip():
            warnings.append("missing_mockup_baseline_selection_evidence")
        source = resolve_record_path(manifest_path, baseline.get("source"))
        if source is None or not source.exists():
            warnings.append("missing_mockup_baseline_source")
        elif baseline.get("kind") == "frontend-repo":
            revision = git_output(source, "rev-parse", "HEAD")
            status = git_output(source, "status", "--porcelain=v1", "--untracked-files=no")
            if revision is None or status is None:
                warnings.append("invalid_frontend_repo_baseline")
            else:
                if revision != baseline.get("revision"):
                    warnings.append("stale_frontend_repo_revision")
                if sha256_bytes(status.encode("utf-8")) != baseline.get("worktree_status_sha256"):
                    warnings.append("stale_frontend_repo_worktree")
        elif sha256_path(source) != baseline.get("sha256"):
            warnings.append("stale_mockup_baseline_hash")

    mockup = manifest.get("mockup")
    mockup_path: Path | None = None
    mockup_hash: str | None = None
    mockup_mtime_ns: int | None = None
    if not isinstance(mockup, dict):
        warnings.append("invalid_mockup_manifest_artifact")
    else:
        mockup_path = resolve_record_path(manifest_path, mockup.get("path"))
        if mockup_path is None or not mockup_path.is_file():
            warnings.append("missing_manifest_mockup_file")
        else:
            mockup_hash = sha256_file(mockup_path)
            mockup_mtime_ns = mockup_path.stat().st_mtime_ns
            if mockup_hash != mockup.get("sha256"):
                warnings.append("stale_mockup_hash")

    image_targets = resolved_image_targets(prd_path, extract_image_targets(feature_text))
    screenshots = manifest.get("screenshots")
    if not isinstance(screenshots, list) or not screenshots:
        warnings.append("missing_manifest_screenshots")
    else:
        for screenshot in screenshots:
            if not isinstance(screenshot, dict):
                warnings.append("invalid_manifest_screenshot")
                continue
            state = screenshot.get("state") or "unknown"
            screenshot_path = resolve_record_path(manifest_path, screenshot.get("path"))
            if screenshot_path is None or not screenshot_path.is_file():
                warnings.append(f"missing_manifest_screenshot_file:{state}")
                continue
            if sha256_file(screenshot_path) != screenshot.get("sha256"):
                warnings.append(f"stale_manifest_screenshot_hash:{state}")
            if mockup_hash is not None and screenshot.get("source_mockup_sha256") != mockup_hash:
                warnings.append(f"stale_screenshot_source_mockup:{state}")
            if mockup_mtime_ns is not None and screenshot_path.stat().st_mtime_ns < mockup_mtime_ns:
                warnings.append(f"stale_screenshot_mtime:{state}")
            if screenshot_path.resolve() not in image_targets:
                warnings.append(f"manifest_screenshot_not_embedded:{state}")

    prd = manifest.get("prd")
    if not isinstance(prd, dict):
        warnings.append("invalid_manifest_prd")
    else:
        manifest_prd_path = resolve_record_path(manifest_path, prd.get("path"))
        if manifest_prd_path != prd_path.resolve():
            warnings.append("manifest_prd_path_mismatch")
        elif sha256_file(prd_path) != prd.get("sha256"):
            warnings.append("stale_manifest_prd_hash")

    return warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Check PRD shape and warn on over-technical drafts.")
    parser.add_argument("path", help="Path to a Markdown PRD")
    parser.add_argument("--type", choices=sorted(REQUIRED_CAPABILITIES), default="standard", help="Expected PRD type")
    parser.add_argument(
        "--maturity",
        choices=("draft", "discussing", "confirmed"),
        help="Override auto-detected document maturity for open-question checks",
    )
    parser.add_argument("--allow-handoff", action="store_true", help="Allow technical schema details in the document")
    parser.add_argument("--publish-ready", action="store_true", help="Check for online-publishing contamination such as local mock links")
    parser.add_argument(
        "--require-version-history",
        action="store_true",
        help="Require the canonical newest-first PRD version history table near the top of the document",
    )
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
    parser.add_argument(
        "--require-current-mockup-evidence",
        action="store_true",
        help="Require a provenance manifest proving screenshots and PRD references match the current HTML and UI baseline",
    )
    parser.add_argument("--mockup-manifest", help="Path to mockup-evidence.json")
    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2

    text = path.read_text(encoding="utf-8")
    body_to_check = text if args.allow_handoff else strip_handoff_appendix(text)
    warnings: list[str] = []

    if args.require_version_history or args.publish_ready:
        _, version_warnings = validate_version_history(text)
        warnings.extend(version_warnings)

    for name, pattern in OVER_TECH_PATTERNS:
        if pattern.search(body_to_check):
            warnings.append(f"over_technical:{name}")

    titles = heading_titles(body_to_check)
    maturity = args.maturity or detect_maturity(text)
    for capability, alternatives in REQUIRED_CAPABILITIES[args.type].items():
        if capability == "open_questions" and (args.publish_ready or maturity == "confirmed"):
            continue
        if not has_heading_capability(titles, alternatives):
            warnings.append(f"missing_expected_capability:{capability}")

    background_marker, background = extract_background(body_to_check)
    if background is not None:
        background_length = visible_character_count(background)
        if background_length > 200:
            warnings.append(f"background_too_long:{background_length}")
    elif background_marker:
        warnings.append("background_uncheckable")

    for title in titles:
        canonical = canonical_heading(title)
        if canonical in LEGACY_PARALLEL_SECTIONS:
            warnings.append(f"legacy_parallel_section:{canonical}")

    modules = extract_feature_modules(body_to_check, args.type)
    if has_heading_capability(titles, REQUIRED_CAPABILITIES[args.type]["feature_modules"]) and not modules:
        warnings.append("missing_feature_module_entries")
    for title, module_text in modules:
        if not module_has_logic_table(module_text, args.type):
            warnings.append(f"missing_module_logic:{title}")

    if "本期只解决" not in text and "本期只讲" not in text:
        warnings.append("missing_scope_sentence")

    if args.publish_ready:
        for name, pattern in PUBLISH_CONTAMINATION_PATTERNS:
            if pattern.search(body_to_check):
                warnings.append(f"publish_contamination:{name}")

    if args.require_mockup_evidence:
        feature_text = "\n".join(module_text for _, module_text in modules)
        image_targets = extract_image_targets(feature_text)
        if not modules:
            warnings.append("missing_mockup_evidence")
        for title, module_text in modules:
            if not extract_target_state_image_targets(module_text):
                warnings.append(f"missing_module_target_state_evidence:{title}")
        for target in missing_local_image_targets(path, image_targets):
            warnings.append(f"missing_mockup_file:{target}")
    else:
        feature_text = "\n".join(module_text for _, module_text in modules)

    if args.require_current_mockup_evidence and not args.mockup_manifest:
        warnings.append("missing_mockup_manifest_argument")
    if args.mockup_manifest:
        manifest_path = Path(args.mockup_manifest).expanduser()
        if not manifest_path.is_absolute():
            manifest_path = path.parent / manifest_path
        warnings.extend(validate_mockup_manifest(manifest_path.resolve(), path.resolve(), feature_text))

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
