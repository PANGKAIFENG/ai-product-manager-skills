from __future__ import annotations

import json
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class DashboardContractTests(unittest.TestCase):
    def test_skill_entrypoint_stays_within_context_budget(self) -> None:
        lines = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8").splitlines()
        self.assertLessEqual(len(lines), 320)

    def test_skill_metadata_exposes_generic_dashboard_triggers(self) -> None:
        text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        frontmatter = text.split("---", 2)[1]

        for trigger in ("本地 HTML 研究看板", "可视化研究报告", "跨职能 Dashboard"):
            self.assertIn(trigger, frontmatter)

    def test_skill_exposes_output_artifact_modes(self) -> None:
        text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## Output Artifact Modes", text)
        self.assertIn("research-dashboard-html", text)
        self.assertIn("concept-dashboard-html", text)
        self.assertIn("Output artifact mode", text)

    def test_general_dashboard_contract_is_bundled_and_routed(self) -> None:
        contract = SKILL_ROOT / "references" / "research-dashboard-output-contract.md"
        self.assertTrue(contract.exists())
        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        routing_text = (SKILL_ROOT / "references" / "mode-routing-guide.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("references/research-dashboard-output-contract.md", skill_text)
        self.assertIn("research-dashboard-html", routing_text)

    def test_dashboard_rendering_preserves_iterative_terminal_gate(self) -> None:
        text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("latest Framework", text)
        self.assertIn("unique terminal status", text)
        self.assertIn("residual Gap", text)

    def test_dashboard_rendering_requires_an_evidence_bearing_state(self) -> None:
        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        contract_text = (
            SKILL_ROOT / "references" / "research-dashboard-output-contract.md"
        ).read_text(encoding="utf-8")

        for text in (skill_text, contract_text):
            self.assertIn("evidence-bearing latest Framework", text)
            self.assertIn("claim-to-evidence", text)
            self.assertIn("escalated", text)
            self.assertIn("explicitly requests a partial Dashboard", text)

    def test_non_dashboard_outputs_are_not_forced_to_html(self) -> None:
        text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Do not generate HTML", text)

    def test_legacy_design_quality_references_are_not_stale(self) -> None:
        for relative_path in (
            "references/concept-lens-output-contract.md",
            "references/concept-lens-html-dashboard-template.md",
        ):
            text = (SKILL_ROOT / relative_path).read_text(encoding="utf-8")
            self.assertNotIn("references/design-quality.md", text)
            self.assertIn("concept-lens-design-quality.md", text)

    def test_dashboard_eval_matrix_is_bundled(self) -> None:
        evals = json.loads((SKILL_ROOT / "evals" / "evals.json").read_text(encoding="utf-8"))
        eval_ids = {case["id"] for case in evals["evals"]}
        self.assertTrue(
            {
                "routing-general-research-dashboard-html",
                "routing-concept-lens-dashboard-compatible",
                "routing-dashboard-does-not-override-decision-owner",
                "general-dashboard-artifact-contract",
                "iterative-loop-survives-dashboard-rendering",
                "dashboard-not-created-when-not-requested",
                "dashboard-transfer-mcp-auth-security",
                "dashboard-partial-state-requires-explicit-acceptance",
            }.issubset(eval_ids)
        )

    def test_dashboard_catalog_discovery_evals_cover_trigger_and_near_miss(self) -> None:
        payload = json.loads(
            (SKILL_ROOT / "evals" / "evals.json").read_text(encoding="utf-8")
        )
        cases = {case["id"]: case for case in payload["evals"]}

        trigger = cases["trigger-generic-research-dashboard"]
        self.assertTrue(trigger["should_trigger"])
        self.assertEqual(trigger["expected_route"], "research-topic-compiler")
        self.assertNotIn("专题研究", trigger["prompt"])

        near_miss = cases["non-trigger-ui-only-dashboard-implementation"]
        self.assertFalse(near_miss["should_trigger"])
        self.assertNotEqual(near_miss["expected_route"], "research-topic-compiler")
        self.assertIn("不需要做研究", near_miss["prompt"])

    def test_dashboard_grader_and_fixture_are_bundled(self) -> None:
        fixture = SKILL_ROOT / "evals" / "fixtures" / "research-dashboard" / "dashboard.html"
        self.assertTrue(
            (SKILL_ROOT / "evals" / "graders" / "dashboard-artifact-rubric.md").exists()
        )
        self.assertTrue(fixture.exists())
        self.assertTrue(
            (SKILL_ROOT / "evals" / "fixtures" / "research-dashboard" / "summary.md").exists()
        )

        fixture_text = fixture.read_text(encoding="utf-8")
        self.assertIn("grid min-w-0 max-w-7xl", fixture_text)
        self.assertIn('data-sources class="panel min-w-0', fixture_text)
        self.assertIn('<link rel="icon" href="data:,">', fixture_text)
        self.assertIn("data-persona-control", fixture_text)
        self.assertIn("data-persona-panel", fixture_text)
        self.assertIn("data-persona-fallback", fixture_text)

    def test_offline_cdn_verification_policy_is_explicit(self) -> None:
        contract = (
            SKILL_ROOT / "references" / "research-dashboard-output-contract.md"
        ).read_text(encoding="utf-8")
        grader = (
            SKILL_ROOT / "evals" / "graders" / "dashboard-artifact-rubric.md"
        ).read_text(encoding="utf-8")

        for text in (contract, grader):
            self.assertIn("HTTP 200 empty stub", text)
            self.assertIn("native fallback", text)
            self.assertIn("zero console errors", text)


if __name__ == "__main__":
    unittest.main()
