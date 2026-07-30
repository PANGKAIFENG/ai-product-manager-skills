#!/usr/bin/env python3
"""Regression tests for PRD mockup evidence gates."""

from __future__ import annotations

import importlib.util
import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_prd_shape.py"
CAPTURE_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "capture_mockup_evidence.py"
SPEC = importlib.util.spec_from_file_location("prd_shape_checker", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
CHECKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECKER)


@dataclass(frozen=True)
class CheckResult:
    returncode: int
    stdout: str
    stderr: str = ""


def standard_prd(body: str) -> str:
    return f"""# Test PRD

本期只解决 mockup 证据承接。

## 功能目标
目标。

## 用户场景
场景。

## 入口
入口。

## 核心对象
对象。

## 交互逻辑
{body}

## 异常
异常。

## 验收标准
验收。

## 待确认
无。
"""


def run_check(
    markdown: str,
    image_paths: tuple[str, ...] = (),
    mockup_artifact: str | None = None,
    create_mockup: bool = False,
) -> CheckResult:
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "prd.md"
        path.write_text(markdown, encoding="utf-8")
        for image_path in image_paths:
            target = path.parent / image_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(b"mock image")
        argv = [
            str(SCRIPT),
            str(path),
            "--type",
            "standard",
            "--require-mockup-evidence",
        ]
        if mockup_artifact:
            target = path.parent / mockup_artifact
            if create_mockup:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("<!doctype html><html><body>Mockup</body></html>", encoding="utf-8")
            argv.extend(["--require-mockup-artifact", mockup_artifact])
        stdout = io.StringIO()
        with patch.object(sys, "argv", argv), redirect_stdout(stdout):
            returncode = CHECKER.main()
        return CheckResult(returncode=returncode, stdout=stdout.getvalue())


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_manifest(
    root: Path,
    prd_path: Path,
    mockup_path: Path,
    screenshot_path: Path,
    baseline_path: Path,
    *,
    source_mockup_hash: str | None = None,
) -> Path:
    manifest_path = root / "mockup-evidence.json"
    mockup_hash = file_hash(mockup_path)
    manifest = {
        "schema_version": 1,
        "workflow": {"stage": "prd_embedded", "captured_at": "2026-07-30T12:00:00+00:00"},
        "baseline": {
            "kind": "screenshot",
            "source": baseline_path.name,
            "source_type": "file",
            "sha256": file_hash(baseline_path),
            "note": "user confirmed no frontend repo is available",
        },
        "mockup": {
            "path": mockup_path.name,
            "sha256": mockup_hash,
            "mtime_ns": mockup_path.stat().st_mtime_ns,
        },
        "screenshots": [
            {
                "state": "default",
                "path": screenshot_path.relative_to(root).as_posix(),
                "sha256": file_hash(screenshot_path),
                "source_mockup_sha256": source_mockup_hash or mockup_hash,
                "mtime_ns": screenshot_path.stat().st_mtime_ns,
            }
        ],
        "prd": {
            "path": prd_path.name,
            "sha256": file_hash(prd_path),
            "mtime_ns": prd_path.stat().st_mtime_ns,
        },
    }
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    return manifest_path


def run_manifest_check(
    *,
    mutate: str | None = None,
) -> CheckResult:
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        screenshot_dir = root / "screenshots"
        screenshot_dir.mkdir()
        baseline_path = root / "baseline.png"
        baseline_path.write_bytes(b"baseline")
        mockup_path = root / "mockup.html"
        mockup_path.write_text("<!doctype html><html><body>Current</body></html>", encoding="utf-8")
        screenshot_path = screenshot_dir / "default.png"
        screenshot_path.write_bytes(b"current screenshot")
        prd_path = root / "prd.md"
        prd_path.write_text(standard_prd("![默认态](./screenshots/default.png)"), encoding="utf-8")
        manifest_path = write_manifest(root, prd_path, mockup_path, screenshot_path, baseline_path)

        if mutate == "html":
            mockup_path.write_text("<!doctype html><html><body>Updated</body></html>", encoding="utf-8")
        elif mutate == "old-screenshot":
            older = mockup_path.stat().st_mtime_ns - 1_000_000_000
            os.utime(screenshot_path, ns=(older, older))
        elif mutate == "baseline":
            baseline_path.write_bytes(b"new baseline")
        elif mutate == "prd-reference":
            prd_path.write_text(standard_prd("![别的状态](./screenshots/other.png)"), encoding="utf-8")

        argv = [
            str(SCRIPT),
            str(prd_path),
            "--type",
            "standard",
            "--require-mockup-evidence",
            "--require-current-mockup-evidence",
            "--mockup-manifest",
            str(manifest_path),
        ]
        stdout = io.StringIO()
        with patch.object(sys, "argv", argv), redirect_stdout(stdout):
            returncode = CHECKER.main()
        return CheckResult(returncode=returncode, stdout=stdout.getvalue())


