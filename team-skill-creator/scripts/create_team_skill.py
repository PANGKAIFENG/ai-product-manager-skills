#!/usr/bin/env python3
"""Create a team Skill through the system skill-creator scaffold."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


SYSTEM_INIT = Path("/Users/linctex/.codex/skills/.system/skill-creator/scripts/init_skill.py")
DEFAULT_PATH = Path("/Users/linctex/.codex/skills")
ALLOWED_RESOURCES = {"scripts", "references", "assets"}


def normalize_skill_name(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value


def title_from_name(skill_name: str) -> str:
    return " ".join(part.capitalize() for part in skill_name.split("-"))


def parse_resources(raw: str) -> list[str]:
    if not raw:
        return []
    resources = [item.strip() for item in raw.split(",") if item.strip()]
    invalid = sorted(set(resources) - ALLOWED_RESOURCES)
    if invalid:
        raise ValueError(
            f"Invalid resources: {', '.join(invalid)}. Allowed: {', '.join(sorted(ALLOWED_RESOURCES))}"
        )
    result: list[str] = []
    for resource in resources:
        if resource not in result:
            result.append(resource)
    return result


def default_short_description(description: str) -> str:
    text = re.sub(r"\s+", " ", description.strip())
    if len(text) <= 64:
        return text
    return text[:61].rstrip() + "..."


def run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, text=True, capture_output=True, check=False)


def replace_description(skill_md: Path, skill_name: str, description: str) -> None:
    content = skill_md.read_text(encoding="utf-8")
    pattern = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
    match = pattern.match(content)
    if not match:
        raise RuntimeError(f"Missing YAML frontmatter in {skill_md}")
    body = content[match.end() :]
    frontmatter = (
        f"---\nname: {skill_name}\ndescription: {json.dumps(description, ensure_ascii=False)}\n---"
    )
    skill_md.write_text(frontmatter + body, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a team-standard Skill scaffold.")
    parser.add_argument("--name", required=True, help="Skill name or title.")
    parser.add_argument("--description", required=True, help="Trigger-first Skill description.")
    parser.add_argument("--path", default=str(DEFAULT_PATH), help="Directory where the skill folder is created.")
    parser.add_argument("--resources", default="", help="Comma-separated resources: scripts,references,assets.")
    parser.add_argument("--dry-run", action="store_true", help="Print the command without creating files.")
    args = parser.parse_args()

    skill_name = normalize_skill_name(args.name)
    if not skill_name:
        print("[ERROR] Skill name must contain letters or digits.", file=sys.stderr)
        return 1
    if len(skill_name) > 64:
        print("[ERROR] Skill name must be <= 64 characters after normalization.", file=sys.stderr)
        return 1
    if not SYSTEM_INIT.exists():
        print(f"[ERROR] System init script not found: {SYSTEM_INIT}", file=sys.stderr)
        return 1

    try:
        resources = parse_resources(args.resources)
    except ValueError as error:
        print(f"[ERROR] {error}", file=sys.stderr)
        return 1

    output_root = Path(args.path).expanduser().resolve()
    skill_dir = output_root / skill_name
    if skill_dir.exists():
        print(f"[ERROR] Skill directory already exists: {skill_dir}", file=sys.stderr)
        return 1

    command = [
        sys.executable,
        str(SYSTEM_INIT),
        skill_name,
        "--path",
        str(output_root),
        "--interface",
        f"display_name={title_from_name(skill_name)}",
        "--interface",
        f"short_description={default_short_description(args.description)}",
        "--interface",
        f"default_prompt=Use ${skill_name} to handle this request.",
    ]
    if resources:
        command.extend(["--resources", ",".join(resources)])

    if args.dry_run:
        print(" ".join(command))
        return 0

    result = run_command(command)
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, file=sys.stderr, end="")
    if result.returncode != 0:
        return result.returncode

    replace_description(skill_dir / "SKILL.md", skill_name, args.description)
    print(f"[OK] Updated trigger description in {skill_dir / 'SKILL.md'}")
    print(f"[OK] Created team Skill scaffold: {skill_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
