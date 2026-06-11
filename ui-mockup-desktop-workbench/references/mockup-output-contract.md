# Mockup Output Contract

Use this contract when packaging a desktop workbench UI mockup, high-fidelity visual handoff, or project-native preview.

The durable deliverable is the UI implementation contract. HTML is one possible visual carrier, not the source of truth for frontend implementation.

## Mode-Specific Artifact Sets

### `project-native-preview`

Use when a real frontend project path is available and the user wants development to reproduce the UI.

Create or update:

- `README.md` or handoff note: purpose, source inputs, preview route, assumptions, open/run instructions, and verification notes.
- `screen-contract.md`: screens, states, PRD traceability, UI spec traceability, and open questions.
- `component-map.md`: production component/style/token mapping for each key UI element.
- `implementation-notes.md`: files to modify, data/state sources, events, migration notes, and preview-to-production plan.
- Project-native preview route, story, fixture state, or preview component.
- `screenshots/`: browser screenshots at required desktop viewports when feasible.

### `visual-handoff`

Use when the PRD is stable and frontend needs high-fidelity guidance, but direct project integration is not requested or is too risky.

Create:

- `README.md` or handoff note.
- `screen-contract.md`.
- `component-map.md`.
- `implementation-notes.md`.
- `mockup.html` or high-fidelity React artifact.
- `screenshots/` when feasible.

The visual artifact must be labeled as a reference, not production implementation.

### `concept-html`

Use only for early layout or product discussion.

Create:

- `README.md`.
- `screen-contract.md`.
- `mockup.html`.
- Optional screenshots.

Component mapping and implementation notes are optional only when the user explicitly says this is not for frontend implementation.

## Default Artifact Set

When the user does not specify a project-native destination, create a small artifact folder with:

- `README.md`: purpose, source inputs, assumptions, open/run instructions, and verification notes.
- `screen-contract.md`: screens, states, PRD traceability, UI spec traceability, and open questions.
- `component-map.md`: required for implementation-oriented runs; optional only for early concept runs.
- `implementation-notes.md`: required for implementation-oriented runs; optional only for early concept runs.
- `mockup.html`: standalone desktop mockup with embedded CSS and minimal embedded JS only if needed.
- `screenshots/`: optional browser screenshots when generated.

If integrating into an existing app, adapt the names to the repo convention and still include a handoff note.

## README Requirements

Include:

- Source PRD path or "pasted by user".
- Source UI spec path or "not provided".
- Target viewport and format.
- Output mode: `project-native-preview`, `visual-handoff`, or `concept-html`.
- Real frontend project path or "not provided".
- Discovered UI constraints summary, including component library, token/style source, icon source, and route/shell evidence.
- How to open or run.
- What screens/states are included.
- Verification performed.
- Known assumptions and unresolved conflicts.
- Migration boundary: what is production-aligned and what is visual-only.

## Screen Contract Requirements

For each screen or page, include:

| Screen | Purpose | Key regions | States covered | PRD source | UI spec source | Notes |
| --- | --- | --- | --- | --- | --- | --- |

Keep entries concrete. "Dashboard" is weaker than "Agent execution workbench with running task and artifact preview".

For each important state, include:

| State | Trigger | Visible regions | Primary actions | Recovery/next state | PRD source | Notes |
| --- | --- | --- | --- | --- | --- | --- |

Cover relevant states:

- Empty or first-run.
- Draft input.
- Queued/starting.
- Running/streaming/progress.
- Stop/cancel/interrupted.
- Success/result.
- Partial failure.
- Error/retry.
- Permission/login/connection.
- Settings/menu/modal open states.

## Component Map Requirements

For implementation-oriented runs, create `component-map.md` with:

| UI element | Production component/style source | Reuse/new/modify | Related files | States | Notes |
| --- | --- | --- | --- | --- | --- |

Rules:

- Map every key region: app shell, navigation, session/task list, composer/input, buttons, menus, modals, avatar/settings popover, artifact panel, status indicators, empty states, error/retry states, and download/export actions when present.
- Use real component names, style class names, token files, or file paths when discovered.
- If the component does not exist, write `New component needed` and explain why.
- Do not present standalone HTML classes as production components.
- Call out icon source and whether icons must be reused or newly created.

## Implementation Notes Requirements

For implementation-oriented runs, create `implementation-notes.md` with:

- Recommended files to add or modify.
- Recommended components to reuse.
- Recommended new components and their props/state.
- State/data sources and event handlers.
- Feature flags, preview route, or fixture strategy.
- Preview-to-production conversion steps.
- Testing or screenshot verification plan.
- Parts of the mockup that should not be copied into production.

For a project-native preview, also include cleanup/turn-into-production guidance so preview-only routes or fixture data do not leak into the product.

## HTML Mockup Requirements

A standalone `mockup.html` should:

- Open directly in a browser without a build step.
- Use semantic regions when practical: `nav`, `main`, `aside`, `section`, `header`.
- Use CSS variables for colors, spacing, radius, and typography.
- Include realistic domain copy and data from the PRD.
- Include visible state variations, either in one composed page or through tabs/segmented controls.
- Avoid external network assets unless the user provided them or explicitly asked.
- Keep all text readable at desktop viewports around 1440x900 and 1280x800.
- Use bounded layout dimensions and scroll containers so panels do not overlap.

Do not ship a blank frame, placeholder lorem ipsum, or a purely skeletal wireframe unless the user explicitly asked for low fidelity.

When the result is for implementation alignment:

- Label the HTML as visual reference.
- Avoid fake production component names.
- Keep token names and comments traceable to the component map.
- Do not claim the HTML/CSS is directly reusable unless it imports or uses the real project system.

## Project-Native Preview Requirements

A project-native preview should:

- Follow local framework and routing conventions.
- Use real components, token files, icon imports, layout shell, and CSS modules/LESS/Tailwind conventions.
- Use fixture data or a preview-only state path that is easy to remove or convert.
- Avoid wiring preview-only data into production runtime or API flows.
- Include a clear route or command to open the preview.
- Preserve unrelated product files and existing behavior.
- Include screenshots from the running app when feasible.

## Verification Requirements

Minimum verification:

- Confirm expected deliverables exist and are non-empty.
- Open or render it if browser tooling is available.
- Check desktop viewport layout around 1440x900.
- Check narrower desktop viewport around 1280x800.
- Check console errors if using JavaScript.
- For project-native preview, run the local app or the closest available build/type/lint command when feasible.
- Verify `component-map.md` does not contain only generic HTML classes when implementation alignment is expected.

If browser tooling is unavailable, record that limitation and run deterministic checks such as file existence, HTML structure grep, and CSS sanity checks.

## Final Response Requirements

Return:

- Files created or modified.
- Source PRD and UI spec used.
- Output mode.
- Screens and states included.
- Component map and implementation notes status.
- Verification commands and results.
- Assumptions and unresolved questions.
- Whether the result is concept-only, visual handoff, project-native preview, or ready for production integration.

## Regression Checklist

Before declaring done, check:

- Did the UI spec override generic visual instincts?
- Did project-local design discovery happen before visual implementation when a project path was available?
- Was the chosen output mode correct for the user's intent?
- Did the mockup include the desktop workbench shell where appropriate?
- Did it include at least one non-happy-path state?
- Did implementation-oriented output include `screen-contract.md`, `component-map.md`, and `implementation-notes.md`?
- Did standalone HTML clearly state its migration boundary?
- Did it avoid landing-page hero composition?
- Did it avoid nested cards and decorative gradient filler?
- Did it preserve readable text and stable dimensions?
- Did it avoid modifying unrelated product files?
