#!/usr/bin/env python3
"""Inspect existing Skills for naming, trigger overlap, and catalog placement."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover - fallback for minimal Python envs.
    yaml = None


DEFAULT_CATALOG_ROOTS = [
    Path("/Users/linctex/.config/skillshare/skills"),
]

DEFAULT_RUNTIME_ROOTS = [
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


@dataclass
class CatalogEntry:
    skill_name: str
    root: Path
    category_id: str
    category_label: str
    status: str
    zh_name: str
    trigger: str
    use_when: str
    do_not_use_when: str


@dataclass
class Category:
    category_id: str
    label: str
    boundary: str
    root: Path


def run_git(root: Path, *args: str) -> tuple[int, str, str]:
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def normalize_name(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value


def unique_resolved_paths(paths: list[Path]) -> list[Path]:
    unique: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        resolved = path.expanduser().resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        unique.append(resolved)
    return unique


def git_catalog_status(root: Path, fetch: bool = False) -> dict[str, Any]:
    if not (root / ".git").exists():
        return {
            "root": str(root),
            "is_git_repo": False,
            "source_of_truth": "github-online",
        }

    if fetch:
        fetch_code, fetch_stdout, fetch_stderr = run_git(root, "fetch", "--prune", "origin")
    else:
        fetch_code, fetch_stdout, fetch_stderr = None, "", ""

    _, remote_url, _ = run_git(root, "remote", "get-url", "origin")
    _, branch, _ = run_git(root, "branch", "--show-current")
    upstream_code, upstream, upstream_err = run_git(root, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    if upstream_code != 0:
        upstream = ""
    _, status_text, _ = run_git(root, "status", "--porcelain")

    ahead = 0
    behind = 0
    if upstream:
        count_code, count_text, _ = run_git(root, "rev-list", "--left-right", "--count", f"{branch}...{upstream}")
        if count_code == 0:
            parts = count_text.split()
            if len(parts) == 2:
                ahead = int(parts[0])
                behind = int(parts[1])

    return {
        "root": str(root),
        "is_git_repo": True,
        "source_of_truth": "github-online",
        "remote": remote_url,
        "branch": branch,
        "upstream": upstream,
        "ahead": ahead,
        "behind": behind,
        "dirty": bool(status_text),
        "dirty_entries": status_text.splitlines(),
        "fetch_attempted": fetch,
        "fetch_exit_code": fetch_code,
        "fetch_stdout": fetch_stdout,
        "fetch_stderr": fetch_stderr,
        "upstream_error": upstream_err if upstream_code != 0 else "",
    }


def tokens(value: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", value.lower())
        if len(token) > 2
    }


def source_label(
    root: Path,
    import_roots: set[Path],
    catalog_roots: set[Path],
    multica_roots: set[Path],
) -> str:
    resolved = root.expanduser().resolve()
    if resolved in catalog_roots:
        return "github-skill-catalog"
    if resolved in multica_roots:
        return "multica-skill-root"
    if resolved in import_roots:
        return "import"
    mapping = {
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


def split_markdown_row(line: str) -> list[str]:
    line = line.strip()
    if not line.startswith("|") or not line.endswith("|"):
        return []
    cells = [cell.strip() for cell in line.strip("|").split("|")]
    if all(set(cell) <= {"-", ":", " "} for cell in cells):
        return []
    return cells


def clean_markdown_cell(value: str) -> str:
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = value.replace("`", "")
    value = value.strip()
    return value


def parse_catalog(root: Path) -> tuple[list[CatalogEntry], list[Category]]:
    resolved_root = root.expanduser().resolve()
    registry = root / "SKILL_REGISTRY.md"
    if not registry.exists():
        return [], []

    text = registry.read_text(encoding="utf-8", errors="replace")
    categories: dict[str, Category] = {}
    entries: dict[str, CatalogEntry] = {}

    current_section = ""
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith("## "):
            current_section = line[3:].strip()
            continue
        cells = split_markdown_row(line)
        if not cells:
            continue

        if current_section == "分类体系" and len(cells) >= 3:
            category_id = clean_markdown_cell(cells[0])
            match = re.search(r"categories/([^/]+)/?", category_id)
            if not match:
                continue
            category_id = match.group(1)
            if category_id == "分类目录":
                continue
            categories[category_id] = Category(
                category_id=category_id,
                label=clean_markdown_cell(cells[1]),
                boundary=clean_markdown_cell(cells[2]),
                root=resolved_root,
            )
            continue

        if current_section == "中文检索表" and len(cells) >= 6:
            skill_name = clean_markdown_cell(cells[0])
            if skill_name.lower() == "skill":
                continue
            entries[normalize_name(skill_name)] = CatalogEntry(
                skill_name=skill_name,
                root=resolved_root,
                category_id="",
                category_label="",
                status=clean_markdown_cell(cells[5]),
                zh_name=clean_markdown_cell(cells[1]),
                trigger=clean_markdown_cell(cells[2]),
                use_when=clean_markdown_cell(cells[3]),
                do_not_use_when=clean_markdown_cell(cells[4]),
            )

    categories_root = root / "categories"
    if categories_root.exists():
        for readme in sorted(categories_root.glob("*/README.md")):
            category_id = readme.parent.name
            category_text = readme.read_text(encoding="utf-8", errors="replace")
            label = categories.get(category_id, Category(category_id, "", "", resolved_root)).label
            for raw_line in category_text.splitlines():
                if raw_line.startswith("# ") and not label:
                    label = raw_line[2:].strip()
                cells = split_markdown_row(raw_line)
                if not cells or len(cells) < 1:
                    continue
                link_match = re.search(r"\]\(\.\./\.\./([^/]+)/\)", cells[0])
                if not link_match:
                    continue
                skill_name = clean_markdown_cell(cells[0])
                key = normalize_name(link_match.group(1) or skill_name)
                existing = entries.get(key)
                if existing is None:
                    existing = CatalogEntry(
                        skill_name=link_match.group(1),
                        root=resolved_root,
                        category_id=category_id,
                        category_label=label,
                        status=clean_markdown_cell(cells[3]) if len(cells) > 3 else "",
                        zh_name=clean_markdown_cell(cells[1]) if len(cells) > 1 else "",
                        trigger=clean_markdown_cell(cells[2]) if len(cells) > 2 else "",
                        use_when=clean_markdown_cell(cells[4]) if len(cells) > 4 else "",
                        do_not_use_when="",
                    )
                else:
                    existing.category_id = category_id
                    existing.category_label = label
                entries[key] = existing

    return list(entries.values()), list(categories.values())


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


def load_skills(
    roots: list[Path],
    import_roots: set[Path],
    catalog_roots: set[Path],
    multica_roots: set[Path],
) -> list[Skill]:
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
                    source=source_label(resolved_root, import_roots, catalog_roots, multica_roots),
                    frontmatter=frontmatter,
                )
            )
    return sorted(skills, key=lambda item: item.name)


def catalog_summary(entry: CatalogEntry) -> dict[str, str]:
    return {
        "root": str(entry.root),
        "category_id": entry.category_id,
        "category_label": entry.category_label,
        "status": entry.status,
        "zh_name": entry.zh_name,
        "trigger": entry.trigger,
        "use_when": entry.use_when,
        "do_not_use_when": entry.do_not_use_when,
    }


def score_category(category: Category, query_name: str, query_description: str) -> dict[str, Any]:
    query_text = " ".join([query_name, query_description]).strip()
    category_text = " ".join([category.category_id, category.label, category.boundary]).strip()
    query_tokens = tokens(query_text)
    category_tokens = tokens(category_text)
    if query_tokens or category_tokens:
        token_overlap = len(query_tokens & category_tokens) / max(len(query_tokens | category_tokens), 1)
    else:
        token_overlap = 0.0
    name_ratio = SequenceMatcher(None, normalize_name(query_name), normalize_name(category.category_id)).ratio()
    label_ratio = SequenceMatcher(None, query_description.lower(), category.boundary.lower()).ratio() if query_description else 0.0
    score = max(token_overlap, name_ratio, label_ratio)
    return {
        "category_id": category.category_id,
        "category_label": category.label,
        "boundary": category.boundary,
        "root": str(category.root),
        "score": round(score, 3),
        "token_overlap": round(token_overlap, 3),
    }


def score_skill(
    skill: Skill,
    query_name: str,
    query_description: str,
    catalog_index: dict[str, list[CatalogEntry]],
) -> dict:
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
        "catalog": [
            catalog_summary(entry)
            for entry in catalog_index.get(normalize_name(skill.name), [])
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Find existing Skills similar to a candidate.")
    parser.add_argument("--name", default="", help="Candidate skill name or title.")
    parser.add_argument("--description", default="", help="Candidate trigger description or request summary.")
    parser.add_argument("--root", action="append", default=[], help="Additional root to scan.")
    parser.add_argument("--import-root", action="append", default=[], help="Imported Skill source root to scan and label as import.")
    parser.add_argument("--catalog-root", action="append", default=[], help="GitHub/public catalog root to scan and label as github-skill-catalog.")
    parser.add_argument("--multica-root", action="append", default=[], help="Multica app/runtime Skill root to scan and label as multica-skill-root.")
    parser.add_argument("--fetch-catalog", action="store_true", help="Run git fetch for catalog roots before reporting GitHub source status.")
    parser.add_argument("--limit", type=int, default=8, help="Maximum matches to print.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text.")
    args = parser.parse_args()

    import_roots = {Path(root).expanduser().resolve() for root in args.import_root}
    catalog_roots = {
        root.expanduser().resolve()
        for root in DEFAULT_CATALOG_ROOTS + [Path(root) for root in args.catalog_root]
    }
    multica_roots = {Path(root).expanduser().resolve() for root in args.multica_root}
    roots = unique_resolved_paths(
        DEFAULT_CATALOG_ROOTS
        + DEFAULT_RUNTIME_ROOTS
        + [Path(root) for root in args.root]
        + list(import_roots)
        + list(catalog_roots)
        + list(multica_roots)
    )

    catalog_entries: list[CatalogEntry] = []
    categories: list[Category] = []
    seen_catalog_entries: set[tuple[Path, str]] = set()
    seen_categories: set[tuple[Path, str]] = set()
    for root in roots:
        entries, root_categories = parse_catalog(root)
        for entry in entries:
            key = (entry.root, normalize_name(entry.skill_name))
            if key in seen_catalog_entries:
                continue
            seen_catalog_entries.add(key)
            catalog_entries.append(entry)
        for category in root_categories:
            key = (category.root, category.category_id)
            if key in seen_categories:
                continue
            seen_categories.add(key)
            categories.append(category)

    catalog_index: dict[str, list[CatalogEntry]] = {}
    for entry in catalog_entries:
        catalog_index.setdefault(normalize_name(entry.skill_name), []).append(entry)

    catalog_status = [
        git_catalog_status(root, fetch=args.fetch_catalog)
        for root in sorted(catalog_roots)
    ]

    skills = load_skills(roots, import_roots, catalog_roots, multica_roots)
    matches = [score_skill(skill, args.name, args.description, catalog_index) for skill in skills]
    matches.sort(key=lambda item: item["score"], reverse=True)
    matches = matches[: max(args.limit, 1)]
    category_suggestions = [score_category(category, args.name, args.description) for category in categories]
    category_suggestions.sort(key=lambda item: item["score"], reverse=True)
    category_suggestions = category_suggestions[:3]

    result = {
        "query": {
            "name": args.name,
            "normalized_name": normalize_name(args.name),
            "description": args.description,
        },
        "roots": [str(root) for root in roots],
        "import_roots": [str(root) for root in sorted(import_roots)],
        "catalog_roots": [str(root) for root in sorted(catalog_roots)],
        "catalog_status": catalog_status,
        "multica_roots": [str(root) for root in sorted(multica_roots)],
        "category_suggestions": category_suggestions,
        "matches": matches,
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0

    print(f"Candidate: {args.name or '(no name)'}")
    print(f"Normalized: {normalize_name(args.name) or '(none)'}")
    print(f"Scanned skills: {len(skills)}")
    if catalog_status:
        print()
        print("GitHub catalog status:")
        for status in catalog_status:
            if not status["is_git_repo"]:
                print(f"- {status['root']} is not a git repo")
                continue
            state = []
            if status["ahead"]:
                state.append(f"ahead={status['ahead']}")
            if status["behind"]:
                state.append(f"behind={status['behind']}")
            if status["dirty"]:
                state.append("dirty")
            if not state:
                state.append("clean/up-to-date")
            print(
                f"- {status['remote']} {status['branch']} -> "
                f"{status['upstream'] or '(no upstream)'} ({', '.join(state)})"
            )
    if category_suggestions:
        print()
        print("Category suggestions:")
        for category in category_suggestions:
            print(
                f"- {category['category_id']} / {category['category_label']} "
                f"score={category['score']}"
            )
            if category["boundary"]:
                print(f"  boundary: {category['boundary']}")
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
        for catalog in match.get("catalog", []):
            category = " / ".join(
                part
                for part in [catalog.get("category_id"), catalog.get("category_label")]
                if part
            )
            status = catalog.get("status")
            if category or status:
                print(f"  catalog: category={category or '(unknown)'} status={status or '(unknown)'}")
        if match["description"]:
            print(f"  description: {match['description'][:240]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
