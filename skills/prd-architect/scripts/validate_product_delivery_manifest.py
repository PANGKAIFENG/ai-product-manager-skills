#!/usr/bin/env python3
"""Validate and update Product Delivery Manifest v1 deterministically."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import posixpath
import re
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

import yaml


CONTRACT_VERSION = "product-delivery-manifest-v1"
MAX_ATTEMPTS = 20
TOP_LEVEL_FIELDS = {
    "schema_version",
    "work_item_id",
    "title",
    "depth",
    "revision",
    "package_status",
    "current_stage",
    "updated_at",
    "package_input_fingerprint",
    "ui_requirement",
    "sources",
    "decisions",
    "artifacts",
    "ui_baselines",
    "anchors",
    "validations",
    "pre_split_review",
    "review",
    "approvals",
    "release",
    "last_transition",
    "extensions",
}
ARTIFACT_GROUPS = {
    "prd",
    "publish_body",
    "action_contract",
    "html",
    "screenshots",
    "version_plan",
    "issue_drafts",
    "coverage_matrix",
}
COLLECTION_ARTIFACT_GROUPS = {"html", "screenshots", "issue_drafts"}
PLANNING_ARTIFACT_GROUPS = {"version_plan", "issue_drafts", "coverage_matrix"}
PRE_SPLIT_ARTIFACT_GROUPS = ARTIFACT_GROUPS - PLANNING_ARTIFACT_GROUPS
ROLE_ARTIFACT_GROUPS = {
    "maker": {"prd", "publish_body"},
    "ui_producer": {"action_contract", "html", "screenshots"},
    "backlog_splitter": PLANNING_ARTIFACT_GROUPS,
}
RELEASE_FIELDS = {
    "mode",
    "title",
    "target",
    "content_artifact_ref",
    "html_artifact_refs",
    "screenshot_artifact_refs",
    "payload_fingerprint",
    "status",
    "node_id",
    "doc_url",
    "completed_artifact_refs",
    "readback",
    "browser_visibility",
    "attempts",
}
REVIEW_FIELDS = {
    "review_id",
    "reviewer_identity",
    "maker_identities",
    "independence_check",
    "input_fingerprint",
    "verdict",
    "checks",
    "findings",
    "reviewed_at",
}
ROLE_PREFIXES = {
    "maker": (
        "work_item_id",
        "title",
        "depth",
        "revision",
        "updated_at",
        "ui_requirement",
        "sources",
        "decisions",
        "artifacts.prd",
        "artifacts.publish_body",
        "extensions",
    ),
    "ui_producer": (
        "updated_at",
        "artifacts.action_contract",
        "artifacts.html",
        "artifacts.screenshots",
        "ui_baselines",
        "anchors",
        "extensions",
    ),
    "backlog_splitter": (
        "updated_at",
        "artifacts.version_plan",
        "artifacts.issue_drafts",
        "artifacts.coverage_matrix",
    ),
    "reviewer": ("updated_at", "pre_split_review", "review"),
    "approver": ("updated_at", "approvals.publish"),
    "publisher": ("updated_at", "release.dingtalk", "last_transition", "package_status", "current_stage"),
    "validator": (
        "updated_at",
        "package_input_fingerprint",
        "package_status",
        "current_stage",
        "validations",
        "last_transition",
    ),
}


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    pre_split_input_fingerprint: str | None = None
    package_input_fingerprint: str | None = None
    publish_payload_fingerprint: str | None = None
    derived_status: str = "invalid"
    earliest_recovery_node: str = "manifest"
    publish_plan: dict[str, Any] | None = None

    @property
    def valid(self) -> bool:
        return not self.errors

    def as_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "contract_version": CONTRACT_VERSION,
            "pre_split_input_fingerprint": self.pre_split_input_fingerprint,
            "package_input_fingerprint": self.package_input_fingerprint,
            "publish_payload_fingerprint": self.publish_payload_fingerprint,
            "derived_status": self.derived_status,
            "earliest_recovery_node": self.earliest_recovery_node,
            "publish_plan": self.publish_plan,
            "errors": self.errors,
            "warnings": self.warnings,
        }


def canonical_fingerprint(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_sha256(value: Any) -> bool:
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) is not None


def normalize_anchor_content(value: str) -> str:
    lines = [line.rstrip(" \t") for line in value.replace("\r\n", "\n").replace("\r", "\n").split("\n")]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)


def markdown_sections(value: str) -> list[dict[str, Any]]:
    lines = value.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    headings: list[dict[str, Any]] = []
    stack: list[tuple[int, str]] = []
    fence: str | None = None
    for index, line in enumerate(lines):
        fence_match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if fence_match:
            marker = fence_match.group(1)[0]
            fence = None if fence == marker else marker if fence is None else fence
            continue
        if fence is not None:
            continue
        match = re.match(r"^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$", line)
        if not match:
            continue
        level = len(match.group(1))
        title = re.sub(r"[ \t]+", " ", match.group(2)).strip()
        while stack and stack[-1][0] >= level:
            stack.pop()
        path = " > ".join([item[1] for item in stack] + [title])
        headings.append({"level": level, "title": title, "path": path, "line": index})
        stack.append((level, title))

    for index, heading in enumerate(headings):
        end = len(lines)
        for candidate in headings[index + 1 :]:
            if candidate["level"] <= heading["level"]:
                end = candidate["line"]
                break
        heading["content"] = normalize_anchor_content("\n".join(lines[heading["line"] + 1 : end]))
    return headings


def resolve_markdown_section(value: str, heading_path: str) -> tuple[str | None, int]:
    target = re.sub(r"[ \t]+", " ", heading_path).strip()
    sections = markdown_sections(value)
    matches = [item for item in sections if item["path"] == target]
    if not matches:
        matches = [item for item in sections if item["title"] == target]
    if len(matches) != 1:
        return None, len(matches)
    return str(matches[0]["content"]), 1


def embedded_image_paths(section: str, prd_path: str) -> set[str]:
    targets: list[str] = []
    markdown_pattern = re.compile(r"!\[[^\]]*\]\(\s*(?:<([^>]+)>|([^\s)]+))(?:\s+[^)]*)?\s*\)")
    for match in markdown_pattern.finditer(section):
        targets.append(match.group(1) or match.group(2))
    targets.extend(re.findall(r"<img\b[^>]*\bsrc=[\"']([^\"']+)[\"']", section, flags=re.IGNORECASE))

    base = posixpath.dirname(prd_path.replace("\\", "/"))
    resolved: set[str] = set()
    for target in targets:
        clean = target.split("#", 1)[0].split("?", 1)[0]
        if not clean or "://" in clean or clean.startswith("/"):
            continue
        resolved.add(posixpath.normpath(posixpath.join(base, clean)))
    return resolved


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise ValueError(f"cannot read YAML: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError("manifest root must be a mapping")
    return value


def is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def is_human_identity(value: Any) -> bool:
    if not is_nonempty_string(value) or not value.startswith("human:"):
        return False
    label = value.removeprefix("human:")
    return bool(label.strip()) and label == label.strip()


def require_mapping(value: Any, location: str, result: ValidationResult) -> dict[str, Any]:
    if not isinstance(value, dict):
        result.errors.append(f"{location}: must be a mapping")
        return {}
    return value


def require_list(value: Any, location: str, result: ValidationResult) -> list[Any]:
    if not isinstance(value, list):
        result.errors.append(f"{location}: must be a list")
        return []
    return value


def artifact_records(artifacts: dict[str, Any], result: ValidationResult) -> Iterable[tuple[str, dict[str, Any]]]:
    for group in sorted(ARTIFACT_GROUPS):
        value = artifacts.get(group)
        if value is None:
            continue
        if group in COLLECTION_ARTIFACT_GROUPS:
            records = require_list(value, f"artifacts.{group}", result)
            for index, record in enumerate(records):
                if isinstance(record, dict):
                    yield group, record
                else:
                    result.errors.append(f"artifacts.{group}[{index}]: must be a mapping")
        elif isinstance(value, dict):
            yield group, value
        else:
            result.errors.append(f"artifacts.{group}: must be a mapping")


def resolve_artifact(root: Path, raw_path: Any, location: str, result: ValidationResult) -> Path | None:
    if not is_nonempty_string(raw_path):
        result.errors.append(f"{location}.path: must be a non-empty relative path")
        return None
    if "\n" in raw_path or "\r" in raw_path or "\t" in raw_path:
        result.errors.append(f"{location}.path: control characters are forbidden")
        return None
    relative = Path(raw_path)
    if relative.is_absolute() or ".." in relative.parts:
        result.errors.append(f"{location}.path: absolute paths and traversal are forbidden")
        return None
    try:
        resolved_root = root.resolve(strict=True)
        resolved = (root / relative).resolve(strict=True)
        resolved.relative_to(resolved_root)
    except (FileNotFoundError, OSError):
        result.errors.append(f"{location}.path: file does not exist")
        return None
    except ValueError:
        result.errors.append(f"{location}.path: symlink or path escapes the Package root")
        return None
    if not resolved.is_file():
        result.errors.append(f"{location}.path: must resolve to a file")
        return None
    return resolved


def validate_artifacts(
    manifest: dict[str, Any], root: Path, result: ValidationResult
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    artifacts = require_mapping(manifest.get("artifacts"), "artifacts", result)
    unknown_groups = sorted(set(artifacts) - ARTIFACT_GROUPS)
    if unknown_groups:
        result.errors.append(f"artifacts: unknown groups: {', '.join(unknown_groups)}")

    by_id: dict[str, dict[str, Any]] = {}
    fingerprint_records: list[dict[str, Any]] = []
    for group, record in artifact_records(artifacts, result):
        artifact_id = record.get("artifact_id")
        if not is_nonempty_string(artifact_id):
            result.errors.append(f"artifacts.{group}: artifact_id is required")
            continue
        if artifact_id in by_id:
            result.errors.append(f"artifacts: duplicate artifact_id {artifact_id}")
            continue
        resolved = resolve_artifact(root, record.get("path"), f"artifacts.{group}[{artifact_id}]", result)
        expected_hash = record.get("sha256")
        if not is_nonempty_string(expected_hash):
            result.errors.append(f"artifacts.{group}[{artifact_id}].sha256: required")
            actual_hash = None
        elif resolved is not None:
            actual_hash = file_sha256(resolved)
            if expected_hash != actual_hash:
                result.errors.append(f"artifacts.{group}[{artifact_id}].sha256: content mismatch")
        else:
            actual_hash = None

        enriched = copy.deepcopy(record)
        enriched["_group"] = group
        enriched["_resolved_path"] = str(resolved) if resolved else None
        enriched["_actual_sha256"] = actual_hash
        by_id[artifact_id] = enriched
        producer_identity = record.get("producer_identity")
        if not is_nonempty_string(producer_identity):
            result.errors.append(
                f"artifacts.{group}[{artifact_id}].producer_identity: required"
            )
        fingerprint_record = {
            "artifact_id": artifact_id,
            "kind": group,
            "path": record.get("path"),
            "sha256": actual_hash or expected_hash,
            "baseline_ref": record.get("baseline_ref"),
            "source_html_ref": record.get("source_html_ref"),
            "source_html_sha256": record.get("source_html_sha256"),
            "state": record.get("state"),
            "action_refs": record.get("action_refs", []),
            "viewport": record.get("viewport"),
        }
        fingerprint_record["producer_identity"] = producer_identity
        fingerprint_records.append(fingerprint_record)
    if not any(record.get("_group") == "prd" for record in by_id.values()):
        result.errors.append("artifacts.prd: a Product Delivery Package requires a valid PRD artifact")
    return by_id, sorted(fingerprint_records, key=lambda item: (str(item["kind"]), str(item["artifact_id"])))


def validate_ui_evidence(
    manifest: dict[str, Any], by_id: dict[str, dict[str, Any]], result: ValidationResult
) -> None:
    requirement = require_mapping(manifest.get("ui_requirement"), "ui_requirement", result)
    required = requirement.get("required")
    decided_by = requirement.get("decided_by")
    if not is_nonempty_string(decided_by):
        result.errors.append("ui_requirement.decided_by: required")
    if not isinstance(required, bool):
        result.errors.append("ui_requirement.required: must be true or false")
        return
    reason = requirement.get("reason")
    if not required:
        if reason != "no_user_visible_surface":
            result.errors.append("ui_requirement.reason: only no_user_visible_surface can exempt UI evidence")
        return
    if reason != "user_visible_surface":
        result.errors.append("ui_requirement.reason: page Packages must use user_visible_surface")

    required_groups = {"prd", "action_contract", "html", "screenshots"}
    present_groups = {record["_group"] for record in by_id.values()}
    for group in sorted(required_groups - present_groups):
        result.errors.append(f"ui_evidence: missing required artifact group {group}")

    baselines = require_list(manifest.get("ui_baselines"), "ui_baselines", result)
    baseline_ids: set[str] = set()
    for index, baseline in enumerate(baselines):
        if not isinstance(baseline, dict) or not is_nonempty_string(baseline.get("baseline_id")):
            result.errors.append(f"ui_baselines[{index}]: baseline_id is required")
            continue
        baseline_ids.add(baseline["baseline_id"])
    if not baselines:
        result.errors.append("ui_evidence: at least one UI baseline is required")

    html_by_id = {key: value for key, value in by_id.items() if value["_group"] == "html"}
    screenshots = {key: value for key, value in by_id.items() if value["_group"] == "screenshots"}
    for artifact_id, html in html_by_id.items():
        if html.get("baseline_ref") not in baseline_ids:
            result.errors.append(f"artifacts.html[{artifact_id}].baseline_ref: unknown baseline")
    for artifact_id, screenshot in screenshots.items():
        source_ref = screenshot.get("source_html_ref")
        source = html_by_id.get(source_ref)
        if source is None:
            result.errors.append(f"artifacts.screenshots[{artifact_id}].source_html_ref: unknown HTML")
        elif screenshot.get("source_html_sha256") != source.get("_actual_sha256"):
            result.errors.append(f"artifacts.screenshots[{artifact_id}]: stale source HTML fingerprint")
        for field_name in ("state", "viewport"):
            if not is_nonempty_string(screenshot.get(field_name)):
                result.errors.append(f"artifacts.screenshots[{artifact_id}].{field_name}: required")

    anchors = require_list(manifest.get("anchors"), "anchors", result)
    anchor_ids: set[str] = set()
    for index, anchor in enumerate(anchors):
        if not isinstance(anchor, dict):
            result.errors.append(f"anchors[{index}]: must be a mapping")
            continue
        anchor_id = anchor.get("anchor_id")
        if not is_nonempty_string(anchor_id) or anchor_id in anchor_ids:
            result.errors.append(f"anchors[{index}].anchor_id: required and unique")
        else:
            anchor_ids.add(anchor_id)
        prd_ref = anchor.get("prd_artifact_ref")
        shot_ref = anchor.get("screenshot_ref")
        prd_record = by_id.get(prd_ref)
        shot_record = screenshots.get(shot_ref)
        if prd_record is None or prd_record["_group"] != "prd":
            result.errors.append(f"anchors[{index}].prd_artifact_ref: must reference PRD")
        if shot_record is None:
            result.errors.append(f"anchors[{index}].screenshot_ref: must reference a screenshot")
        for field_name in ("heading_path", "content_sha256"):
            if not is_nonempty_string(anchor.get(field_name)):
                result.errors.append(f"anchors[{index}].{field_name}: required")
        if (
            prd_record is None
            or prd_record.get("_group") != "prd"
            or not prd_record.get("_resolved_path")
            or not is_nonempty_string(anchor.get("heading_path"))
        ):
            continue
        try:
            prd_text = Path(prd_record["_resolved_path"]).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            result.errors.append(f"anchors[{index}].prd_artifact_ref: cannot read PRD as UTF-8: {exc}")
            continue
        section, match_count = resolve_markdown_section(prd_text, anchor["heading_path"])
        if match_count != 1 or section is None:
            result.errors.append(f"anchors[{index}].heading_path: does not resolve uniquely in the current PRD")
            continue
        actual_content_hash = hashlib.sha256(section.encode("utf-8")).hexdigest()
        if anchor.get("content_sha256") != actual_content_hash:
            result.errors.append(f"anchors[{index}].content_sha256: normalized section content mismatch")
        if shot_record is not None:
            prd_relative = str(prd_record.get("path", "")).replace("\\", "/")
            shot_relative = posixpath.normpath(str(shot_record.get("path", "")).replace("\\", "/"))
            if shot_relative not in embedded_image_paths(section, prd_relative):
                result.errors.append(f"anchors[{index}].screenshot_ref: screenshot is not embedded in the resolved PRD section")
    if not anchors:
        result.errors.append("ui_evidence: at least one PRD anchor is required")


def compute_input_fingerprint(
    manifest: dict[str, Any], artifact_inputs: list[dict[str, Any]]
) -> str:
    value = {
        "contract_version": CONTRACT_VERSION,
        "schema_version": manifest.get("schema_version"),
        "work_item_id": manifest.get("work_item_id"),
        "revision": manifest.get("revision"),
        "ui_requirement": manifest.get("ui_requirement"),
        "sources": manifest.get("sources", []),
        "decisions": manifest.get("decisions", []),
        "artifacts": artifact_inputs,
        "ui_baselines": manifest.get("ui_baselines", []),
        "anchors": manifest.get("anchors", []),
    }
    return canonical_fingerprint(value)


def validate_review(
    manifest: dict[str, Any],
    field_name: str,
    input_fingerprint: str,
    by_id: dict[str, dict[str, Any]],
    producer_groups: set[str],
    result: ValidationResult,
) -> str:
    review = manifest.get(field_name)
    if review is None:
        return "missing"
    review = require_mapping(review, field_name, result)
    unknown = sorted(set(review) - REVIEW_FIELDS)
    if unknown:
        result.errors.append(f"{field_name}: unknown fields: {', '.join(unknown)}")
    reviewer = review.get("reviewer_identity")
    makers = require_list(
        review.get("maker_identities"), f"{field_name}.maker_identities", result
    )
    if not is_nonempty_string(reviewer):
        result.errors.append(f"{field_name}.reviewer_identity: required")
    if not makers or not all(is_nonempty_string(item) for item in makers):
        result.errors.append(
            f"{field_name}.maker_identities: at least one non-empty identity is required"
        )
    decided_by = manifest.get("ui_requirement", {}).get("decided_by")
    artifact_producers = {
        record.get("producer_identity")
        for record in by_id.values()
        if record.get("_group") in producer_groups
        and is_nonempty_string(record.get("producer_identity"))
    }
    declared_makers = {item for item in makers if is_nonempty_string(item)}
    if is_nonempty_string(decided_by) and decided_by not in declared_makers:
        result.errors.append(
            f"{field_name}.maker_identities: must include ui_requirement.decided_by"
        )
    missing_producers = sorted(artifact_producers - declared_makers)
    if missing_producers:
        result.errors.append(
            f"{field_name}.maker_identities: must include authoritative producer identities: "
            + ", ".join(missing_producers)
        )
    if reviewer in declared_makers or reviewer in artifact_producers or reviewer == decided_by:
        result.errors.append(
            f"{field_name}: Reviewer identity must be independent from Maker identities"
        )
    if review.get("input_fingerprint") != input_fingerprint:
        result.errors.append(f"{field_name}.input_fingerprint: stale or incorrect")
    verdict = review.get("verdict")
    if verdict not in {"ready", "changes_requested"}:
        result.errors.append(f"{field_name}.verdict: must be ready or changes_requested")
    checks = require_mapping(review.get("checks"), f"{field_name}.checks", result)
    required_checks = {"content", "artifacts", "publish"}
    if set(checks) != required_checks:
        result.errors.append(
            f"{field_name}.checks: must contain exactly content, artifacts, and publish"
        )
    for check in sorted(required_checks):
        if checks.get(check) not in {"passed", "failed"}:
            result.errors.append(
                f"{field_name}.checks.{check}: must be passed or failed"
            )
    if verdict == "ready" and any(checks.get(check) != "passed" for check in required_checks):
        result.errors.append(f"{field_name}: ready requires all three checks to pass")
    if verdict == "changes_requested" or any(checks.get(check) == "failed" for check in required_checks):
        return "changes_requested"
    return "ready"


def validate_publish_plan(
    manifest: dict[str, Any], by_id: dict[str, dict[str, Any]], result: ValidationResult
) -> dict[str, Any] | None:
    release = require_mapping(manifest.get("release"), "release", result)
    dingtalk = release.get("dingtalk")
    if dingtalk is None:
        return None
    dingtalk = require_mapping(dingtalk, "release.dingtalk", result)
    unknown = sorted(set(dingtalk) - RELEASE_FIELDS)
    if unknown:
        result.errors.append(f"release.dingtalk: unknown fields: {', '.join(unknown)}")

    mode = dingtalk.get("mode")
    title = dingtalk.get("title")
    target = require_mapping(dingtalk.get("target"), "release.dingtalk.target", result)
    selector = target.get("selector")
    target_value = target.get("value")
    if mode not in {"doc", "file"}:
        result.errors.append("release.dingtalk.mode: must be doc or file")
    if not is_nonempty_string(title):
        result.errors.append("release.dingtalk.title: required")
    if selector not in {"parent", "folder", "workspace"}:
        result.errors.append("release.dingtalk.target.selector: must be parent, folder, or workspace")
    if not is_nonempty_string(target_value):
        result.errors.append("release.dingtalk.target.value: required")

    content_ref = dingtalk.get("content_artifact_ref")
    html_refs = require_list(dingtalk.get("html_artifact_refs", []), "release.dingtalk.html_artifact_refs", result)
    screenshot_refs = require_list(
        dingtalk.get("screenshot_artifact_refs", []), "release.dingtalk.screenshot_artifact_refs", result
    )
    if mode == "file" and (html_refs or screenshot_refs):
        result.errors.append("release.dingtalk: file mode cannot publish HTML or screenshot artifacts")
    allowlist = [content_ref, *html_refs, *screenshot_refs]
    if not is_nonempty_string(content_ref):
        result.errors.append("release.dingtalk.content_artifact_ref: required")
    if len(allowlist) != len(set(allowlist)):
        result.errors.append("release.dingtalk: artifact allowlist contains duplicates")
    expected_groups = [(content_ref, {"prd", "publish_body"})]
    expected_groups.extend((ref, {"html"}) for ref in html_refs)
    expected_groups.extend((ref, {"screenshots"}) for ref in screenshot_refs)
    for ref, groups in expected_groups:
        record = by_id.get(ref)
        if record is None:
            result.errors.append(f"release.dingtalk: unknown artifact ref {ref}")
        elif record["_group"] not in groups:
            result.errors.append(f"release.dingtalk: artifact {ref} has wrong kind")

    fingerprint_input = {
        "mode": mode,
        "title": title,
        "target": {"selector": selector, "value": target_value},
        "artifacts": [
            {
                "artifact_id": ref,
                "kind": by_id.get(ref, {}).get("_group"),
                "sha256": by_id.get(ref, {}).get("_actual_sha256") or by_id.get(ref, {}).get("sha256"),
            }
            for ref in allowlist
        ],
    }
    payload_fingerprint = canonical_fingerprint(fingerprint_input)
    result.publish_payload_fingerprint = payload_fingerprint
    recorded = dingtalk.get("payload_fingerprint")
    if recorded is not None and recorded != payload_fingerprint:
        result.errors.append("release.dingtalk.payload_fingerprint: stale or incorrect")

    completed = require_list(
        dingtalk.get("completed_artifact_refs", []), "release.dingtalk.completed_artifact_refs", result
    )
    if any(ref not in allowlist for ref in completed):
        result.errors.append("release.dingtalk.completed_artifact_refs: contains a non-allowlisted artifact")
    attempts = require_list(dingtalk.get("attempts", []), "release.dingtalk.attempts", result)
    if len(attempts) > MAX_ATTEMPTS:
        result.errors.append(f"release.dingtalk.attempts: maximum is {MAX_ATTEMPTS}")

    def plan_item(ref: str) -> dict[str, Any]:
        record = by_id.get(ref, {})
        return {
            "artifact_id": ref,
            "path": record.get("_resolved_path"),
            "sha256": record.get("_actual_sha256") or record.get("sha256"),
        }

    plan = {
        "mode": mode,
        "title": title,
        "target": {"selector": selector, "value": target_value},
        "content": plan_item(content_ref) if is_nonempty_string(content_ref) else None,
        "html": [plan_item(ref) for ref in html_refs],
        "screenshots": [plan_item(ref) for ref in screenshot_refs],
        "payload_fingerprint": payload_fingerprint,
        "node_id": dingtalk.get("node_id"),
        "doc_url": dingtalk.get("doc_url"),
        "completed_artifact_refs": completed,
        "release_status": dingtalk.get("status", "pending"),
        "last_attempt": attempts[-1] if attempts else None,
    }
    result.publish_plan = plan
    return dingtalk


def validate_approval(manifest: dict[str, Any], payload_fingerprint: str | None, result: ValidationResult) -> bool:
    approvals = require_mapping(manifest.get("approvals"), "approvals", result)
    approval = approvals.get("publish")
    if approval is None:
        return False
    approval = require_mapping(approval, "approvals.publish", result)
    approver_identity = approval.get("approver_identity")
    if not is_nonempty_string(approver_identity):
        result.errors.append("approvals.publish.approver_identity: required")
    elif not is_human_identity(approver_identity):
        result.errors.append(
            "approvals.publish.approver_identity: must use human:<stable-label>"
        )
    if not is_nonempty_string(approval.get("approved_at")):
        result.errors.append("approvals.publish.approved_at: required")
    if payload_fingerprint is None or approval.get("payload_fingerprint") != payload_fingerprint:
        result.warnings.append(
            "approvals.publish.payload_fingerprint: stale or incorrect; approval ignored"
        )
        return False
    return True


def release_status(manifest: dict[str, Any], dingtalk: dict[str, Any] | None, result: ValidationResult) -> str | None:
    if dingtalk is None:
        return None
    status = dingtalk.get("status", "pending")
    allowed = {"pending", "publishing", "publish_failed", "published_unverified", "verified"}
    if status not in allowed:
        result.errors.append(f"release.dingtalk.status: unsupported status {status}")
        return None
    readback = dingtalk.get("readback")
    browser = dingtalk.get("browser_visibility")
    readback_passed = isinstance(readback, dict) and readback.get("passed") is True
    browser_passed = isinstance(browser, dict) and browser.get("passed") is True
    node_id = dingtalk.get("node_id")
    completed_value = dingtalk.get("completed_artifact_refs", [])
    completed = completed_value if isinstance(completed_value, list) else []
    attempts_value = dingtalk.get("attempts", [])
    attempts = attempts_value if isinstance(attempts_value, list) else []
    latest_attempt = attempts[-1] if attempts and isinstance(attempts[-1], dict) else None
    html_value = dingtalk.get("html_artifact_refs", [])
    html_refs = html_value if isinstance(html_value, list) else []
    screenshot_value = dingtalk.get("screenshot_artifact_refs", [])
    screenshot_refs = screenshot_value if isinstance(screenshot_value, list) else []
    allowlist = [
        dingtalk.get("content_artifact_ref"),
        *html_refs,
        *screenshot_refs,
    ]
    if readback_passed:
        if not is_nonempty_string(readback.get("checked_at")):
            result.errors.append("release.dingtalk.readback.checked_at: required")
        if readback.get("node_id") != node_id:
            result.errors.append("release.dingtalk.readback.node_id: must match the published node")
        if readback.get("title") != dingtalk.get("title"):
            result.errors.append("release.dingtalk.readback.title: must match the approved title")
        if dingtalk.get("mode") == "doc" and not is_sha256(readback.get("content_sha256")):
            result.errors.append("release.dingtalk.readback.content_sha256: valid SHA-256 required for document mode")
    if browser_passed:
        if not is_nonempty_string(browser.get("verifier_identity")):
            result.errors.append("release.dingtalk.browser_visibility.verifier_identity: required")
        if not is_nonempty_string(browser.get("checked_at")):
            result.errors.append("release.dingtalk.browser_visibility.checked_at: required")
        if not is_nonempty_string(browser.get("evidence_ref")):
            result.errors.append("release.dingtalk.browser_visibility.evidence_ref: required")
        checks = browser.get("checks")
        required_checks = {"title_visible", "content_visible", "artifacts_visible", "publish_pollution_absent"}
        if not isinstance(checks, dict) or any(checks.get(key) is not True for key in required_checks):
            result.errors.append("release.dingtalk.browser_visibility.checks: all visibility checks must pass")
        if browser.get("node_id") != node_id:
            result.errors.append("release.dingtalk.browser_visibility.node_id: must match the published node")
        if browser.get("payload_fingerprint") != dingtalk.get("payload_fingerprint"):
            result.errors.append("release.dingtalk.browser_visibility.payload_fingerprint: stale or incorrect")
        if is_nonempty_string(dingtalk.get("doc_url")) and browser.get("doc_url") != dingtalk.get("doc_url"):
            result.errors.append("release.dingtalk.browser_visibility.doc_url: must match the published document")
    if status in {"publishing", "publish_failed", "published_unverified", "verified"} and latest_attempt is None:
        result.errors.append(f"release.dingtalk.{status} evidence: a current publish attempt is required")
    if status in {"published_unverified", "verified"}:
        if not is_nonempty_string(node_id):
            result.errors.append(f"release.dingtalk.{status} evidence: published node_id is required")
        if dingtalk.get("content_artifact_ref") not in completed:
            result.errors.append(f"release.dingtalk.{status} evidence: content artifact must be completed")
        if not readback_passed:
            result.errors.append(f"release.dingtalk.{status} evidence: read-back must pass")
    if status == "published_unverified" and latest_attempt is not None:
        if latest_attempt.get("status") != "readback_passed" or not is_nonempty_string(latest_attempt.get("started_at")):
            result.errors.append("release.dingtalk.published_unverified evidence: latest attempt must record readback_passed")
    if status == "publish_failed" and latest_attempt is not None:
        if latest_attempt.get("status") != "failed" or not is_nonempty_string(latest_attempt.get("failed_step")):
            result.errors.append("release.dingtalk.publish_failed evidence: latest attempt must record the failed step")
    if status == "verified":
        if not (readback_passed and browser_passed):
            result.errors.append("release.dingtalk.verified evidence: read-back and browser evidence must pass")
        if any(ref not in completed for ref in allowlist):
            result.errors.append("release.dingtalk.verified evidence: completed artifacts must cover the approved allowlist")
        if latest_attempt is None or latest_attempt.get("status") != "verified":
            result.errors.append("release.dingtalk.verified evidence: latest attempt must record verified")
        elif not all(is_nonempty_string(latest_attempt.get(field)) for field in ("attempt_id", "started_at", "completed_at")):
            result.errors.append("release.dingtalk.verified evidence: latest attempt timestamps and identity are required")
        transition = manifest.get("last_transition")
        if (
            not isinstance(transition, dict)
            or transition.get("from_status") != "published_unverified"
            or transition.get("to_status") != "verified"
            or transition.get("input_fingerprint") != result.package_input_fingerprint
            or not is_nonempty_string(transition.get("actor"))
            or not is_nonempty_string(transition.get("occurred_at"))
        ):
            result.errors.append("release.dingtalk.verified evidence: final transition is incomplete or inconsistent")
        elif isinstance(browser, dict) and browser.get("verifier_identity") == transition.get("actor"):
            result.errors.append("release.dingtalk.verified evidence: browser verifier must be independent from Publisher")
    if browser_passed and not readback_passed:
        result.errors.append("release.dingtalk.browser_visibility: read-back must pass first")
    if readback_passed and not browser_passed and status not in {"published_unverified", "publish_failed"}:
        result.warnings.append("release.dingtalk.status: read-back passed but browser verification is incomplete")
    return status


def derive_state(
    result: ValidationResult, review_state: str, approval_valid: bool, dingtalk_status: str | None
) -> None:
    if result.errors:
        result.derived_status = "invalid"
        result.earliest_recovery_node = "manifest"
        return
    if review_state == "missing":
        result.derived_status = "review_pending"
        result.earliest_recovery_node = "review"
        return
    if review_state == "changes_requested":
        result.derived_status = "changes_requested"
        result.earliest_recovery_node = "review_finding"
        return
    result.derived_status = "package_ready"
    result.earliest_recovery_node = "approval"
    if not approval_valid:
        return
    result.derived_status = "publish_approved"
    result.earliest_recovery_node = "publish"
    if dingtalk_status in {"publishing", "publish_failed", "published_unverified", "verified"}:
        result.derived_status = dingtalk_status
        result.earliest_recovery_node = {
            "publishing": "publish",
            "publish_failed": "publish",
            "published_unverified": "browser_verification",
            "verified": "complete",
        }[dingtalk_status]


def flattened_changes(before: Any, after: Any, prefix: str = "") -> set[str]:
    if type(before) is not type(after):
        return {prefix or "<root>"}
    if isinstance(before, dict):
        paths: set[str] = set()
        for key in set(before) | set(after):
            child = f"{prefix}.{key}" if prefix else str(key)
            if key not in before or key not in after:
                paths.add(child)
            else:
                paths.update(flattened_changes(before[key], after[key], child))
        return paths
    if before != after:
        return {prefix or "<root>"}
    return set()


def validate_actor_changes(
    previous: dict[str, Any],
    current: dict[str, Any],
    actor_role: str,
    actor_identity: str | None,
    result: ValidationResult,
) -> None:
    prefixes = ROLE_PREFIXES[actor_role]
    changes = flattened_changes(previous, current)
    unauthorized = sorted(
        path for path in changes if not any(path == allowed or path.startswith(f"{allowed}.") for allowed in prefixes)
    )
    if unauthorized:
        result.errors.append(f"actor_role.{actor_role}: unauthorized changes: {', '.join(unauthorized)}")

    if actor_role == "reviewer":
        changed_review_fields = [
            field_name
            for field_name in ("pre_split_review", "review")
            if any(
                path == field_name or path.startswith(f"{field_name}.")
                for path in changes
            )
        ]
        if changed_review_fields and not is_nonempty_string(actor_identity):
            result.errors.append(
                "actor_role.reviewer: actor_identity is required for Review changes"
            )
        for field_name in changed_review_fields:
            if field_name == "pre_split_review":
                previous_artifacts = previous.get("artifacts", {})
                if isinstance(previous_artifacts, dict) and any(
                    previous_artifacts.get(group) not in (None, [], {})
                    for group in PLANNING_ARTIFACT_GROUPS
                ):
                    result.errors.append(
                        "actor_role.reviewer: pre_split_review cannot be added or changed after planning artifacts exist"
                    )
            current_record = current.get(field_name)
            previous_record = previous.get(field_name)
            authoritative = (
                current_record if isinstance(current_record, dict) else previous_record
            )
            if (
                is_nonempty_string(actor_identity)
                and isinstance(authoritative, dict)
                and authoritative.get("reviewer_identity") != actor_identity
            ):
                result.errors.append(
                    f"actor_role.reviewer: {field_name}.reviewer_identity must match actor_identity"
                )

    if actor_role == "approver" and any(
        path == "approvals.publish" or path.startswith("approvals.publish.")
        for path in changes
    ):
        if not is_nonempty_string(actor_identity):
            result.errors.append(
                "actor_role.approver: actor_identity is required for approval changes"
            )
        elif not is_human_identity(actor_identity):
            result.errors.append(
                "actor_role.approver: actor_identity must use human:<stable-label>"
            )
        current_approvals = current.get("approvals")
        previous_approvals = previous.get("approvals")
        current_approval = (
            current_approvals.get("publish")
            if isinstance(current_approvals, dict)
            else None
        )
        previous_approval = (
            previous_approvals.get("publish")
            if isinstance(previous_approvals, dict)
            else None
        )
        authoritative = (
            current_approval if isinstance(current_approval, dict) else previous_approval
        )
        if (
            is_nonempty_string(actor_identity)
            and isinstance(authoritative, dict)
            and authoritative.get("approver_identity") != actor_identity
        ):
            result.errors.append(
                "actor_role.approver: approvals.publish.approver_identity must match actor_identity"
            )

    owned_groups = ROLE_ARTIFACT_GROUPS.get(actor_role)
    if not owned_groups:
        return
    changed_groups = {
        group
        for group in owned_groups
        if any(
            path == "artifacts"
            or path == f"artifacts.{group}"
            or path.startswith(f"artifacts.{group}.")
            for path in changes
        )
    }
    if not changed_groups:
        return
    if not is_nonempty_string(actor_identity):
        result.errors.append(
            f"actor_role.{actor_role}: actor_identity is required for artifact changes"
        )
        return

    previous_artifacts = previous.get("artifacts", {})
    current_artifacts = current.get("artifacts", {})
    for group in sorted(changed_groups):
        previous_value = previous_artifacts.get(group)
        current_value = current_artifacts.get(group)
        previous_records = (
            previous_value if group in COLLECTION_ARTIFACT_GROUPS else [previous_value]
        )
        current_records = (
            current_value if group in COLLECTION_ARTIFACT_GROUPS else [current_value]
        )
        previous_by_id = {
            record.get("artifact_id"): record
            for record in previous_records
            if isinstance(record, dict) and is_nonempty_string(record.get("artifact_id"))
        } if isinstance(previous_records, list) else {}
        current_by_id = {
            record.get("artifact_id"): record
            for record in current_records
            if isinstance(record, dict) and is_nonempty_string(record.get("artifact_id"))
        } if isinstance(current_records, list) else {}

        for artifact_id in sorted(set(previous_by_id) | set(current_by_id)):
            before = previous_by_id.get(artifact_id)
            after = current_by_id.get(artifact_id)
            if before == after:
                continue
            authoritative = after if after is not None else before
            if authoritative.get("producer_identity") != actor_identity:
                result.errors.append(
                    f"actor_role.{actor_role}: artifacts.{group}[{artifact_id}] must record actor_identity"
                )


def validate_manifest(
    manifest: dict[str, Any],
    root: Path,
    previous: dict[str, Any] | None = None,
    actor_role: str | None = None,
    actor_identity: str | None = None,
) -> ValidationResult:
    result = ValidationResult()
    if manifest.get("schema_version") != 1:
        result.errors.append("schema_version: only version 1 is supported")
    unknown = sorted(set(manifest) - TOP_LEVEL_FIELDS)
    if unknown:
        result.errors.append(f"manifest: unknown top-level fields: {', '.join(unknown)}")
    for field_name in ("work_item_id", "title"):
        if not is_nonempty_string(manifest.get(field_name)):
            result.errors.append(f"{field_name}: required")
    revision = manifest.get("revision")
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 1:
        result.errors.append("revision: must be a positive integer")
    for field_name in ("sources", "decisions", "validations", "ui_baselines", "anchors"):
        if field_name in manifest:
            require_list(manifest[field_name], field_name, result)
    if "extensions" in manifest and not isinstance(manifest["extensions"], dict):
        result.errors.append("extensions: must be a mapping")

    by_id, artifact_inputs = validate_artifacts(manifest, root, result)
    validate_ui_evidence(manifest, by_id, result)
    input_fingerprint = compute_input_fingerprint(manifest, artifact_inputs)
    result.package_input_fingerprint = input_fingerprint
    recorded_input = manifest.get("package_input_fingerprint")
    if recorded_input is not None and recorded_input != input_fingerprint:
        result.errors.append("package_input_fingerprint: stale or incorrect")

    pre_split_artifact_inputs = [
        record
        for record in artifact_inputs
        if record.get("kind") in PRE_SPLIT_ARTIFACT_GROUPS
    ]
    pre_split_input_fingerprint = compute_input_fingerprint(
        manifest, pre_split_artifact_inputs
    )
    result.pre_split_input_fingerprint = pre_split_input_fingerprint
    pre_split_review_state = validate_review(
        manifest,
        "pre_split_review",
        pre_split_input_fingerprint,
        by_id,
        PRE_SPLIT_ARTIFACT_GROUPS,
        result,
    )
    planning_artifacts_present = any(
        record.get("_group") in PLANNING_ARTIFACT_GROUPS
        for record in by_id.values()
    )
    if planning_artifacts_present and pre_split_review_state != "ready":
        result.errors.append(
            "pre_split_review: current ready review is required before planning artifacts"
        )

    review_state = validate_review(
        manifest,
        "review",
        input_fingerprint,
        by_id,
        ARTIFACT_GROUPS,
        result,
    )
    dingtalk = validate_publish_plan(manifest, by_id, result)
    approval_valid = validate_approval(manifest, result.publish_payload_fingerprint, result)
    current_release_status = release_status(manifest, dingtalk, result)

    if previous is not None:
        if actor_role is None:
            result.errors.append("actor_role: required with previous manifest")
        else:
            validate_actor_changes(
                previous, manifest, actor_role, actor_identity, result
            )
    derive_state(result, review_state, approval_valid, current_release_status)

    recorded_status = manifest.get("package_status")
    if recorded_status is not None and recorded_status != result.derived_status:
        result.warnings.append(
            f"package_status: recorded {recorded_status}, validator derives {result.derived_status}"
        )
    return result


def stage_for_status(status: str) -> str:
    if status in {"review_pending", "changes_requested"}:
        return "review"
    if status == "package_ready":
        return "approval"
    if status in {"publish_approved", "publishing", "publish_failed", "published_unverified"}:
        return "publish"
    if status == "verified":
        return "complete"
    return "validation"


def ensure_current_attempt(dingtalk: dict[str, Any], attempt_id: str, occurred_at: str) -> dict[str, Any]:
    attempts = dingtalk.setdefault("attempts", [])
    if attempts and attempts[-1].get("attempt_id") == attempt_id:
        return attempts[-1]
    attempt = {"attempt_id": attempt_id, "started_at": occurred_at, "status": "started"}
    attempts.append(attempt)
    del attempts[:-MAX_ATTEMPTS]
    return attempt


def load_browser_evidence(
    path: Path,
    actor_identity: str | None,
    *,
    node_id: str,
    doc_url: str | None,
    payload_fingerprint: str,
) -> dict[str, Any]:
    try:
        evidence = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid browser evidence: {exc}") from exc
    if not isinstance(evidence, dict) or evidence.get("passed") is not True:
        raise ValueError("browser evidence must record passed=true")
    verifier = evidence.get("verifier_identity")
    if not is_nonempty_string(verifier):
        raise ValueError("browser evidence requires verifier_identity")
    if actor_identity and verifier == actor_identity:
        raise ValueError("browser evidence must come from an identity independent from Publisher")
    if not is_nonempty_string(evidence.get("checked_at")):
        raise ValueError("browser evidence requires checked_at")
    if evidence.get("node_id") != node_id:
        raise ValueError("browser evidence node_id does not match the published node")
    if evidence.get("payload_fingerprint") != payload_fingerprint:
        raise ValueError("browser evidence payload_fingerprint is stale or incorrect")
    if is_nonempty_string(doc_url) and evidence.get("doc_url") != doc_url:
        raise ValueError("browser evidence doc_url does not match the published document")
    checks = evidence.get("checks")
    required = {"title_visible", "content_visible", "artifacts_visible", "publish_pollution_absent"}
    if not isinstance(checks, dict) or any(checks.get(key) is not True for key in required):
        raise ValueError("browser evidence requires all visibility checks to pass")
    return {
        "passed": True,
        "verifier_identity": verifier,
        "checked_at": evidence["checked_at"],
        "node_id": node_id,
        "doc_url": doc_url,
        "payload_fingerprint": payload_fingerprint,
        "checks": {key: True for key in sorted(required)},
        "evidence_ref": str(path.name),
    }


def atomic_write_yaml(path: Path, manifest: dict[str, Any]) -> None:
    rendered = yaml.safe_dump(manifest, allow_unicode=True, sort_keys=False)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(rendered)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    except BaseException:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def record_publish_event(path: Path, manifest: dict[str, Any], args: argparse.Namespace) -> ValidationResult:
    before = validate_manifest(manifest, path.parent)
    expected = args.expected_payload_fingerprint
    if not expected or expected != before.publish_payload_fingerprint:
        before.errors.append("expected payload fingerprint does not match the current publish plan")
    event = args.record_publish_event
    allowed_statuses = {
        "started": {"publish_approved", "publish_failed", "published_unverified"},
        "remote_created": {"publishing"},
        "artifact_completed": {"publishing"},
        "failed": {"publishing"},
        "readback_passed": {"publishing"},
        "browser_verified": {"published_unverified"},
    }
    if before.derived_status not in allowed_statuses[event]:
        before.errors.append(
            f"publish event {event} is not allowed from {before.derived_status}; "
            "a current approval and valid transition are required"
        )
    current_dingtalk = manifest.get("release", {}).get("dingtalk", {})
    current_attempts = current_dingtalk.get("attempts", []) if isinstance(current_dingtalk, dict) else []
    if event != "started" and (
        not isinstance(current_attempts, list)
        or not current_attempts
        or current_attempts[-1].get("attempt_id") != args.attempt_id
    ):
        before.errors.append(f"publish event {event} requires started for the current attempt")
    if before.errors:
        derive_state(before, "missing", False, None)
        return before

    updated = copy.deepcopy(manifest)
    dingtalk = updated["release"]["dingtalk"]
    old_status = updated.get("package_status", before.derived_status)
    occurred_at = args.occurred_at
    attempt = ensure_current_attempt(dingtalk, args.attempt_id, occurred_at)

    if event == "started":
        dingtalk["status"] = "publishing"
        attempt["status"] = "publishing"
    elif event == "remote_created":
        if not is_nonempty_string(args.node_id):
            raise ValueError("remote_created requires --node-id")
        existing = dingtalk.get("node_id")
        if existing and existing != args.node_id:
            raise ValueError("remote_created cannot replace the recorded node_id")
        dingtalk["node_id"] = args.node_id
        if args.doc_url:
            dingtalk["doc_url"] = args.doc_url
        dingtalk["status"] = "publishing"
        attempt["status"] = "remote_created"
    elif event == "artifact_completed":
        if not is_nonempty_string(args.artifact_ref):
            raise ValueError("artifact_completed requires --artifact-ref")
        if not is_nonempty_string(dingtalk.get("node_id")):
            raise ValueError("artifact_completed requires a recorded node_id")
        allowlist = {
            dingtalk.get("content_artifact_ref"),
            *dingtalk.get("html_artifact_refs", []),
            *dingtalk.get("screenshot_artifact_refs", []),
        }
        if args.artifact_ref not in allowlist:
            raise ValueError("artifact_completed ref is outside the publish allowlist")
        completed = dingtalk.setdefault("completed_artifact_refs", [])
        if args.artifact_ref not in completed:
            completed.append(args.artifact_ref)
        dingtalk["status"] = "publishing"
        attempt["status"] = "publishing"
    elif event == "failed":
        if not is_nonempty_string(args.failed_step):
            raise ValueError("failed requires --failed-step")
        dingtalk["status"] = "publish_failed"
        attempt.update(
            {"status": "failed", "failed_step": args.failed_step, "error_summary": args.error_summary or "failed"}
        )
    elif event == "readback_passed":
        if not is_nonempty_string(dingtalk.get("node_id")):
            raise ValueError("readback_passed requires a recorded node_id")
        if args.readback_node_id != dingtalk.get("node_id"):
            raise ValueError("readback_passed requires the published node_id")
        if args.readback_title != dingtalk.get("title"):
            raise ValueError("readback_passed requires the approved title")
        if dingtalk.get("mode") == "doc" and not is_nonempty_string(args.readback_content_sha256):
            raise ValueError("readback_passed requires --readback-content-sha256 in document mode")
        dingtalk["readback"] = {
            "passed": True,
            "checked_at": occurred_at,
            "node_id": args.readback_node_id,
            "title": args.readback_title,
            "content_sha256": args.readback_content_sha256,
        }
        dingtalk["status"] = "published_unverified"
        attempt["status"] = "readback_passed"
    elif event == "browser_verified":
        if not isinstance(dingtalk.get("readback"), dict) or dingtalk["readback"].get("passed") is not True:
            raise ValueError("browser_verified requires read-back to pass first")
        if args.browser_evidence is None:
            raise ValueError("browser_verified requires --browser-evidence")
        dingtalk["browser_visibility"] = load_browser_evidence(
            args.browser_evidence,
            args.actor_identity,
            node_id=dingtalk["node_id"],
            doc_url=dingtalk.get("doc_url"),
            payload_fingerprint=before.publish_payload_fingerprint,
        )
        dingtalk["status"] = "verified"
        attempt["status"] = "verified"
        attempt["completed_at"] = occurred_at
    else:
        raise ValueError(f"unsupported publish event: {event}")

    updated["updated_at"] = occurred_at
    updated["last_transition"] = {
        "actor": args.actor_identity or args.actor_role,
        "from_status": old_status,
        "to_status": dingtalk["status"],
        "input_fingerprint": before.package_input_fingerprint,
        "occurred_at": occurred_at,
    }
    interim = validate_manifest(updated, path.parent)
    if interim.errors:
        return interim
    updated["package_input_fingerprint"] = interim.package_input_fingerprint
    updated["package_status"] = interim.derived_status
    updated["current_stage"] = stage_for_status(interim.derived_status)
    updated["last_transition"]["to_status"] = interim.derived_status
    updated["last_transition"]["input_fingerprint"] = interim.package_input_fingerprint
    scoped = validate_manifest(
        updated,
        path.parent,
        previous=manifest,
        actor_role=args.actor_role,
        actor_identity=args.actor_identity,
    )
    if scoped.errors:
        return scoped
    atomic_write_yaml(path, updated)
    return validate_manifest(updated, path.parent)


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("manifest", type=Path)
    value.add_argument("--json", action="store_true", dest="as_json")
    value.add_argument("--previous-manifest", type=Path)
    value.add_argument("--actor-role", choices=sorted(ROLE_PREFIXES))
    value.add_argument("--actor-identity")
    value.add_argument("--require-status", action="append", dest="required_statuses")
    value.add_argument("--expected-payload-fingerprint")
    value.add_argument(
        "--record-publish-event",
        choices=("started", "remote_created", "artifact_completed", "failed", "readback_passed", "browser_verified"),
    )
    value.add_argument("--attempt-id", default="attempt-1")
    value.add_argument("--occurred-at", default="1970-01-01T00:00:00+00:00")
    value.add_argument("--node-id")
    value.add_argument("--doc-url")
    value.add_argument("--artifact-ref")
    value.add_argument("--failed-step")
    value.add_argument("--error-summary")
    value.add_argument("--readback-node-id")
    value.add_argument("--readback-title")
    value.add_argument("--readback-content-sha256")
    value.add_argument("--browser-evidence", type=Path)
    return value


def main() -> int:
    args = parser().parse_args()
    try:
        manifest = load_manifest(args.manifest)
        if args.record_publish_event:
            if args.actor_role != "publisher":
                raise ValueError("publish events require --actor-role publisher")
            result = record_publish_event(args.manifest, manifest, args)
        else:
            previous = load_manifest(args.previous_manifest) if args.previous_manifest else None
            result = validate_manifest(
                manifest,
                args.manifest.parent,
                previous,
                args.actor_role,
                args.actor_identity,
            )
    except ValueError as exc:
        result = ValidationResult(errors=[str(exc)])

    if args.expected_payload_fingerprint and not args.record_publish_event:
        if result.publish_payload_fingerprint != args.expected_payload_fingerprint:
            result.errors.append("expected payload fingerprint does not match the current publish plan")
            result.derived_status = "invalid"
            result.earliest_recovery_node = "approval"
    if args.required_statuses and result.derived_status not in args.required_statuses:
        result.errors.append(
            f"required status one of {', '.join(args.required_statuses)}, derived {result.derived_status}"
        )
    payload = result.as_dict()
    if args.as_json:
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    else:
        print(f"Product Delivery Manifest: {'PASS' if result.valid else 'FAIL'}")
        print(f"Derived status: {result.derived_status}")
        print(f"Earliest recovery node: {result.earliest_recovery_node}")
        if result.package_input_fingerprint:
            print(f"Package input fingerprint: {result.package_input_fingerprint}")
        if result.publish_payload_fingerprint:
            print(f"Publish payload fingerprint: {result.publish_payload_fingerprint}")
        for warning in result.warnings:
            print(f"warning: {warning}")
        for error in result.errors:
            print(f"error: {error}")
    return 0 if result.valid else 1


if __name__ == "__main__":
    raise SystemExit(main())
