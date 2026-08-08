#!/usr/bin/env python3
"""Deterministic checks for the B1 four-Skill core-loop contract."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml


TARGET_SKILLS = (
    "research-topic-compiler",
    "decision-research",
    "brainstorming",
    "grill-me",
)

LEGACY_EVAL_IDS = {
    "research-topic-compiler": {
        "framing-vague-roadmap-input",
        "normal-research-with-sources",
        "product-candidate-research",
        "radar-loop-boundary",
        "non-trigger-final-selection",
        "iterative-anthropic-skill-best-practices",
        "framework-invalidation-by-primary-evidence",
        "fake-google-official-source-downgrade",
        "saturation-stops-before-reading-duplicates",
        "l1-quick-answer-does-not-over-loop",
        "l2-compact-map-bounded-acquisition",
        "authoritative-materials-sufficient-no-expansion",
        "transfer-mcp-auth-security",
        "routing-general-research-dashboard-html",
        "routing-concept-lens-dashboard-compatible",
        "routing-dashboard-does-not-override-decision-owner",
        "general-dashboard-artifact-contract",
        "iterative-loop-survives-dashboard-rendering",
        "dashboard-not-created-when-not-requested",
        "dashboard-transfer-mcp-auth-security",
        "trigger-generic-research-dashboard",
        "non-trigger-ui-only-dashboard-implementation",
        "dashboard-partial-state-requires-explicit-acceptance",
        "paired-research-path-still-unstable",
        "paired-research-question-stable-systematic-evidence",
    },
    "decision-research": {
        "platform-integration-official-api",
        "technical-selection-options",
        "business-model-tiering",
        "candidate-backlog-final-recommendation",
        "non-trigger-system-learning",
        "non-trigger-fuzzy-problem",
        "paired-competitor-evidence-still-missing",
        "paired-competitor-evidence-ready-final-selection",
        "paired-unstable-exploration-before-decision",
        "paired-stable-decision-ready-for-recommendation",
    },
    "brainstorming": {
        "design-options-before-prd",
        "visual-design-discovery",
        "non-trigger-fuzzy-problem",
        "non-trigger-established-solution",
        "paired-problem-unstable-before-design-options",
        "paired-problem-stable-needs-design-options",
        "paired-multiround-complex-exploration",
    },
    "grill-me": {
        "pressure-test-design",
        "prd-solution-pressure",
        "non-trigger-prd-readiness",
        "non-trigger-fuzzy-problem-calibration",
    },
}

EXPECTED_PAIRED_IDS = {
    "b1-paired-candidate-pool-not-final-choice",
    "b1-paired-evidence-ready-final-choice",
    "b1-paired-decision-gap-is-researchable",
    "b1-paired-options-not-yet-solution",
    "b1-paired-solution-formed-needs-critique",
    "b1-paired-critic-finding-needs-design-delta",
    "b1-product-work-graph-uses-public-brainstorming",
    "b1-superpowers-qualified-explicit-only",
}

MIN_TYPE_COUNTS = {
    "b1-negative-boundary": 8,
    "b1-single-call": 8,
    "b1-chained-call": 5,
    "b1-return-edge": 7,
}

REQUIRED_CASE_FIELDS = {
    "id",
    "type",
    "prompt",
    "should_trigger",
    "expected_route",
    "expected_output",
    "assertions",
}

REFERENCE_MARKERS = {
    "research-topic-compiler/references/core-loop-research-handoff.md": (
        "Role Contract",
        "Evidence Pack",
        "Evidence Delta",
        "preserved_items",
        "resume_point",
        "A handoff or chain is not authorization for external writes",
        "Runtime sync",
        "Skillshare/Multica publishing",
        "DingTalk/Yunxiao writes",
        "Stop before any such write",
        "specialist publisher/operation under separate explicit authorization",
        "cycle-limit-reached",
    ),
    "decision-research/references/core-loop-decision-handoff.md": (
        "Role Contract",
        "Decision Record",
        "Research Return Request",
        "material",
        "researchable",
        "closure criterion",
        "human-decision-required",
    ),
    "brainstorming/references/maker-handoff-contract.md": (
        "solution Maker",
        "Product Work Graph",
        "superpowers:brainstorming",
        "Design Delta",
        "preserved_items",
        "Human Gate",
    ),
    "grill-me/references/critic-handoff-contract.md": (
        "Critic",
        "Challenge Record",
        "Smallest Responsible Return",
        "research-topic-compiler",
        "decision-research",
        "brainstorming",
        "Human Gate",
    ),
}

SKILL_MARKERS = {
    "research-topic-compiler": (
        "references/core-loop-research-handoff.md",
        "Evidence Pack",
        "Evidence Delta",
        "handoff/chain 不构成外部写入授权",
        "Runtime sync",
        "Skillshare/Multica 发布",
        "钉钉/云效写入",
        "必须停止",
        "另行明确授权的专业 publisher/operation",
        "Human Gate",
    ),
    "decision-research": (
        "references/core-loop-decision-handoff.md",
        "当前 `decision_question` 内为选择服务的有界取证与反证搜索",
        "不拥有开放式知识工程",
        "不执行已经通过 Research Return Request 明确交给 Research 的证据 gap",
        "不拥有方案设计、Critic clearance 或 readiness 审批",
        "material、researchable、closable",
        "Evidence Delta",
        "Human Gate",
    ),
    "brainstorming": (
        "references/maker-handoff-contract.md",
        "PUBLIC unqualified `brainstorming`",
        "superpowers:brainstorming",
        "Design Delta",
        "Human Gate",
    ),
    "grill-me": (
        "references/critic-handoff-contract.md",
        "Challenge/Critic Handoff",
        "最早因果缺口",
        "clear-for-owner-confirmation",
        "Human Gate",
    ),
}

TOP_LEVEL_MARKERS = {
    "README.md": (
        "PUBLIC unqualified `brainstorming`",
        "`superpowers:brainstorming`",
        "同一 gap 两轮",
    ),
    "SKILL_REGISTRY.md": (
        "Core Loop handoff 不是第五个 Skill",
        "Product Work Graph 使用 PUBLIC unqualified `brainstorming`",
        "两轮不收敛进入 Human Gate",
    ),
    "SKILL_ROUTING.md": (
        "## Product Work Graph Core Loop",
        "PUBLIC unqualified `brainstorming`",
        "`superpowers:brainstorming` 仅在用户显式写出该完整限定名时可选",
        "不新增第五个 Skill、mega Skill、Orchestrator、中心状态机或 Runtime 服务",
    ),
}

EXPECTED_TARGET_STATUSES = {
    "research-topic-compiler": "core",
    "decision-research": "active",
    "brainstorming": "core",
    "grill-me": "active",
}


def load_eval_cases(root: Path) -> dict[str, list[dict]]:
    cases: dict[str, list[dict]] = {}
    for skill in TARGET_SKILLS:
        path = root / "skills" / skill / "evals" / "evals.json"
        payload = json.loads(path.read_text(encoding="utf-8"))
        cases[skill] = payload["evals"]
    return cases


def validate_eval_contracts(cases_by_skill: dict[str, list[dict]]) -> list[str]:
    errors: list[str] = []
    all_cases: list[tuple[str, dict]] = []

    for skill, cases in cases_by_skill.items():
        ids = {case.get("id") for case in cases}
        missing_legacy = sorted(LEGACY_EVAL_IDS[skill] - ids)
        if missing_legacy:
            errors.append(f"{skill}: legacy eval IDs removed: {', '.join(missing_legacy)}")
        all_cases.extend((skill, case) for case in cases)

    b1_cases = [(skill, case) for skill, case in all_cases if str(case.get("type", "")).startswith("b1-")]
    for skill, case in b1_cases:
        case_id = case.get("id", "<unknown>")
        missing = sorted(REQUIRED_CASE_FIELDS - case.keys())
        if missing:
            errors.append(f"{skill}/{case_id}: missing fields: {', '.join(missing)}")
        assertions = case.get("assertions")
        if not isinstance(assertions, list) or not assertions:
            errors.append(f"{skill}/{case_id}: assertions must be a non-empty list")

    type_counts = Counter(case.get("type") for _, case in b1_cases)
    for eval_type, minimum in MIN_TYPE_COUNTS.items():
        if type_counts[eval_type] < minimum:
            errors.append(f"{eval_type}: expected at least {minimum}, found {type_counts[eval_type]}")

    paired: dict[str, list[tuple[str, dict]]] = defaultdict(list)
    for skill, case in b1_cases:
        if case.get("type") == "b1-paired-routing":
            paired[str(case.get("id"))].append((skill, case))

    paired_ids = set(paired)
    if paired_ids != EXPECTED_PAIRED_IDS:
        missing = sorted(EXPECTED_PAIRED_IDS - paired_ids)
        extra = sorted(paired_ids - EXPECTED_PAIRED_IDS)
        if missing:
            errors.append(f"paired routing IDs missing: {', '.join(missing)}")
        if extra:
            errors.append(f"unexpected paired routing IDs: {', '.join(extra)}")

    for pair_id, entries in sorted(paired.items()):
        if len(entries) != 2:
            errors.append(f"{pair_id}: expected 2 mirrored entries, found {len(entries)}")
            continue
        prompts = {case.get("prompt") for _, case in entries}
        if len(prompts) != 1:
            errors.append(f"{pair_id}: mirrored prompts differ")
        true_entries = [(skill, case) for skill, case in entries if case.get("should_trigger") is True]
        if len(true_entries) != 1:
            errors.append(f"{pair_id}: expected exactly one true owner, found {len(true_entries)}")
            continue
        true_skill, true_case = true_entries[0]
        if true_case.get("expected_route") != true_skill:
            errors.append(f"{pair_id}: true owner {true_skill} does not match expected_route")
        routes = {case.get("expected_route") for _, case in entries}
        if routes != {true_skill}:
            errors.append(f"{pair_id}: mirrored entries do not agree on owner {true_skill}")

    explicit_external = [
        case
        for skill, case in b1_cases
        if skill == "brainstorming" and case.get("id") == "b1-explicit-superpowers-qualified-route"
    ]
    if len(explicit_external) != 1 or explicit_external[0].get("should_trigger") is not False:
        errors.append("explicit superpowers:brainstorming must remain an external non-trigger route")
    elif explicit_external[0].get("expected_route") != "external:superpowers-brainstorming":
        errors.append("explicit Superpowers eval must use external:superpowers-brainstorming")

    return errors


def validate_repository(root: Path) -> tuple[list[str], Counter]:
    errors: list[str] = []

    cases_by_skill = load_eval_cases(root)
    errors.extend(validate_eval_contracts(cases_by_skill))

    research_lines = len((root / "skills/research-topic-compiler/SKILL.md").read_text(encoding="utf-8").splitlines())
    if research_lines > 320:
        errors.append(f"research-topic-compiler/SKILL.md exceeds 320 lines: {research_lines}")

    for skill, markers in SKILL_MARKERS.items():
        text = (root / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(f"skills/{skill}/SKILL.md missing marker: {marker}")

    for relative, markers in REFERENCE_MARKERS.items():
        path = root / "skills" / relative
        if not path.is_file():
            errors.append(f"missing B1 reference: skills/{relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(f"skills/{relative} missing marker: {marker}")

    for relative, markers in TOP_LEVEL_MARKERS.items():
        text = (root / relative).read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                errors.append(f"{relative} missing marker: {marker}")

    catalog = yaml.safe_load((root / "catalog/skills.yaml").read_text(encoding="utf-8"))
    catalog_entries = catalog.get("skills", [])
    catalog_ids = {entry.get("id") for entry in catalog_entries}
    skill_dirs = {
        path.name
        for path in (root / "skills").iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    }
    if len(catalog_ids) != 13 or len(skill_dirs) != 13:
        errors.append(f"B1 must keep the 13-Skill baseline; catalog={len(catalog_ids)}, dirs={len(skill_dirs)}")
    if catalog_ids != skill_dirs:
        errors.append("catalog IDs and installable Skill directories differ")
    for skill, status in EXPECTED_TARGET_STATUSES.items():
        matches = [entry for entry in catalog_entries if entry.get("id") == skill]
        if len(matches) != 1 or matches[0].get("status") != status:
            errors.append(f"catalog must keep {skill} status={status}")

    forbidden_ids = sorted(
        skill_id
        for skill_id in catalog_ids
        if isinstance(skill_id, str)
        and any(token in skill_id for token in ("core-loop", "orchestrator", "mega-skill"))
    )
    if forbidden_ids:
        errors.append(f"B1 introduced forbidden aggregate Skill IDs: {', '.join(forbidden_ids)}")

    b1_types = Counter(
        case.get("type")
        for cases in cases_by_skill.values()
        for case in cases
        if str(case.get("type", "")).startswith("b1-")
    )
    return errors, b1_types


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", type=Path)
    args = parser.parse_args(argv)

    try:
        errors, counts = validate_repository(args.root.resolve())
    except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError, yaml.YAMLError) as error:
        print(f"B1 core-loop contract check: FAIL\n- unable to load contract assets: {error}")
        return 1

    if errors:
        print("B1 core-loop contract check: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("B1 core-loop contract check: PASS")
    print("- legacy evals preserved: 46/46")
    print(f"- paired routing: {len(EXPECTED_PAIRED_IDS)}/8 IDs, 16 mirrored entries, unique owner")
    for eval_type in MIN_TYPE_COUNTS:
        print(f"- {eval_type}: {counts[eval_type]}")
    print("- Skill/reference/routing/catalog boundaries: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
