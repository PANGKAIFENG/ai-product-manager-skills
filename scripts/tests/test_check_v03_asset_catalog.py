from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "check_v03_asset_catalog.py"
SPEC = importlib.util.spec_from_file_location("check_v03_asset_catalog", MODULE_PATH)
assert SPEC and SPEC.loader
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)

ROOT = Path(__file__).resolve().parents[2]


class V03AssetCatalogTests(unittest.TestCase):
    def test_repository_contract_passes(self) -> None:
        errors, counts = checker.validate_repository(ROOT)

        self.assertEqual(errors, [])
        self.assertEqual(
            counts,
            {"skills": 15, "loops": 3, "workflows": 2, "tools": 4, "packs": 4},
        )

    def test_missing_skill_id_fails(self) -> None:
        expected = checker.EXPECTED_IDS["skills"]
        entries = [{"id": skill_id} for skill_id in sorted(expected)[1:]]

        errors = checker.validate_ids("skills", entries, expected)

        self.assertTrue(any("missing v0.3 IDs" in error for error in errors), errors)

    def test_extra_workflow_id_fails(self) -> None:
        expected = checker.EXPECTED_IDS["workflows"]
        entries = [{"id": value} for value in sorted(expected | {"mega-workflow"})]

        errors = checker.validate_ids("workflows", entries, expected)

        self.assertTrue(any("unexpected v0.3 IDs" in error for error in errors), errors)

    def test_explicit_runtime_adapter_contract_passes(self) -> None:
        entry = {
            "id": "decision-loop",
            "runtime_adapter": "loops/decision-loop",
            "runtime_skill_id": "decision-loop",
        }

        errors = checker.validate_runtime_adapter(
            ROOT, "loops", entry, "decision-loop"
        )

        self.assertEqual(errors, [])

    def test_runtime_adapter_id_mismatch_fails(self) -> None:
        entry = {
            "id": "decision-loop",
            "runtime_adapter": "loops/decision-loop",
            "runtime_skill_id": "old-decision-loop",
        }

        errors = checker.validate_runtime_adapter(
            ROOT, "loops", entry, "decision-loop"
        )

        self.assertTrue(any("runtime_skill_id must be decision-loop" in error for error in errors), errors)

    def test_runtime_adapter_eval_unknown_route_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            adapter = root / "loops" / "decision-loop"
            shutil.copytree(ROOT / "loops" / "decision-loop", adapter)
            eval_path = adapter / "evals" / "evals.json"
            payload = json.loads(eval_path.read_text(encoding="utf-8"))
            payload["evals"][0]["expected_route"] = "missing-runtime-entry"
            eval_path.write_text(json.dumps(payload), encoding="utf-8")

            errors = checker.validate_runtime_adapter(
                root,
                "loops",
                {
                    "id": "decision-loop",
                    "runtime_adapter": "loops/decision-loop",
                    "runtime_skill_id": "decision-loop",
                },
                "decision-loop",
            )

            self.assertTrue(any("repository Runtime entry" in error for error in errors), errors)

    def test_runtime_adapter_eval_coverage_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            adapter = root / "loops" / "decision-loop"
            shutil.copytree(ROOT / "loops" / "decision-loop", adapter)
            eval_path = adapter / "evals" / "evals.json"
            payload = json.loads(eval_path.read_text(encoding="utf-8"))
            payload["evals"] = payload["evals"][:1]
            eval_path.write_text(json.dumps(payload), encoding="utf-8")

            errors = checker.validate_runtime_adapter(
                root,
                "loops",
                {
                    "id": "decision-loop",
                    "runtime_adapter": "loops/decision-loop",
                    "runtime_skill_id": "decision-loop",
                },
                "decision-loop",
            )

            self.assertTrue(any("at least 2 trigger cases" in error for error in errors), errors)
            self.assertTrue(any("at least 2 non-trigger cases" in error for error in errors), errors)
            self.assertTrue(any("known-risk or regression" in error for error in errors), errors)

    def test_archived_id_cannot_reappear_under_composition_roots(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT, root, dirs_exist_ok=True)
            retired = root / "workflows" / "product-discovery"
            retired.mkdir(parents=True, exist_ok=True)
            (retired / "SKILL.md").write_text(
                "---\nname: product-discovery\ndescription: Retired.\n---\n",
                encoding="utf-8",
            )

            errors, _ = checker.validate_repository(root)

            self.assertTrue(
                any(
                    "product-discovery: retired ID remains installable under workflows/"
                    in error
                    for error in errors
                ),
                errors,
            )

    def test_archive_must_be_excluded_from_skill_discovery(self) -> None:
        errors = checker.validate_discovery_ignores(".DS_Store\ncategories/\n")

        self.assertEqual(
            errors,
            [".skillignore: archive/ must be excluded from Skill discovery"],
        )


if __name__ == "__main__":
    unittest.main()
