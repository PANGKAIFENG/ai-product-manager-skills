#!/usr/bin/env python3
"""Regression tests for enrich_prd_with_screenshots.py."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("enrich_prd_with_screenshots.py")


class EnrichPrdWithScreenshotsTest(unittest.TestCase):
    def make_fixture(self, root: Path) -> tuple[Path, Path]:
        html = root / "x-app-intellistyle/docs/PRD/tp-translation-queue-cancel-mock.html"
        html.parent.mkdir(parents=True)
        html.write_text(
            "<!doctype html><title>Mock</title><main><h1>Queue mock</h1></main>",
            encoding="utf-8",
        )
        prd = root / "TP翻译-PRD.md"
        prd.write_text(
            "\n".join(
                [
                    "# TP翻译任务排队展示与取消能力 PRD",
                    "",
                    "## 0. 文档信息",
                    "",
                    "| 项 | 内容 |",
                    "|---|---|",
                    "| 关联 mock | [tp-translation-queue-cancel-mock.html](x-app-intellistyle/docs/PRD/tp-translation-queue-cancel-mock.html) |",
                    "",
                    "## 1. 功能目标",
                    "",
                    "正文。",
                    "",
                    "## 4.2 选择文件后的输入框状态",
                    "",
                    "截图占位：[tp-translation-queue-cancel-mock.html](x-app-intellistyle/docs/PRD/tp-translation-queue-cancel-mock.html)",
                    "",
                    "## 9. 关联产物",
                    "",
                    "- 静态 mock：[tp-translation-queue-cancel-mock.html](x-app-intellistyle/docs/PRD/tp-translation-queue-cancel-mock.html)",
                    "",
                    "## 10. 待确认事项",
                    "",
                    "- 是否还需要保留本地 mock 链接。",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        return prd, html

    def run_script(self, *args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=str(cwd),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def test_dry_run_dedupes_and_prefers_semantic_section(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prd, html = self.make_fixture(root)

            result = self.run_script(str(prd), "--dry-run", "--json", cwd=root)

            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(len(report["targets"]), 1)
            target = report["targets"][0]
            self.assertEqual(Path(target["resolved_path"]).resolve(), html.resolve())
            self.assertEqual(target["placement"]["section"], "4.2 选择文件后的输入框状态")
            self.assertTrue(target["url"].startswith("file://"))

    def test_placeholder_capture_writes_enriched_copy_without_touching_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prd, _html = self.make_fixture(root)
            original = prd.read_text(encoding="utf-8")
            output = root / "TP翻译-PRD.enriched.md"
            asset_dir = root / "assets"

            result = self.run_script(
                str(prd),
                "--capture-mode",
                "placeholder",
                "--output",
                str(output),
                "--asset-dir",
                str(asset_dir),
                "--json",
                cwd=root,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertTrue(output.exists())
            self.assertTrue(Path(report["targets"][0]["screenshot_path"]).exists())
            self.assertEqual(prd.read_text(encoding="utf-8"), original)

            enriched = output.read_text(encoding="utf-8")
            marker = "<!-- dingtalk-prd-screenshot:"
            self.assertIn(marker, enriched)
            self.assertIn("![tp-translation-queue-cancel-mock.html screenshot]", enriched)
            self.assertLess(enriched.index("## 4.2 选择文件后的输入框状态"), enriched.index(marker))
            self.assertNotIn("关联 mock", enriched)
            self.assertNotIn("## 9. 关联产物", enriched)
            self.assertNotIn("## 10. 待确认事项", enriched)
            self.assertEqual(report["publish_cleanup"]["removed_table_rows"], 1)
            self.assertIn("9. 关联产物", report["publish_cleanup"]["removed_sections"])
            self.assertIn("10. 待确认事项", report["publish_cleanup"]["removed_sections"])


if __name__ == "__main__":
    unittest.main()
