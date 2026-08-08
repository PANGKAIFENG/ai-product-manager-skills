import copy
import importlib.util
import unittest
from pathlib import Path
from unittest import mock


MODULE_PATH = Path(__file__).resolve().parents[1] / "check_b1_core_loop_contracts.py"
SPEC = importlib.util.spec_from_file_location("check_b1_core_loop_contracts", MODULE_PATH)
assert SPEC and SPEC.loader
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)

ROOT = Path(__file__).resolve().parents[2]


class B1CoreLoopContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cases = checker.load_eval_cases(ROOT)

    def test_repository_contract_passes(self) -> None:
        errors, counts = checker.validate_repository(ROOT)

        self.assertEqual(errors, [])
        self.assertEqual(counts["b1-single-call"], 8)
        self.assertEqual(counts["b1-chained-call"], 5)
        self.assertEqual(counts["b1-return-edge"], 7)

    def test_removed_legacy_eval_fails(self) -> None:
        cases = copy.deepcopy(self.cases)
        removed_id = "framing-vague-roadmap-input"
        cases["research-topic-compiler"] = [
            case for case in cases["research-topic-compiler"] if case["id"] != removed_id
        ]

        errors = checker.validate_eval_contracts(cases)

        self.assertTrue(any(removed_id in error for error in errors), errors)

    def test_paired_eval_requires_one_true_owner(self) -> None:
        cases = copy.deepcopy(self.cases)
        pair_id = "b1-paired-candidate-pool-not-final-choice"
        for skill_cases in cases.values():
            for case in skill_cases:
                if case["id"] == pair_id:
                    case["should_trigger"] = True

        errors = checker.validate_eval_contracts(cases)

        self.assertTrue(any("exactly one true owner" in error for error in errors), errors)

    def test_paired_eval_requires_identical_prompt(self) -> None:
        cases = copy.deepcopy(self.cases)
        pair_id = "b1-paired-options-not-yet-solution"
        for case in cases["grill-me"]:
            if case["id"] == pair_id:
                case["prompt"] += " changed"

        errors = checker.validate_eval_contracts(cases)

        self.assertTrue(any("mirrored prompts differ" in error for error in errors), errors)

    def test_explicit_superpowers_route_stays_external(self) -> None:
        cases = copy.deepcopy(self.cases)
        for case in cases["brainstorming"]:
            if case["id"] == "b1-explicit-superpowers-qualified-route":
                case["should_trigger"] = True
                case["expected_route"] = "brainstorming"

        errors = checker.validate_eval_contracts(cases)

        self.assertTrue(any("external non-trigger route" in error for error in errors), errors)

    def test_removed_critical_skill_boundary_fails(self) -> None:
        targets = (
            (ROOT / "skills/research-topic-compiler/SKILL.md", "handoff/chain 不构成外部写入授权"),
            (ROOT / "skills/research-topic-compiler/references/core-loop-research-handoff.md", (
                "A handoff or chain is not authorization for external writes"
            )),
            (ROOT / "skills/decision-research/SKILL.md", (
                "当前 `decision_question` 内为选择服务的有界取证与反证搜索"
            )),
            (ROOT / "skills/decision-research/SKILL.md", "不拥有开放式知识工程"),
            (ROOT / "skills/decision-research/SKILL.md", (
                "不执行已经通过 Research Return Request 明确交给 Research 的证据 gap"
            )),
            (ROOT / "skills/decision-research/SKILL.md", (
                "不拥有方案设计、Critic clearance 或 readiness 审批"
            )),
        )
        original_read_text = Path.read_text

        for target, marker in targets:
            with self.subTest(target=target):
                def read_without_marker(path: Path, *args, **kwargs) -> str:
                    text = original_read_text(path, *args, **kwargs)
                    return text.replace(marker, "") if path == target else text

                with mock.patch.object(Path, "read_text", autospec=True, side_effect=read_without_marker):
                    errors, _ = checker.validate_repository(ROOT)

                self.assertTrue(any(marker in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
