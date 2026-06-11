# Mockup Output Contract

Use this contract when packaging a desktop workbench UI mockup.

## Default Artifact Set

When the user does not specify a project-native destination, create a small artifact folder with:

- `README.md`: purpose, source inputs, assumptions, open/run instructions, and verification notes.
- `screen-contract.md`: screens, states, PRD traceability, UI spec traceability, and open questions.
- `mockup.html`: standalone desktop mockup with embedded CSS and minimal embedded JS only if needed.
- `screenshots/`: optional browser screenshots when generated.

If integrating into an existing app, adapt the names to the repo convention and still include a handoff note.

## README Requirements

Include:

- Source PRD path or "pasted by user".
- Source UI spec path or "not provided".
- Target viewport and format.
- How to open or run.
- What screens/states are included.
- Verification performed.
- Known assumptions and unresolved conflicts.

## Screen Contract Requirements

For each screen or page, include:

| Screen | Purpose | Key regions | States covered | PRD source | UI spec source | Notes |
| --- | --- | --- | --- | --- | --- | --- |

Keep entries concrete. "Dashboard" is weaker than "Agent execution workbench with running task and artifact preview".

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

## Verification Requirements

Minimum verification:

- Confirm the mockup file exists and is non-empty.
- Open or render it if browser tooling is available.
- Check desktop viewport layout around 1440x900.
- Check narrower desktop viewport around 1280x800.
- Check console errors if using JavaScript.

If browser tooling is unavailable, record that limitation and run deterministic checks such as file existence, HTML structure grep, and CSS sanity checks.

## Final Response Requirements

Return:

- Files created or modified.
- Source PRD and UI spec used.
- Screens and states included.
- Verification commands and results.
- Assumptions and unresolved questions.
- Whether the result is a mockup only or ready for production integration.

## Regression Checklist

Before declaring done, check:

- Did the UI spec override generic visual instincts?
- Did the mockup include the desktop workbench shell where appropriate?
- Did it include at least one non-happy-path state?
- Did it avoid landing-page hero composition?
- Did it avoid nested cards and decorative gradient filler?
- Did it preserve readable text and stable dimensions?
- Did it avoid modifying unrelated product files?
