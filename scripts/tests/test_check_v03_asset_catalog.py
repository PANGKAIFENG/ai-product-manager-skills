from __future__ import annotations

import importlib.util
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

    def test_archive_must_be_excluded_from_skill_discovery(self) -> None:
        errors = checker.validate_discovery_ignores(".DS_Store\ncategories/\n")

        self.assertEqual(
            errors,
            [".skillignore: archive/ must be excluded from Skill discovery"],
        )


if __name__ == "__main__":
    unittest.main()
