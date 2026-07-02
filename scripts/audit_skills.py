#!/usr/bin/env python3
"""Repository-level audit for public AI PM Skills."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


SKIP_DIRS = {
    ".git",
    ".github",
    "assets",
    "docs",
    "examples",
    "loop-patterns",
    "promotions",
    "scripts",
}

LOCAL_PATH_RE = re.compile(
    r"(/Users/|~/(?:\.honeycomb-agent|\.codex|\.claude)|\.claude/hooks|honeycomb diagram-guard|/propose-honeycomb-change)"
)

HIGH_RISK_SCRIPT_SKILLS = {
    "brainstorming",
    "competitive-analysis",
    "decision-research",
    "prd-architect",
    "prd-review",
    "prd-to-issues",
    "research-topic-compiler",
    "ui-mockup-desktop-workbench",
    "ui-wireframe-to-html",
}


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    raw = text[4:end]
    data: dict[str, str] = {}
    current_key: str | None = None
    current_value: list[str] = []
    for line in raw.splitlines():
        if line.startswith(" ") and current_key:
            current_value.append(line.strip())
            continue
        if current_key:
            data[current_key] = " ".join(current_value).strip().strip('"')
            current_key = None
            current_value = []
        if ":" in line:
            key, value = line.split(":", 1)
            current_key = key.strip()
            current_value = [value.strip().strip(">")]
    if current_key:
        data[current_key] = " ".join(current_value).strip().strip('"')
    return data


def list_skill_dirs(root: Path) -> list[Path]:
    dirs: list[Path] = []
    for path in sorted(root.iterdir()):
        if not path.is_dir() or path.name in SKIP_DIRS:
            continue
        if (path / "SKILL.md").exists():
            dirs.append(path)
    return dirs


def validate_eval_file(skill_dir: Path) -> list[str]:
    warnings: list[str] = []
    eval_path = skill_dir / "evals" / "evals.json"
    if not eval_path.exists():
        warnings.append("missing evals/evals.json")
        return warnings
    try:
        payload = json.loads(eval_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return [f"invalid evals/evals.json: {error}"]
    if payload.get("skill_name") != skill_dir.name:
        warnings.append("eval skill_name does not match folder")
    evals = payload.get("evals")
    if not isinstance(evals, list) or not evals:
        warnings.append("evals array is missing or empty")
        return warnings
    for item in evals:
        if not isinstance(item, dict):
            warnings.append("eval item is not an object")
            continue
        for field in ("id", "prompt", "expected_output"):
            if field not in item:
                warnings.append(f"eval {item.get('id', '<unknown>')} missing {field}")
    return warnings


def compare_duplicate_scripts(root: Path, rel: str) -> list[str]:
    left = root / "prd-architect" / rel
    right = root / "prd-review" / rel
    if not left.exists() or not right.exists():
        return []
    if left.read_bytes() != right.read_bytes():
        return [f"duplicate PRD script drift: {rel}"]
    return []


def audit(root: Path) -> int:
    errors: list[str] = []
    warnings: list[str] = []
    skill_dirs = list_skill_dirs(root)

    if not skill_dirs:
        errors.append("no Skill directories found")

    for skill_dir in skill_dirs:
        rel = skill_dir.name
        skill_path = skill_dir / "SKILL.md"
        text = skill_path.read_text(encoding="utf-8")
        lines = text.splitlines()
        fm = parse_frontmatter(text)

        if fm.get("name") != skill_dir.name:
            errors.append(f"{rel}: frontmatter name missing or mismatched")
        if not fm.get("description"):
            errors.append(f"{rel}: frontmatter description missing")
        if len(lines) > 320:
            warnings.append(f"{rel}: SKILL.md has {len(lines)} lines; consider router-plus-assets refactor")

        local_refs = LOCAL_PATH_RE.findall(text)
        if local_refs:
            warnings.append(f"{rel}: public SKILL.md contains local/private runtime reference(s)")

        eval_warnings = validate_eval_file(skill_dir)
        warnings.extend(f"{rel}: {warning}" for warning in eval_warnings)

        if rel in HIGH_RISK_SCRIPT_SKILLS and not (skill_dir / "scripts").exists():
            warnings.append(f"{rel}: high-risk output Skill has no scripts/ checker")

    errors.extend(compare_duplicate_scripts(root, Path("scripts/check_prd_shape.py")))
    errors.extend(compare_duplicate_scripts(root, Path("scripts/validate_drawio.py")))

    print(f"Audited {len(skill_dirs)} Skill(s).")
    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"- {warning}")
    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("\nAudit completed without hard errors.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit AI PM Skill repository structure.")
    parser.add_argument("root", nargs="?", default=".", help="Repository root")
    args = parser.parse_args()
    return audit(Path(args.root).expanduser().resolve())


if __name__ == "__main__":
    raise SystemExit(main())
