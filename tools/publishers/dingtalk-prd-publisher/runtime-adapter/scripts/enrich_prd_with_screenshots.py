#!/usr/bin/env python3
"""Capture PRD lookup/mock pages and insert screenshots into an enriched copy."""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse


LOOKUP_KEYWORDS = (
    "look up",
    "lookup",
    "mock",
    "prototype",
    "preview",
    "demo",
    "关联",
    "产物",
    "原型",
    "预览",
    "截图",
    "页面",
)

PUBLISH_AUX_SECTION_KEYWORDS = (
    "文档信息",
    "关联产物",
    "本地草稿附录",
    "待确认事项",
    "待确认",
)

SEMANTIC_SECTION_KEYWORDS = (
    "页面",
    "结构",
    "布局",
    "交互",
    "状态",
    "输入框",
    "任务卡",
    "取消",
    "流程",
    "展示",
    "前端",
    "样式",
    "反馈",
)

PUBLISH_TABLE_ROW_PATTERNS = (
    re.compile(r"^\|.*关联\s*mock.*\|", re.I),
    re.compile(r"^\|.*(?:\.html|\.htm|dingtalk-assets|file://|localhost|127\.0\.0\.1).*\|", re.I),
)

MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)")
RAW_URL_RE = re.compile(r"(?<!\()https?://[^\s<>)|]+")
HTML_PATH_RE = re.compile(r"(?<!\()((?:\.{1,2}/|/|[\w.-]+/)[^\s|()<>]*?\.html(?:[#?][^\s|)]*)?)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
PLACEHOLDER_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII="
)


@dataclass
class Occurrence:
    label: str
    href: str
    line_index: int
    section: str
    context: str


@dataclass
class Target:
    label: str
    href: str
    line_index: int
    section: str
    context: str
    url: str
    resolved_path: Path | None
    exists: bool
    screenshot_path: Path | None = None
    insert_after: int = 0
    warnings: list[str] = field(default_factory=list)
    publish_cleanup: dict[str, Any] = field(default_factory=dict)


def clean_href(raw: str) -> str:
    value = raw.strip()
    if value.startswith("<") and ">" in value:
        return value[1 : value.index(">")].strip()
    match = re.match(r"([^\s]+)(?:\s+['\"].*)?$", value)
    return (match.group(1) if match else value).strip()


def strip_fragment_and_query(href: str) -> str:
    return re.split(r"[#?]", href, maxsplit=1)[0]


def keyword_hit(*values: str) -> bool:
    text = " ".join(values).lower()
    return any(keyword.lower() in text for keyword in LOOKUP_KEYWORDS)


def section_for_line(lines: list[str], line_index: int) -> str:
    current = ""
    for index in range(0, line_index + 1):
        match = HEADING_RE.match(lines[index])
        if match:
            current = match.group(2).strip()
    return current


def section_is_publish_aux(section: str) -> bool:
    normalized = section.lower()
    return any(keyword.lower() in normalized for keyword in PUBLISH_AUX_SECTION_KEYWORDS)


def discover_occurrences(markdown: str) -> list[Occurrence]:
    lines = markdown.splitlines()
    found: list[Occurrence] = []

    for line_index, line in enumerate(lines):
        context = "\n".join(lines[max(0, line_index - 1) : min(len(lines), line_index + 2)])
        seen_spans: list[tuple[int, int]] = []

        for match in MARKDOWN_LINK_RE.finditer(line):
            label = match.group(1).strip()
            href = clean_href(match.group(2))
            seen_spans.append(match.span(2))
            if should_consider(label, href, context):
                found.append(
                    Occurrence(
                        label=label or href,
                        href=href,
                        line_index=line_index,
                        section=section_for_line(lines, line_index),
                        context=context,
                    )
                )

        for match in RAW_URL_RE.finditer(line):
            if any(start <= match.start() <= end for start, end in seen_spans):
                continue
            href = match.group(0).rstrip(".,;")
            if should_consider(href, href, context):
                found.append(
                    Occurrence(
                        label=href,
                        href=href,
                        line_index=line_index,
                        section=section_for_line(lines, line_index),
                        context=context,
                    )
                )

        for match in HTML_PATH_RE.finditer(line):
            if any(start <= match.start() <= end for start, end in seen_spans):
                continue
            href = clean_href(match.group(1))
            if should_consider(href, href, context):
                found.append(
                    Occurrence(
                        label=Path(strip_fragment_and_query(href)).name or href,
                        href=href,
                        line_index=line_index,
                        section=section_for_line(lines, line_index),
                        context=context,
                    )
                )

    return found


