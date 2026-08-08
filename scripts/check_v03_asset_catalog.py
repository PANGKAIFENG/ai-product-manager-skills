#!/usr/bin/env python3
"""Validate the v0.3 Skill/Loop/Workflow/Tool/Pack catalog contract."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml


EXPECTED_IDS = {
    "skills": {
        "agent-trace-diagnoser",
        "ai-collaboration-calibration",
        "brainstorming",
        "customer-requirement-discovery",
        "decision-research",
        "grill-me",
        "prd-architect",
        "prd-review",
        "prd-to-issues",
        "project-context-steward",
        "research-topic-compiler",
        "skill-reviewer",
        "stylework-requirement-planning",
        "team-skill-creator",
        "ui-mockup-desktop-workbench",
    },
    "loops": {
        "prd-delivery-readiness-loop",
        "research-decision-loop",
        "solution-challenge-loop",
    },
    "workflows": {"product-delivery", "product-discovery"},
    "tools": {
        "dingtalk-prd-publisher",
        "product-delivery-validator",
        "yunxiao-requirement-sheet-sync",
        "yunxiao-work-item-publisher",
    },
    "packs": {"engineering", "pm-core", "skill-maintainer", "stylework-business"},
}

CONTRACT_FILES = {
    "skills": "SKILL.md",
    "loops": "LOOP.md",
    "workflows": "WORKFLOW.md",
    "tools": "TOOL.md",
}

EXPECTED_RUNTIME_ADAPTERS = {
    "dingtalk-prd-publisher": "dingtalk-prd-publisher",
    "yunxiao-work-item-publisher": "stylework-yunxiao-workitem-submitter",
    "yunxiao-requirement-sheet-sync": "stylework-yunxiao-requirement-sync",
}

EXPECTED_ARCHIVE_IDS = {
    "ai-work-assetization-diagnoser",
    "competitive-analysis",
    "complex-exploration",
    "stylework-solution-scoper",
    "ui-wireframe-to-html",
}


def validate_discovery_ignores(text: str) -> list[str]:
    patterns = {
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    if "archive/" not in patterns:
        return [".skillignore: archive/ must be excluded from Skill discovery"]
    return []


def load_yaml(path: Path) -> dict:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a mapping")
    return payload


def load_skill_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        raise ValueError(f"{path} must start with YAML frontmatter")
    payload = yaml.safe_load(parts[1])
    if not isinstance(payload, dict):
        raise ValueError(f"{path} frontmatter must contain a mapping")
    return payload


def validate_ids(kind: str, entries: object, expected: set[str]) -> list[str]:
    if not isinstance(entries, list):
        return [f"catalog/assets.yaml: {kind} must be a list"]
    ids = {
        str(entry.get("id"))
        for entry in entries
        if isinstance(entry, dict) and entry.get("id")
    }
    errors: list[str] = []
    missing = sorted(expected - ids)
    extra = sorted(ids - expected)
    if missing:
        errors.append(f"{kind}: missing v0.3 IDs: {', '.join(missing)}")
    if extra:
        errors.append(f"{kind}: unexpected v0.3 IDs: {', '.join(extra)}")
    if len(ids) != len(entries):
        errors.append(f"{kind}: entries must have unique non-empty IDs")
    return errors


def validate_repository(root: Path) -> tuple[list[str], dict[str, int]]:
    errors: list[str] = []
    assets = load_yaml(root / "catalog" / "assets.yaml")
    skills_catalog = load_yaml(root / "catalog" / "skills.yaml")
    counts: dict[str, int] = {}

    skillignore = root / ".skillignore"
    if not skillignore.is_file():
        errors.append(".skillignore: missing repository discovery exclusions")
    else:
        errors.extend(validate_discovery_ignores(skillignore.read_text(encoding="utf-8")))

    if assets.get("schema_version") != 1:
        errors.append("catalog/assets.yaml: schema_version must be 1")

    for kind, expected in EXPECTED_IDS.items():
        entries = assets.get(kind)
        errors.extend(validate_ids(kind, entries, expected))
        counts[kind] = len(entries) if isinstance(entries, list) else 0
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            relative = entry.get("path")
            if not isinstance(relative, str) or not relative:
                errors.append(f"{kind}/{entry.get('id', '<unknown>')}: missing path")
                continue
            path = root / relative
            if not path.exists():
                errors.append(f"{kind}/{entry.get('id')}: missing path {relative}")
                continue
            contract = CONTRACT_FILES.get(kind)
            if contract and not (path / contract).is_file():
                errors.append(f"{kind}/{entry.get('id')}: missing {contract}")

            if kind == "tools" and entry.get("id") in EXPECTED_RUNTIME_ADAPTERS:
                tool_id = str(entry["id"])
                expected_skill_id = EXPECTED_RUNTIME_ADAPTERS[tool_id]
                adapter_relative = entry.get("runtime_adapter")
                if not isinstance(adapter_relative, str) or not adapter_relative:
                    errors.append(f"tools/{tool_id}: missing runtime_adapter")
                    continue
                adapter_skill = root / adapter_relative / "SKILL.md"
                if not adapter_skill.is_file():
                    errors.append(
                        f"tools/{tool_id}: missing runtime adapter SKILL.md at {adapter_relative}"
                    )
                    continue
                declared_skill_id = entry.get("runtime_skill_id")
                if declared_skill_id != expected_skill_id:
                    errors.append(
                        f"tools/{tool_id}: runtime_skill_id must be {expected_skill_id}"
                    )
                frontmatter = load_skill_frontmatter(adapter_skill)
                if frontmatter.get("name") != expected_skill_id:
                    errors.append(
                        f"tools/{tool_id}: runtime adapter name must be {expected_skill_id}"
                    )

    catalog_skill_ids = {
        str(entry.get("id"))
        for entry in skills_catalog.get("skills", [])
        if isinstance(entry, dict) and entry.get("id")
    }
    if catalog_skill_ids != EXPECTED_IDS["skills"]:
        errors.append("catalog/skills.yaml does not match the v0.3 Skill inventory")

    archive_entries = assets.get("archive", [])
    errors.extend(validate_ids("archive", archive_entries, EXPECTED_ARCHIVE_IDS))
    archived_ids = {
        str(entry.get("id"))
        for entry in archive_entries
        if isinstance(entry, dict) and entry.get("id")
    }
    for archived_id in sorted(archived_ids):
        if (root / "skills" / archived_id).exists():
            errors.append(f"archive/{archived_id}: retired ID remains installable")

    valid_refs = {kind: set(ids) for kind, ids in EXPECTED_IDS.items()}
    for pack_entry in assets.get("packs", []):
        if not isinstance(pack_entry, dict):
            continue
        pack_id = str(pack_entry.get("id", "<unknown>"))
        pack_path = root / str(pack_entry.get("path", ""))
        if not pack_path.is_file():
            continue
        pack = load_yaml(pack_path)
        if pack.get("pack_id") != pack_id:
            errors.append(f"packs/{pack_id}: pack_id does not match catalog")
        for key in ("skills", "loops", "workflows", "tools"):
            values = pack.get(key, [])
            if not isinstance(values, list):
                errors.append(f"packs/{pack_id}: {key} must be a list")
                continue
            unknown = sorted({str(value) for value in values} - valid_refs[key])
            if unknown:
                errors.append(
                    f"packs/{pack_id}: unknown {key}: {', '.join(unknown)}"
                )

    return errors, counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve()
    try:
        errors, counts = validate_repository(root)
    except (OSError, ValueError, yaml.YAMLError) as error:
        print(f"[ERROR] {error}")
        return 1

    if errors:
        for error in errors:
            print(f"[ERROR] {error}")
        return 1

    summary = ", ".join(f"{kind}={counts[kind]}" for kind in EXPECTED_IDS)
    print(f"[OK] v0.3 asset catalog verified: {summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
