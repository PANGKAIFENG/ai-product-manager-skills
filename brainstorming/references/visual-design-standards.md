# Visual Design Standards

Use this reference when `brainstorming` discusses UI, page structure, desktop/workbench surfaces, HTML mockups, visual companion artifacts, or handoff into a UI mockup Skill.

## Core Rule

Project-local design language wins. Before generating a UI, mockup, or HTML artifact, inspect the target project for existing visual conventions and summarize them. Only use default standards after confirming that local standards are unavailable or too incomplete for the task.

## Design Discovery Gate

Inspect the most relevant available materials:

- Project stack: `package.json`, app package files, `nuxt.config`, `vite.config`, `next.config`, `tailwind.config`, `unocss.config`, theme providers.
- Global styles: `assets/styles`, `styles`, `globals.css`, `variables.less`, `variables.scss`, CSS variables, Less/Sass variables, reset files.
- Tokens and themes: color tokens, typography, spacing scale, radius, shadows, dark/light theme classes, density settings.
- Component system: Ant Design, MUI, Radix, shadcn, Element, Naive, internal `components/`, modal/drawer/table/form/button patterns.
- Icon system: lucide, Iconify, Ant icons, SVG sprite, internal `SvgIcon`, asset naming and sizing.
- Target surface: route/page shell, left navigation, top toolbar, side panels, cards, tables, composer, canvas/work area, artifact pane.
- Adjacent UI states: empty, loading, busy, streaming, progress, error, retry, disabled, permission, auth, session switch, upload, download.
- Existing product evidence: PRD, docs, screenshots, current mockups, storybook, Figma notes, README/PROJECT_MAP.

Before drawing or writing HTML, output a compact design constraint summary:

```markdown
**Visual Constraints**
- Product surface:
- Local UI stack:
- Layout shell:
- Tokens / palette:
- Typography:
- Components to reuse:
- Required states:
- Gaps / assumptions:
```

## When Local Standards Exist

- Reuse local tokens and component proportions before inventing new colors, radius, shadows, or spacing.
- Match the product density. Operational tools should be scan-friendly and compact; consumer/marketing pages can be more expressive only when that is the actual surface.
- Match the existing navigation model and page chrome. Do not replace a real sidebar/topbar/workbench shell with a decorative landing page.
- Prefer the project's icon system. If none exists, use familiar icons from the available library instead of text-only tool buttons.
- If the existing product has dark/light modes, follow the requested mode; otherwise choose the mode that matches the current product surface. For enterprise SaaS and admin mockups, prefer light mode unless the project clearly defaults to dark.

## Default Standards

Use these only when project-local standards are missing.

### SaaS / Admin Workbench

- Light, neutral, dense, work-focused.
- Persistent navigation, clear page title area, filters/actions near the data they affect.
- 4/8px spacing rhythm, 14px body text, 16-20px compact headings, card radius <= 8px.
- Tables, lists, segmented controls, status tags, drawers and modals should feel production-like.
- Avoid marketing hero sections, decorative cards, decorative gradients, and nested cards.

### Desktop Agent Workbench

- App-like shell with fixed sidebar, conversation/session list when needed, main transcript/work area, bottom composer, and optional artifact pane.
- Stable dimensions for sidebars, icon buttons, composer, result cards and artifact thumbnails.
- Cover empty, busy, streaming, tool-call/progress, result/artifact, error/retry and disabled states.
- Keep controls close to the workflow: workspace selector, model/skill selector, attach, send/stop, artifact actions.
- Prefer quiet surfaces and high information density over large promotional copy.

### Research Dashboard

- Lead with the decision or insight, then expose evidence, filters and confidence.
- Use tables, timelines, matrices and comparison views before decorative cards.
- Color encodes status/category/confidence; never rely on color alone.
- Include decision basis, last updated, confidence or assumption status when the workflow needs traceability.
- Keep chart titles specific and conclusion-oriented.

### Marketing / Consumer

- Use only when the requested surface is actually public-facing, branded, consumer or conversion-oriented.
- First viewport must show the brand/product/object directly, ideally with relevant imagery.
- Copy can be larger and more emotional, but conversion path, pricing, proof, cases and next action must be clear.
- Mobile first viewport should hint at the next section, not trap the user in a full-screen poster.

## Mockup Quality Gate

Before saying a visual artifact is ready, check:

1. The page type, target user, primary workflow and required states are explicit.
2. Local visual constraints or the selected default standard are named.
3. Layout has stable dimensions and responsive constraints for sidebars, toolbars, grids, buttons, cards, tables and panes.
4. Text does not overflow buttons, cards, sidebars, table cells or mobile widths.
5. UI elements do not overlap at common desktop and mobile widths.
6. Color contrast is readable; status information is also expressed through text, labels or icons.
7. Cards are not nested inside cards unless the product system already uses that exact pattern.
8. SaaS, admin and workbench surfaces avoid decorative blobs, generic AI gradients and marketing-style hero layouts.
9. Interactive controls show or specify hover, disabled, loading and error states when relevant.
10. If an HTML mockup is generated and a browser is available, verify it with screenshots rather than judging from code alone.

## When To Ask

Ask one concise question only when the visual direction would materially change based on the answer, for example:

- The project has both dark and light modes and the requested target mode is unclear.
- Multiple product shells exist and the target route/surface is ambiguous.
- The user asks for visual polish but no PRD, workflow, target user or page states are available.
