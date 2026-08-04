#!/usr/bin/env python3
"""Validate a Yunxiao work-item draft and compute its confirmation fingerprint."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ALLOWED_TYPES = {"需求", "缺陷"}
ALLOWED_PRIORITIES = {"紧急", "高", "中", "低"}
ALLOWED_EVIDENCE_LEVELS = {"已验证", "有依据的推断", "弱推断", "待验证"}
REQUIRED_SECTIONS = {
    "缺陷": ["问题现象", "期望结果", "排查证据", "排查结论", "验收标准"],
    "需求": ["需求背景", "目标与价值", "范围", "排查证据", "验收标准"],
}
MAX_ATTACHMENT_BYTES = 10 * 1024 * 1024
MIME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9.+-]*/[a-z0-9][a-z0-9.+-]*$")
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
KNOWN_ATTACHMENT_MIME_TYPES = {
    ".gif": "image/gif",
    ".jpeg": "image/jpeg",
    ".jpg": "image/jpeg",
    ".pdf": "application/pdf",
    ".png": "image/png",
    ".webp": "image/webp",
}


def canonical_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in payload.items() if key != "confirmation"}


def fingerprint(payload: dict[str, Any]) -> str:
    serialized = json.dumps(
        canonical_payload(payload),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(serialized).hexdigest()


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(
    payload: dict[str, Any], require_confirmed: bool
) -> tuple[list[str], list[str], str]:
    errors: list[str] = []
    warnings: list[str] = []

    project = payload.get("project")
    if not isinstance(project, dict) or not nonempty_string(project.get("id")):
        errors.append("project.id is required")

    work_item_type = payload.get("work_item_type")
    if work_item_type not in ALLOWED_TYPES:
        errors.append("work_item_type must be 需求 or 缺陷")

    title = payload.get("title")
    if not nonempty_string(title):
        errors.append("title is required")
    elif len(title.strip()) > 120:
        warnings.append("title is longer than 120 characters; verify the live MCP limit")

    if payload.get("priority") not in ALLOWED_PRIORITIES:
        errors.append("priority must be 紧急, 高, 中, or 低")

    description = payload.get("description")
    if not nonempty_string(description):
        errors.append("description is required")
    elif work_item_type in REQUIRED_SECTIONS:
        for section in REQUIRED_SECTIONS[work_item_type]:
            if f"【{section}】" not in description:
                errors.append(f"description is missing section: {section}")

    evidence = payload.get("evidence")
    if evidence is None:
        errors.append("evidence must be present as a list, even when empty")
    elif not isinstance(evidence, list):
        errors.append("evidence must be a list")
    else:
        for index, item in enumerate(evidence):
            prefix = f"evidence[{index}]"
            if not isinstance(item, dict):
                errors.append(f"{prefix} must be an object")
                continue
            if item.get("level") not in ALLOWED_EVIDENCE_LEVELS:
                errors.append(f"{prefix}.level is invalid")
            for field in ["kind", "source", "observation", "supports"]:
                if not nonempty_string(item.get(field)):
                    errors.append(f"{prefix}.{field} is required")

    attachments = payload.get("attachments", [])
    if not isinstance(attachments, list):
        errors.append("attachments must be a list")
    else:
        for index, item in enumerate(attachments):
            prefix = f"attachments[{index}]"
            if not isinstance(item, dict):
                errors.append(f"{prefix} must be an object")
                continue

            file_name = item.get("file_name")
            if not nonempty_string(file_name):
                errors.append(f"{prefix}.file_name is required")
            elif "/" in file_name or "\\" in file_name:
                errors.append(f"{prefix}.file_name must not contain a local path")
            elif "." not in file_name:
                errors.append(f"{prefix}.file_name must include an extension")
            elif nonempty_string(description) and file_name not in description:
                errors.append(f"description must mention attachment file name: {file_name}")

            mime_type = item.get("mime_type")
            if not nonempty_string(mime_type) or not MIME_PATTERN.fullmatch(mime_type):
                errors.append(f"{prefix}.mime_type is invalid")
            elif nonempty_string(file_name):
                expected_mime = KNOWN_ATTACHMENT_MIME_TYPES.get(
                    Path(file_name).suffix.lower()
                )
                if expected_mime and mime_type != expected_mime:
                    errors.append(
                        f"{prefix}.mime_type must be {expected_mime} "
                        f"for {Path(file_name).suffix.lower()}"
                    )

            size_bytes = item.get("size_bytes")
            if (
                not isinstance(size_bytes, int)
                or isinstance(size_bytes, bool)
                or size_bytes <= 0
            ):
                errors.append(f"{prefix}.size_bytes must be a positive integer")
            elif size_bytes > MAX_ATTACHMENT_BYTES:
                errors.append(f"{prefix}.size_bytes exceeds the 10 MB MCP limit")

            sha256 = item.get("sha256")
            if not nonempty_string(sha256) or not SHA256_PATTERN.fullmatch(sha256):
                errors.append(f"{prefix}.sha256 must be a lowercase SHA256 hex digest")

            if item.get("sensitivity_check") != "passed":
                errors.append(f"{prefix}.sensitivity_check must be passed")

    duplicate_check = payload.get("duplicate_check")
    if not isinstance(duplicate_check, dict) or duplicate_check.get("status") not in {
        "passed",
        "candidate_found",
        "unavailable",
    }:
        errors.append(
            "duplicate_check.status must be passed, candidate_found, or unavailable"
        )
    elif duplicate_check.get("status") == "candidate_found":
        errors.append("duplicate candidate must be resolved before confirmation")
    elif duplicate_check.get("status") == "unavailable":
        warnings.append(
            "duplicate check was unavailable; preview must disclose duplicate risk"
        )

    current_fingerprint = fingerprint(payload)
    confirmation = payload.get("confirmation", {})
    status = confirmation.get("status") if isinstance(confirmation, dict) else None
    if require_confirmed:
        if status != "confirmed":
            errors.append("confirmation.status must be confirmed")
        else:
            for field in ["confirmed_by", "confirmed_at", "confirmed_fingerprint"]:
                if not nonempty_string(confirmation.get(field)):
                    errors.append(f"confirmation.{field} is required")
            if confirmation.get("confirmed_fingerprint") != current_fingerprint:
                errors.append("confirmed fingerprint does not match the current payload")
    elif status not in {None, "pending", "confirmed"}:
        errors.append("confirmation.status must be pending or confirmed")

    return errors, warnings, current_fingerprint


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", type=Path)
    parser.add_argument("--require-confirmed", action="store_true")
    args = parser.parse_args()

    try:
        payload = json.loads(args.draft.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"valid": False, "errors": [str(exc)]}, ensure_ascii=False))
        return 1

    if not isinstance(payload, dict):
        print(
            json.dumps(
                {"valid": False, "errors": ["draft root must be an object"]},
                ensure_ascii=False,
            )
        )
        return 1

    errors, warnings, current_fingerprint = validate(payload, args.require_confirmed)
    result = {
        "valid": not errors,
        "fingerprint": current_fingerprint,
        "errors": errors,
        "warnings": warnings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