def should_consider(label: str, href: str, context: str) -> bool:
    parsed = urlparse(href)
    if parsed.scheme and parsed.scheme not in {"http", "https", "file"}:
        return False
    href_path = strip_fragment_and_query(href).lower()
    if href_path.endswith(".html") or href_path.endswith(".htm"):
        return True
    return keyword_hit(label, href, context)


def resolve_url(prd_dir: Path, href: str) -> tuple[str, Path | None, bool]:
    parsed = urlparse(href)
    if parsed.scheme in {"http", "https"}:
        return href, None, True
    if parsed.scheme == "file":
        path = Path(unquote(parsed.path))
        return href, path, path.exists()

    local_part = unquote(strip_fragment_and_query(href))
    local_path = Path(local_part)
    if not local_path.is_absolute():
        local_path = prd_dir / local_path
    local_path = local_path.resolve()

    suffix = ""
    if "#" in href:
        suffix = "#" + href.split("#", 1)[1]
    return local_path.as_uri() + suffix, local_path, local_path.exists()


def occurrence_score(occurrence: Occurrence) -> tuple[int, int]:
    section = occurrence.section.lower()
    score = 0
    if section_is_publish_aux(occurrence.section):
        score -= 100
    if any(keyword.lower() in section for keyword in SEMANTIC_SECTION_KEYWORDS):
        score += 80
    if keyword_hit(occurrence.label, occurrence.context):
        score += 20
    return score, -occurrence.line_index


def dedupe_targets(prd_dir: Path, occurrences: list[Occurrence]) -> list[Target]:
    grouped: dict[str, list[tuple[Occurrence, str, Path | None, bool]]] = {}
    for occurrence in occurrences:
        url, resolved_path, exists = resolve_url(prd_dir, occurrence.href)
        key = str(resolved_path) if resolved_path else url
        grouped.setdefault(key, []).append((occurrence, url, resolved_path, exists))

    targets: list[Target] = []
    for items in grouped.values():
        occurrence, url, resolved_path, exists = max(items, key=lambda item: occurrence_score(item[0]))
        targets.append(
            Target(
                label=occurrence.label,
                href=occurrence.href,
                line_index=occurrence.line_index,
                section=occurrence.section,
                context=occurrence.context,
                url=url,
                resolved_path=resolved_path,
                exists=exists,
            )
        )
    targets.sort(key=lambda target: target.line_index)
    return targets


def find_publish_fallback_line(lines: list[str]) -> tuple[int, str] | None:
    for index, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if not match:
            continue
        section = match.group(2).strip()
        if section and not section_is_publish_aux(section):
            return index, section
    return None


def adjust_publish_placements(markdown: str, targets: list[Target]) -> None:
    lines = markdown.splitlines()
    fallback = find_publish_fallback_line(lines)
    if not fallback:
        return
    fallback_line, fallback_section = fallback
    for target in targets:
        if section_is_publish_aux(target.section):
            target.publish_cleanup["original_section"] = target.section
            target.line_index = fallback_line
            target.section = fallback_section
            target.warnings.append("placement moved out of local-only section for DingTalk publishing")


def heading_level(line: str) -> int | None:
    match = HEADING_RE.match(line)
    return len(match.group(1)) if match else None


def should_remove_publish_section(title: str) -> bool:
    return section_is_publish_aux(title) and "文档信息" not in title


