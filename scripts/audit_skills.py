#!/usr/bin/env python3
"""Repository-level structure and quality audit for public AI PM Skills."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

try:
    import yaml
except ImportError:  # pragma: no cover - exercised by the setup check below
    yaml = None


CATALOG_PATH = Path("catalog/skills.yaml")
SKILLS_PATH = Path("skills")
SKILL_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
LOCAL_PATH_RE = re.compile(
    r"(/Users/|~/(?:\.honeycomb-agent|\.codex|\.claude)|\.claude/hooks|honeycomb diagram-guard|/propose-honeycomb-change)"
)

ALLOWED_CATEGORIES = {
    "collaboration-thinking",
    "research-learning",
    "decision-research",
    "product-prd",
    "stylework-business",
    "skill-governance",
    "engineering-governance",
}
ALLOWED_STATUSES = {"core", "active", "review"}
HIGH_RISK_SCRIPT_SKILLS = {
    "brainstorming",
    "decision-research",
    "prd-architect",
    "prd-review",
    "prd-to-issues",
    "research-topic-compiler",
    "ui-mockup-desktop-workbench",
    "skill-reviewer",
    "team-skill-creator",
}
DUPLICATE_PRD_FILES = (
    Path("scripts/check_prd_shape.py"),
    Path("scripts/validate_drawio.py"),
    Path("references/drawio-templates.md"),
)


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


def load_catalog(root: Path) -> tuple[list[dict[str, str]], list[str]]:
    errors: list[str] = []
    path = root / CATALOG_PATH
    if yaml is None:
        return [], ["PyYAML is required; run: python3 -m pip install -r requirements-dev.txt"]
    if not path.exists():
        return [], [f"missing machine-readable catalog: {CATALOG_PATH}"]

    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as error:
        return [], [f"invalid {CATALOG_PATH}: {error}"]

    if not isinstance(payload, dict):
        return [], [f"{CATALOG_PATH} must contain a mapping"]
    if payload.get("schema_version") != 1:
        errors.append(f"{CATALOG_PATH}: schema_version must be 1")
    if payload.get("skills_root") != SKILLS_PATH.as_posix():
        errors.append(f"{CATALOG_PATH}: skills_root must be '{SKILLS_PATH}'")

    skills = payload.get("skills")
    if not isinstance(skills, list) or not skills:
        errors.append(f"{CATALOG_PATH}: skills must be a non-empty list")
        return [], errors

    normalized: list[dict[str, str]] = []
    seen: set[str] = set()
    required = {"id", "path", "name_zh", "category", "status", "example"}
    for index, entry in enumerate(skills, start=1):
        if not isinstance(entry, dict):
            errors.append(f"{CATALOG_PATH}: skill entry {index} must be a mapping")
            continue
        missing = sorted(required - entry.keys())
        if missing:
            errors.append(
                f"{CATALOG_PATH}: skill entry {index} missing: {', '.join(missing)}"
            )
            continue
        item = {key: str(entry[key]) for key in required}
        skill_id = item["id"]
        if not SKILL_ID_RE.fullmatch(skill_id):
            errors.append(f"{CATALOG_PATH}: invalid Skill id: {skill_id}")
        if skill_id in seen:
            errors.append(f"{CATALOG_PATH}: duplicate Skill id: {skill_id}")
        seen.add(skill_id)
        if item["path"] != f"skills/{skill_id}":
            errors.append(f"{skill_id}: catalog path must be skills/{skill_id}")
        if item["example"] != f"docs/examples/{skill_id}.md":
            errors.append(f"{skill_id}: catalog example must be docs/examples/{skill_id}.md")
        if item["category"] not in ALLOWED_CATEGORIES:
            errors.append(f"{skill_id}: unknown category {item['category']}")
        if item["status"] not in ALLOWED_STATUSES:
            errors.append(f"{skill_id}: unknown status {item['status']}")
        normalized.append(item)
    return normalized, errors


def list_skill_dirs(root: Path) -> list[Path]:
    skills_root = root / SKILLS_PATH
    if not skills_root.is_dir():
        return []
    return sorted(
        path
        for path in skills_root.iterdir()
        if path.is_dir() and (path / "SKILL.md").exists()
    )


def validate_skill_manifest_locations(root: Path) -> list[str]:
    errors: list[str] = []
    for manifest in sorted(root.rglob("SKILL.md")):
        relative = manifest.relative_to(root)
        if ".git" in relative.parts or "archive" in relative.parts:
            continue
        if relative.parts[:2] in (("tools", "publishers"), ("tools", "automations")):
            if len(relative.parts) >= 4 and relative.parts[-2] == "runtime-adapter":
                continue
        if (
            len(relative.parts) != 3
            or relative.parts[0] != SKILLS_PATH.as_posix()
            or relative.parts[2] != "SKILL.md"
        ):
            errors.append(f"SKILL.md outside canonical installable root: {relative}")
    return errors


def validate_eval_file(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    eval_path = skill_dir / "evals" / "evals.json"
    if not eval_path.exists():
        errors.append("missing evals/evals.json")
        return errors
    try:
        payload = json.loads(eval_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return [f"invalid evals/evals.json: {error}"]
    if not isinstance(payload, dict):
        return ["evals/evals.json must contain an object"]
    if payload.get("skill_name") != skill_dir.name:
        errors.append("eval skill_name does not match folder")
    evals = payload.get("evals")
    if not isinstance(evals, list) or not evals:
        errors.append("evals array is missing or empty")
        return errors

    seen_ids: set[str] = set()
    repository_skill_ids = {
        path.name for path in list_skill_dirs(skill_dir.parent.parent)
    }
    trigger_count = 0
    non_trigger_count = 0
    known_risk_count = 0
    for item in evals:
        if not isinstance(item, dict):
            errors.append("eval item is not an object")
            continue

        item_id = item.get("id")
        case_id = (
            item_id
            if isinstance(item_id, str) and item_id.strip()
            else "<unknown>"
        )
        for field in ("id", "type", "prompt", "expected_route", "expected_output"):
            if field not in item:
                errors.append(f"eval {case_id} missing {field}")
            elif not isinstance(item[field], str) or not item[field].strip():
                errors.append(
                    f"eval {case_id} {field} must be a non-empty string"
                )

        if isinstance(item_id, str) and item_id.strip():
            if item_id in seen_ids:
                errors.append(f"duplicate eval id: {item_id}")
            seen_ids.add(item_id)

        if "should_trigger" not in item:
            errors.append(f"eval {case_id} missing should_trigger")
        elif type(item["should_trigger"]) is not bool:
            errors.append(f"eval {case_id} should_trigger must be boolean")
        elif item["should_trigger"]:
            trigger_count += 1
        else:
            non_trigger_count += 1

        expected_route = item.get("expected_route")
        if isinstance(expected_route, str) and expected_route.strip():
            external_skill_id = (
                expected_route.removeprefix("external:")
                if expected_route.startswith("external:")
                else None
            )
            route_is_valid = expected_route in repository_skill_ids or (
                external_skill_id is not None
                and SKILL_ID_RE.fullmatch(external_skill_id) is not None
            )
            if not route_is_valid:
                errors.append(
                    f"eval {case_id} expected_route must name a repository Skill "
                    "or use external:<skill-id>"
                )

            should_trigger = item.get("should_trigger")
            if type(should_trigger) is bool:
                if should_trigger and expected_route != skill_dir.name:
                    errors.append(
                        f"eval {case_id} trigger expected_route must be "
                        f"{skill_dir.name}"
                    )
                elif not should_trigger and expected_route == skill_dir.name:
                    errors.append(
                        f"eval {case_id} non-trigger expected_route must not be "
                        f"{skill_dir.name}"
                    )

        assertions = item.get("assertions")
        if "assertions" not in item:
            errors.append(f"eval {case_id} missing assertions")
        elif not isinstance(assertions, list) or not assertions:
            errors.append(f"eval {case_id} assertions must be a non-empty list")
        else:
            for index, assertion in enumerate(assertions, start=1):
                if not isinstance(assertion, dict):
                    errors.append(
                        f"eval {case_id} assertion {index} must be an object"
                    )
                    continue
                text = assertion.get("text")
                if not isinstance(text, str) or not text.strip():
                    errors.append(
                        f"eval {case_id} assertion {index} text must be a non-empty string"
                    )

        eval_type = item.get("type")
        known_regression = item.get("known_regression")
        has_known_regression = (
            isinstance(known_regression, str) and bool(known_regression.strip())
        )
        has_risk_type = isinstance(eval_type, str) and any(
            marker in eval_type.lower() for marker in ("risk", "regression")
        )
        if has_known_regression or has_risk_type:
            known_risk_count += 1

    if trigger_count < 2:
        errors.append(
            f"eval coverage requires at least 2 trigger cases; found {trigger_count}"
        )
    if non_trigger_count < 2:
        errors.append(
            "eval coverage requires at least 2 non-trigger cases; "
            f"found {non_trigger_count}"
        )
    if known_risk_count < 1:
        errors.append(
            "eval coverage requires at least 1 known-risk or regression case; "
            f"found {known_risk_count}"
        )
    return errors


def validate_duplicate_prd_files(root: Path) -> list[str]:
    errors: list[str] = []
    for relative in DUPLICATE_PRD_FILES:
        left = root / SKILLS_PATH / "prd-architect" / relative
        right = root / SKILLS_PATH / "prd-review" / relative
        if not left.exists() or not right.exists():
            errors.append(f"missing self-contained PRD duplicate: {relative}")
        elif left.read_bytes() != right.read_bytes():
            errors.append(f"self-contained PRD duplicate drift: {relative}")
    return errors


def validate_markdown_links(root: Path) -> list[str]:
    errors: list[str] = []
    for markdown in root.rglob("*.md"):
        if ".git" in markdown.parts or "archive" in markdown.parts:
            continue
        text = markdown.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK_RE.findall(text):
            target = raw_target.strip().strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            target = unquote(target.split("#", 1)[0])
            if not target:
                continue
            # This is an intentional placeholder in the public image-placement
            # contract, not a repository-relative asset.
            if target in {"path/to/image.png", "path/to/screenshot.png"}:
                continue
            resolved = (markdown.parent / target).resolve()
            if not resolved.exists():
                rel_markdown = markdown.relative_to(root)
                errors.append(f"{rel_markdown}: broken link target: {raw_target}")
    return errors


def validate_catalog_surfaces(
    root: Path, catalog: list[dict[str, str]], actual_ids: set[str]
) -> list[str]:
    errors: list[str] = []
    catalog_ids = {item["id"] for item in catalog}
    missing_from_disk = sorted(catalog_ids - actual_ids)
    missing_from_catalog = sorted(actual_ids - catalog_ids)
    if missing_from_disk:
        errors.append(f"catalog Skills missing from disk: {', '.join(missing_from_disk)}")
    if missing_from_catalog:
        errors.append(f"uncataloged Skills on disk: {', '.join(missing_from_catalog)}")

    readme = (root / "README.md").read_text(encoding="utf-8")
    registry = (root / "SKILL_REGISTRY.md").read_text(encoding="utf-8")
    for item in catalog:
        skill_id = item["id"]
        if f"(skills/{skill_id}/)" not in readme:
            errors.append(f"{skill_id}: README missing canonical Skill link")
        if f"(docs/examples/{skill_id}.md)" not in readme:
            errors.append(f"{skill_id}: README missing canonical example link")
        if f"`{skill_id}`" not in registry:
            errors.append(f"{skill_id}: SKILL_REGISTRY missing catalog entry")
        if not (root / item["example"]).is_file():
            errors.append(f"{skill_id}: missing example {item['example']}")
    return errors


def audit(root: Path) -> int:
    errors: list[str] = []
    warnings: list[str] = []
    catalog, catalog_errors = load_catalog(root)
    errors.extend(catalog_errors)
    skill_dirs = list_skill_dirs(root)
    actual_ids = {path.name for path in skill_dirs}

    if not skill_dirs:
        errors.append(f"no Skill directories found under {SKILLS_PATH}/")

    errors.extend(validate_skill_manifest_locations(root))

    for skill_dir in skill_dirs:
        skill_id = skill_dir.name
        skill_path = skill_dir / "SKILL.md"
        text = skill_path.read_text(encoding="utf-8")
        lines = text.splitlines()
        frontmatter = parse_frontmatter(text)

        if frontmatter.get("name") != skill_id:
            errors.append(f"{skill_id}: frontmatter name missing or mismatched")
        if not frontmatter.get("description"):
            errors.append(f"{skill_id}: frontmatter description missing")
        if len(lines) > 320:
            warnings.append(
                f"{skill_id}: SKILL.md has {len(lines)} lines; consider router-plus-assets refactor"
            )
        if LOCAL_PATH_RE.search(text):
            warnings.append(f"{skill_id}: public SKILL.md contains local/private runtime reference(s)")

        errors.extend(
            f"{skill_id}: {warning}" for warning in validate_eval_file(skill_dir)
        )
        if skill_id in HIGH_RISK_SCRIPT_SKILLS and not (skill_dir / "scripts").exists():
            errors.append(f"{skill_id}: high-risk output Skill has no scripts/ checker")

    if catalog:
        errors.extend(validate_catalog_surfaces(root, catalog, actual_ids))
    errors.extend(validate_duplicate_prd_files(root))
    errors.extend(validate_markdown_links(root))

    print(f"Audited {len(skill_dirs)} Skill(s) under {SKILLS_PATH}/.")
    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"- {warning}")
    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"\nCatalog and repository audit completed without hard errors ({CATALOG_PATH}).")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit AI PM Skill repository structure.")
    parser.add_argument("root", nargs="?", default=".", help="Repository root")
    args = parser.parse_args()
    return audit(Path(args.root).expanduser().resolve())


if __name__ == "__main__":
    raise SystemExit(main())
