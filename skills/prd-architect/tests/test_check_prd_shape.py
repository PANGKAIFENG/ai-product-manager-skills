#!/usr/bin/env python3
"""Regression tests for PRD mockup evidence gates."""

from __future__ import annotations

import importlib.util
import hashlib
import io
import json
import os
import re
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


def standard_prd(body: str, *, background: str = "当前页面缺少本期目标状态，研发和测试无法直接对齐改动结果。") -> str:
    return f"""# Test PRD

## 版本记录

| 版本 | 日期 | 修改内容 |
| --- | --- | --- |
| V1.0 | 2026-08-15 | 首次创建 |

## 背景与目标

- **背景**：{background}
- **本期只解决**：补齐 mockup 证据承接。
- **成功标准**：功能模块可直接验证。

## 功能模块

### 目标状态

**模块目的**：让读者直接理解目标状态。

{body}

| 条件 / 状态 | 用户操作 | 系统行为 | UI 反馈 |
| --- | --- | --- | --- |
| 默认 | 打开页面 | 展示目标状态 | 页面可见 |

## 待确认事项
无。
"""


def run_shape_only(
    markdown: str,
    *,
    prd_type: str = "standard",
    publish_ready: bool = False,
    maturity: str | None = None,
    require_version_history: bool = False,
) -> CheckResult:
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "prd.md"
        path.write_text(markdown, encoding="utf-8")
        argv = [str(SCRIPT), str(path), "--type", prd_type]
        if publish_ready:
            argv.append("--publish-ready")
        if require_version_history:
            argv.append("--require-version-history")
        if maturity:
            argv.extend(["--maturity", maturity])
        stdout = io.StringIO()
        with patch.object(sys, "argv", argv), redirect_stdout(stdout):
            returncode = CHECKER.main()
        return CheckResult(returncode=returncode, stdout=stdout.getvalue())


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
    temp_root: Path,
    prd_path: Path,
    mockup_path: Path,
    screenshot_path: Path,
    baseline_path: Path,
    *,
    source_mockup_hash: str | None = None,
) -> Path:
    manifest_path = temp_root / "mockup-evidence.json"
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
                "path": screenshot_path.relative_to(temp_root).as_posix(),
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
        prd_path.write_text(standard_prd("![目标态：默认态](./screenshots/default.png)"), encoding="utf-8")
        manifest_path = write_manifest(root, prd_path, mockup_path, screenshot_path, baseline_path)

        if mutate == "html":
            mockup_path.write_text("<!doctype html><html><body>Updated</body></html>", encoding="utf-8")
        elif mutate == "old-screenshot":
            older = mockup_path.stat().st_mtime_ns - 1_000_000_000
            os.utime(screenshot_path, ns=(older, older))
        elif mutate == "baseline":
            baseline_path.write_bytes(b"new baseline")
        elif mutate == "prd-reference":
            prd_path.write_text(standard_prd("![目标态：别的状态](./screenshots/other.png)"), encoding="utf-8")

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
        self.assertIn("missing_module_target_state_evidence:目标状态", result.stdout)

    def test_inline_screenshot_in_feature_section_passes(self) -> None:
        result = run_check(
            standard_prd("![目标态：默认态](./assets/default-state.png)"),
            ("assets/default-state.png",),
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_local_screenshot_file_is_reported(self) -> None:
        result = run_check(standard_prd("![目标态：默认态](./assets/not-generated.png)"))

        self.assertEqual(result.returncode, 1)
        self.assertIn("missing_mockup_file", result.stdout)

    def test_screenshot_only_in_local_appendix_is_reported(self) -> None:
        markdown = standard_prd("这里没有截图。") + """

## 本地草稿附录
![原型总览](./assets/overview.png)
"""
        result = run_check(markdown, ("assets/overview.png",))

        self.assertEqual(result.returncode, 1)
        self.assertIn("missing_module_target_state_evidence:目标状态", result.stdout)

    def test_existing_html_mockup_artifact_passes(self) -> None:
        result = run_check(
            standard_prd("![目标态：默认态](./assets/default-state.png)"),
            ("assets/default-state.png",),
            "mockup.html",
            create_mockup=True,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_html_mockup_artifact_is_reported(self) -> None:
        result = run_check(
            standard_prd("![目标态：默认态](./assets/default-state.png)"),
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
            prd_path.write_text(standard_prd("![目标态：默认态](./default.png)"), encoding="utf-8")
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
            prd_path.write_text(standard_prd("![目标态：默认态](./default.png)"), encoding="utf-8")

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


class FlexibleTemplateShapeTest(unittest.TestCase):
    def test_concise_standard_without_legacy_sections_passes(self) -> None:
        result = run_shape_only(standard_prd("功能逻辑已写入模块。"))

        self.assertEqual(result.returncode, 0, result.stdout)

    def test_required_version_history_passes_for_new_prd(self) -> None:
        result = run_shape_only(standard_prd("功能逻辑已写入模块。"), require_version_history=True)

        self.assertEqual(result.returncode, 0, result.stdout)

    def test_missing_version_history_is_reported(self) -> None:
        markdown = standard_prd("功能逻辑已写入模块。").replace(
            "## 版本记录\n\n| 版本 | 日期 | 修改内容 |\n| --- | --- | --- |\n| V1.0 | 2026-08-15 | 首次创建 |\n\n",
            "",
        )

        result = run_shape_only(markdown, require_version_history=True)

        self.assertEqual(result.returncode, 1)
        self.assertIn("missing_version_history", result.stdout)

    def test_publish_ready_implicitly_requires_version_history(self) -> None:
        markdown = standard_prd("功能逻辑已写入模块。").replace(
            "## 版本记录\n\n| 版本 | 日期 | 修改内容 |\n| --- | --- | --- |\n| V1.0 | 2026-08-15 | 首次创建 |\n\n",
            "",
        )

        result = run_shape_only(markdown, publish_ready=True)

        self.assertEqual(result.returncode, 1)
        self.assertIn("missing_version_history", result.stdout)

    def test_version_history_must_be_newest_first_with_concrete_changes(self) -> None:
        markdown = standard_prd("功能逻辑已写入模块。").replace(
            "| V1.0 | 2026-08-15 | 首次创建 |",
            "| V1.0 | 2026-08-01 | 首次创建 |\n| V1.1 | 2026-08-15 | 更新 PRD |",
        )

        result = run_shape_only(markdown, require_version_history=True)

        self.assertEqual(result.returncode, 1)
        self.assertIn("version_history_not_newest_first", result.stdout)
        self.assertIn("generic_version_changes:V1.1", result.stdout)

    def test_version_history_must_be_the_first_h2(self) -> None:
        markdown = standard_prd("功能逻辑已写入模块。").replace(
            "## 版本记录\n\n| 版本 | 日期 | 修改内容 |\n| --- | --- | --- |\n| V1.0 | 2026-08-15 | 首次创建 |\n\n",
            "",
        ).replace(
            "## 背景与目标",
            "## 背景与目标\n\n## 版本记录\n\n| 版本 | 日期 | 修改内容 |\n| --- | --- | --- |\n| V1.0 | 2026-08-15 | 首次创建 |\n",
        )

        result = run_shape_only(markdown, require_version_history=True)

        self.assertEqual(result.returncode, 1)
        self.assertIn("version_history_not_at_top", result.stdout)

    def test_missing_feature_module_capability_is_reported(self) -> None:
        markdown = standard_prd("功能逻辑已写入模块。").replace("## 功能模块", "## 方案说明")
        result = run_shape_only(markdown)

        self.assertEqual(result.returncode, 1)
        self.assertIn("missing_expected_capability:feature_modules", result.stdout)

    def test_background_over_200_visible_characters_is_reported(self) -> None:
        result = run_shape_only(standard_prd("功能逻辑已写入模块。", background="背" * 201))

        self.assertEqual(result.returncode, 1)
        self.assertIn("background_too_long:201", result.stdout)

    def test_heading_background_excludes_scope_and_success_fields(self) -> None:
        markdown = standard_prd("功能逻辑已写入模块。").replace(
            "- **背景**：当前页面缺少本期目标状态，研发和测试无法直接对齐改动结果。",
            f"### 背景\n\n{'背' * 190}",
        )

        result = run_shape_only(markdown)

        self.assertEqual(result.returncode, 0, result.stdout)

    def test_publish_ready_does_not_require_open_questions(self) -> None:
        markdown = standard_prd("功能逻辑已写入模块。").replace("\n## 待确认事项\n无。\n", "\n")
        result = run_shape_only(markdown, publish_ready=True)

        self.assertEqual(result.returncode, 0, result.stdout)

    def test_confirmed_maturity_does_not_require_open_questions(self) -> None:
        markdown = standard_prd("功能逻辑已写入模块。").replace(
            "# Test PRD",
            "# Test PRD\n\n**文档状态**：已确认",
        ).replace("\n## 待确认事项\n无。\n", "\n")

        result = run_shape_only(markdown)

        self.assertEqual(result.returncode, 0, result.stdout)

    def test_confirmed_maturity_is_detected_from_document_table(self) -> None:
        markdown = standard_prd("功能逻辑已写入模块。").replace(
            "# Test PRD",
            "# Test PRD\n\n## 文档信息\n\n| 功能名 | 状态 | 模块 |\n| --- | --- | --- |\n| 测试功能 | 已确认 | 订单 |",
        ).replace("\n## 待确认事项\n无。\n", "\n")

        result = run_shape_only(markdown)

        self.assertEqual(result.returncode, 0, result.stdout)

    def test_feature_state_does_not_override_document_maturity(self) -> None:
        markdown = standard_prd("**文档状态**：已确认\n\n| 结果状态 | 用户操作 | 系统行为 | UI 反馈 |\n| --- | --- | --- | --- |\n| 已确认 | 查看 | 展示结果 | 可见 |").replace(
            "\n## 待确认事项\n无。\n",
            "\n",
        )

        result = run_shape_only(markdown)

        self.assertEqual(result.returncode, 1)
        self.assertIn("missing_expected_capability:open_questions", result.stdout)

    def test_draft_maturity_requires_open_questions(self) -> None:
        markdown = standard_prd("功能逻辑已写入模块。").replace("\n## 待确认事项\n无。\n", "\n")

        result = run_shape_only(markdown, maturity="draft")

        self.assertEqual(result.returncode, 1)
        self.assertIn("missing_expected_capability:open_questions", result.stdout)

    def test_heading_background_over_200_visible_characters_is_reported(self) -> None:
        markdown = standard_prd("功能逻辑已写入模块。").replace(
            "- **背景**：当前页面缺少本期目标状态，研发和测试无法直接对齐改动结果。",
            f"### 背景\n\n{'背' * 201}",
        )

        result = run_shape_only(markdown)

        self.assertEqual(result.returncode, 1)
        self.assertIn("background_too_long:", result.stdout)

    def test_unparseable_background_region_is_reported(self) -> None:
        markdown = standard_prd("功能逻辑已写入模块。").replace(
            "- **背景**：当前页面缺少本期目标状态，研发和测试无法直接对齐改动结果。",
            "当前页面说明未标记背景边界。",
        )

        result = run_shape_only(markdown)

        self.assertEqual(result.returncode, 1)
        self.assertIn("background_uncheckable", result.stdout)

    def test_legacy_parallel_section_is_reported(self) -> None:
        markdown = standard_prd("功能逻辑已写入模块。").replace(
            "## 功能模块",
            "## 用户场景\n\n用户打开页面。\n\n## 功能模块",
        )

        result = run_shape_only(markdown)

        self.assertEqual(result.returncode, 1)
        self.assertIn("legacy_parallel_section:用户场景", result.stdout)

    def test_interaction_heading_cannot_substitute_for_feature_modules(self) -> None:
        markdown = standard_prd("功能逻辑已写入模块。").replace("## 功能模块", "## 交互逻辑")

        result = run_shape_only(markdown)

        self.assertEqual(result.returncode, 1)
        self.assertIn("missing_expected_capability:feature_modules", result.stdout)
        self.assertIn("legacy_parallel_section:交互逻辑", result.stdout)

    def test_each_module_requires_its_own_ui_evidence(self) -> None:
        markdown = standard_prd("模块一没有目标态截图。").replace(
            "- **成功标准**：功能模块可直接验证。",
            "- **成功标准**：功能模块可直接验证。\n\n![现状参考](./assets/current.png)",
        ).replace(
            "## 待确认事项",
            """### 模块二

**模块目的**：展示第二个状态。

| 条件 / 状态 | 用户操作 | 系统行为 | UI 反馈 |
| --- | --- | --- | --- |
| 默认 | 打开页面 | 展示状态 | 页面可见 |

## 待确认事项""",
        )

        result = run_check(markdown, ("assets/current.png",))

        self.assertEqual(result.returncode, 1)
        self.assertIn("missing_module_target_state_evidence:目标状态", result.stdout)
        self.assertIn("missing_module_target_state_evidence:模块二", result.stdout)

    def test_current_state_image_cannot_substitute_for_target_state_evidence(self) -> None:
        result = run_check(
            standard_prd("![现状参考](./assets/current.png)"),
            ("assets/current.png",),
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("missing_module_target_state_evidence:目标状态", result.stdout)

    def test_module_without_logic_table_is_reported(self) -> None:
        markdown = standard_prd("功能逻辑已写入模块。").replace(
            "| 条件 / 状态 | 用户操作 | 系统行为 | UI 反馈 |\n| --- | --- | --- | --- |\n| 默认 | 打开页面 | 展示目标状态 | 页面可见 |",
            "打开页面后展示目标状态。",
        )

        result = run_shape_only(markdown)

        self.assertEqual(result.returncode, 1)
        self.assertIn("missing_module_logic:目标状态", result.stdout)

    def test_module_logic_table_requires_a_nonempty_data_row(self) -> None:
        markdown = standard_prd("功能逻辑已写入模块。").replace(
            "| 默认 | 打开页面 | 展示目标状态 | 页面可见 |",
            "|  |  |  |  |",
        )

        result = run_shape_only(markdown)

        self.assertEqual(result.returncode, 1)
        self.assertIn("missing_module_logic:目标状态", result.stdout)

    def test_lite_module_first_shape_passes(self) -> None:
        markdown = """# Lite PRD

## 版本记录
| 版本 | 日期 | 修改内容 |
| --- | --- | --- |
| V1.0 | 2026-08-15 | 首次创建 |

## 背景与目标
- **背景**：当前按钮缺少权限反馈。
- **本期只解决**：补充无权限提示。

## 功能模块
### 下载权限提示
| 条件 / 状态 | 用户操作 | 系统行为 | UI 反馈 |
| --- | --- | --- | --- |
| 无权限 | 点击下载 | 保留筛选条件 | 展示权限提示 |

## 待确认事项
无。
"""
        result = run_shape_only(markdown, prd_type="lite")

        self.assertEqual(result.returncode, 0, result.stdout)

    def test_ai_native_module_first_shape_passes(self) -> None:
        markdown = """# AI PRD

## 版本记录
| 版本 | 日期 | 修改内容 |
| --- | --- | --- |
| V1.0 | 2026-08-15 | 首次创建 |

## 背景与目标
- **背景**：当前生成结果缺少人工确认。
- **本期只解决**：增加确认与回退。

## AI 协作边界
人工确认，AI 生成，系统反馈。

## 功能模块
### 结果确认
| 条件 / 状态 | 用户动作 | AI 动作 | 系统反馈 | 失败 / 接管 |
| --- | --- | --- | --- | --- |
| 待确认 | 确认结果 | 保存确认 | 展示成功 | 可回退 |

## 待确认事项
无。
"""
        result = run_shape_only(markdown, prd_type="ai-native")

        self.assertEqual(result.returncode, 0, result.stdout)

    def test_standalone_acceptance_sections_are_reported(self) -> None:
        for heading in ("验收标准", "模块验收", "整体验收"):
            with self.subTest(heading=heading):
                markdown = standard_prd("功能逻辑已写入模块。").replace(
                    "## 待确认事项",
                    f"## {heading}\n\n不应单列。\n\n## 待确认事项",
                )

                result = run_shape_only(markdown)

                self.assertEqual(result.returncode, 1)
                self.assertIn(f"legacy_parallel_section:{heading}", result.stdout)

    def test_all_templates_omit_standalone_acceptance_sections(self) -> None:
        template_root = Path(__file__).resolve().parents[1] / "references" / "templates"
        forbidden = re.compile(r"^(?:#{1,6}\s+(?:\d+\.\s*)?)?(?:\*\*)?(?:验收标准|模块验收|整体验收)(?:\*\*)?\s*$", re.M)

        for template in sorted(template_root.glob("prd-*.md")):
            with self.subTest(template=template.name):
                self.assertIsNone(forbidden.search(template.read_text(encoding="utf-8")))

    def test_all_templates_include_version_history(self) -> None:
        template_root = Path(__file__).resolve().parents[1] / "references" / "templates"

        for template in sorted(template_root.glob("prd-*.md")):
            with self.subTest(template=template.name):
                text = template.read_text(encoding="utf-8")
                self.assertIn("| 版本 | 日期 | 修改内容 |", text)
                self.assertIn("| V1.0 | YYYY-MM-DD | 首次创建 |", text)


if __name__ == "__main__":
    unittest.main()
