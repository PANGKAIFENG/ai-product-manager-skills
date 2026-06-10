# Output Contract

## File Layout

Unless the user specifies a target path, create:

```text
./concept-lens-outputs/<concept-slug>/
  dashboard.html
  summary.md
```

Use lowercase ASCII slugs for folder names. Keep the visible concept title in Chinese or the user's requested language.

## Markdown Summary

`summary.md` should include:

1. Essence statement.
2. Concept lineage: origin context, original use, original contradiction, major semantic shifts, and current semantic drift.
3. Source-backed evolution matrix.
4. Debt detector table.
5. PM review scripts.
6. Sources and assumptions.

The final chat response can summarize the same content briefly, but the file should contain the durable artifact.

## HTML Requirements

`dashboard.html` must:

- Run by double-clicking the file.
- Use Tailwind CSS CDN and Alpine.js CDN.
- Store all dashboard data inline in the file.
- Include no backend calls and no build step.
- Include a concept lineage section covering origin, original use, semantic shifts, and current drift.
- Include a timeline or tab navigation for stages.
- Include copy buttons for review questions.
- Include a debt detector section.
- Include a visible sources section.
- Include validation markers required by `scripts/validate_html_artifact.py`.
- Pass the visual preflight in `references/design-quality.md`.

Required markers:

```html
data-concept-lens
data-concept-lineage
data-stage-tabs
data-debt-detector
data-sources
```

## Final Response

Report:

- Generated file links.
- Validation command and result.
- Visual preflight result.
- Browser verification result or limitation.
- Source links used.
- Key lineage findings: origin, original use, and current semantic drift.
- Key assumptions and confidence gaps.

Do not paste the full HTML into the final chat response unless the user explicitly asks.
