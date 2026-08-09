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
                            "id": "smoke-trigger-1",
                            "type": "trigger",
                            "prompt": "Run the first smoke test.",
                            "should_trigger": True,
                            "expected_route": skill_id,
                            "expected_output": "A valid first result.",
                            "assertions": [{"text": "Returns the first result."}],
                            "known_regression": "docs/audits/sample-routing-risk.md",
                        },
                        {
                            "id": "smoke-trigger-2",
                            "type": "trigger",
                            "prompt": "Run the second smoke test.",
                            "should_trigger": True,
                            "expected_route": skill_id,
                            "expected_output": "A valid second result.",
                            "assertions": [{"text": "Returns the second result."}],
                        },
                        {
                            "id": "smoke-non-trigger-1",
                            "type": "non-trigger",
                            "prompt": "Route the first adjacent request.",
                            "should_trigger": False,
                            "expected_route": "external:adjacent-skill",
                            "expected_output": "Hands off the first request.",
                            "assertions": [{"text": "Does not select this Skill."}],
                        },
                        {
                            "id": "smoke-non-trigger-2",
                            "type": "non-trigger",
                            "prompt": "Route the second adjacent request.",
                            "should_trigger": False,
                            "expected_route": "external:adjacent-skill",
                            "expected_output": "Hands off the second request.",
                            "assertions": [{"text": "Uses the adjacent route."}],
                        },
                        {
                            "id": "routing-regression-trigger-3",
                            "type": "routing-regression",
                            "prompt": "Re-run the known routing boundary.",
                            "should_trigger": True,
                            "expected_route": skill_id,
                            "expected_output": "Keeps the known boundary on this Skill.",
                            "assertions": [{"text": "Selects this Skill at the boundary."}],
                        },
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

    def read_evals(self, root: Path, skill_id: str = "sample-skill") -> dict:
        path = root / "skills" / skill_id / "evals" / "evals.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def write_evals(
        self, root: Path, payload: dict, skill_id: str = "sample-skill"
    ) -> None:
        path = root / "skills" / skill_id / "evals" / "evals.json"
        path.write_text(json.dumps(payload), encoding="utf-8")

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

    def test_composition_runtime_manifests_with_contracts_pass(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            loop = root / "loops" / "decision-loop"
            workflow = root / "workflows" / "problem-to-solution"
            loop.mkdir(parents=True)
            workflow.mkdir(parents=True)
            (loop / "SKILL.md").write_text("# Runtime adapter\n", encoding="utf-8")
            (loop / "LOOP.md").write_text("# Loop contract\n", encoding="utf-8")
            (workflow / "SKILL.md").write_text(
                "# Runtime adapter\n", encoding="utf-8"
            )
            (workflow / "WORKFLOW.md").write_text(
                "# Workflow contract\n", encoding="utf-8"
            )

            errors = audit_skills.validate_skill_manifest_locations(root)

            self.assertEqual(errors, [])

    def test_composition_runtime_manifest_without_contract_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            adapter = root / "loops" / "decision-loop" / "SKILL.md"
            adapter.parent.mkdir(parents=True)
            adapter.write_text("# Runtime adapter\n", encoding="utf-8")

            errors = audit_skills.validate_skill_manifest_locations(root)

            self.assertEqual(
                errors,
                [
                    "SKILL.md outside canonical installable root: "
                    "loops/decision-loop/SKILL.md"
                ],
            )

    def test_missing_eval_file_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.create_valid_repo(root)
            (root / "skills" / "sample-skill" / "evals" / "evals.json").unlink()

            result, output = self.run_audit(root)

            self.assertEqual(result, 1)
            self.assertIn("sample-skill: missing evals/evals.json", output)

    def test_eval_required_string_fields_reject_invalid_values(self) -> None:
        invalid_values = (
            ("missing", None),
            ("empty", ""),
            ("whitespace", "   "),
            ("integer", 1),
            ("list", []),
            ("boolean", True),
        )
        for field in ("id", "type", "prompt", "expected_route", "expected_output"):
            for invalid_kind, invalid_value in invalid_values:
                with (
                    self.subTest(field=field, invalid_kind=invalid_kind),
                    tempfile.TemporaryDirectory() as directory,
                ):
                    root = Path(directory)
                    self.create_valid_repo(root)
                    payload = self.read_evals(root)
                    item = payload["evals"][0]
                    if invalid_kind == "missing":
                        del item[field]
                    else:
                        item[field] = invalid_value
                    self.write_evals(root, payload)

                    result, output = self.run_audit(root)

                    case_id = "<unknown>" if field == "id" else "smoke-trigger-1"
                    if invalid_kind == "missing":
                        expected_error = f"eval {case_id} missing {field}"
                    else:
                        expected_error = (
                            f"eval {case_id} {field} must be a non-empty string"
                        )
                    self.assertEqual(result, 1, output)
                    self.assertIn(expected_error, output)

    def test_eval_should_trigger_and_assertions_are_required(self) -> None:
        expected_errors = {
            "should_trigger": "eval smoke-trigger-1 missing should_trigger",
            "assertions": "eval smoke-trigger-1 missing assertions",
        }
        for field, expected_error in expected_errors.items():
            with self.subTest(field=field), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.create_valid_repo(root)
                payload = self.read_evals(root)
                del payload["evals"][0][field]
                self.write_evals(root, payload)

                result, output = self.run_audit(root)

                self.assertEqual(result, 1, output)
                self.assertIn(expected_error, output)

    def test_eval_should_trigger_must_be_json_boolean(self) -> None:
        invalid_values = (("string", "true"), ("integer", 1))
        for invalid_kind, invalid_value in invalid_values:
            with (
                self.subTest(invalid_kind=invalid_kind),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = Path(directory)
                self.create_valid_repo(root)
                payload = self.read_evals(root)
                payload["evals"][0]["should_trigger"] = invalid_value
                self.write_evals(root, payload)

                result, output = self.run_audit(root)

                self.assertEqual(result, 1, output)
                self.assertIn(
                    "eval smoke-trigger-1 should_trigger must be boolean", output
                )

    def test_eval_route_must_name_repository_skill_or_external_skill(self) -> None:
        invalid_routes = ("adjacent-skill", "external:", "external:   ")
        for invalid_route in invalid_routes:
            with (
                self.subTest(invalid_route=invalid_route),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = Path(directory)
                self.create_valid_repo(root)
                payload = self.read_evals(root)
                payload["evals"][2]["expected_route"] = invalid_route
                self.write_evals(root, payload)

                result, output = self.run_audit(root)

                self.assertEqual(result, 1, output)
                self.assertIn(
                    "eval smoke-non-trigger-1 expected_route must name a "
                    "repository Runtime entry or use external:<skill-id>",
                    output,
                )

    def test_trigger_route_must_point_to_current_skill(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.create_valid_repo(root)
            payload = self.read_evals(root)
            payload["evals"][0]["expected_route"] = "external:adjacent-skill"
            self.write_evals(root, payload)

            result, output = self.run_audit(root)

            self.assertEqual(result, 1, output)
            self.assertIn(
                "eval smoke-trigger-1 trigger expected_route must be sample-skill",
                output,
            )

    def test_non_trigger_route_must_not_point_to_current_skill(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.create_valid_repo(root)
            payload = self.read_evals(root)
            payload["evals"][2]["expected_route"] = "sample-skill"
            self.write_evals(root, payload)

            result, output = self.run_audit(root)

            self.assertEqual(result, 1, output)
            self.assertIn(
                "eval smoke-non-trigger-1 non-trigger expected_route must not be "
                "sample-skill",
                output,
            )

    def test_eval_assertions_must_be_a_non_empty_list(self) -> None:
        invalid_values = (
            ("empty-list", []),
            ("object", {"text": "Not a list."}),
            ("string", "Not a list."),
        )
        for invalid_kind, invalid_value in invalid_values:
            with (
                self.subTest(invalid_kind=invalid_kind),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = Path(directory)
                self.create_valid_repo(root)
                payload = self.read_evals(root)
                payload["evals"][0]["assertions"] = invalid_value
                self.write_evals(root, payload)

                result, output = self.run_audit(root)

                self.assertEqual(result, 1, output)
                self.assertIn(
                    "eval smoke-trigger-1 assertions must be a non-empty list", output
                )

    def test_eval_assertion_items_must_be_objects(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.create_valid_repo(root)
            payload = self.read_evals(root)
            payload["evals"][0]["assertions"] = ["Not an object."]
            self.write_evals(root, payload)

            result, output = self.run_audit(root)

            self.assertEqual(result, 1, output)
            self.assertIn(
                "eval smoke-trigger-1 assertion 1 must be an object", output
            )

    def test_eval_assertion_text_must_be_a_non_empty_string(self) -> None:
        invalid_values = (
            ("missing", {}),
            ("empty", {"text": ""}),
            ("whitespace", {"text": "   "}),
            ("integer", {"text": 1}),
        )
        for invalid_kind, invalid_assertion in invalid_values:
            with (
                self.subTest(invalid_kind=invalid_kind),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = Path(directory)
                self.create_valid_repo(root)
                payload = self.read_evals(root)
                payload["evals"][0]["assertions"] = [invalid_assertion]
                self.write_evals(root, payload)

                result, output = self.run_audit(root)

                self.assertEqual(result, 1, output)
                self.assertIn(
                    "eval smoke-trigger-1 assertion 1 text must be a non-empty string",
                    output,
                )

    def test_duplicate_eval_id_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.create_valid_repo(root)
            payload = self.read_evals(root)
            payload["evals"][1]["id"] = payload["evals"][0]["id"]
            self.write_evals(root, payload)

            result, output = self.run_audit(root)

            self.assertEqual(result, 1)
            self.assertIn("duplicate eval id: smoke-trigger-1", output)

    def test_eval_minimum_trigger_coverage_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.create_valid_repo(root)
            payload = self.read_evals(root)
            payload["evals"][1]["should_trigger"] = False
            payload["evals"][1]["expected_route"] = "external:adjacent-skill"
            payload["evals"][4]["should_trigger"] = False
            payload["evals"][4]["expected_route"] = "external:adjacent-skill"
            self.write_evals(root, payload)

            result, output = self.run_audit(root)

            self.assertEqual(result, 1)
            self.assertIn(
                "eval coverage requires at least 2 trigger cases; found 1", output
            )

    def test_exactly_two_trigger_cases_satisfy_minimum_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.create_valid_repo(root)
            payload = self.read_evals(root)
            payload["evals"][4]["should_trigger"] = False
            payload["evals"][4]["expected_route"] = "external:adjacent-skill"
            self.write_evals(root, payload)

            result, output = self.run_audit(root)

            self.assertEqual(result, 0, output)

    def test_eval_minimum_non_trigger_coverage_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.create_valid_repo(root)
            payload = self.read_evals(root)
            payload["evals"][3]["should_trigger"] = True
            payload["evals"][3]["expected_route"] = "sample-skill"
            self.write_evals(root, payload)

            result, output = self.run_audit(root)

            self.assertEqual(result, 1)
            self.assertIn(
                "eval coverage requires at least 2 non-trigger cases; found 1", output
            )

    def test_eval_known_risk_coverage_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.create_valid_repo(root)
            payload = self.read_evals(root)
            del payload["evals"][0]["known_regression"]
            payload["evals"][4]["type"] = "trigger"
            self.write_evals(root, payload)

            result, output = self.run_audit(root)

            self.assertEqual(result, 1)
            self.assertIn(
                "eval coverage requires at least 1 known-risk or regression case; found 0",
                output,
            )

    def test_empty_or_whitespace_known_regression_does_not_count_as_risk(
        self,
    ) -> None:
        for invalid_kind, invalid_value in (("empty", ""), ("whitespace", "   ")):
            with (
                self.subTest(invalid_kind=invalid_kind),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = Path(directory)
                self.create_valid_repo(root)
                payload = self.read_evals(root)
                payload["evals"][0]["known_regression"] = invalid_value
                payload["evals"][4]["type"] = "trigger"
                self.write_evals(root, payload)

                result, output = self.run_audit(root)

                self.assertEqual(result, 1, output)
                self.assertIn(
                    "eval coverage requires at least 1 known-risk or regression case; found 0",
                    output,
                )

    def test_non_empty_known_regression_satisfies_known_risk_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.create_valid_repo(root)
            payload = self.read_evals(root)
            payload["evals"][4]["type"] = "trigger"
            self.write_evals(root, payload)

            result, output = self.run_audit(root)

            self.assertEqual(result, 0, output)

    def test_regression_type_satisfies_known_risk_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.create_valid_repo(root)
            payload = self.read_evals(root)
            del payload["evals"][0]["known_regression"]
            self.write_evals(root, payload)

            result, output = self.run_audit(root)

            self.assertEqual(result, 0, output)

    def test_risk_type_satisfies_known_risk_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.create_valid_repo(root)
            payload = self.read_evals(root)
            del payload["evals"][0]["known_regression"]
            payload["evals"][4]["type"] = "routing-risk"
            self.write_evals(root, payload)

            result, output = self.run_audit(root)

            self.assertEqual(result, 0, output)

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
