from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = SKILL_ROOT / "scripts" / "validate_html_artifact.py"
SPEC = importlib.util.spec_from_file_location("validate_html_artifact", VALIDATOR_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


def html_document(body: str, *, extra_script: str = "") -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <script src="https://cdn.tailwindcss.com"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
</head>
<body>{body}<script>{extra_script}</script></body>
</html>
"""


CONCEPT_BODY = """
<main data-concept-lens x-data="{}">
  <section data-concept-lineage></section>
  <nav data-stage-tabs></nav>
  <section data-debt-detector></section>
  <section data-sources><a href="https://example.com/a">A</a></section>
  <button data-copy-action>Copy</button>
</main>
"""

RESEARCH_BODY = """
<main data-research-dashboard x-data="{persona: 'product'}">
  <header data-dashboard-summary></header>
  <nav data-persona-tabs></nav>
  <section data-evidence-map></section>
  <section data-confidence></section>
  <section data-next-actions></section>
  <section data-sources><span data-source-path>sources/local-report.md</span></section>
</main>
"""


class HtmlArtifactValidatorTests(unittest.TestCase):
    def validate_text(self, text: str, suffix: str = ".html") -> tuple[bool, list[str]]:
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / f"dashboard{suffix}"
            path.write_text(text, encoding="utf-8")
            return VALIDATOR.validate(path)

    def assert_invalid(self, text: str, expected_issue: str) -> None:
        ok, issues = self.validate_text(text)
        self.assertFalse(ok)
        self.assertTrue(
            any(expected_issue in issue for issue in issues),
            f"Expected issue containing {expected_issue!r}, got {issues!r}",
        )

    def test_legacy_concept_lens_dashboard_passes(self) -> None:
        ok, issues = self.validate_text(html_document(CONCEPT_BODY))
        self.assertTrue(ok, issues)

    def test_legacy_clipboard_event_attribute_passes(self) -> None:
        body = CONCEPT_BODY.replace(
            "<button data-copy-action>Copy</button>",
            '<button @click="navigator.clipboard.writeText(\'example\')">摘要</button>',
        )
        ok, issues = self.validate_text(html_document(body))
        self.assertTrue(ok, issues)

    def test_general_research_dashboard_with_local_source_path_passes(self) -> None:
        ok, issues = self.validate_text(html_document(RESEARCH_BODY))
        self.assertTrue(ok, issues)

    def test_missing_general_marker_fails(self) -> None:
        body = RESEARCH_BODY.replace(" data-evidence-map", "")
        self.assert_invalid(html_document(body), "Evidence map marker")

    def test_both_dashboard_roots_fail(self) -> None:
        body = RESEARCH_BODY.replace(
            "data-research-dashboard", "data-research-dashboard data-concept-lens"
        )
        self.assert_invalid(html_document(body), "exactly one dashboard root")

    def test_duplicate_same_dashboard_root_fails(self) -> None:
        body = RESEARCH_BODY + '<aside data-research-dashboard x-data="{}"></aside>'
        self.assert_invalid(html_document(body), "exactly one dashboard root")

    def test_required_marker_outside_dashboard_root_fails(self) -> None:
        body = RESEARCH_BODY.replace("<section data-evidence-map></section>", "")
        body += "<section data-evidence-map></section>"
        self.assert_invalid(html_document(body), "Evidence map marker")

    def test_marker_only_in_comment_fails(self) -> None:
        body = RESEARCH_BODY.replace(" data-evidence-map", "") + "<!-- data-evidence-map -->"
        self.assert_invalid(html_document(body), "Evidence map marker")

    def test_marker_only_in_script_string_fails(self) -> None:
        body = RESEARCH_BODY.replace(" data-evidence-map", "")
        self.assert_invalid(
            html_document(body, extra_script="const fake = 'data-evidence-map';"),
            "Evidence map marker",
        )

    def test_backend_call_fails(self) -> None:
        self.assert_invalid(
            html_document(RESEARCH_BODY, extra_script="fetch('/api/research')"),
            "backend call",
        )

    def test_backend_like_text_in_presentation_attribute_passes(self) -> None:
        body = RESEARCH_BODY.replace(
            "<header data-dashboard-summary></header>",
            '<header data-dashboard-summary title="Example: fetch(\'/api/docs\')"></header>',
        )
        ok, issues = self.validate_text(html_document(body))
        self.assertTrue(ok, issues)

    def test_backend_call_in_alpine_attribute_fails(self) -> None:
        body = RESEARCH_BODY.replace(
            "x-data=\"{persona: 'product'}\"",
            "x-data=\"{persona: 'product'}\" x-init=\"fetch('/api/research')\"",
        )
        self.assert_invalid(html_document(body), "backend call")

    def test_axios_call_in_event_attribute_fails(self) -> None:
        body = RESEARCH_BODY.replace(
            "<section data-next-actions></section>",
            '<button data-next-actions @click="axios.get(\'/api/research\')">Run</button>',
        )
        self.assert_invalid(html_document(body), "backend call")

    def test_unresolved_placeholder_fails(self) -> None:
        self.assert_invalid(html_document(RESEARCH_BODY + "<p>TODO</p>"), "TODO")

    def test_non_html_extension_fails(self) -> None:
        ok, issues = self.validate_text(html_document(RESEARCH_BODY), suffix=".txt")
        self.assertFalse(ok)
        self.assertIn("File extension should be .html or .htm", issues)

    def test_persisted_general_dashboard_fixture_passes(self) -> None:
        fixture = SKILL_ROOT / "evals" / "fixtures" / "research-dashboard" / "dashboard.html"
        ok, issues = VALIDATOR.validate(fixture)
        self.assertTrue(ok, issues)


if __name__ == "__main__":
    unittest.main()
