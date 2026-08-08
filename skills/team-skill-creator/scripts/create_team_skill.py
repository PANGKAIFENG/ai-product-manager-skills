#!/usr/bin/env python3
"""Create a team Skill through the system skill-creator scaffold."""

from __future__ import annotations

import argparse
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path


SYSTEM_INIT = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts" / "init_skill.py"
ALLOWED_RESOURCES = {"scripts", "references", "assets"}
MIXED_SKILLSHARE_ROOT = Path.home() / ".config" / "skillshare" / "skills"
RUNTIME_ROOTS = tuple(
    Path.home() / suffix
    for suffix in (
        ".codex/skills",
        ".claude/skills",
        ".agents/skills",
        ".config/opencode/skills",
        ".qoder/skills",
        ".workbuddy/skills",
    )
)


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


def normalize_remote(value: str) -> str:
    normalized = value.strip().removesuffix(".git").rstrip("/")
    if normalized.startswith("git@") and ":" in normalized:
        host, path = normalized[4:].split(":", 1)
        return f"{host}/{path}".lower()
    normalized = re.sub(r"^[a-z][a-z0-9+.-]*://", "", normalized, flags=re.IGNORECASE)
    return normalized.lower()


def is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def validate_authoritative_checkout(
    output_root: Path,
    expected_remote: str,
    *,
    mixed_root: Path = MIXED_SKILLSHARE_ROOT,
    runtime_roots: tuple[Path, ...] = RUNTIME_ROOTS,
) -> tuple[Path | None, str | None]:
    if not output_root.is_dir():
        return None, f"Destination does not exist or is not a directory: {output_root}"

    resolved_mixed_root = mixed_root.expanduser().resolve()
    if is_within(output_root, resolved_mixed_root):
        return None, f"Destination is inside the mixed Skillshare source: {resolved_mixed_root}"

    for runtime_root in runtime_roots:
        resolved_runtime = runtime_root.expanduser().resolve()
        if is_within(output_root, resolved_runtime):
            return None, f"Destination is inside a runtime target: {resolved_runtime}"

    repo_result = run_command(["git", "-C", str(output_root), "rev-parse", "--show-toplevel"])
    if repo_result.returncode != 0:
        return None, f"Destination is not inside a Git checkout: {output_root}"
    git_root = Path(repo_result.stdout.strip()).resolve()
    if not is_within(output_root, git_root):
        return None, f"Destination is outside the detected Git checkout: {git_root}"

    remote_result = run_command(["git", "-C", str(git_root), "remote", "get-url", "origin"])
    if remote_result.returncode != 0 or not remote_result.stdout.strip():
        return None, f"Git checkout has no origin remote: {git_root}"
    actual_remote = remote_result.stdout.strip()
    if normalize_remote(actual_remote) != normalize_remote(expected_remote):
        return None, (
            "Origin remote does not match --expected-remote: "
            f"expected {expected_remote}, found {actual_remote}"
        )
    return git_root, None


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
    parser.add_argument(
        "--path",
        required=True,
        help="Authoritative Git checkout where the skill folder is created.",
    )
    parser.add_argument(
        "--expected-remote",
        required=True,
        help="Expected origin URL for the selected authoritative Git checkout.",
    )
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
    _, checkout_error = validate_authoritative_checkout(output_root, args.expected_remote)
    if checkout_error:
        print(f"[ERROR] {checkout_error}", file=sys.stderr)
        return 1
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
        print(shlex.join(command))
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