class MockupEvidenceGateTest(unittest.TestCase):
    def test_missing_inline_screenshot_is_reported(self) -> None:
        result = run_check(standard_prd("只有 HTML 原型路径，没有截图。"))

        self.assertEqual(result.returncode, 1)
        self.assertIn("missing_mockup_evidence", result.stdout)

    def test_inline_screenshot_in_feature_section_passes(self) -> None:
        result = run_check(
            standard_prd("![默认态](./assets/default-state.png)"),
            ("assets/default-state.png",),
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_local_screenshot_file_is_reported(self) -> None:
        result = run_check(standard_prd("![默认态](./assets/not-generated.png)"))

        self.assertEqual(result.returncode, 1)
        self.assertIn("missing_mockup_file", result.stdout)

    def test_screenshot_only_in_local_appendix_is_reported(self) -> None:
        markdown = standard_prd("这里没有截图。") + """

## 本地草稿附录
![原型总览](./assets/overview.png)
"""
        result = run_check(markdown, ("assets/overview.png",))

        self.assertEqual(result.returncode, 1)
        self.assertIn("missing_mockup_evidence", result.stdout)

    def test_existing_html_mockup_artifact_passes(self) -> None:
        result = run_check(
            standard_prd("![默认态](./assets/default-state.png)"),
            ("assets/default-state.png",),
            "mockup.html",
            create_mockup=True,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_html_mockup_artifact_is_reported(self) -> None:
        result = run_check(
            standard_prd("![默认态](./assets/default-state.png)"),
            ("assets/default-state.png",),
            "missing-mockup.html",
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("missing_mockup_artifact", result.stdout)

    def test_current_screenshot_baseline_manifest_passes(self) -> None:
        result = run_manifest_check()

        self.assertEqual(result.returncode, 0, result.stdout)

    def test_updated_html_invalidates_old_screenshot_manifest(self) -> None:
        result = run_manifest_check(mutate="html")

        self.assertEqual(result.returncode, 1)
        self.assertIn("stale_mockup_hash", result.stdout)
        self.assertIn("stale_screenshot_source_mockup", result.stdout)

    def test_screenshot_older_than_html_is_reported(self) -> None:
        result = run_manifest_check(mutate="old-screenshot")

        self.assertEqual(result.returncode, 1)
        self.assertIn("stale_screenshot_mtime", result.stdout)

    def test_changed_screenshot_baseline_is_reported(self) -> None:
        result = run_manifest_check(mutate="baseline")

        self.assertEqual(result.returncode, 1)
        self.assertIn("stale_mockup_baseline_hash", result.stdout)

    def test_manifest_screenshot_must_be_embedded_in_current_prd(self) -> None:
        result = run_manifest_check(mutate="prd-reference")

        self.assertEqual(result.returncode, 1)
        self.assertIn("manifest_screenshot_not_embedded", result.stdout)
        self.assertIn("stale_manifest_prd_hash", result.stdout)

    def test_current_evidence_requires_manifest_argument(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            prd_path = Path(tmpdir) / "prd.md"
            screenshot_path = Path(tmpdir) / "default.png"
            screenshot_path.write_bytes(b"screenshot")
            prd_path.write_text(standard_prd("![默认态](./default.png)"), encoding="utf-8")
            argv = [
                str(SCRIPT),
                str(prd_path),
                "--type",
                "standard",
                "--require-mockup-evidence",
                "--require-current-mockup-evidence",
            ]
            stdout = io.StringIO()
            with patch.object(sys, "argv", argv), redirect_stdout(stdout):
                returncode = CHECKER.main()

        self.assertEqual(returncode, 1)
        self.assertIn("missing_mockup_manifest_argument", stdout.getvalue())

    def test_capture_rejects_screenshot_older_than_html(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            baseline_path = root / "baseline.png"
            baseline_path.write_bytes(b"baseline")
            screenshot_path = root / "default.png"
            screenshot_path.write_bytes(b"old screenshot")
            mockup_path = root / "mockup.html"
            mockup_path.write_text("<!doctype html><html><body>New</body></html>", encoding="utf-8")
            prd_path = root / "prd.md"
            prd_path.write_text(standard_prd("![默认态](./default.png)"), encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(CAPTURE_SCRIPT),
                    "--manifest",
                    str(root / "mockup-evidence.json"),
                    "--baseline-kind",
                    "screenshot",
                    "--baseline-source",
                    str(baseline_path),
                    "--baseline-note",
                    "user confirmed no frontend repo is available",
                    "--mockup",
                    str(mockup_path),
                    "--prd",
                    str(prd_path),
                    "--screenshot",
                    f"default={screenshot_path}",
                ],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(result.returncode, 2)
        self.assertIn("stale screenshot", result.stderr)


if __name__ == "__main__":
    unittest.main()
