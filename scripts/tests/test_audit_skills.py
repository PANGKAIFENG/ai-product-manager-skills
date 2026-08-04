import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "audit_skills.py"
SPEC = importlib.util.spec_from_file_location("audit_skills", MODULE_PATH)
assert SPEC and SPEC.loader
audit_skills = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit_skills)


class AuditSkillsTests(unittest.TestCase):
    def create_valid_repo(self, root: Path, skill_id: str = "sample-skill") -> None:
        skill_dir = root / "skills" / skill_id
        (skill_dir / "evals").mkdir(parents=True)
        (root / "catalog").mkdir()
        (root / "docs" / "examples").mkdir(parents=True)

        (skill_dir / "SKILL.md").write_text(
            f"---\nname: {skill_id}\ndescription: Use when testing the audit.\n---\n",
            encoding="utf-8",
        )
        (skill_dir / "evals" / "evals.json").write_text(
            json.dumps(
                {
                    "skill_name": skill_id,
                    "evals": [
                        {
                            "id": "smoke",
                            "prompt": "Run the smoke test.",
                            "expected_output": "A valid result.",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        (root / "catalog" / "skills.yaml").write_text(
            "\n".join(
                [
                    "schema_version: 1",
                    "skills_root: skills",
                    "skills:",
                    f"  - id: {skill_id}",
                    f"    path: skills/{skill_id}",
                    "    name_zh: Test Skill",
                    "    category: collaboration-thinking",
                    "    status: active",
                    f"    example: docs/examples/{skill_id}.md",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        (root / "docs" / "examples" / f"{skill_id}.md").write_text(
            "# Example\n", encoding="utf-8"
        )
        (root / "README.md").write_text(
            f"[Skill](skills/{skill_id}/)\n[Example](docs/examples/{skill_id}.md)\n",
            encoding="utf-8",
        )
        (root / "SKILL_REGISTRY.md").write_text(
            f"`{skill_id}`\n", encoding="utf-8"
        )

        for relative in audit_skills.DUPLICATE_PRD_FILES:
            for duplicate_skill in ("prd-architect", "prd-review"):
                path = root / "skills" / duplicate_skill / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(f"shared fixture: {relative}\n", encoding="utf-8")

    def run_audit(self, root: Path) -> tuple[int, str]:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = audit_skills.audit(root)
        return result, output.getvalue()

    def test_valid_repository_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.create_valid_repo(root)

            result, output = self.run_audit(root)

            self.assertEqual(result, 0, output)

    def test_skill_manifest_outside_canonical_root_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.create_valid_repo(root)
            rogue = root / "docs" / "rogue" / "SKILL.md"
            rogue.parent.mkdir(parents=True)
            rogue.write_text("# Rogue Skill\n", encoding="utf-8")

            result, output = self.run_audit(root)

            self.assertEqual(result, 1)
            self.assertIn(
                "SKILL.md outside canonical installable root: docs/rogue/SKILL.md",
                output,
            )

    def test_missing_eval_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.create_valid_repo(root)
            (root / "skills" / "sample-skill" / "evals" / "evals.json").unlink()

            result, output = self.run_audit(root)

            self.assertEqual(result, 1)
            self.assertIn("sample-skill: missing evals/evals.json", output)

    def test_high_risk_skill_without_checker_directory_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.create_valid_repo(root, skill_id="brainstorming")

            result, output = self.run_audit(root)

            self.assertEqual(result, 1)
            self.assertIn(
                "brainstorming: high-risk output Skill has no scripts/ checker",
                output,
            )


if __name__ == "__main__":
    unittest.main()
