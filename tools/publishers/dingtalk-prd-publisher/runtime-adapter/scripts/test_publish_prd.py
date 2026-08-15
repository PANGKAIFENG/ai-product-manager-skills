#!/usr/bin/env python3
"""Regression tests for publish-prd target resolution."""

from __future__ import annotations

import json
import hashlib
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

import yaml


SCRIPT = Path(__file__).with_name("publish-prd")
PRODUCT_DELIVERY_VALIDATOR = os.environ.get("PRODUCT_DELIVERY_VALIDATOR")


class PublishPrdTest(unittest.TestCase):
    def make_fake_dws(self, temp_root: Path, *, log_name: str = "dws-calls.jsonl") -> tuple[Path, Path]:
        bin_dir = temp_root / "bin"
        bin_dir.mkdir(exist_ok=True)
        log = temp_root / log_name
        dws = bin_dir / "dws"
        dws.write_text(
            textwrap.dedent(
                """\
                #!/usr/bin/env python3
                import json
                import os
                import sys

                args = sys.argv[1:]
                with open(os.environ["DWS_FAKE_LOG"], "a", encoding="utf-8") as handle:
                    handle.write(json.dumps(args, ensure_ascii=False) + "\\n")

                if args[:2] == ["auth", "status"]:
                    print(json.dumps({"authenticated": True}))
                elif args[:2] == ["doc", "info"]:
                    selected_node = args[args.index("--node") + 1]
                    if os.environ.get("DWS_FAKE_FAIL_PARENT_INFO") == "1" and selected_node == "broken-parent":
                        print(json.dumps({"success": False, "error": "parent lookup failed"}), file=sys.stderr)
                        sys.exit(75)
                    if selected_node == "uploaded-file":
                        print(json.dumps({
                            "success": True,
                            "contentType": "DOCUMENT",
                            "extension": "md",
                            "nodeType": "file",
                            "nodeId": "uploaded-file",
                            "name": "Package PRD",
                            "docUrl": "https://alidocs.dingtalk.com/i/nodes/uploaded-file",
                        }))
                        sys.exit(0)
                    print("warning: noisy prefix before JSON")
                    print(json.dumps({
                        "success": True,
                        "contentType": "ALIDOC",
                        "extension": "adoc",
                        "nodeType": "file",
                        "nodeId": "anchor-node",
                        "folderId": "containing-folder",
                        "workspaceId": "workspace-1",
                    }))
                elif args[:3] == ["doc", "folder", "create"]:
                    print(json.dumps({
                        "success": True,
                        "nodeId": "created-folder",
                        "docUrl": "https://alidocs.dingtalk.com/i/nodes/created-folder",
                    }))
                elif args[:2] == ["doc", "create"]:
                    if os.environ.get("DWS_FAKE_CREATE_NONZERO_WITH_NODE") == "1":
                        print(json.dumps({
                            "success": False,
                            "nodeId": "created-doc",
                            "docUrl": "https://alidocs.dingtalk.com/i/nodes/created-doc",
                        }))
                        sys.exit(74)
                    print(json.dumps({
                        "success": True,
                        "nodeId": "created-doc",
                        "docUrl": "https://alidocs.dingtalk.com/i/nodes/created-doc",
                    }))
                elif args[:2] == ["doc", "read"]:
                    if os.environ.get("DWS_FAKE_WRONG_READBACK") == "1":
                        print(json.dumps({
                            "success": True,
                            "nodeId": "created-doc",
                            "title": "Wrong package",
                            "markdown": "# Unrelated document\\n",
                        }))
                    else:
                        print(json.dumps({
                            "success": True,
                            "nodeId": "created-doc",
                            "title": os.environ.get("DWS_FAKE_READBACK_TITLE", "Package PRD"),
                            "markdown": os.environ.get(
                                "DWS_FAKE_READBACK_MARKDOWN",
                                "# Package PRD\\n\\n## 版本记录\\n\\n| 版本 | 日期 | 修改内容 |\\n| --- | --- | --- |\\n| V1.0 | 2026-08-15 | 首次创建 |\\n\\n## Default\\nBody.\\n",
                            ),
                        }))
                elif args[:3] == ["doc", "media", "insert"]:
                    fail_name = os.environ.get("DWS_FAKE_FAIL_MEDIA_ONCE")
                    fail_state = os.environ.get("DWS_FAKE_FAIL_STATE")
                    selected = args[args.index("--file") + 1] if "--file" in args else ""
                    if fail_name and os.path.basename(selected) == fail_name and fail_state and not os.path.exists(fail_state):
                        open(fail_state, "w", encoding="utf-8").write("failed once\\n")
                        print(json.dumps({"success": False, "error": "fake media failure"}), file=sys.stderr)
                        sys.exit(73)
                    print(json.dumps({
                        "success": True,
                        "blockType": "file",
                        "index": 0,
                    }))
                elif args[:2] == ["drive", "upload"]:
                    print(json.dumps({
                        "success": True,
                        "nodeId": "uploaded-file",
                        "docUrl": "https://alidocs.dingtalk.com/i/nodes/uploaded-file",
                    }))
                else:
                    print(json.dumps({"success": False, "args": args}), file=sys.stderr)
                    sys.exit(64)
                """
            ),
            encoding="utf-8",
        )
        dws.chmod(0o755)
        return bin_dir, log

    def run_publish(
        self,
        temp_root: Path,
        *args: str,
        log_name: str = "dws-calls.jsonl",
        default_parent: str | None = "https://alidocs.dingtalk.com/i/nodes/default-parent",
        html_files: list[tuple[str, int]] | None = None,
        prd_content: str | None = None,
        fake_env: dict[str, str] | None = None,
    ) -> tuple[subprocess.CompletedProcess[str], list[list[str]]]:
        bin_dir, log = self.make_fake_dws(temp_root, log_name=log_name)
        prd = temp_root / "PRD.md"
        prd.write_text(
            prd_content
            or "# My PRD\n\n## 版本记录\n\n| 版本 | 日期 | 修改内容 |\n| --- | --- | --- |\n| V1.0 | 2026-08-15 | 首次创建 |\n\nBody.\n",
            encoding="utf-8",
        )
        for relative_path, modified_at in html_files or []:
            html = temp_root / relative_path
            html.parent.mkdir(parents=True, exist_ok=True)
            html.write_text(f"<html><body>{relative_path}</body></html>\n", encoding="utf-8")
            os.utime(html, (modified_at, modified_at))
        env = os.environ.copy()
        env["PATH"] = f"{bin_dir}{os.pathsep}{env['PATH']}"
        env["DWS_FAKE_LOG"] = str(log)
        if default_parent is not None:
            env["DINGTALK_PRD_DEFAULT_PARENT"] = default_parent
        else:
            env.pop("DINGTALK_PRD_DEFAULT_PARENT", None)
        env["DINGTALK_PRD_TIMESTAMP"] = "20260702-1700"
        env["DWS_FAKE_READBACK_TITLE"] = "My PRD"
        env["DWS_FAKE_READBACK_MARKDOWN"] = prd.read_text(encoding="utf-8")
        env.update(fake_env or {})
        result = subprocess.run(
            ["/bin/bash", str(SCRIPT), str(prd), "--name", "My PRD", *args],
            cwd=str(temp_root),
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        calls = []
        if log.exists():
            calls = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]
        return result, calls

    def artifact(self, temp_root: Path, relative: str, content: bytes, artifact_id: str, **extra) -> dict:
        path = temp_root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return {
            "artifact_id": artifact_id,
            "path": relative,
            "sha256": hashlib.sha256(content).hexdigest(),
            **extra,
        }

    def make_approved_package(self, temp_root: Path) -> tuple[Path, str]:
        if PRODUCT_DELIVERY_VALIDATOR is None:
            self.skipTest("set PRODUCT_DELIVERY_VALIDATOR to run Package mode integration tests")
        prd = self.artifact(
            temp_root,
            "PRD.md",
            (
                "# Package PRD\n\n"
                "## 版本记录\n\n"
                "| 版本 | 日期 | 修改内容 |\n"
                "| --- | --- | --- |\n"
                "| V1.0 | 2026-08-15 | 首次创建 |\n\n"
                "## Default\nBody.\n\n"
                "![Default](ui/screenshots/default.png)\n"
            ).encode("utf-8"),
            "ART-PRD",
            producer_identity="run-maker",
        )
        action = self.artifact(
            temp_root,
            "ui/screen-contract.md",
            b"# Action Contract\n",
            "ART-ACTION",
            producer_identity="run-ui",
        )
        html = self.artifact(
            temp_root,
            "ui/approved.html",
            b"<html><body>approved</body></html>\n",
            "ART-HTML",
            producer_identity="run-ui",
            baseline_ref="BASE-1",
        )
        shot = self.artifact(
            temp_root,
            "ui/screenshots/default.png",
            b"fake-approved-screenshot",
            "ART-SHOT",
            producer_identity="run-ui",
            source_html_ref="ART-HTML",
            source_html_sha256=html["sha256"],
            state="default",
            viewport="1440x900",
        )
        manifest = {
            "schema_version": 1,
            "work_item_id": "WI-PUBLISHER-TEST",
            "title": "Package PRD",
            "revision": 1,
            "package_status": "review_pending",
            "current_stage": "review",
            "ui_requirement": {
                "required": True,
                "reason": "user_visible_surface",
                "decided_by": "run-maker",
            },
            "sources": [],
            "decisions": [],
            "artifacts": {
                "prd": prd,
                "action_contract": action,
                "html": [html],
                "screenshots": [shot],
            },
            "ui_baselines": [
                {
                    "baseline_id": "BASE-1",
                    "kind": "frontend-repo",
                    "source": "verified-test-project",
                    "revision": "abc123",
                }
            ],
            "anchors": [
                {
                    "anchor_id": "ANCHOR-DEFAULT",
                    "prd_artifact_ref": "ART-PRD",
                    "heading_path": "Default",
                    "content_sha256": hashlib.sha256(
                        b"Body.\n\n![Default](ui/screenshots/default.png)"
                    ).hexdigest(),
                    "screenshot_ref": "ART-SHOT",
                    "state_refs": ["default"],
                }
            ],
            "validations": [],
            "pre_split_review": None,
            "review": None,
            "approvals": {"publish": None},
            "release": {
                "dingtalk": {
                    "mode": "doc",
                    "title": "Package PRD",
                    "target": {"selector": "folder", "value": "package-folder"},
                    "content_artifact_ref": "ART-PRD",
                    "html_artifact_refs": ["ART-HTML"],
                    "screenshot_artifact_refs": ["ART-SHOT"],
                    "payload_fingerprint": None,
                    "status": "pending",
                    "node_id": None,
                    "doc_url": None,
                    "completed_artifact_refs": [],
                    "readback": None,
                    "browser_visibility": None,
                    "attempts": [],
                }
            },
            "last_transition": None,
            "extensions": {},
        }
        manifest_path = temp_root / "product-delivery-manifest.yaml"
        manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
        initial = subprocess.run(
            [sys.executable, PRODUCT_DELIVERY_VALIDATOR, str(manifest_path), "--json"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(initial.returncode, 0, initial.stderr + initial.stdout)
        derived = json.loads(initial.stdout)
        input_fingerprint = derived["package_input_fingerprint"]
        payload_fingerprint = derived["publish_payload_fingerprint"]
        manifest["package_input_fingerprint"] = input_fingerprint
        manifest["review"] = {
            "review_id": "REVIEW-1",
            "reviewer_identity": "run-reviewer",
            "maker_identities": ["run-maker", "run-ui"],
            "input_fingerprint": input_fingerprint,
            "verdict": "ready",
            "checks": {"content": "passed", "artifacts": "passed", "publish": "passed"},
            "findings": [],
        }
        manifest["release"]["dingtalk"]["payload_fingerprint"] = payload_fingerprint
        manifest["approvals"]["publish"] = {
            "approver_identity": "human:owner",
            "payload_fingerprint": payload_fingerprint,
            "approved_at": "2026-08-06T12:00:00+08:00",
        }
        manifest["package_status"] = "publish_approved"
        manifest["current_stage"] = "publish"
        manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
        return manifest_path, payload_fingerprint

    def run_manifest_publish(
        self,
        temp_root: Path,
        manifest: Path,
        payload_fingerprint: str,
        *args: str,
        attempt_id: str = "attempt-1",
        fail_media_once: str | None = None,
        fake_env: dict[str, str] | None = None,
    ) -> tuple[subprocess.CompletedProcess[str], list[list[str]]]:
        if PRODUCT_DELIVERY_VALIDATOR is None:
            self.skipTest("set PRODUCT_DELIVERY_VALIDATOR to run Package mode integration tests")
        bin_dir, log = self.make_fake_dws(temp_root, log_name="package-dws-calls.jsonl")
        env = os.environ.copy()
        env["PATH"] = f"{bin_dir}{os.pathsep}{env['PATH']}"
        env["DWS_FAKE_LOG"] = str(log)
        env["DINGTALK_PRD_ATTEMPT_ID"] = attempt_id
        env["DINGTALK_PRD_OCCURRED_AT"] = "2026-08-06T12:01:00+08:00"
        if fail_media_once:
            env["DWS_FAKE_FAIL_MEDIA_ONCE"] = fail_media_once
            env["DWS_FAKE_FAIL_STATE"] = str(temp_root / ".fake-media-failed")
        env.update(fake_env or {})
        result = subprocess.run(
            [
                "/bin/bash",
                str(SCRIPT),
                "--manifest",
                str(manifest),
                "--validator",
                PRODUCT_DELIVERY_VALIDATOR,
                "--expected-payload-fingerprint",
                payload_fingerprint,
                "--actor-identity",
                "run-publisher",
                *args,
            ],
            cwd=str(temp_root),
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        calls = []
        if log.exists():
            calls = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]
        return result, calls

    def test_default_alidoc_parent_publishes_direct_child_document(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result, calls = self.run_publish(Path(tmp), "--read-back")

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertIn(["doc", "info", "--node", "https://alidocs.dingtalk.com/i/nodes/default-parent", "--format", "json"], calls)
            self.assertFalse(any(call[:3] == ["wiki", "node", "create"] for call in calls))
            self.assertFalse(any(call[:3] == ["doc", "folder", "create"] for call in calls))

            create_call = next(call for call in calls if call[:2] == ["doc", "create"])
            self.assertIn("--folder", create_call)
            self.assertEqual(create_call[create_call.index("--folder") + 1], "anchor-node")
            self.assertIn(
                ["doc", "read", "--node", "created-doc", "--content-format", "markdown", "--format", "json"],
                calls,
            )

    def test_missing_version_history_fails_before_any_dws_call(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result, calls = self.run_publish(Path(tmp), prd_content="# My PRD\n\nBody.\n")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing_version_history", result.stderr)
            self.assertEqual(calls, [])

    def test_readback_rejects_mismatched_latest_version_row(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            remote = "# My PRD\n\n## 版本记录\n\n| 版本 | 日期 | 修改内容 |\n| --- | --- | --- |\n| V1.1 | 2026-08-15 | 不一致的修改 |\n| V1.0 | 2026-08-01 | 首次创建 |\n\nBody.\n"
            result, calls = self.run_publish(
                Path(tmp),
                "--read-back",
                fake_env={"DWS_FAKE_READBACK_MARKDOWN": remote},
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("latest version row does not match source", result.stderr)
            self.assertTrue(any(call[:2] == ["doc", "read"] for call in calls))

    def test_builtin_default_parent_is_agent_requirements_anchor(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result, calls = self.run_publish(
                Path(tmp),
                log_name="dws-calls-default-anchor.jsonl",
                default_parent=None,
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertIn(
                [
                    "doc",
                    "info",
                    "--node",
                    "https://alidocs.dingtalk.com/i/nodes/MNDoBb60VLrdedxLSrZmae9N8lemrZQ3?utm_scene=team_space",
                    "--format",
                    "json",
                ],
                calls,
            )

    def test_explicit_folder_publishes_directly_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result, calls = self.run_publish(Path(tmp), "--folder", "existing-folder", log_name="dws-calls-2.jsonl")

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertFalse(any(call[:3] == ["doc", "folder", "create"] for call in calls))
            create_call = next(call for call in calls if call[:2] == ["doc", "create"])
            self.assertIn("--folder", create_call)
            self.assertEqual(create_call[create_call.index("--folder") + 1], "existing-folder")

    def test_explicit_folder_can_create_child_with_doc_folder_api(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result, calls = self.run_publish(
                Path(tmp),
                "--folder",
                "existing-folder",
                "--create-run-folder",
                log_name="dws-calls-3.jsonl",
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertFalse(any(call[:3] == ["wiki", "node", "create"] for call in calls))
            folder_call = next(call for call in calls if call[:3] == ["doc", "folder", "create"])
            self.assertEqual(folder_call[folder_call.index("--folder") + 1], "existing-folder")

            create_call = next(call for call in calls if call[:2] == ["doc", "create"])
            self.assertEqual(create_call[create_call.index("--folder") + 1], "created-folder")

    def test_doc_mode_attaches_newest_sibling_html_at_first_block(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result, calls = self.run_publish(
                Path(tmp),
                "--read-back",
                html_files=[("older.html", 100), ("mockup.html", 200)],
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            media_calls = [call for call in calls if call[:3] == ["doc", "media", "insert"]]
            self.assertEqual(1, len(media_calls), calls)
            media_call = media_calls[0]
            self.assertEqual(
                (Path(tmp) / "mockup.html").resolve(),
                Path(media_call[media_call.index("--file") + 1]).resolve(),
            )
            self.assertEqual("0", media_call[media_call.index("--index") + 1])
            self.assertLess(calls.index(media_call), next(i for i, call in enumerate(calls) if call[:2] == ["doc", "read"]))

    def test_doc_mode_discovers_newest_htm_sibling(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result, calls = self.run_publish(
                Path(tmp),
                html_files=[("older.html", 100), ("latest.htm", 200)],
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            media_call = next(call for call in calls if call[:3] == ["doc", "media", "insert"])
            self.assertEqual(
                (Path(tmp) / "latest.htm").resolve(),
                Path(media_call[media_call.index("--file") + 1]).resolve(),
            )

    def test_doc_mode_without_html_candidate_skips_media_insert(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result, calls = self.run_publish(Path(tmp))

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertFalse(any(call[:3] == ["doc", "media", "insert"] for call in calls))
            self.assertNotIn("HTML attachment selected:", result.stderr)

    def test_dry_run_reports_html_without_media_write(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result, calls = self.run_publish(
                Path(tmp),
                "--dry-run",
                html_files=[("mockup.html", 200)],
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertIn("Dry run: would attach HTML at document index 0", result.stdout)
            self.assertFalse(any(call[:3] == ["doc", "media", "insert"] for call in calls))

    def test_explicit_html_wins_over_newer_sibling(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            explicit = root / "artifacts" / "approved.html"
            result, calls = self.run_publish(
                root,
                "--html",
                str(explicit),
                html_files=[("artifacts/approved.html", 100), ("unrelated-newer.html", 300)],
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            media_call = next(call for call in calls if call[:3] == ["doc", "media", "insert"])
            self.assertEqual(explicit.resolve(), Path(media_call[media_call.index("--file") + 1]).resolve())

    def test_no_html_disables_automatic_attachment(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result, calls = self.run_publish(
                Path(tmp),
                "--no-html",
                html_files=[("mockup.html", 200)],
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertFalse(any(call[:3] == ["doc", "media", "insert"] for call in calls))

    def test_missing_explicit_html_fails_before_document_creation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result, calls = self.run_publish(Path(tmp), "--html", str(Path(tmp) / "missing.html"))

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("HTML file not found", result.stderr)
            self.assertFalse(any(call[:2] == ["doc", "create"] for call in calls))

    def test_file_mode_does_not_insert_html_into_a_document(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result, calls = self.run_publish(
                Path(tmp),
                "--mode",
                "file",
                "--folder",
                "archive-folder",
                html_files=[("mockup.html", 200)],
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertFalse(any(call[:3] == ["doc", "media", "insert"] for call in calls))

    def test_eval_b2_05_invalid_approval_or_payload_makes_zero_dws_calls(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest_path, payload = self.make_approved_package(root)
            manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
            manifest["approvals"]["publish"]["payload_fingerprint"] = "0" * 64
            manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
            before = manifest_path.read_bytes()

            result, calls = self.run_manifest_publish(root, manifest_path, payload)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("before any DingTalk call", result.stderr)
            self.assertEqual(calls, [])
            self.assertEqual(manifest_path.read_bytes(), before)

    def test_eval_b2_06_package_real_publish_requires_host_approval_capability(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest_path, payload = self.make_approved_package(root)
            before = manifest_path.read_bytes()

            result, calls = self.run_manifest_publish(root, manifest_path, payload)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("authorization_required", result.stderr)
            self.assertEqual(calls, [])
            self.assertEqual(manifest_path.read_bytes(), before)

    def test_eval_b2_07_package_dry_run_validates_without_side_effects(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest_path, payload = self.make_approved_package(root)
            before = manifest_path.read_bytes()

            result, calls = self.run_manifest_publish(
                root,
                manifest_path,
                payload,
                "--dry-run",
            )

            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertIn("Package mode validated", result.stdout)
            self.assertIn("DingTalk call count is 0", result.stdout)
            self.assertEqual(calls, [])
            self.assertEqual(manifest_path.read_bytes(), before)

    def test_package_file_mode_with_media_refs_fails_before_dws_calls(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest_path, payload = self.make_approved_package(root)
            manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
            manifest["release"]["dingtalk"]["mode"] = "file"
            manifest_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")

            result, calls = self.run_manifest_publish(root, manifest_path, payload)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("file mode cannot publish HTML or screenshot", result.stderr)
            self.assertEqual(calls, [])

    def test_eval_b2_08_traversal_and_cli_override_fail_without_side_effects(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest_path, payload = self.make_approved_package(root)
            original = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))

            override, override_calls = self.run_manifest_publish(
                root, manifest_path, payload, "--folder", "not-allowlisted"
            )
            self.assertNotEqual(override.returncode, 0)
            self.assertEqual(override_calls, [])
            self.assertEqual(yaml.safe_load(manifest_path.read_text(encoding="utf-8")), original)

            escaped = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
            escaped["artifacts"]["prd"]["path"] = "../outside.md"
            manifest_path.write_text(yaml.safe_dump(escaped, sort_keys=False), encoding="utf-8")
            traversal, traversal_calls = self.run_manifest_publish(root, manifest_path, payload)
            self.assertNotEqual(traversal.returncode, 0)
            self.assertEqual(traversal_calls, [])
            after = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(after["review"], escaped["review"])
            self.assertEqual(after["approvals"], escaped["approvals"])

if __name__ == "__main__":
    unittest.main()
