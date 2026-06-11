# Issue 010 - Add ai-work-assetization-diagnoser

## Title

Add public-safe `ai-work-assetization-diagnoser` Router / Gate Skill

## Type

HITL

## Priority / Labels

P2

Suggested labels: `new-skill`, `router`, `governance`

## Source

- `docs/skill-boundary-and-loop-audit.md`
- `SKILL_ROUTING.md`
- `SKILL_REGISTRY.md`
- `ai-collaboration-calibration/references/modes/12-asset-capture.md`

## Problem

The repo has good Skill-to-Skill routing, but no public-safe Router / Gate that answers:

```text
Should this repeated AI work become a Prompt, Context Pack, Workflow, Skill, Loop, or System?
Should it be assetized at all?
What is the smallest useful next asset?
```

Some asset-capture ideas exist under calibration, but that is not a standalone assetization diagnosis workflow.

## What To Build

Create `ai-work-assetization-diagnoser/`.

Minimum files:

- `ai-work-assetization-diagnoser/SKILL.md`
- Optional `references/assetization-levels.md`
- Optional `references/examples.md`

Minimum behavior:

- Input: AI collaboration session, repeated task, prompt, workflow description, team use case, or trace of successful work.
- Output:
  - current maturity
  - recommended asset layer
  - reason
  - why not the adjacent layers
  - smallest next artifact
  - evaluation / reuse signal to watch
  - do-not-assetize cases
- Boundary:
  - It diagnoses and routes.
  - It does not replace creating the actual Skill / Workflow / Loop.
  - It does not expose private internal governance language unless rewritten public-safe.

Required catalog updates:

- README
- SKILL_REGISTRY.md
- SKILL_ROUTING.md
- install / quickstart docs if public distribution includes it

## Acceptance Criteria

- [ ] New Skill folder exists with valid `SKILL.md`.
- [ ] Frontmatter description is trigger-first and public-safe.
- [ ] It distinguishes Prompt / Context Pack / Workflow / Skill / Loop / System.
- [ ] It includes non-trigger cases.
- [ ] README / Registry / Routing are updated together.
- [ ] Existing Skill count badges are updated if this becomes public.

## Verification

Static:

```bash
test -f ai-work-assetization-diagnoser/SKILL.md
rg -n "ai-work-assetization-diagnoser|Prompt|Context Pack|Workflow|Skill|Loop|System" README.md SKILL_REGISTRY.md SKILL_ROUTING.md ai-work-assetization-diagnoser/SKILL.md
```

Smoke prompts:

- [ ] `这段工作是不是值得做成 Skill？`
- [ ] `这个 prompt 应该沉淀成 workflow 还是 Skill？`
- [ ] `我们连续三次做了类似 AI 协作，帮我判断该资产化到哪层。`
- [ ] `这只是一次性任务，不要过度沉淀。`

## Blocked By

- Issue 002
- Issue 003
- Issue 004
- Issue 007

## Open Questions

- Should this be public in this repo, or remain private/team-local?
- Should it be a full Skill or only a `docs/router-gate.md` guide first?