def clean_for_publish(markdown: str) -> tuple[str, dict[str, Any]]:
    lines = markdown.splitlines()
    cleaned: list[str] = []
    removed_sections: list[str] = []
    removed_rows = 0
    skip_level: int | None = None

    for line in lines:
        current_level = heading_level(line)
        if skip_level is not None:
            if current_level is not None and current_level <= skip_level:
                skip_level = None
            else:
                continue

        if current_level is not None:
            title = HEADING_RE.match(line).group(2).strip()  # type: ignore[union-attr]
            if should_remove_publish_section(title):
                removed_sections.append(title)
                skip_level = current_level
                continue

        stripped = line.strip()
        if stripped.startswith("|") and any(pattern.search(stripped) for pattern in PUBLISH_TABLE_ROW_PATTERNS):
            removed_rows += 1
            continue

        cleaned.append(line)

    while cleaned and not cleaned[-1].strip():
        cleaned.pop()
    return "\n".join(cleaned).rstrip() + "\n", {
        "removed_sections": removed_sections,
        "removed_table_rows": removed_rows,
    }


def insertion_index(lines: list[str], line_index: int) -> int:
    stripped = lines[line_index].strip()
    if stripped.startswith("|") and "|" in stripped[1:]:
        index = line_index
        while index + 1 < len(lines) and lines[index + 1].strip().startswith("|"):
            index += 1
        return index + 1
    if re.match(r"^[-*+]\s+", stripped):
        return line_index + 1

    index = line_index
    while index + 1 < len(lines) and lines[index + 1].strip():
        if HEADING_RE.match(lines[index + 1]):
            break
        index += 1
    return index + 1


def slug(value: str, fallback: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-._")
    cleaned = re.sub(r"-{2,}", "-", cleaned)
    return cleaned[:72] or fallback


def screenshot_filename(target: Target, index: int) -> str:
    source = target.resolved_path.name if target.resolved_path else target.label
    name = slug(source, f"lookup-{index}")
    if not name.lower().endswith(".png"):
        name = f"{name}.png"
    return f"{index:02d}-{name}"


def capture_placeholder(output: Path) -> None:
    output.write_bytes(PLACEHOLDER_PNG)


def capture_with_playwright(target: Target, output: Path, viewport: str, wait_ms: int, timeout_ms: int) -> None:
    if not shutil.which("npx"):
        raise RuntimeError("missing npx; install Node.js/npm or use --capture-mode placeholder for smoke tests")
    args = [
        "npx",
        "--yes",
        "playwright",
        "screenshot",
        "--full-page",
        "--viewport-size",
        viewport,
        "--wait-for-timeout",
        str(wait_ms),
        "--timeout",
        str(timeout_ms),
        target.url,
        str(output),
    ]
    result = subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"playwright screenshot failed for {target.url}: {detail}")


def capture_targets(
    targets: list[Target],
    asset_dir: Path,
    capture_mode: str,
    viewport: str,
    wait_ms: int,
    timeout_ms: int,
) -> None:
    asset_dir.mkdir(parents=True, exist_ok=True)
    for index, target in enumerate(targets, start=1):
        output = asset_dir / screenshot_filename(target, index)
        target.screenshot_path = output
        if capture_mode == "none":
            target.warnings.append("capture skipped")
            continue
        if capture_mode == "placeholder":
            capture_placeholder(output)
            continue
        if target.resolved_path is not None and not target.exists:
            raise RuntimeError(f"local lookup target not found: {target.resolved_path}")
        capture_with_playwright(target, output, viewport, wait_ms, timeout_ms)


def relative_markdown_path(image: Path, output_markdown: Path) -> str:
    relative = os.path.relpath(image, output_markdown.parent)
    return relative.replace(os.sep, "/")


def insert_screenshots(markdown: str, output_markdown: Path, targets: list[Target]) -> str:
    lines = markdown.splitlines()
    blocks_by_index: dict[int, list[str]] = {}

    for target in targets:
        if not target.screenshot_path:
            continue
        target.insert_after = insertion_index(lines, target.line_index)
        image_path = relative_markdown_path(target.screenshot_path, output_markdown)
        marker_payload = {
            "source": target.href,
            "url": target.url,
            "section": target.section,
        }
        block = [
            "",
            f"<!-- dingtalk-prd-screenshot: {json.dumps(marker_payload, ensure_ascii=False)} -->",
            f"![{target.label} screenshot]({image_path})",
            f"*截图来源：{target.label}*",
            "",
        ]
        blocks_by_index.setdefault(target.insert_after, []).extend(block)

    enriched = list(lines)
    for index in sorted(blocks_by_index, reverse=True):
        enriched[index:index] = blocks_by_index[index]
    return "\n".join(enriched).rstrip() + "\n"


