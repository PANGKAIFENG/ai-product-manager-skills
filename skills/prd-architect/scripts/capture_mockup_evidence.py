#!/usr/bin/env python3
"""Capture a provenance manifest for page-oriented PRD UI evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


BASELINE_KINDS = ("frontend-repo", "design-system", "reference-html", "screenshot")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_path(path: Path) -> str:
    if path.is_file():
        return sha256_file(path)
    if not path.is_dir():
        raise ValueError(f"baseline source does not exist: {path}")

    digest = hashlib.sha256()
    files = sorted(candidate for candidate in path.rglob("*") if candidate.is_file() and ".git" not in candidate.parts)
    for candidate in files:
        digest.update(candidate.relative_to(path).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(bytes.fromhex(sha256_file(candidate)))
    return digest.hexdigest()


def git_output(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise ValueError(f"cannot inspect frontend repo {repo}: {detail}")
    return result.stdout.strip()


def stored_path(path: Path, manifest_dir: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(manifest_dir).as_posix()
    except ValueError:
        return str(resolved)


def file_record(path: Path, manifest_dir: Path) -> dict[str, object]:
    if not path.is_file():
        raise ValueError(f"file does not exist: {path}")
    stat = path.stat()
    return {
        "path": stored_path(path, manifest_dir),
        "sha256": sha256_file(path),
        "mtime_ns": stat.st_mtime_ns,
    }


def baseline_record(kind: str, source: Path, note: str) -> dict[str, object]:
    source = source.resolve()
    if kind == "frontend-repo":
        root = Path(git_output(source, "rev-parse", "--show-toplevel")).resolve()
        status = git_output(root, "status", "--porcelain=v1", "--untracked-files=no")
        return {
            "kind": kind,
            "source": str(root),
            "revision": git_output(root, "rev-parse", "HEAD"),
            "branch": git_output(root, "branch", "--show-current"),
            "dirty": bool(status),
            "worktree_status_sha256": sha256_bytes(status.encode("utf-8")),
            "note": note,
        }

    if not source.exists():
        raise ValueError(f"baseline source does not exist: {source}")
    return {
        "kind": kind,
        "source": str(source),
        "source_type": "directory" if source.is_dir() else "file",
        "sha256": sha256_path(source),
        "note": note,
    }


def parse_screenshot(value: str) -> tuple[str, Path]:
    state, separator, raw_path = value.partition("=")
    if not separator or not state.strip() or not raw_path.strip():
        raise ValueError(f"invalid --screenshot value {value!r}; expected STATE=PATH")
    return state.strip(), Path(raw_path).expanduser().resolve()


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture current mockup, screenshot, PRD, and UI baseline evidence.")
    parser.add_argument("--manifest", required=True, help="Output mockup-evidence.json path")
    parser.add_argument("--baseline-kind", required=True, choices=BASELINE_KINDS)
    parser.add_argument("--baseline-source", required=True, help="Frontend repo or fallback evidence path")
    parser.add_argument("--baseline-note", required=True, help="Why this source represents the confirmed target UI")
    parser.add_argument("--mockup", required=True, help="Current HTML mockup path")
    parser.add_argument("--prd", required=True, help="Current PRD Markdown path")
    parser.add_argument(
        "--screenshot",
        action="append",
        required=True,
        metavar="STATE=PATH",
        help="Screenshot state and path; repeat for every required state",
    )
    args = parser.parse_args()

    manifest_path = Path(args.manifest).expanduser().resolve()
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_dir = manifest_path.parent
    mockup_path = Path(args.mockup).expanduser().resolve()
    prd_path = Path(args.prd).expanduser().resolve()

    try:
        mockup = file_record(mockup_path, manifest_dir)
        prd = file_record(prd_path, manifest_dir)
        baseline = baseline_record(
            args.baseline_kind,
            Path(args.baseline_source).expanduser(),
            args.baseline_note,
        )

        screenshots: list[dict[str, object]] = []
        for value in args.screenshot:
            state, screenshot_path = parse_screenshot(value)
            record = file_record(screenshot_path, manifest_dir)
            if int(record["mtime_ns"]) < int(mockup["mtime_ns"]):
                raise ValueError(
                    f"stale screenshot for state {state!r}: {screenshot_path} is older than {mockup_path}; re-render it"
                )
            record.update(
                {
                    "state": state,
                    "source_mockup_sha256": mockup["sha256"],
                }
            )
            screenshots.append(record)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    manifest = {
        "schema_version": 1,
        "workflow": {
            "stage": "prd_embedded",
            "captured_at": datetime.now(timezone.utc).isoformat(),
        },
        "baseline": baseline,
        "mockup": mockup,
        "screenshots": screenshots,
        "prd": prd,
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Captured mockup evidence: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
