# Agent Orientation

This is a thin index for agents working in this repository. It does not replace `README.md`, `SKILL_REGISTRY.md`, or `SKILL_ROUTING.md`.

## Start Here

1. Read `SKILL_ROUTING.md` before choosing between adjacent Skills.
2. Use `SKILL_REGISTRY.md` for catalog status, Chinese names, and public boundaries.
3. Use `README.md` for human-facing workflow orientation.
4. Load only the relevant Skill and reference files for the user's current stage.

## Role Model

| Role | Primary Skill |
| --- | --- |
| Framer | `ai-collaboration-calibration` |
| Researcher | `research-topic-compiler` / `decision-research` |
| Maker | `prd-architect` |
| Critic | `grill-me` |
| Reviewer | `prd-review` |
| Backlog Splitter | `prd-to-issues` |
| UI Mockup Maker | `ui-mockup-desktop-workbench` |
| Router / Gate | `ai-work-assetization-diagnoser` |

## Loop Pattern Index

Loop patterns are orchestration docs, not new Skills:

- `loop-patterns/prd-readiness-loop.md`
- `loop-patterns/decision-research-loop.md`
- `loop-patterns/research-radar-loop.md`

Use loop patterns only when the user needs multi-round state, resumability, readiness convergence, or a repeated handoff between Skills.

## State Convention

Use `.loop-state/<loop-name>/` only when the user asks to save or resume state. For chat-only work, keep the same fields in the response.

Do not create state folders for ordinary one-pass tasks.

## Stop And Human Handoff

Stop and ask the user when:

- A business or product owner decision is missing.
- Two loop rounds fail to reduce blockers.
- A recommendation has high product, legal, financial, or engineering impact.
- A required private, paid, logged-in, or customer-specific source needs authorization.
- The task is becoming a system build, not a Skill run.

## Anti-Over-Looping

- Route by current workflow stage, not keyword alone.
- Do not run every Skill in a loop by default.
- Do not let a Critic Skill hold long-running state.
- Do not let a Maker Skill self-approve readiness.
- Do not hide unresolved decisions inside implementation planning.

## Catalog Update Rule

When adding or publicizing a Skill, update the coordinated surfaces together:

- `README.md`
- `SKILL_REGISTRY.md`
- `SKILL_ROUTING.md`
- install / quickstart docs
- examples or issue templates when relevant

Keep root-level Skill folder names stable. The flat namespace is the public invocation surface.
