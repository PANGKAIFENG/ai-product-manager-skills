#!/usr/bin/env python3
"""Read-only project skeleton scanner for PROJECT_CONTEXT bootstrapping."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path
from typing import Any


INTERESTING_DIRS = {
    "apps",
    "packages",
    "services",
    "server",
    "client",
    "frontend",
    "backend",
    "docs",
    "doc",
    "prd",
    "prds",
    "research",
    "decisions",
    "decision",
    "runbook",
    "runbooks",
    "handoff",
    "handoffs",
    "tests",
    "test",
    "e2e",
    "scripts",
    "skills",
    "agents",
}

INTERESTING_FILES = {
    "README.md",
    "PROJECT_CONTEXT.md",
    "CONTEXT.md",
    "AGENTS.md",
    "CLAUDE.md",
    "package.json",
    "pnpm-workspace.yaml",
    "turbo.json",
    "nx.json",
    "pyproject.toml",
    "go.mod",
    "Cargo.toml",
    "docker-compose.yml",
    "docker-compose.yaml",
    "Dockerfile",
    "SKILL.md",
}

SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".next",
    ".nuxt",
    ".turbo",
    ".cache",
    ".venv",
    "node_modules",
    "dist",
    "build",
    "coverage",
    "__pycache__",
}


def run_git(root: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip() or None


def is_git_repo(path: Path) -> bool:
    return (path / ".git").exists()


def rel(root: Path, path: Path) -> str:
    if path == root:
        return "."
    return path.relative_to(root).as_posix()


def depth(root: Path, path: Path) -> int:
    if path == root:
        return 0
    return len(path.relative_to(root).parts)


def scan(root: Path, max_depth: int) -> dict[str, Any]:
    root = root.resolve()
    if not root.exists():
        raise SystemExit(f"Path does not exist: {root}")
    if not root.is_dir():
        raise SystemExit(f"Path is not a directory: {root}")

    git_info = {
        "is_repo": is_git_repo(root),
        "branch": run_git(root, "branch", "--show-current"),
        "remote_origin": run_git(root, "remote", "get-url", "origin"),
        "status_short": run_git(root, "status", "--short", "--branch"),
    }

    child_repositories: list[str] = []
    interesting_dirs: list[str] = []
    interesting_files: list[str] = []
    skill_dirs: list[str] = []

    for current, dirs, files in os.walk(root):
        current_path = Path(current)
        current_depth = depth(root, current_path)

        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        files = sorted(files)

        if current_depth > 0 and is_git_repo(current_path):
            child_repositories.append(rel(root, current_path))

        for dirname in dirs:
            child = current_path / dirname
            child_depth = depth(root, child)
            if child_depth <= max_depth and dirname in INTERESTING_DIRS:
                interesting_dirs.append(rel(root, child))

        for filename in files:
            if filename in INTERESTING_FILES:
                path = current_path / filename
                if current_depth <= max_depth:
                    interesting_files.append(rel(root, path))
                if filename == "SKILL.md":
                    skill_dirs.append(rel(root, current_path))

        if current_depth >= max_depth:
            dirs[:] = []

    return {
        "root": str(root),
        "git": git_info,
        "child_repositories": sorted(set(child_repositories)),
        "interesting_dirs": sorted(set(interesting_dirs)),
        "interesting_files": sorted(set(interesting_files)),
        "skill_dirs": sorted(set(skill_dirs)),
    }


def render_list(items: list[str]) -> str:
    if not items:
        return "- None found"
    return "\n".join(f"- `{item}`" for item in items)


def render_markdown(data: dict[str, Any]) -> str:
    git = data["git"]
    status = git.get("status_short") or "Unavailable"
    return "\n".join(
        [
            "# Project Skeleton Scan",
            "",
            f"- Root: `{data['root']}`",
            f"- Git repo: `{git['is_repo']}`",
            f"- Branch: `{git.get('branch') or 'Unavailable'}`",
            f"- Remote origin: `{git.get('remote_origin') or 'Unavailable'}`",
            "",
            "## Git Status",
            "",
            "```text",
            status,
            "```",
            "",
            "## Child Repositories",
            "",
            render_list(data["child_repositories"]),
            "",
            "## Interesting Directories",
            "",
            render_list(data["interesting_dirs"]),
            "",
            "## Interesting Files",
            "",
            render_list(data["interesting_files"]),
            "",
            "## Skill Directories",
            "",
            render_list(data["skill_dirs"]),
            "",
        ]
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Read-only scanner for project context bootstrapping."
    )
    parser.add_argument("root", help="Project root or workspace folder to scan.")
    parser.add_argument("--max-depth", type=int, default=3, help="Directory depth to scan.")
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format.",
    )
    args = parser.parse_args()

    data = scan(Path(args.root), max(0, args.max_depth))
    if args.format == "json":
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(data))


if __name__ == "__main__":
    main()
