#!/usr/bin/env python3
"""Static checks for research-topic-compiler HTML dashboard artifacts."""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path


COMMON_REQUIRED_ATTRIBUTES = {
    "Alpine data binding": "x-data",
    "Sources marker": "data-sources",
}

DASHBOARD_TYPES = {
    "concept-lens": {
        "root": "data-concept-lens",
        "required_attributes": {
            "Concept lineage marker": "data-concept-lineage",
            "Stage tabs marker": "data-stage-tabs",
            "Debt detector marker": "data-debt-detector",
        },
    },
    "research-dashboard": {
        "root": "data-research-dashboard",
        "required_attributes": {
            "Dashboard summary marker": "data-dashboard-summary",
            "Persona marker": "data-persona-tabs",
            "Evidence map marker": "data-evidence-map",
            "Confidence marker": "data-confidence",
            "Next actions marker": "data-next-actions",
        },
    },
}

FORBIDDEN_PATTERNS = [
    re.compile(r"TODO|TBD|FIXME|PLACEHOLDER", re.IGNORECASE),
    re.compile(r"随着时代的发展"),
    re.compile(r"技术是一把双刃剑"),
    re.compile(r"\blorem\s+ipsum\b", re.IGNORECASE),
]

BACKEND_CALL_PATTERNS = [
    re.compile(r"\bfetch\s*\(", re.IGNORECASE),
    re.compile(r"\bXMLHttpRequest\b", re.IGNORECASE),
    re.compile(r"\baxios\s*\.", re.IGNORECASE),
    re.compile(r"[\"']/api/", re.IGNORECASE),
    re.compile(r"(?:^|[\"'(])/api/", re.IGNORECASE),
]

VOID_ELEMENTS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}


class ArtifactParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.attributes: set[str] = set()
        self.attribute_values: list[str] = []
        self.executable_attribute_values: list[str] = []
        self.attributes_by_root = {dashboard_type: set() for dashboard_type in DASHBOARD_TYPES}
        self.attribute_values_by_root = {
            dashboard_type: [] for dashboard_type in DASHBOARD_TYPES
        }
        self.visible_text_by_root = {dashboard_type: [] for dashboard_type in DASHBOARD_TYPES}
        self.root_occurrences: list[str] = []
        self.script_sources: list[str] = []
        self.script_text: list[str] = []
        self.visible_text: list[str] = []
        self._tag_stack: list[tuple[str, str | None]] = []
        self._inside_script = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        values = {name.lower(): value or "" for name, value in attrs}
        names = set(values)
        self.attributes.update(names)
        self.attribute_values.extend(value for value in values.values() if value)
        for name, value in values.items():
            executable_binding = name.startswith(("x-", "@", "on", ":"))
            request_target = name in {"action", "formaction"}
            script_source = tag == "script" and name == "src"
            javascript_url = value.lstrip().lower().startswith("javascript:")
            if value and (executable_binding or request_target or script_source or javascript_url):
                self.executable_attribute_values.append(value)

        declared_roots = [
            dashboard_type
            for dashboard_type, rules in DASHBOARD_TYPES.items()
            if rules["root"] in names
        ]
        self.root_occurrences.extend(declared_roots)

        inherited_root = self._tag_stack[-1][1] if self._tag_stack else None
        active_root = declared_roots[0] if len(declared_roots) == 1 else inherited_root
        if active_root:
            self.attributes_by_root[active_root].update(names)
            self.attribute_values_by_root[active_root].extend(
                value for value in values.values() if value
            )

        if tag == "script":
            self._inside_script = True
            if values.get("src"):
                self.script_sources.append(values["src"])

        if tag not in VOID_ELEMENTS:
            self._tag_stack.append((tag, active_root))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag.lower() not in VOID_ELEMENTS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "script":
            self._inside_script = False
        for index in range(len(self._tag_stack) - 1, -1, -1):
            if self._tag_stack[index][0] == tag:
                del self._tag_stack[index:]
                break

    def handle_data(self, data: str) -> None:
        if self._inside_script:
            self.script_text.append(data)
        else:
            self.visible_text.append(data)
            active_root = self._tag_stack[-1][1] if self._tag_stack else None
            if active_root:
                self.visible_text_by_root[active_root].append(data)


def _parse(text: str) -> ArtifactParser:
    parser = ArtifactParser()
    parser.feed(text)
    parser.close()
    return parser


def validate(path: Path) -> tuple[bool, list[str]]:
    issues: list[str] = []
    if not path.exists():
        return False, [f"File not found: {path}"]
    if path.suffix.lower() not in {".html", ".htm"}:
        issues.append("File extension should be .html or .htm")

    text = path.read_text(encoding="utf-8", errors="ignore")
    parser = _parse(text)

    if not re.search(r"<html\b", text, flags=re.IGNORECASE):
        issues.append("Missing <html> tag")
    if not re.search(r"</html>", text, flags=re.IGNORECASE):
        issues.append("Missing closing </html> tag")
    if not parser.script_sources and not parser.script_text:
        issues.append("Missing <script> tag")

    sources = [source.lower() for source in parser.script_sources]
    if not any("cdn.tailwindcss.com" in source for source in sources):
        issues.append("Missing required script: Tailwind CSS CDN")
    if not any("alpinejs" in source for source in sources):
        issues.append("Missing required script: Alpine.js CDN")

    if len(parser.root_occurrences) != 1:
        issues.append("Expected exactly one dashboard root marker")
    else:
        dashboard_type = parser.root_occurrences[0]
        rules = DASHBOARD_TYPES[dashboard_type]
        scoped_attributes = parser.attributes_by_root[dashboard_type]
        required = {**COMMON_REQUIRED_ATTRIBUTES, **rules["required_attributes"]}
        for label, attribute in required.items():
            if attribute not in scoped_attributes:
                issues.append(f"Missing required attribute: {label} ({attribute})")

        if dashboard_type == "concept-lens":
            if len(re.findall(r"https?://", text)) < 3:
                issues.append("Expected at least 3 source or CDN URLs")
            visible = " ".join(parser.visible_text_by_root[dashboard_type])
            attribute_values = " ".join(parser.attribute_values_by_root[dashboard_type])
            if (
                "data-copy-action" not in scoped_attributes
                and not re.search(r"copy|复制|clipboard", visible, flags=re.IGNORECASE)
                and not re.search(r"copy|clipboard", attribute_values, flags=re.IGNORECASE)
            ):
                issues.append("Missing copy interaction hint")

    for pattern in FORBIDDEN_PATTERNS:
        match = pattern.search(text)
        if match:
            issues.append(f"Forbidden or unresolved text found: {match.group(0)}")

    executable_text = "\n".join(
        [*parser.script_text, *parser.executable_attribute_values]
    )
    for pattern in BACKEND_CALL_PATTERNS:
        match = pattern.search(executable_text)
        if match:
            issues.append(f"Forbidden backend call found: {match.group(0)}")
            break

    return not issues, issues


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_html_artifact.py <dashboard.html>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1]).expanduser().resolve()
    ok, issues = validate(path)
    if ok:
        print(f"PASS: {path}")
        return 0

    print(f"FAIL: {path}")
    for issue in issues:
        print(f"- {issue}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
