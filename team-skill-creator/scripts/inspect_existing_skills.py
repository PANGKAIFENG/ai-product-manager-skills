#!/usr/bin/env python3
"""Inspect existing Skills for naming and trigger overlap."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - fallback for minimal Python envs.
    yaml = None


DEFAULT_ROOTS = [
    Path("/Users/linctex/.config/skillshare/skills"),
    Path("/Users/linctex/.codex/skills"),
    Path("/Users/linctex/.claude/skills"),
    Path("/Users/linctex/.agents/skills"),
    Path("/Users/linctex/.codex/skills/.system"),
]


@dataclass
class Skill:
    name: str
    description: str
    path: Path
    root: Path
    source: str
    frontmatter: dict[str, Any]


def normalize_name(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value


def tokens(value: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", value.lower())
        if len(token) > 2
    }


def source_label(root: Path, import_roots: set[Path]) -> str:
    resolved = root.expanduser().resolve()
    if resolved in import_roots:
        return "import"
    mapping = {
        Path("/Users/linctex/.config/skillshare/skills").resolve(): "skillshare-canonical",
        Path("/Users/linctex/.codex/skills").resolve(): "codex-target",
        Path("/Users/linctex/.claude/skills").resolve(): "claude-target",
        Path("/Users/linctex/.agents/skills").resolve(): "agents",
        Path("/Users/linctex/.codex/skills/.system").resolve(): "codex-system",
    }
    return mapping.get(resolved, "custom")


def frontmatter_summary(frontmatter: dict[str, Any]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for key in ["name", "description", "metadata", "license"]:
        if key in frontmatter:
            summary[key] = frontmatter[key]
    extra_keys = sorted(set(frontmatter) - set(summary))
    if extra_keys:
        summary["extra_keys"] = extra_keys
    return summary


def parse_frontmatter(skill_md: Path) -> tuple[str, str, dict[str, Any]]:
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return skill_md.parent.name, "", {}

    if yaml is not None:
        try:
            parsed = yaml.safe_load(match.group(1)) or {}
            if isinstance(parsed, dict):
                name = str(parsed.get("name") or skill_md.parent.name)
                description = parsed.get("description") or ""
                if not isinstance(description, str):
                    description = str(description)
                return name, re.sub(r"\s+", " ", description).strip(), parsed
        except Exception:
            pass

    name = skill_md.parent.name
    description_lines: list[str] = []
    in_description = False

    for raw_line in match.group(1).splitlines():
        line = raw_line.rstrip()
        if line.startswith("name:"):
            name = line.split(":", 1)[1].strip().strip("\"'")
            in_description = False
            continue
        if line.startswith("description:"):
            value = line.split(":", 1)[1].strip()
            if value in {">", "|", ">-", "|-"}:
                in_description = True
                description_lines = []
            else:
                in_description = False
                description_lines = [value.strip("\"'")]
            continue
        if in_description:
            if line.startswith(" ") or line.startswith("\t"):
                description_lines.append(line.strip())
            elif line:
                in_description = False

    description = " ".join(description_lines).strip()
    return name, description, {"name": name, "description": description}


def iter_skill_dirs(root: Path) -> list[Path]:
    if not root.exists():
        return []
    dirs: list[Path] = []
    for skill_md in root.rglob("SKILL.md"):
        parts = set(skill_md.parts)
        if "__pycache__" in parts:
            continue
        dirs.append(skill_md.parent)
    return sorted(set(dirs))


def load_skills(roots: list[Path], import_roots: set[Path]) -> list[Skill]:
    skills: list[Skill] = []
    seen: set[Path] = set()
    for root in roots:
        resolved_root = root.expanduser().resolve()
        for skill_dir in iter_skill_dirs(root):
            resolved = skill_dir.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            name, description, frontmatter = parse_frontmatter(skill_dir / "SKILL.md")
            skills.append(
                Skill(
                    name=name,
                    description=description,
                    path=resolved,
                    root=resolved_root,
                    source=source_label(resolved_root, import_roots),
                    frontmatter=frontmatter,
                )
            )
    return sorted(skills, key=lambda item: item.name)


def score_skill(skill: Skill, query_name: str, query_description: str) -> dict:
    normalized_query = normalize_name(query_name)
    normalized_skill = normalize_name(skill.name)
    name_ratio = SequenceMatcher(None, normalized_query, normalized_skill).ratio()

    query_text = " ".join([query_name, query_description]).strip()
    skill_text = " ".join([skill.name, skill.description]).strip()
    query_tokens = tokens(query_text)
    skill_tokens = tokens(skill_text)
    if query_tokens or skill_tokens:
        token_overlap = len(query_tokens & skill_tokens) / max(len(query_tokens | skill_tokens), 1)
    else:
        token_overlap = 0.0

    description_ratio = SequenceMatcher(
        None,
        query_description.lower(),
        skill.description.lower(),
    ).ratio() if query_description and skill.description else 0.0

    exact_name = normalized_query == normalized_skill and bool(normalized_query)
    score = max(name_ratio, token_overlap, description_ratio, 1.0 if exact_name else 0.0)

    return {
        "name": skill.name,
        "path": str(skill.path),
        "root": str(skill.root),
        "source": skill.source,
        "description": skill.description,
        "frontmatter": frontmatter_summary(skill.frontmatter),
        "score": round(score, 3),
        "name_similarity": round(name_ratio, 3),
        "token_overlap": round(token_overlap, 3),
        "description_similarity": round(description_ratio, 3),
        "exact_name": exact_name,
        "exact-name": exact_name,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Find existing Skills similar to a candidate.")
    parser.add_argument("--name", default="", help="Candidate skill name or title.")
    parser.add_argument("--description", default="", help="Candidate trigger description or request summary.")
    parser.add_argument("--root", action="append", default=[], help="Additional root to scan.")
    parser.add_argument("--import-root", action="append", default=[], help="Imported Skill source root to scan and label as import.")
    parser.add_argument("--limit", type=int, default=8, help="Maximum matches to print.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    args = parser.parse_args()

    import_roots = {Path(root).expanduser().resolve() for root in args.import_root}
    roots = DEFAULT_ROOTS + [Path(root).expanduser() for root in args.root] + list(import_roots)
    skills = load_skills(roots, import_roots)
    matches = [score_skill(skill, args.name, args.description) for skill in skills]
    matches.sort(key=lambda item: item["score"], reverse=True)
    matches = matches[: max(args.limit, 1)]

    result = {
        "query": {
            "name": args.name,
            "normalized_name": normalize_name(args.name),
            "description": args.description,
        },
        "roots": [str(root) for root in roots],
        "import_roots": [str(root) for root in sorted(import_roots)],
        "matches": matches,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    print(f"Candidate: {args.name or '(no name)'}")
    print(f"Normalized: {normalize_name(args.name) or '(none)'}")
    print(f"Scanned skills: {len(skills)}")
    print()
    for match in matches:
        flags = []
        if match["exact_name"]:
            flags.append("EXACT_NAME")
        if match["score"] >= 0.7:
            flags.append("HIGH_OVERLAP")
        flag_text = f" [{' '.join(flags)}]" if flags else ""
        print(f"- {match['name']} score={match['score']}{flag_text}")
        print(f"  source: {match['source']} root={match['root']}")
        print(f"  path: {match['path']}")
        if match["description"]:
            print(f"  description: {match['description'][:240]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