def target_to_json(target: Target) -> dict[str, Any]:
    return {
        "label": target.label,
        "href": target.href,
        "line": target.line_index + 1,
        "url": target.url,
        "resolved_path": str(target.resolved_path) if target.resolved_path else None,
        "exists": target.exists,
        "screenshot_path": str(target.screenshot_path) if target.screenshot_path else None,
        "placement": {
            "section": target.section,
            "line": target.line_index + 1,
            "insert_after": target.insert_after + 1 if target.insert_after else None,
        },
        "warnings": target.warnings,
        "publish_cleanup": target.publish_cleanup,
    }


def build_report(prd: Path, output: Path | None, asset_dir: Path | None, targets: list[Target]) -> dict[str, Any]:
    return {
        "source": str(prd),
        "output": str(output) if output else None,
        "asset_dir": str(asset_dir) if asset_dir else None,
        "targets": [target_to_json(target) for target in targets],
        "publish_cleanup": {},
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prd", help="Local PRD Markdown file")
    parser.add_argument("--output", help="Enriched Markdown output path")
    parser.add_argument("--asset-dir", help="Screenshot asset directory")
    parser.add_argument("--dry-run", action="store_true", help="Only discover targets and print a report")
    parser.add_argument("--json", action="store_true", help="Print JSON report")
    parser.add_argument(
        "--capture-mode",
        choices=("playwright", "placeholder", "none"),
        default="playwright",
        help="Screenshot capture backend. placeholder is for deterministic smoke tests.",
    )
    parser.add_argument("--viewport", default="1440,1200", help="Playwright viewport, for example 1440,1200")
    parser.add_argument("--wait-ms", type=int, default=1500, help="Wait before screenshot")
    parser.add_argument("--timeout-ms", type=int, default=30000, help="Playwright action timeout")
    parser.add_argument("--max-targets", type=int, default=10, help="Maximum lookup targets to capture")
    parser.add_argument(
        "--no-publish-cleanup",
        action="store_true",
        help="Keep local-only PRD sections such as 关联产物 and 待确认事项 in the enriched copy",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    prd = Path(args.prd).expanduser().resolve()
    if not prd.exists():
        print(f"error: PRD not found: {prd}", file=sys.stderr)
        return 2
    if prd.suffix.lower() not in {".md", ".markdown"}:
        print(f"error: expected a Markdown PRD, got: {prd}", file=sys.stderr)
        return 2

    markdown = prd.read_text(encoding="utf-8")
    occurrences = discover_occurrences(markdown)
    targets = dedupe_targets(prd.parent, occurrences)
    if not args.no_publish_cleanup:
        adjust_publish_placements(markdown, targets)
    if len(targets) > args.max_targets:
        print(f"error: found {len(targets)} lookup targets; raise --max-targets if intended", file=sys.stderr)
        return 2

    if args.dry_run:
        report = build_report(prd, None, None, targets)
    else:
        output = Path(args.output).expanduser().resolve() if args.output else prd.with_name(f"{prd.stem}.dingtalk.enriched.md")
        asset_dir = (
            Path(args.asset_dir).expanduser().resolve()
            if args.asset_dir
            else prd.with_name(f"{prd.stem}.dingtalk-assets")
        )
        capture_targets(targets, asset_dir, args.capture_mode, args.viewport, args.wait_ms, args.timeout_ms)
        enriched = insert_screenshots(markdown, output, targets)
        cleanup_report: dict[str, Any] = {}
        if not args.no_publish_cleanup:
            enriched, cleanup_report = clean_for_publish(enriched)
        output.write_text(enriched, encoding="utf-8")
        report = build_report(prd, output, asset_dir, targets)
        report["publish_cleanup"] = cleanup_report

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Source: {report['source']}")
        if report["output"]:
            print(f"Output: {report['output']}")
        print(f"Targets: {len(report['targets'])}")
        for target in report["targets"]:
            print(f"- line {target['line']}: {target['label']} -> {target['url']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
