# Desktop Workbench UI Principles

Use this reference when producing realistic desktop Agent workbench mockups.

## Product Shape

A desktop workbench is an operational surface. It should help users repeatedly inspect, decide, execute, recover, and export. It is not a landing page, a campaign page, or a decorative dashboard.

Default mental model:

- Left rail: product navigation, workspace switcher, account, global create action.
- Task/session rail: recent tasks, queues, filters, pinned work, status counts.
- Center: execution canvas, conversation, plan, logs, editor, or primary work state.
- Right panel: artifact preview, inspector, resources, citations, settings, version history, or handoff actions.

Use the four-zone shell when it matches the PRD. Collapse or merge zones only when the workflow is simpler.

## Information Architecture

Start with user jobs, not widgets:

1. What work is the user trying to start?
2. What in-progress work needs monitoring?
3. What outputs must be inspected or edited?
4. What decisions or confirmations block progress?
5. What needs to be exported, copied, saved, or handed off?

Every major UI region should answer one of those questions.

## Required States

For Agent workbench mockups, cover the states that affect trust:

- First-run empty state with a clear start action.
- Draft or unsent input state.
- Queued or starting state.
- Streaming/running state with visible progress, logs, or current step.
- Completed state with artifact preview and next actions.
- Partial result state when some tools or assets fail.
- Error state with retry, inspect details, or fallback.
- Permission/login/connection state when the PRD mentions accounts, local runtime, APIs, or workspace access.

Do not hide failures in generic toast-only UI. Put recoverable errors near the affected task, artifact, or execution stream.

## Density And Layout

Desktop workbenches should support scanning:

- Use compact but readable rows, tabs, segmented controls, and grouped settings.
- Prefer persistent navigation and persistent context over giant page headers.
- Keep primary controls close to the region they affect.
- Use fixed or bounded rail widths so content does not jump.
- Make scroll containers explicit: task rail scrolls independently from execution canvas and artifact panel.
- Avoid nested cards. Use cards only for repeated items, modals, or contained artifacts.

Typical desktop constraints:

- Left nav: 64-240px depending on icon-only vs labeled.
- Task/session rail: 260-360px.
- Center execution area: flexible, min 480px.
- Right panel: 320-460px.
- Top bars: 48-64px.

These are defaults, not mandates. Follow the UI spec when it gives stronger constraints.

## Visual Quality

Use the UI spec as the visual source of truth. If no spec exists:

- Choose a restrained, operational palette with semantic status colors.
- Avoid a one-note purple, dark-blue, beige, or brown theme.
- Use contrast, spacing, and typography for hierarchy before adding decoration.
- Use icons for tool actions when a library exists.
- Keep text labels short enough for narrow rails.
- Avoid fake glassmorphism, oversized glowing gradients, and marketing-style hero blocks.

For product-facing desktop tools, "polished" usually means precise alignment, readable state hierarchy, clear affordances, and realistic data.

## Screen Types

### Main Workbench

Must show:

- Global navigation and current workspace.
- Task/session list with statuses.
- Primary execution area with user input, agent progress, and result.
- Artifact/resource panel with preview, metadata, and actions.

### Task List

Must support:

- Status filters or grouping.
- Recent and pinned work.
- Clear status labels for running, failed, completed, draft, and waiting.
- Empty and no-results states.

### Execution Area

Must support:

- Current step or plan.
- User input or command composer.
- Running progress and interruptions.
- Inline failures and retry.
- Final output summary and next action.

### Artifact Page Or Panel

Must support:

- Preview of the deliverable.
- Version, source, timestamp, or provenance.
- Export/copy/open actions.
- Warnings when output is incomplete.

### Settings Page

Must support:

- Grouped controls and clear save/reset behavior.
- Account, runtime, model, workspace, privacy, and notification sections when relevant.
- Connection status and validation feedback.

## Traceability

Every screen in the mockup should be traceable to:

- A PRD requirement or workflow.
- A UI spec rule or explicit assumption.
- A user-visible state.

If a screen cannot be traced, either remove it or label it as an exploratory assumption.
