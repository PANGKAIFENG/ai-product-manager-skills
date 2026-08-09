#!/usr/bin/env python3
"""Validate the v0.3 Skill/Loop/Workflow/Tool/Pack catalog contract."""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

import yaml

try:
    from audit_skills import validate_eval_file
except ModuleNotFoundError:  # Loaded directly by tests outside scripts/.
    _AUDIT_PATH = Path(__file__).with_name("audit_skills.py")
    _AUDIT_SPEC = importlib.util.spec_from_file_location(
        "runtime_entrypoint_audit_contract", _AUDIT_PATH
    )
    if _AUDIT_SPEC is None or _AUDIT_SPEC.loader is None:
        raise RuntimeError(f"cannot load eval validator from {_AUDIT_PATH}")
    _AUDIT_MODULE = importlib.util.module_from_spec(_AUDIT_SPEC)
    _AUDIT_SPEC.loader.exec_module(_AUDIT_MODULE)
    validate_eval_file = _AUDIT_MODULE.validate_eval_file


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
        "decision-loop",
        "delivery-loop",
        "solution-loop",
    },
    "workflows": {"problem-to-solution", "solution-to-delivery"},
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
    "loops": {
        "decision-loop": "decision-loop",
        "delivery-loop": "delivery-loop",
        "solution-loop": "solution-loop",
    },
    "workflows": {
        "problem-to-solution": "problem-to-solution",
        "solution-to-delivery": "solution-to-delivery",
    },
    "tools": {
        "dingtalk-prd-publisher": "dingtalk-prd-publisher",
        "yunxiao-work-item-publisher": "stylework-yunxiao-workitem-submitter",
        "yunxiao-requirement-sheet-sync": "stylework-yunxiao-requirement-sync",
    },
}

EXPECTED_ARCHIVE_IDS = {
    "ai-work-assetization-diagnoser",
    "competitive-analysis",
    "complex-exploration",
    "prd-delivery-readiness-loop",
    "product-delivery",
    "product-discovery",
    "research-decision-loop",
    "solution-challenge-loop",
    "stylework-solution-scoper",
    "ui-wireframe-to-html",
}

EXPECTED_ROUTE_IDS = set().union(
    EXPECTED_IDS["skills"], EXPECTED_IDS["loops"], EXPECTED_IDS["workflows"]
)


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


def validate_runtime_adapter(
    root: Path,
    kind: str,
    entry: dict,
    expected_skill_id: str,
) -> list[str]:
    asset_id = str(entry["id"])
    adapter_relative = entry.get("runtime_adapter")
    if not isinstance(adapter_relative, str) or not adapter_relative:
        return [f"{kind}/{asset_id}: missing runtime_adapter"]

    adapter_path = root / adapter_relative
    skill_file = adapter_path / "SKILL.md"
    if not skill_file.is_file():
        return [
            f"{kind}/{asset_id}: missing runtime adapter SKILL.md at {adapter_relative}"
        ]

    errors: list[str] = []
    if entry.get("runtime_skill_id") != expected_skill_id:
        errors.append(
            f"{kind}/{asset_id}: runtime_skill_id must be {expected_skill_id}"
        )
    frontmatter = load_skill_frontmatter(skill_file)
    if frontmatter.get("name") != expected_skill_id:
        errors.append(
            f"{kind}/{asset_id}: runtime adapter name must be {expected_skill_id}"
        )

    openai_path = adapter_path / "agents" / "openai.yaml"
    if not openai_path.is_file():
        errors.append(f"{kind}/{asset_id}: missing agents/openai.yaml")
    else:
        openai = load_yaml(openai_path)
        policy = openai.get("policy")
        if (
            kind in {"loops", "workflows"}
            and (
                not isinstance(policy, dict)
                or policy.get("allow_implicit_invocation") is not False
            )
        ):
            errors.append(
                f"{kind}/{asset_id}: runtime adapter must disable implicit invocation"
            )

    eval_path = adapter_path / "evals" / "evals.json"
    if not eval_path.is_file():
        errors.append(f"{kind}/{asset_id}: missing evals/evals.json")
    elif kind in {"loops", "workflows"}:
        errors.extend(
            f"{kind}/{asset_id}: {error}"
            for error in validate_eval_file(adapter_path, EXPECTED_ROUTE_IDS)
        )
    return errors


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

            expected_runtime_ids = EXPECTED_RUNTIME_ADAPTERS.get(kind, {})
            if entry.get("id") in expected_runtime_ids:
                tool_id = str(entry["id"])
                errors.extend(
                    validate_runtime_adapter(
                        root,
                        kind,
                        entry,
                        expected_runtime_ids[tool_id],
                    )
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
        install_contracts = {
            "skills": ("SKILL.md",),
            "loops": ("SKILL.md", "LOOP.md"),
            "workflows": ("SKILL.md", "WORKFLOW.md"),
        }
        for install_root, contracts in install_contracts.items():
            retired_root = root / install_root / archived_id
            if any((retired_root / contract).is_file() for contract in contracts):
                errors.append(
                    f"archive/{archived_id}: retired ID remains installable "
                    f"under {install_root}/"
                )

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
