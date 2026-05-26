#!/usr/bin/env python3
"""对 Codex Skill 目录或 SKILL.md 做轻量确定性检查。"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path


CORE_SIGNALS = {
    "overview/purpose": ["overview", "purpose", "goal", "概览", "目的", "目标"],
    "workflow/procedure": ["workflow", "process", "procedure", "steps", "工作流", "流程", "步骤"],
    "input/context intake": ["input", "context intake", "required information", "inputs", "输入", "背景补齐", "必要信息"],
    "output/deliverable": ["output", "deliverable", "output format", "final answer", "输出", "交付物", "输出格式"],
    "definition of done": ["definition of done", "done", "acceptance criteria", "success criteria", "完成定义", "验收标准", "成功标准"],
    "resources/assets": ["resources", "resource guide", "references", "scripts", "assets", "资源", "资源指南", "资产"],
    "evaluation/testing": ["evaluation", "testing", "smoke", "grader", "regression", "评测", "测试", "回归"],
}

TRIGGER_TERMS = [
    r"\buse when\b",
    r"\bwhen\b",
    r"\buse this skill\b",
    r"\btrigger\b",
    "使用场景",
    "什么时候",
    "何时使用",
    "触发",
    "用于",
    "当用户",
    "当需要",
]

WORKFLOW_TERMS = [
    r"\bstep\b",
    r"\bfirst\b",
    r"\bthen\b",
    r"\bfinally\b",
    r"\bworkflow\b",
    r"\bprocess\b",
    "步骤",
    "流程",
    "然后",
    "最后",
    "先",
]

EVALUATION_TERMS = [
    "evaluation",
    "testing",
    "smoke",
    "grader",
    "regression",
    "validation",
    "verify",
    "评测",
    "测试",
    "回归",
    "验证",
]

OUTPUT_TERMS = ["output", "deliverable", "final answer", "输出", "交付物", "输出格式"]
DONE_TERMS = ["definition of done", "acceptance criteria", "success criteria", "完成定义", "验收标准", "成功标准"]

CODEX_KEYS = {"name", "description"}
KNOWN_ECOSYSTEM_KEYS = {
    "allowed-tools",
    "triggers",
    "version",
    "argument-hint",
    "handoffs",
    "scripts",
    "requires",
    "tools",
    "origin",
    "color",
    "metadata",
}


def is_top_level_key(line: str) -> bool:
    return bool(line.strip()) and not line.startswith((" ", "\t")) and ":" in line


def normalize_block_scalar(lines: list[str], folded: bool) -> str:
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    if not lines:
        return ""

    indents = [len(line) - len(line.lstrip(" ")) for line in lines if line.strip()]
    strip_width = min(indents) if indents else 0
    stripped = [line[strip_width:] if len(line) >= strip_width else line for line in lines]
    return " ".join(line.strip() for line in stripped if line.strip()) if folded else "\n".join(stripped)


def parse_frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    if not text.startswith("---\n"):
        return {}, ["缺少由 --- 包裹的 YAML frontmatter"]

    end = text.find("\n---", 4)
    if end == -1:
        return {}, ["frontmatter 起始 --- 没有对应的结束 ---"]

    raw = text[4:end].strip("\n")
    data: dict[str, str] = {}
    current_key: str | None = None
    lines = raw.splitlines()
    idx = 0
    while idx < len(lines):
        line = lines[idx]
        line_no = idx + 2
        if not line.strip():
            idx += 1
            continue
        if line.startswith((" ", "\t")) and current_key:
            idx += 1
            continue
        if ":" not in line:
            errors.append(f"frontmatter 第 {line_no} 行不是 key: value 格式")
            idx += 1
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        if value.startswith(("|", ">")):
            folded = value.startswith(">")
            block_lines: list[str] = []
            idx += 1
            while idx < len(lines) and not is_top_level_key(lines[idx]):
                block_lines.append(lines[idx])
                idx += 1
            value = normalize_block_scalar(block_lines, folded)
            data[key] = value
            current_key = key
            continue
        data[key] = value
        current_key = key
        idx += 1
    return data, errors


def body_text(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---", 4)
    if end == -1:
        return text
    return text[end + 4 :]


def find_sections(text: str) -> set[str]:
    sections: set[str] = set()
    for match in re.finditer(r"^#{2,3}\s+(.+?)\s*$", text, flags=re.MULTILINE):
        sections.add(match.group(1).strip().lower())
    return sections


def has_signal(text: str, sections: set[str], terms: list[str]) -> bool:
    lower_text = text.lower()
    for term in terms:
        if term in sections or term in lower_text:
            return True
    return False


def has_any(text: str, terms: list[str]) -> bool:
    lower_text = text.lower()
    return any(re.search(term, text, flags=re.IGNORECASE) if term.startswith(r"\b") else term.lower() in lower_text for term in terms)


def line_for_pattern(text: str, pattern: str) -> int | None:
    for idx, line in enumerate(text.splitlines(), start=1):
        if pattern in line:
            return idx
    return None


def line_for_unresolved_placeholder(text: str) -> int | None:
    placeholder = re.compile(r"^\s*(?:[-*]\s*)?(?:<!--\s*)?(?:TODO|TBD|FIXME)(?:\b|[:：<])", re.IGNORECASE)
    for idx, line in enumerate(text.splitlines(), start=1):
        if placeholder.search(line):
            return idx
    return None


def add_issue(issues: list[tuple[str, str]], severity: str, message: str) -> None:
    issues.append((severity, message))


def check_description(description: str, issues: list[tuple[str, str]]) -> None:
    if len(description) < 80:
        add_issue(issues, "P1", "description 偏短，可能不足以承担触发契约 Trigger Contract")
    if len(description) > 700:
        add_issue(issues, "W", "description 很长，可能把正文职责塞进触发契约")
    if not any(re.search(term, description, flags=re.IGNORECASE) for term in TRIGGER_TERMS):
        add_issue(issues, "P1", "description 没有清楚说明何时使用该 Skill")
    if line_for_unresolved_placeholder(description):
        add_issue(issues, "P0", "description 仍包含未处理占位符 TODO/TBD/FIXME")

    workflow_hits = sum(1 for term in WORKFLOW_TERMS if re.search(term, description, flags=re.IGNORECASE))
    if workflow_hits >= 4:
        add_issue(issues, "W", "description 包含较多流程词，建议确认它是否仍是 trigger-only description")

    if not re.search(r"\b(use when|when the user|when codex|use this skill)\b", description, flags=re.IGNORECASE) and not any(
        term in description for term in ["当用户", "当需要", "何时使用", "触发"]
    ):
        add_issue(issues, "W", "description 缺少明确的自然语言触发表达，建议加入 Use when / 当用户 语义")


def check_body(text: str, skill_dir: Path, issues: list[tuple[str, str]]) -> None:
    body = body_text(text)
    body_lines = body.splitlines()
    sections = find_sections(text)

    missing = [
        signal for signal, terms in CORE_SIGNALS.items()
        if not has_signal(text, sections, terms)
    ]
    if len(missing) >= 5:
        add_issue(issues, "P1", f"缺少多项预期设计信号：{', '.join(missing)}")
    elif missing:
        add_issue(issues, "P2", f"建议补充或明确覆盖这些设计信号：{', '.join(missing)}")

    if len(body_lines) > 500:
        add_issue(issues, "W", f"SKILL.md 正文约 {len(body_lines)} 行，接近或超过 context budget 建议上限")
    elif len(body_lines) > 350 and not (skill_dir / "references").exists():
        add_issue(issues, "W", f"SKILL.md 正文约 {len(body_lines)} 行且没有 references/，建议拆分详细内容")

    if not has_any(text, DONE_TERMS):
        add_issue(issues, "W", "缺少明确 Definition of Done / 验收标准 / 成功标准线索")
    if not has_any(text, OUTPUT_TERMS):
        add_issue(issues, "W", "缺少明确输出格式或交付物线索")
    if not has_any(text, EVALUATION_TERMS):
        add_issue(issues, "W", "缺少 smoke / eval / validation / regression 等评测线索")


def check_resources(text: str, skill_dir: Path, issues: list[tuple[str, str]]) -> None:
    lower_text = text.lower()
    for dirname in ["references", "scripts", "assets"]:
        resource_dir = skill_dir / dirname
        if resource_dir.exists() and resource_dir.is_dir():
            files = [p for p in resource_dir.rglob("*") if p.is_file()]
            if not files:
                add_issue(issues, "P2", f"{dirname}/ 存在但为空")
                continue
            if dirname not in lower_text:
                add_issue(issues, "P2", f"{dirname}/ 存在但没有在 SKILL.md 中说明")

    references_dir = skill_dir / "references"
    if references_dir.exists():
        for ref in references_dir.rglob("*"):
            if not ref.is_file():
                continue
            rel = ref.relative_to(skill_dir).as_posix()
            name = ref.name
            if rel not in text and name not in text:
                add_issue(issues, "W", f"reference 未被 SKILL.md 直接提及，可能不易发现：{rel}")

    scripts_dir = skill_dir / "scripts"
    if scripts_dir.exists():
        for script in scripts_dir.rglob("*.py"):
            rel = script.relative_to(skill_dir).as_posix()
            first_line = script.read_text(encoding="utf-8", errors="ignore").splitlines()[:1]
            if first_line and "python" not in first_line[0] and os.access(script, os.X_OK):
                add_issue(issues, "P2", f"可执行 Python script 缺少 python shebang：{rel}")
            if rel not in text and script.name not in text:
                add_issue(issues, "W", f"script 未被 SKILL.md 直接提及，可能缺少使用说明：{rel}")


def check(path: Path) -> int:
    issues: list[tuple[str, str]] = []

    if path.is_dir():
        skill_dir = path
        skill_file = skill_dir / "SKILL.md"
    else:
        skill_file = path
        skill_dir = path.parent

    if not skill_file.exists():
        print(f"P0: 未找到 SKILL.md：{skill_file}")
        return 2

    text = skill_file.read_text(encoding="utf-8")
    frontmatter, fm_errors = parse_frontmatter(text)
    for err in fm_errors:
        add_issue(issues, "P0", err)

    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    folder_name = skill_dir.name

    is_codex_skill_target = path.is_dir() or skill_file.name == "SKILL.md"

    if not name:
        if is_codex_skill_target:
            add_issue(issues, "P0", "frontmatter 缺少必需字段 'name'")
        else:
            add_issue(issues, "W", "输入文件不是 SKILL.md 且缺少 name；作为跨生态 command/template 可兼容，迁移为 Codex Skill 时需补齐")
    elif not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,62}", name):
        add_issue(issues, "P0", f"name '{name}' 必须只使用小写字母、数字和连字符")

    if path.is_dir() and name and name != folder_name:
        add_issue(issues, "P1", f"name '{name}' 与目录名 '{folder_name}' 不一致")

    if not description:
        add_issue(issues, "P0", "frontmatter 缺少必需字段 'description'")
    else:
        check_description(description, issues)

    extra_keys = sorted(set(frontmatter) - CODEX_KEYS)
    known_extra = [key for key in extra_keys if key in KNOWN_ECOSYSTEM_KEYS]
    unknown_extra = [key for key in extra_keys if key not in KNOWN_ECOSYSTEM_KEYS]
    if known_extra:
        add_issue(issues, "W", f"frontmatter 存在兼容生态扩展字段：{', '.join(known_extra)}")
    if unknown_extra:
        add_issue(issues, "P2", f"frontmatter 存在未知额外字段：{', '.join(unknown_extra)}")

    placeholder_line = line_for_unresolved_placeholder(text)
    if placeholder_line:
        add_issue(issues, "P1", f"SKILL.md 第 {placeholder_line} 行仍包含未处理占位符 TODO/TBD/FIXME")

    check_body(text, skill_dir, issues)
    check_resources(text, skill_dir, issues)

    if not issues:
        print("未发现确定性结构问题。")
        return 0

    severity_rank = {"P0": 0, "P1": 1, "P2": 2, "W": 3}
    for severity, message in sorted(issues, key=lambda item: severity_rank[item[0]]):
        print(f"{severity}: {message}")

    return 2 if any(sev == "P0" for sev, _ in issues) else 1 if any(sev in {"P1", "P2"} for sev, _ in issues) else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="检查 Codex Skill 目录或 SKILL.md。")
    parser.add_argument("path", help="Skill 目录或 SKILL.md 路径")
    args = parser.parse_args()
    return check(Path(args.path).expanduser().resolve())


if __name__ == "__main__":
    sys.exit(main())
