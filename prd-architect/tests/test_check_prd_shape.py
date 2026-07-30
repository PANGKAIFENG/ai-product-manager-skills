#!/usr/bin/env python3
"""Regression tests for PRD mockup evidence gates."""

from __future__ import annotations

import importlib.util
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from dataclasses import dataclass
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_prd_shape.py"
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


if __name__ == "__main__":
    unittest.main()
