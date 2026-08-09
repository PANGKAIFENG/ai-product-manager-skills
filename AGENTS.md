# Agent Orientation

This is a thin index for agents working in this repository. Read `SKILL_ROUTING.md`
before choosing between adjacent Skills and `SKILL_REGISTRY.md` for the public
catalog and boundaries.

## Role Model

| Role | Primary Skill |
| --- | --- |
| Framer | `ai-collaboration-calibration` |
| Researcher | `research-topic-compiler` / `decision-research` |
| Designer / Maker | `brainstorming` / `prd-architect` |
| Critic | `grill-me` |
| UI Handoff | `ui-mockup-desktop-workbench` |
| Reviewer | `prd-review` |
| Backlog Splitter | `prd-to-issues` |
| Customer Discovery | `customer-requirement-discovery` |
| Skill Governance | `team-skill-creator` / `skill-reviewer` |
| Engineering Context | `project-context-steward` / `agent-trace-diagnoser` |

## Loop And Workflow Index

Loop contracts live under `loops/` and coordinate state, return edges, and stop
conditions. Stage composition lives under `workflows/`:

- `decision-loop`
- `solution-loop`
- `delivery-loop`
- `problem-to-solution`
- `solution-to-delivery`

The two Workflows and three Loops expose explicit-only Codex Runtime adapters
through their co-located `SKILL.md` files. Use a Loop only when the user needs
multi-round state, resumability, or a repeated handoff. Do not run every Skill
in a Loop by default.

## External Writes

Only `tools/` publishers and automations own DingTalk/Yunxiao side effects. A
Skill handoff, Loop return edge, Workflow chain, or Manifest approval is not a
trusted host capability. Package mode is dry-run-only in the current Agent
runtime; real Package writes stop with `authorization_required`. Legacy direct
publishing remains a separate explicitly confirmed path, never a Package bypass.

## State Convention

Use `.loop-state/<loop-name>/` only when the user asks to save or resume state.
For chat-only work, keep the same fields in the response and do not create a
state folder.

## Catalog Update Rule

When adding or publicizing a Skill, update these coordinated surfaces together:

- `README.md`
- `SKILL_REGISTRY.md`
- `SKILL_ROUTING.md`
- `catalog/skills.yaml`
- `catalog/assets.yaml`
- install / quickstart docs
- examples or issue templates when relevant

Keep each stable Skill ID at `skills/<skill-id>/`. `archive/` is historical
material and is excluded from discovery and installation.
