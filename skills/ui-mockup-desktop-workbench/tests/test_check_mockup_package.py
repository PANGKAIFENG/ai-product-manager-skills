from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_mockup_package.py"


class MockupPackageCheckerTest(unittest.TestCase):
    def run_checker(self, root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(root), *args],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_structure_only_accepts_complete_wireframe_package_without_html(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in (
                "screen-inventory.md",
                "state-model.md",
                "ascii-layout.md",
                "wireframe-handoff.md",
            ):
                (root / name).write_text("# fixture\n", encoding="utf-8")

            result = self.run_checker(root, "--structure-only")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_structure_only_reports_missing_state_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "ascii-layout.md").write_text("# fixture\n", encoding="utf-8")

            result = self.run_checker(root, "--structure-only")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing:state-model.md", result.stdout)
            self.assertNotIn("mockup.html|preview.md|screenshots.md", result.stdout)

    def test_implementation_mode_keeps_visual_handoff_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in (
                "ascii-layout.md",
                "screen-contract.md",
                "component-map.md",
                "implementation-notes.md",
                "mockup.html",
            ):
                (root / name).write_text("fixture\n", encoding="utf-8")

            result = self.run_checker(root, "--implementation")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
