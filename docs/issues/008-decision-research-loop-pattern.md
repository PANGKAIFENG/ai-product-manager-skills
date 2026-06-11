# Issue 008 - Add Decision Research loop pattern

## Title

Add `loop-patterns/decision-research-loop.md` with optional Critic checkpoints

## Type

HITL

## Priority / Labels

P2

Suggested labels: `loop-pattern`, `research`, `decision`

## Source

- `docs/skill-boundary-and-loop-audit.md`
- `decision-research/references/decision-loop-contract.md`
- `decision-research/SKILL.md`
- `grill-me/SKILL.md`
- `ai-collaboration-calibration/SKILL.md`

## Problem

`decision-research` has the strongest single-Skill loop contract in the repo. It already has research map, hypothesis matrix, evidence table, assumption ledger, scope drift log, conclusion version, convergence conditions, ROI fuse, and Human Gate.

What is missing is a thin multi-Skill pattern that defines when an external Critic (`grill-me`) should challenge the research design or interim conclusion.

## What To Build

Create `loop-patterns/decision-research-loop.md`.

Minimum structure:

- Purpose
- When to use
- When not to use
- Node table:
  - optional `ai-collaboration-calibration` entry when decision question is fuzzy
  - `decision-research` as loop owner
  - optional `grill-me` checkpoint after Research Map
  - optional `grill-me` checkpoint before final recommendation for high-risk decisions
- State references to `decision-research/references/decision-loop-contract.md`
- Critic Handoff fields
- Stop conditions:
  - recommendation
  - PoC needed
  - insufficient evidence
  - user decision required
  - stop due to low ROI
- Guardrail: do not force grill-me into every research run.

## Acceptance Criteria

- [ ] `loop-patterns/decision-research-loop.md` exists.
- [ ] It references the existing decision loop contract instead of duplicating it.
- [ ] It includes optional Critic checkpoints.
- [ ] It states when Critic checkpoints should be skipped.
- [ ] It preserves `decision-research` ownership of final recommendation.

## Verification

```bash
test -f loop-patterns/decision-research-loop.md
rg -n "decision-research|grill-me|Research Map|Critic|recommendation|PoC|Human Gate" loop-patterns/decision-research-loop.md
```

Manual workflow check:

- [ ] Low-risk factual selection can run only `decision-research`.
- [ ] High-risk product direction can insert grill-me after Research Map.
- [ ] Final recommendation still comes from `decision-research`.

## Blocked By

- Issue 004
- Issue 005 is recommended first to establish loop-pattern style.

## Open Questions

- What threshold makes a decision “high risk” enough to require the second Critic checkpoint?
