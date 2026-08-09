from __future__ import annotations

import importlib.util
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_product_delivery_manifest.py"
SPEC = importlib.util.spec_from_file_location("validate_product_delivery_manifest", MODULE_PATH)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


class ProductDeliveryManifestTest(unittest.TestCase):
    def write_artifact(self, root: Path, relative: str, content: bytes) -> dict[str, str]:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return {"path": relative, "sha256": validator.file_sha256(path)}

    def base_manifest(self, root: Path, *, ui_required: bool = True) -> dict:
        prd = self.write_artifact(
            root,
            "PRD.md",
            b"# PRD\n\n## Default state\nReady.\n\n![Default state](ui/screenshots/default.png)\n",
        )
        artifacts: dict = {
            "prd": {
                "artifact_id": "ART-PRD",
                "producer_identity": "run-maker",
                **prd,
            },
        }
        baselines: list[dict] = []
        anchors: list[dict] = []
        if ui_required:
            contract = self.write_artifact(root, "ui/screen-contract.md", b"# Screen Contract\n")
            html = self.write_artifact(root, "ui/mockup.html", b"<html>default</html>\n")
            screenshot = self.write_artifact(root, "ui/screenshots/default.png", b"fake-png-default")
            artifacts.update(
                {
                    "action_contract": {
                        "artifact_id": "ART-ACTION",
                        "producer_identity": "run-ui",
                        **contract,
                    },
                    "html": [
                        {
                            "artifact_id": "ART-HTML",
                            "producer_identity": "run-ui",
                            **html,
                            "baseline_ref": "BASE-1",
                        }
                    ],
                    "screenshots": [
                        {
                            "artifact_id": "ART-SHOT",
                            "producer_identity": "run-ui",
                            **screenshot,
                            "source_html_ref": "ART-HTML",
                            "source_html_sha256": html["sha256"],
                            "state": "default",
                            "viewport": "1440x900",
                        }
                    ],
                }
            )
            baselines = [
                {
                    "baseline_id": "BASE-1",
                    "kind": "frontend-repo",
                    "source": "verified-project-reference",
                    "revision": "abc123",
                }
            ]
            anchors = [
                {
                    "anchor_id": "ANCHOR-DEFAULT",
                    "prd_artifact_ref": "ART-PRD",
                    "heading_path": "Default state",
                    "content_sha256": hashlib.sha256(
                        b"Ready.\n\n![Default state](ui/screenshots/default.png)"
                    ).hexdigest(),
                    "screenshot_ref": "ART-SHOT",
                    "state_refs": ["default"],
                }
            ]

        html_refs = ["ART-HTML"] if ui_required else []
        screenshot_refs = ["ART-SHOT"] if ui_required else []
        return {
            "schema_version": 1,
            "work_item_id": "WI-TEST",
            "title": "Test Package",
            "revision": 1,
            "package_status": "review_pending",
            "current_stage": "review",
            "ui_requirement": {
                "required": ui_required,
                "reason": "user_visible_surface" if ui_required else "no_user_visible_surface",
                "decided_by": "run-maker",
            },
            "sources": [],
            "decisions": [],
            "artifacts": artifacts,
            "ui_baselines": baselines,
            "anchors": anchors,
            "validations": [],
            "pre_split_review": None,
            "review": None,
            "approvals": {"publish": None},
            "release": {
                "dingtalk": {
                    "mode": "doc",
                    "title": "Test Package",
                    "target": {"selector": "folder", "value": "fake-folder"},
                    "content_artifact_ref": "ART-PRD",
                    "html_artifact_refs": html_refs,
                    "screenshot_artifact_refs": screenshot_refs,
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

    def add_pre_split_review(self, root: Path, manifest: dict) -> None:
        initial = validator.validate_manifest(manifest, root)
        self.assertTrue(initial.valid, initial.errors)
        manifest["pre_split_review"] = {
            "review_id": "REVIEW-PRE-SPLIT",
            "reviewer_identity": "run-pre-split-reviewer",
            "maker_identities": ["run-maker", "run-ui"]
            if manifest["ui_requirement"]["required"]
            else ["run-maker"],
            "input_fingerprint": initial.pre_split_input_fingerprint,
            "verdict": "ready",
            "checks": {
                "content": "passed",
                "artifacts": "passed",
                "publish": "passed",
            },
            "findings": [],
        }
        reviewed = validator.validate_manifest(manifest, root)
        self.assertTrue(reviewed.valid, reviewed.errors)

    def make_approved(self, root: Path, *, ui_required: bool = True) -> dict:
        manifest = self.base_manifest(root, ui_required=ui_required)
        initial = validator.validate_manifest(manifest, root)
        self.assertTrue(initial.valid, initial.errors)
        manifest["package_input_fingerprint"] = initial.package_input_fingerprint
        manifest["review"] = {
            "review_id": "REVIEW-1",
            "reviewer_identity": "run-reviewer",
            "maker_identities": ["run-maker", "run-ui"] if ui_required else ["run-maker"],
            "input_fingerprint": initial.package_input_fingerprint,
            "verdict": "ready",
            "checks": {"content": "passed", "artifacts": "passed", "publish": "passed"},
            "findings": [],
        }
        reviewed = validator.validate_manifest(manifest, root)
        self.assertTrue(reviewed.valid, reviewed.errors)
        manifest["release"]["dingtalk"]["payload_fingerprint"] = reviewed.publish_payload_fingerprint
        manifest["approvals"]["publish"] = {
            "approver_identity": "human:owner",
            "payload_fingerprint": reviewed.publish_payload_fingerprint,
            "approved_at": "2026-08-06T12:00:00+08:00",
        }
        manifest["package_status"] = "publish_approved"
        manifest["current_stage"] = "publish"
        approved = validator.validate_manifest(manifest, root)
        self.assertTrue(approved.valid, approved.errors)
        self.assertEqual(approved.derived_status, "publish_approved")
        return manifest

    def add_delivery_plan_artifacts(
        self, root: Path, manifest: dict, *, producer_identity: str = "run-backlog"
    ) -> None:
        version_plan = self.write_artifact(
            root, "delivery/version-plan.md", b"# Version plan\n\nV1 first.\n"
        )
        issue_drafts = self.write_artifact(
            root, "delivery/issues.md", b"# Issues\n\n- Slice 1\n"
        )
        coverage = self.write_artifact(
            root,
            "delivery/prd-issue-coverage.md",
            b"# Coverage\n\nPRD section -> Slice 1\n",
        )
        manifest["artifacts"].update(
            {
                "version_plan": {
                    "artifact_id": "ART-VERSION-PLAN",
                    "producer_identity": producer_identity,
                    **version_plan,
                },
                "issue_drafts": [
                    {
                        "artifact_id": "ART-ISSUES",
                        "producer_identity": producer_identity,
                        **issue_drafts,
                    }
                ],
                "coverage_matrix": {
                    "artifact_id": "ART-COVERAGE",
                    "producer_identity": producer_identity,
                    **coverage,
                },
            }
        )

    def save_manifest(self, root: Path, manifest: dict) -> Path:
        path = root / "product-delivery-manifest.yaml"
        path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
        return path

    def event_args(self, event: str, payload: str, **overrides):
        values = {
            "record_publish_event": event,
            "expected_payload_fingerprint": payload,
            "attempt_id": "attempt-1",
            "occurred_at": "2026-08-06T12:01:00+08:00",
            "actor_role": "publisher",
            "actor_identity": "run-publisher",
            "node_id": None,
            "doc_url": None,
            "artifact_ref": None,
            "failed_step": None,
            "error_summary": None,
            "readback_node_id": None,
            "readback_title": None,
            "readback_content_sha256": None,
            "browser_evidence": None,
        }
        values.update(overrides)
        return type("Args", (), values)()

    def test_eval_b2_01_complete_page_package_reaches_review_pending_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self.base_manifest(root)

            result = validator.validate_manifest(manifest, root)

            self.assertTrue(result.valid, result.errors)
            self.assertEqual(result.derived_status, "review_pending")
            self.assertEqual(result.earliest_recovery_node, "review")
            self.assertIsNotNone(result.package_input_fingerprint)

    def test_eval_b2_02_page_evidence_is_required_but_real_no_ui_exemption_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = self.base_manifest(root)
            del page["artifacts"]["html"]
            invalid = validator.validate_manifest(page, root)
            self.assertFalse(invalid.valid)
            self.assertTrue(any("missing required artifact group html" in item for item in invalid.errors))

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            no_ui = validator.validate_manifest(self.base_manifest(root, ui_required=False), root)
            self.assertTrue(no_ui.valid, no_ui.errors)

    def test_no_ui_package_still_requires_prd_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self.base_manifest(root, ui_required=False)
            del manifest["artifacts"]["prd"]

            result = validator.validate_manifest(manifest, root)

            self.assertFalse(result.valid)
            self.assertTrue(any("requires a valid PRD artifact" in item for item in result.errors))

    def test_eval_b2_03_content_changes_invalidate_hash_review_and_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self.make_approved(root)
            old_input = manifest["package_input_fingerprint"]
            old_payload = manifest["release"]["dingtalk"]["payload_fingerprint"]
            (root / "PRD.md").write_text("# PRD\n\nChanged.\n", encoding="utf-8")

            result = validator.validate_manifest(manifest, root)

            self.assertFalse(result.valid)
            self.assertNotEqual(result.package_input_fingerprint, old_input)
            self.assertNotEqual(result.publish_payload_fingerprint, old_payload)
            self.assertTrue(any("content mismatch" in item for item in result.errors))
            self.assertTrue(any("stale or incorrect" in item for item in result.errors))

    def test_stale_approval_preserves_package_readiness(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self.make_approved(root)
            manifest["approvals"]["publish"]["payload_fingerprint"] = "0" * 64

            result = validator.validate_manifest(manifest, root)

            self.assertTrue(result.valid, result.errors)
            self.assertEqual(result.derived_status, "package_ready")
            self.assertEqual(result.earliest_recovery_node, "approval")
            self.assertTrue(
                any("approval ignored" in item for item in result.warnings),
                result.warnings,
            )

    def test_delivery_plan_changes_invalidate_independent_review(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self.base_manifest(root, ui_required=False)
            self.add_pre_split_review(root, manifest)
            self.add_delivery_plan_artifacts(root, manifest)
            current = validator.validate_manifest(manifest, root)
            self.assertTrue(current.valid, current.errors)
            manifest["package_input_fingerprint"] = current.package_input_fingerprint
            manifest["review"] = {
                "review_id": "REVIEW-PLAN",
                "reviewer_identity": "run-reviewer",
                "maker_identities": ["run-maker", "run-backlog"],
                "input_fingerprint": current.package_input_fingerprint,
                "verdict": "ready",
                "checks": {
                    "content": "passed",
                    "artifacts": "passed",
                    "publish": "passed",
                },
                "findings": [],
            }
            reviewed = validator.validate_manifest(manifest, root)
            self.assertTrue(reviewed.valid, reviewed.errors)
            self.assertEqual(reviewed.derived_status, "package_ready")

            (root / "delivery" / "issues.md").write_text(
                "# Issues\n\n- Changed after Review\n", encoding="utf-8"
            )
            changed = validator.validate_manifest(manifest, root)

            self.assertFalse(changed.valid)
            self.assertNotEqual(
                changed.package_input_fingerprint, current.package_input_fingerprint
            )
            self.assertTrue(
                any("review.input_fingerprint: stale" in item for item in changed.errors),
                changed.errors,
            )

    def test_planning_artifacts_require_current_pre_split_review(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            previous = self.base_manifest(root, ui_required=False)
            current = json.loads(json.dumps(previous))
            self.add_delivery_plan_artifacts(root, current)

            result = validator.validate_manifest(
                current,
                root,
                previous=previous,
                actor_role="backlog_splitter",
                actor_identity="run-backlog",
            )

            self.assertFalse(result.valid)
            self.assertTrue(
                any("pre_split_review" in item and "required" in item for item in result.errors),
                result.errors,
            )

    def test_reviewer_cannot_retroactively_authorize_existing_planning_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            previous = self.base_manifest(root, ui_required=False)
            self.add_delivery_plan_artifacts(root, previous)
            fingerprint = validator.validate_manifest(
                previous, root
            ).pre_split_input_fingerprint
            current = json.loads(json.dumps(previous))
            current["pre_split_review"] = {
                "review_id": "REVIEW-RETROACTIVE",
                "reviewer_identity": "run-pre-split-reviewer",
                "maker_identities": ["run-maker"],
                "input_fingerprint": fingerprint,
                "verdict": "ready",
                "checks": {
                    "content": "passed",
                    "artifacts": "passed",
                    "publish": "passed",
                },
                "findings": [],
            }

            result = validator.validate_manifest(
                current,
                root,
                previous=previous,
                actor_role="reviewer",
                actor_identity="run-pre-split-reviewer",
            )

            self.assertFalse(result.valid)
            self.assertTrue(
                any("cannot be added or changed after planning artifacts exist" in item for item in result.errors),
                result.errors,
            )

    def test_reviewer_actor_identity_is_bound_to_review_record(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            previous = self.base_manifest(root, ui_required=False)
            initial = validator.validate_manifest(previous, root)
            current = json.loads(json.dumps(previous))
            current["review"] = {
                "review_id": "REVIEW-FORGED-ACTOR",
                "reviewer_identity": "run-independent-reviewer",
                "maker_identities": ["run-maker"],
                "input_fingerprint": initial.package_input_fingerprint,
                "verdict": "ready",
                "checks": {
                    "content": "passed",
                    "artifacts": "passed",
                    "publish": "passed",
                },
                "findings": [],
            }

            forged = validator.validate_manifest(
                current,
                root,
                previous=previous,
                actor_role="reviewer",
                actor_identity="run-maker",
            )
            legitimate = validator.validate_manifest(
                current,
                root,
                previous=previous,
                actor_role="reviewer",
                actor_identity="run-independent-reviewer",
            )

            self.assertFalse(forged.valid)
            self.assertTrue(
                any("review.reviewer_identity must match actor_identity" in item for item in forged.errors),
                forged.errors,
            )
            self.assertTrue(legitimate.valid, legitimate.errors)
            self.assertEqual(legitimate.derived_status, "package_ready")

    def test_approver_actor_identity_is_bound_and_must_be_human(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            previous = self.make_approved(root, ui_required=False)
            previous["approvals"]["publish"] = None
            previous["package_status"] = "package_ready"
            previous["current_stage"] = "approval"
            self.assertTrue(validator.validate_manifest(previous, root).valid)

            forged_label = json.loads(json.dumps(previous))
            forged_label["approvals"]["publish"] = {
                "approver_identity": "human:owner",
                "payload_fingerprint": previous["release"]["dingtalk"]["payload_fingerprint"],
                "approved_at": "2026-08-06T12:00:00+08:00",
            }
            mismatch = validator.validate_manifest(
                forged_label,
                root,
                previous=previous,
                actor_role="approver",
                actor_identity="run-maker",
            )
            legitimate = validator.validate_manifest(
                forged_label,
                root,
                previous=previous,
                actor_role="approver",
                actor_identity="human:owner",
            )

            nonhuman = json.loads(json.dumps(previous))
            nonhuman["approvals"]["publish"] = {
                "approver_identity": "run-maker",
                "payload_fingerprint": previous["release"]["dingtalk"]["payload_fingerprint"],
                "approved_at": "2026-08-06T12:00:00+08:00",
            }
            nonhuman_result = validator.validate_manifest(
                nonhuman,
                root,
                previous=previous,
                actor_role="approver",
                actor_identity="run-maker",
            )

            self.assertFalse(mismatch.valid)
            self.assertTrue(
                any("approver_identity must match actor_identity" in item for item in mismatch.errors),
                mismatch.errors,
            )
            self.assertTrue(legitimate.valid, legitimate.errors)
            self.assertEqual(legitimate.derived_status, "publish_approved")
            self.assertFalse(nonhuman_result.valid)
            self.assertTrue(
                any("must use human:<stable-label>" in item for item in nonhuman_result.errors),
                nonhuman_result.errors,
            )

    def test_eval_b2_04_reviewer_must_be_independent_and_all_checks_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self.base_manifest(root)
            current = validator.validate_manifest(manifest, root)
            manifest["package_input_fingerprint"] = current.package_input_fingerprint
            manifest["review"] = {
                "review_id": "REVIEW-SELF",
                "reviewer_identity": "run-maker",
                "maker_identities": ["run-maker"],
                "input_fingerprint": current.package_input_fingerprint,
                "verdict": "ready",
                "checks": {"content": "passed", "artifacts": "passed"},
                "findings": [],
            }

            result = validator.validate_manifest(manifest, root)

            self.assertFalse(result.valid)
            self.assertTrue(any("independent" in item for item in result.errors))
            self.assertTrue(any("exactly content, artifacts, and publish" in item for item in result.errors))
            self.assertNotEqual(result.derived_status, "package_ready")

    def test_anchor_hash_must_match_uniquely_resolved_prd_section(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self.base_manifest(root)
            manifest["anchors"][0]["content_sha256"] = "0" * 64

            mismatch = validator.validate_manifest(manifest, root)

            self.assertFalse(mismatch.valid)
            self.assertTrue(any("content_sha256" in item and "mismatch" in item for item in mismatch.errors))

            (root / "PRD.md").write_text(
                "# PRD\n\n## Default state\nReady.\n\n## Default state\nDuplicate.\n",
                encoding="utf-8",
            )
            manifest["artifacts"]["prd"]["sha256"] = validator.file_sha256(root / "PRD.md")
            ambiguous = validator.validate_manifest(manifest, root)
            self.assertFalse(ambiguous.valid)
            self.assertTrue(any("does not resolve uniquely" in item for item in ambiguous.errors))

    def test_review_cannot_omit_ui_decision_maker_identity(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self.base_manifest(root)
            current = validator.validate_manifest(manifest, root)
            manifest["package_input_fingerprint"] = current.package_input_fingerprint
            manifest["review"] = {
                "review_id": "REVIEW-FORGED",
                "reviewer_identity": "run-maker",
                "maker_identities": ["run-ui"],
                "input_fingerprint": current.package_input_fingerprint,
                "verdict": "ready",
                "checks": {"content": "passed", "artifacts": "passed", "publish": "passed"},
                "findings": [],
            }

            result = validator.validate_manifest(manifest, root)

            self.assertFalse(result.valid)
            self.assertTrue(any("must include ui_requirement.decided_by" in item for item in result.errors))
            self.assertTrue(any("independent" in item for item in result.errors))

    def test_ui_producer_identity_is_authoritative_for_review_independence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self.base_manifest(root)
            current = validator.validate_manifest(manifest, root)
            manifest["review"] = {
                "review_id": "REVIEW-UI-SELF",
                "reviewer_identity": "run-ui",
                "maker_identities": ["run-maker"],
                "input_fingerprint": current.package_input_fingerprint,
                "verdict": "ready",
                "checks": {
                    "content": "passed",
                    "artifacts": "passed",
                    "publish": "passed",
                },
                "findings": [],
            }

            result = validator.validate_manifest(manifest, root)

            self.assertFalse(result.valid)
            self.assertTrue(
                any("authoritative producer identities" in item for item in result.errors),
                result.errors,
            )
            self.assertTrue(any("independent" in item for item in result.errors), result.errors)

            previous = self.base_manifest(root)
            forged_ui = json.loads(json.dumps(previous))
            forged_ui["artifacts"]["html"][0]["producer_identity"] = "forged-ui"
            forged_ui_result = validator.validate_manifest(
                forged_ui,
                root,
                previous=previous,
                actor_role="ui_producer",
                actor_identity="run-ui",
            )
            self.assertTrue(
                any("actor_role.ui_producer" in item and "actor_identity" in item for item in forged_ui_result.errors),
                forged_ui_result.errors,
            )

            forged_maker = json.loads(json.dumps(previous))
            forged_maker["artifacts"]["prd"]["producer_identity"] = "forged-maker"
            forged_maker_result = validator.validate_manifest(
                forged_maker,
                root,
                previous=previous,
                actor_role="maker",
                actor_identity="run-maker",
            )
            self.assertTrue(
                any("actor_role.maker" in item and "actor_identity" in item for item in forged_maker_result.errors),
                forged_maker_result.errors,
            )

    def test_anchor_requires_screenshot_to_be_embedded_in_current_prd_section(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self.base_manifest(root)
            (root / "PRD.md").write_text("# PRD\n\n## Default state\nReady.\n", encoding="utf-8")
            manifest["artifacts"]["prd"]["sha256"] = validator.file_sha256(root / "PRD.md")
            manifest["anchors"][0]["content_sha256"] = hashlib.sha256(b"Ready.").hexdigest()

            result = validator.validate_manifest(manifest, root)

            self.assertFalse(result.valid)
            self.assertTrue(any("screenshot is not embedded" in item for item in result.errors))

    def test_file_mode_rejects_media_allowlist_that_publisher_would_drop(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self.base_manifest(root)
            manifest["release"]["dingtalk"]["mode"] = "file"

            result = validator.validate_manifest(manifest, root)

            self.assertFalse(result.valid)
            self.assertTrue(any("file mode cannot publish HTML or screenshot" in item for item in result.errors))

    def test_static_verified_claim_requires_complete_event_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self.make_approved(root)
            manifest["release"]["dingtalk"]["status"] = "published_unverified"

            empty_unverified = validator.validate_manifest(manifest, root)

            self.assertFalse(empty_unverified.valid)
            self.assertTrue(any("published_unverified evidence" in item for item in empty_unverified.errors))

            payload = manifest["release"]["dingtalk"]["payload_fingerprint"]
            release = manifest["release"]["dingtalk"]
            release.update(
                {
                    "status": "verified",
                    "node_id": "node-1",
                    "doc_url": "https://example.invalid/node-1",
                    "completed_artifact_refs": ["ART-PRD", "ART-HTML", "ART-SHOT"],
                    "readback": {
                        "passed": True,
                        "node_id": "node-1",
                        "title": "Test Package",
                        "content_sha256": "b" * 64,
                    },
                    "browser_visibility": {
                        "passed": True,
                        "node_id": "node-1",
                        "doc_url": "https://example.invalid/node-1",
                        "payload_fingerprint": payload,
                    },
                    "attempts": [],
                }
            )

            result = validator.validate_manifest(manifest, root)

            self.assertFalse(result.valid)
            self.assertTrue(any("verified evidence" in item for item in result.errors))

    def test_eval_b2_08_rejects_traversal_symlink_escape_unknown_version_and_role_overreach(self) -> None:
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as outside_tmp:
            root = Path(tmp)
            manifest = self.base_manifest(root, ui_required=False)
            outside = Path(outside_tmp) / "outside.md"
            outside.write_text("outside", encoding="utf-8")
            link = root / "linked.md"
            link.symlink_to(outside)
            manifest["artifacts"]["prd"].update(
                {"path": "linked.md", "sha256": validator.file_sha256(outside)}
            )
            escaped = validator.validate_manifest(manifest, root)
            self.assertFalse(escaped.valid)
            self.assertTrue(any("escapes" in item for item in escaped.errors))

            traversal = self.base_manifest(root, ui_required=False)
            traversal["artifacts"]["prd"]["path"] = "../outside.md"
            self.assertFalse(validator.validate_manifest(traversal, root).valid)

            unknown = self.base_manifest(root, ui_required=False)
            unknown["schema_version"] = 2
            unknown["surprise"] = True
            unknown_result = validator.validate_manifest(unknown, root)
            self.assertTrue(any("only version 1" in item for item in unknown_result.errors))
            self.assertTrue(any("unknown top-level" in item for item in unknown_result.errors))

            previous = self.base_manifest(root, ui_required=False)
            current = json.loads(json.dumps(previous))
            current["review"] = {"verdict": "ready"}
            scoped = validator.validate_manifest(current, root, previous=previous, actor_role="maker")
            self.assertTrue(any("unauthorized changes" in item for item in scoped.errors))

    def test_backlog_splitter_can_only_change_delivery_planning_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            previous = self.base_manifest(root, ui_required=False)
            self.add_pre_split_review(root, previous)
            current = json.loads(json.dumps(previous))
            self.add_delivery_plan_artifacts(root, current)

            allowed = validator.validate_manifest(
                current,
                root,
                previous=previous,
                actor_role="backlog_splitter",
                actor_identity="run-backlog",
            )

            self.assertTrue(allowed.valid, allowed.errors)

            current["title"] = "Backlog Splitter must not rewrite the package"
            overreach = validator.validate_manifest(
                current,
                root,
                previous=previous,
                actor_role="backlog_splitter",
                actor_identity="run-backlog",
            )

            self.assertTrue(
                any(
                    "actor_role.backlog_splitter: unauthorized changes: title" in item
                    for item in overreach.errors
                ),
                overreach.errors,
            )

    def test_backlog_splitter_identity_is_bound_to_planning_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            previous = self.base_manifest(root, ui_required=False)
            self.add_pre_split_review(root, previous)
            current = json.loads(json.dumps(previous))
            self.add_delivery_plan_artifacts(root, current, producer_identity="forged-actor")

            missing_identity = validator.validate_manifest(
                current, root, previous=previous, actor_role="backlog_splitter"
            )
            forged_identity = validator.validate_manifest(
                current,
                root,
                previous=previous,
                actor_role="backlog_splitter",
                actor_identity="run-backlog",
            )

            self.assertTrue(
                any("actor_identity is required" in item for item in missing_identity.errors),
                missing_identity.errors,
            )
            self.assertTrue(
                any("must record actor_identity" in item for item in forged_identity.errors),
                forged_identity.errors,
            )

    def test_planning_producer_cannot_self_review_or_be_omitted(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self.base_manifest(root, ui_required=False)
            self.add_pre_split_review(root, manifest)
            self.add_delivery_plan_artifacts(root, manifest)
            current = validator.validate_manifest(manifest, root)
            self.assertTrue(current.valid, current.errors)
            manifest["package_input_fingerprint"] = current.package_input_fingerprint
            manifest["review"] = {
                "review_id": "REVIEW-PLANNING",
                "reviewer_identity": "run-backlog",
                "maker_identities": ["run-maker"],
                "input_fingerprint": current.package_input_fingerprint,
                "verdict": "ready",
                "checks": {
                    "content": "passed",
                    "artifacts": "passed",
                    "publish": "passed",
                },
                "findings": [],
            }

            result = validator.validate_manifest(manifest, root)

            self.assertFalse(result.valid)
            self.assertTrue(
                any("must include authoritative producer identities" in item for item in result.errors),
                result.errors,
            )
            self.assertTrue(
                any("Reviewer identity must be independent" in item for item in result.errors),
                result.errors,
            )

    def test_planning_producer_identity_is_part_of_package_fingerprint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self.base_manifest(root, ui_required=False)
            self.add_pre_split_review(root, manifest)
            self.add_delivery_plan_artifacts(root, manifest)

            original = validator.validate_manifest(manifest, root)
            manifest["artifacts"]["version_plan"]["producer_identity"] = "run-backlog-2"
            changed = validator.validate_manifest(manifest, root)

            self.assertTrue(original.valid, original.errors)
            self.assertTrue(changed.valid, changed.errors)
            self.assertNotEqual(
                original.package_input_fingerprint,
                changed.package_input_fingerprint,
            )

    def test_publish_events_reuse_node_and_require_external_browser_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self.make_approved(root)
            path = self.save_manifest(root, manifest)
            payload = manifest["release"]["dingtalk"]["payload_fingerprint"]

            started = validator.record_publish_event(path, validator.load_manifest(path), self.event_args("started", payload))
            self.assertTrue(started.valid, started.errors)
            created = validator.record_publish_event(
                path,
                validator.load_manifest(path),
                self.event_args(
                    "remote_created",
                    payload,
                    node_id="node-1",
                    doc_url="https://example.invalid/node-1",
                ),
            )
            self.assertTrue(created.valid, created.errors)
            content_completed = validator.record_publish_event(
                path,
                validator.load_manifest(path),
                self.event_args("artifact_completed", payload, artifact_ref="ART-PRD"),
            )
            self.assertTrue(content_completed.valid, content_completed.errors)
            failed = validator.record_publish_event(
                path,
                validator.load_manifest(path),
                self.event_args("failed", payload, failed_step="html:ART-HTML", error_summary="fake failure"),
            )
            self.assertTrue(failed.valid, failed.errors)
            resumed = validator.record_publish_event(path, validator.load_manifest(path), self.event_args("started", payload))
            self.assertTrue(resumed.valid, resumed.errors)
            self.assertEqual(validator.load_manifest(path)["release"]["dingtalk"]["node_id"], "node-1")
            for artifact_ref in ("ART-HTML", "ART-SHOT"):
                completed = validator.record_publish_event(
                    path,
                    validator.load_manifest(path),
                    self.event_args("artifact_completed", payload, artifact_ref=artifact_ref),
                )
                self.assertTrue(completed.valid, completed.errors)

            readback = validator.record_publish_event(
                path,
                validator.load_manifest(path),
                self.event_args(
                    "readback_passed",
                    payload,
                    readback_node_id="node-1",
                    readback_title="Test Package",
                    readback_content_sha256="b" * 64,
                ),
            )
            self.assertTrue(readback.valid, readback.errors)
            self.assertEqual(readback.derived_status, "published_unverified")

            browser_path = root / "browser-evidence.json"
            browser_path.write_text(
                json.dumps(
                    {
                        "passed": True,
                        "verifier_identity": "human:browser-checker",
                        "checked_at": "2026-08-06T12:10:00+08:00",
                        "node_id": "node-1",
                        "doc_url": "https://example.invalid/node-1",
                        "payload_fingerprint": payload,
                        "checks": {
                            "title_visible": True,
                            "content_visible": True,
                            "artifacts_visible": True,
                            "publish_pollution_absent": True,
                        },
                    }
                ),
                encoding="utf-8",
            )
            verified = validator.record_publish_event(
                path,
                validator.load_manifest(path),
                self.event_args("browser_verified", payload, browser_evidence=browser_path),
            )
            self.assertTrue(verified.valid, verified.errors)
            self.assertEqual(verified.derived_status, "verified")

    def test_browser_self_assertion_and_payload_mismatch_do_not_write_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self.make_approved(root)
            path = self.save_manifest(root, manifest)
            before = path.read_bytes()
            bad = validator.record_publish_event(path, validator.load_manifest(path), self.event_args("started", "0" * 64))
            self.assertFalse(bad.valid)
            self.assertEqual(path.read_bytes(), before)

            payload = manifest["release"]["dingtalk"]["payload_fingerprint"]
            validator.record_publish_event(path, validator.load_manifest(path), self.event_args("started", payload))
            validator.record_publish_event(
                path,
                validator.load_manifest(path),
                self.event_args("remote_created", payload, node_id="node-1"),
            )
            validator.record_publish_event(
                path,
                validator.load_manifest(path),
                self.event_args("artifact_completed", payload, artifact_ref="ART-PRD"),
            )
            for artifact_ref in ("ART-HTML", "ART-SHOT"):
                validator.record_publish_event(
                    path,
                    validator.load_manifest(path),
                    self.event_args("artifact_completed", payload, artifact_ref=artifact_ref),
                )
            validator.record_publish_event(
                path,
                validator.load_manifest(path),
                self.event_args(
                    "readback_passed",
                    payload,
                    readback_node_id="node-1",
                    readback_title="Test Package",
                    readback_content_sha256="b" * 64,
                ),
            )
            browser_path = root / "browser-evidence.json"
            browser_path.write_text(
                json.dumps(
                    {
                        "passed": True,
                        "verifier_identity": "run-publisher",
                        "checked_at": "2026-08-06T12:10:00+08:00",
                        "node_id": "node-1",
                        "payload_fingerprint": payload,
                        "checks": {
                            "title_visible": True,
                            "content_visible": True,
                            "artifacts_visible": True,
                            "publish_pollution_absent": True,
                        },
                    }
                ),
                encoding="utf-8",
            )
            before_browser = path.read_bytes()
            with self.assertRaisesRegex(ValueError, "independent"):
                validator.record_publish_event(
                    path,
                    validator.load_manifest(path),
                    self.event_args("browser_verified", payload, browser_evidence=browser_path),
                )
            self.assertEqual(path.read_bytes(), before_browser)

    def test_publish_events_require_approval_started_attempt_and_valid_transition(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self.make_approved(root)
            payload = manifest["release"]["dingtalk"]["payload_fingerprint"]
            manifest["approvals"]["publish"] = None
            manifest["package_status"] = "package_ready"
            path = self.save_manifest(root, manifest)
            before = path.read_bytes()

            without_approval = validator.record_publish_event(
                path,
                validator.load_manifest(path),
                self.event_args("remote_created", payload, node_id="unauthorized-node"),
            )

            self.assertFalse(without_approval.valid)
            self.assertEqual(path.read_bytes(), before)

            approved = self.make_approved(root)
            path = self.save_manifest(root, approved)
            before = path.read_bytes()
            without_started = validator.record_publish_event(
                path,
                validator.load_manifest(path),
                self.event_args("remote_created", payload, node_id="out-of-order-node"),
            )

            self.assertFalse(without_started.valid)
            self.assertEqual(path.read_bytes(), before)

    def test_browser_evidence_is_bound_to_node_url_and_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            manifest = self.make_approved(root)
            path = self.save_manifest(root, manifest)
            payload = manifest["release"]["dingtalk"]["payload_fingerprint"]
            validator.record_publish_event(path, validator.load_manifest(path), self.event_args("started", payload))
            validator.record_publish_event(
                path,
                validator.load_manifest(path),
                self.event_args(
                    "remote_created",
                    payload,
                    node_id="node-1",
                    doc_url="https://example.invalid/node-1",
                ),
            )
            validator.record_publish_event(
                path,
                validator.load_manifest(path),
                self.event_args("artifact_completed", payload, artifact_ref="ART-PRD"),
            )
            for artifact_ref in ("ART-HTML", "ART-SHOT"):
                validator.record_publish_event(
                    path,
                    validator.load_manifest(path),
                    self.event_args("artifact_completed", payload, artifact_ref=artifact_ref),
                )
            validator.record_publish_event(
                path,
                validator.load_manifest(path),
                self.event_args(
                    "readback_passed",
                    payload,
                    readback_node_id="node-1",
                    readback_title="Test Package",
                    readback_content_sha256="b" * 64,
                ),
            )
            browser_path = root / "browser-evidence.json"
            browser_path.write_text(
                json.dumps(
                    {
                        "passed": True,
                        "verifier_identity": "human:browser-checker",
                        "checked_at": "2026-08-06T12:10:00+08:00",
                        "node_id": "old-node",
                        "doc_url": "https://example.invalid/old-node",
                        "payload_fingerprint": "0" * 64,
                        "checks": {
                            "title_visible": True,
                            "content_visible": True,
                            "artifacts_visible": True,
                            "publish_pollution_absent": True,
                        },
                    }
                ),
                encoding="utf-8",
            )
            before = path.read_bytes()

            with self.assertRaisesRegex(ValueError, "node_id"):
                validator.record_publish_event(
                    path,
                    validator.load_manifest(path),
                    self.event_args("browser_verified", payload, browser_evidence=browser_path),
                )
            self.assertEqual(path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
