# Vertical Slice Rules

Use these rules when drafting implementation issues from PRDs.

## Core Rule

Each issue should deliver one narrow but complete path through the product. A completed issue should be demoable or verifiable by itself.

Good slices usually include enough of:

- Data shape or persistence.
- API or service behavior.
- UI or user-visible workflow.
- Error, empty, or permission states.
- Tests or verification steps.

Do not require every issue to touch every layer. Require every issue to produce an independently verifiable behavior.

## AFK vs HITL

Use `AFK` when an implementation agent can complete and verify the issue without additional human judgment.

Use `HITL` when the issue depends on:

- Product scope choice.
- UX or visual design approval.
- Architecture decision.
- Data migration or release decision.
- Security, compliance, legal, or customer-specific approval.
- Ambiguous business rule.

Prefer AFK where possible, but do not hide uncertainty by marking uncertain work as AFK.

## Dependency Rules

- Create blockers first.
- Prefer shallow dependency graphs.
- If many issues depend on one unresolved decision, create one HITL clarification issue first.
- Do not create artificial dependencies just because implementation order is convenient.

## Anti-Patterns

Avoid these issue shapes:

- `Build backend`
- `Build frontend`
- `Add tests`
- `Refactor module`
- `Integrate everything`
- `Polish UI`
- `Handle edge cases`

These are horizontal layers or vague buckets. Replace them with end-to-end behaviors:

- `Create saved search and show it in the sidebar`
- `Reject duplicate invite and surface the existing member`
- `Generate proposal draft and require user confirmation before export`

## Size Heuristics

A good issue is usually:

- Small enough for one focused implementation pass.
- Large enough to be meaningful when merged.
- Has 2-6 acceptance criteria.
- Has one primary user-visible or system-visible outcome.

Split an issue when it has multiple independent outcomes, multiple unrelated user stories, or more than one major unresolved risk.

Merge issues when each part cannot be verified alone or when the split only follows technical layers.
