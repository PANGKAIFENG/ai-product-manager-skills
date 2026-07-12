# Research Dashboard Output Contract

Use this contract when `research-topic-compiler` chooses `research-dashboard-html` for a general research topic, Application translation, business-facing explanation, or cross-functional review artifact.

The dashboard is a reading and decision-support surface. It makes a completed research result easier to scan, compare, challenge, and reuse. It is not a marketing page, UI mockup, slide deck, final decision authority, or replacement for the evidence matrix.

## File Layout

Unless the user specifies a target path, create:

```text
./research-dashboard-outputs/<topic-slug>/
  dashboard.html
  summary.md
```

Use lowercase ASCII slugs for folder names. Keep visible titles in the user's requested language.

## Research-State Projection

For Normal Research/Application, generate the files only when the run has a renderable research state. A terminal label alone is not enough. All of the following must exist:

- One unique terminal status.
- An evidence-bearing latest Framework that is more than a restatement of the Seed.
- At least one locatable claim-to-evidence link supporting or challenging a decision-relevant claim.
- Visible confidence, material uncertainty, residual Gaps, and limits on the next action.

Apply terminal status policy before rendering:

- `complete-saturated` / `complete-fit-for-purpose`: render only when the minimum state above exists.
- `partial-access` / `partial-budget`: do not render by default. Render only when the user, after seeing the limitation, explicitly requests a partial Dashboard or explicitly accepts one; make the missing evidence, weak conclusions, and unsupported next actions prominent.
- `blocked-authorization`: do not render when missing authorization prevents the minimum state. Never substitute Seed text or unauthorized material.
- `escalated`: do not render by default. The receiving Skill or the user decision owns the next artifact.

When the gate passes, project the latest research state rather than restating the seed material:

- Latest Framework and material Framework Change Events.
- Important claims and their Source/Evidence support.
- Confidence, uncertainty, contradictions, and counterexamples.
- Unique terminal status, stop reason, residual Gaps, and residual risks.
- Next actions tied to the user's product, business, learning, or validation goal.

The visual layer may compress detail, but it must not hide a weakness that could change the conclusion. Link or point back to the underlying evidence matrix when one exists.

## Markdown Summary

`summary.md` should include:

1. One-sentence conclusion.
2. Research goal, audience, scope, research mode, output artifact mode, and unique terminal status.
3. Key findings with evidence level or confidence.
4. Material framework changes and what evidence caused them.
5. Role-specific reading notes for the resolved persona set.
6. Risks, uncertainty, counterexamples, residual Gaps, and assumptions.
7. Recommended next actions.
8. Sources or local source paths.

## HTML Requirements

`dashboard.html` must:

- Run by double-clicking the file.
- Use Tailwind CSS CDN and Alpine.js CDN.
- Store all dashboard data inline in the file.
- Include no backend calls, runtime API dependency, or build step.
- Put the one-sentence conclusion, audience, confidence/source status, and navigation in the first viewport.
- Include role or persona tabs when the research serves multiple readers. For one reader, keep the `data-persona-tabs` marker on a single visible persona section so the contract remains deterministic.
- For multiple readers, make persona switching work when Alpine.js cannot load. Add native JavaScript fallback controls and panels marked with `data-persona-control`, `data-persona-panel`, and `data-persona-fallback`; Alpine.js may progressively enhance the same state.
- Include a visible evidence map, not just final opinions.
- Include confidence, uncertainty, or evidence-strength labels for important claims.
- Include the terminal status and unresolved material Gaps or explicitly state that none remain.
- Include next actions that map to the user's requested business or product goal.
- Include a visible sources section with title, URL or local path, claim area, and evidence level.
- Include validation markers required by `scripts/validate_html_artifact.py`.
- Pass the visual preflight below.

Required markers must be attributes on real HTML elements, not comments or JavaScript strings:

```html
data-research-dashboard
data-dashboard-summary
data-persona-tabs
data-evidence-map
data-confidence
data-next-actions
data-sources
```

Use exactly one dashboard root family. Do not place `data-concept-lens` and `data-research-dashboard` in the same document.

## Information Architecture

Use this page order unless the research result has a stronger reason to differ:

1. Executive summary: topic, one-sentence conclusion, audience, confidence, source coverage, and terminal status.
2. Reader tabs or section: role-specific interpretation and "what this means for you".
3. Key findings: 3-7 findings with evidence labels and implications.
4. Evidence map: source-backed claims, weak signals, inferred judgments, contradictions, and unknowns.
5. Framework change: what materially changed from the initial framing and why.
6. Decision-support or application layer: roadmap input, PRD input, workflow design, eval checklist, SOP, or validation plan.
7. Risks and counterexamples: where the conclusion may fail, plus residual Gaps.
8. Next actions: concrete reading, experiment, PRD, validation, or team handoff steps.
9. Sources and assumptions.

## Design Rules

- The first viewport should feel like a working research dashboard, not a landing page.
- Use a restrained professional interface with one purposeful accent color and semantic status colors.
- Use cards only for repeated findings, sources, risks, or next actions. Do not nest cards.
- Prefer grids, tabs, segmented controls, compact tables, and sticky or top navigation for scanability.
- Keep text readable on desktop and mobile; no overlapping panels or horizontal overflow.
- Surface uncertainty early; do not hide it in an appendix.
- Do not use decorative blobs, glassmorphism blankets, oversized hero sections, stock-like imagery, or generic purple/blue gradients.
- Do not make the HTML look like a UI product mockup. It is a research artifact.

## Visual Preflight

Before final delivery, verify:

- First viewport shows conclusion, audience, confidence/source status, terminal status, and navigation.
- Persona tabs switch content correctly when multiple audiences are present; a single-reader section remains visible without an empty control.
- Multiple-persona controls still switch content when the Alpine.js CDN is blocked or returns an empty response.
- Evidence map distinguishes sourced facts, weak signals, model/user inferences, contradictions, and unknowns.
- Next actions are concrete enough to become PRD input, roadmap input, validation task, or team handoff.
- Source links or local source paths are visible and readable.
- Desktop and mobile layouts show no overlap, hidden text, or horizontal overflow.
- Browser console has no errors during the checked interactions.
- The page avoids one-note slate/blue, purple-gradient, beige, or decorative marketing styling unless the user explicitly asked for it.

### Offline CDN Verification Policy

When browser verification must prove offline resilience, intercept each Tailwind or Alpine CDN request with a local `HTTP 200 empty stub`; do not allow the browser to reach the public CDN and do not treat a network error as an acceptable test result. Verify that inline styles and the native fallback keep the page readable and persona controls functional, and require zero console errors throughout the checked interactions.

## Final Response

Report:

- Generated file links.
- Validation command and result.
- Visual preflight result.
- Browser verification result or limitation.
- Source links or paths used.
- One-sentence conclusion, terminal status, and confidence level.
- Key assumptions, residual Gaps, and confidence limits.

Do not paste the full HTML into the final chat response unless the user explicitly asks.
