# HTML Dashboard Template

## Required Libraries

Use these CDN patterns unless the user requires offline assets:

```html
<script src="https://cdn.tailwindcss.com"></script>
<script defer src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js"></script>
```

## Required Structure

The generated file should have this shape:

```html
<main data-concept-lens x-data="dashboardData()">
  <section>
    <!-- Essence statement and concept metadata -->
  </section>

  <section data-concept-lineage>
    <!-- Origin context, original use, semantic shifts, and current drift -->
  </section>

  <nav data-stage-tabs>
    <!-- Timeline or tab buttons bound with Alpine -->
  </nav>

  <section>
    <!-- Active stage detail -->
  </section>

  <section data-debt-detector>
    <!-- Anti-pattern cards -->
  </section>

  <section data-sources>
    <!-- Source list -->
  </section>
</main>
```

## Component Requirements

Page shell:

- The first viewport should feel like a decision dashboard, not a marketing landing page.
- Show the concept essence, confidence/source status, lineage signal, and stage navigation early.
- Keep the page width constrained with a stable max-width and predictable gutters.

Concept lineage:

- Show origin context, original problem, original users or use case, major semantic shifts, and current usage drift.
- Distinguish sourced history from inference or uncertain origin claims.
- Keep lineage concise enough to orient the stage matrix; do not turn it into a full chronology article.
- Make it visibly separate from the stage tabs so readers know it is the calibration layer behind the matrix.

Stage navigation:

- Use stable buttons with fixed spacing.
- Show active stage clearly.
- Do not resize the page when switching stages.

Stage detail:

- Show the five PM matrix dimensions.
- Keep review questions copyable.
- Use concise but specific prose.

Debt detector:

- Show symptom, root mismatch, false fix, breakthrough, and PM question.
- Make it visually distinct from the stage matrix.

Sources:

- Include title, URL, and claim area supported.
- Keep URLs clickable.

## Design Rules

- Read `design-quality.md` before composing visual style.
- Use a restrained professional interface, not a marketing landing page, portfolio, or decorative artifact.
- Avoid decorative gradient blobs, oversized hero sections, generic glassmorphism, nested cards, and repeated three-card feature rows.
- Keep text readable on mobile and desktop; button labels and tab labels must not wrap awkwardly or hide meaning.
- Use icons only when available from simple text or CSS-safe symbols; do not depend on icon packages.
- Prefer dense, scan-friendly panels for PM work, with a clear typography hierarchy and one consistent accent color.
- Surface sources and uncertainty as first-class interface elements.

## Visual Preflight

Before final delivery, verify:

- Desktop and mobile layouts show no overlap or horizontal overflow.
- Stage switching does not cause large layout jumps.
- Copy feedback is visible and does not resize buttons.
- Debt detector cards are visually distinct from stage-detail panels.
- Source links are visible, clickable, and readable.
- The page avoids one-note slate/blue or purple-gradient styling unless the concept or brand justifies it.

## Copy Button Pattern

Use Alpine state for copy feedback:

```html
<button
  type="button"
  @click="navigator.clipboard.writeText(question); copied = question"
  class="..."
>
  <span x-text="copied === question ? '已复制' : '复制'"></span>
</button>
```

Include a fallback note if clipboard permissions fail only when implementing custom JavaScript beyond Alpine's inline handler.
