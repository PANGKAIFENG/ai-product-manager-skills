from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_product_decision_brief.py"


def load_checker():
    spec = importlib.util.spec_from_file_location("check_product_decision_brief", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load product decision brief checker")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class ProductDecisionBriefCheckerTest(unittest.TestCase):
    def test_accepts_evidence_led_brief_with_selection_owner(self) -> None:
        checker = load_checker()
        text = """
        # Product Decision Brief
        Decision question: Should we adapt this onboarding pattern?
        Direction: Adapt
        Confidence: Medium
        Evidence: official docs and dated walkthrough
        Copy, Adapt, Avoid, Validate: avoid broad OAuth scope
        Next Validation: five-user activation test
        Final option selection owner: decision-research
        """
        self.assertEqual(checker.validate(text), [])

    def test_rejects_feature_inventory_without_decision_contract(self) -> None:
        checker = load_checker()
        missing = checker.validate("# Features\n- AI assistant\n- dashboards\n")
        self.assertIn("Decision question", missing)
        self.assertIn("Final option selection owner", missing)


if __name__ == "__main__":
    unittest.main()
