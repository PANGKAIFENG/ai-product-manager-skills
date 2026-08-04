# Dashboard Design Quality

This reference adapts only the useful design discipline from high-taste frontend skills. Do not turn the output into a landing page, portfolio, or cinematic marketing site. The deliverable is a PM decision dashboard for understanding a complex concept.

## Design Read

Before writing HTML, internally decide:

- Audience: PM, founder, technical lead, buyer, or executive reader.
- Work mode: learning, review, vendor evaluation, architecture challenge, or strategy decision.
- Density: usually medium-high; optimize for scanning and comparison, not dramatic whitespace.
- Tone: restrained, sharp, credible, source-aware.

If the user asks for a special visual direction, adapt it only when it does not reduce readability or source traceability.

## Baseline Style

- Prefer a quiet neutral base with one purposeful accent color. Avoid default AI purple/blue gradients unless the concept or brand requires them.
- Use 8px or smaller radii for dashboard panels unless a stronger local visual rule is chosen and applied consistently.
- Use cards only for repeated stage, debt, or source units. Do not put page sections inside floating cards, and do not nest cards inside cards.
- Use borders, dividers, subtle tinted backgrounds, and typographic hierarchy before reaching for shadows.
- Keep the first viewport useful: concept essence, stage navigation, and one decision-relevant signal should be visible without a marketing hero.

## Typography

- Use a clear sans stack and a mono style for formulas, code, metrics, stage IDs, or technical terms.
- Display text should be compact. Avoid hero-scale headings inside panels.
- Body copy should stay readable: short paragraphs, stable line height, and max-width constraints for long prose.
- Enable tabular figures for metrics or stage numbers when feasible with CSS.
- Avoid repetitive uppercase eyebrow labels. Use them only where they help navigation.

## Layout

- Build from an information hierarchy: essence, stage map, active stage detail, debt detector, review script, sources.
- Use CSS Grid for multi-column comparison. Avoid fragile flex percentage math.
- Keep stage tabs stable: switching tabs must not resize the control area or shift the page unexpectedly.
- On desktop, show comparison and diagnosis side by side where useful. On mobile, collapse to one column with clear section boundaries.
- Do not create a left sidebar by default. Use top tabs or compact segmented controls unless the concept genuinely has many persistent filters.

## Color And Surfaces

- Pick one accent and reuse it consistently for active state, key callouts, and copy actions.
- Use semantic colors sparingly: danger for debt or mismatch, success for mature patterns, warning for uncertainty.
- Never rely on color alone. Pair color with labels, borders, icons made from text/CSS, or structural placement.
- Avoid one-hue dashboards made only from slate/blue variants. Add a small, controlled secondary neutral or semantic tint when it clarifies meaning.
- Button and badge text must maintain readable contrast.

## Interactions

- Implement hover, active, and focus states for tabs, copy buttons, and debt cards.
- Copy buttons should provide visible feedback without layout shift.
- Keep animation subtle and optional. Motion should clarify state changes, not perform.
- Do not import icon or motion packages for a self-contained artifact unless the user explicitly asks.

## Source And Claim Clarity

- Sources are part of the interface, not an appendix afterthought.
- Every stage should make clear which claims are evidence-backed, inferred, or assumption-based.
- The sources section should show title, URL, claim area, and why the source matters.
- Use uncertainty labels for weak or changing claims.

## Visual Preflight

Before final delivery, check the generated dashboard against this list:

- First viewport is a dashboard, not a marketing hero.
- No decorative blobs, generic glassmorphism blanket, random gradients, or stock-like atmospheric imagery.
- No nested cards or repeated three-card feature rows unless the content is truly repeated units.
- Stage tabs, copy buttons, debt detector, and sources are visible and readable on desktop and mobile.
- Text does not overlap, truncate important meaning, or overflow buttons.
- Active, hover, focus, empty, and copied states are represented where relevant.
- The color system has one clear accent, readable contrast, and no default AI-gradient palette.
- Source links are clickable and visually findable.
