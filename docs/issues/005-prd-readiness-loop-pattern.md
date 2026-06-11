# Issue 005 - Add PRD Readiness loop pattern

## Title

Add `loop-patterns/prd-readiness-loop.md` as the first multi-Skill loop pattern

## Type

HITL

## Priority / Labels

P1

Suggested labels: `loop-pattern`, `prd`, `workflow`

## Source

- `docs/skill-boundary-and-loop-audit.md`
- `prd-review/references/prd-readiness-loop-contract.md`
- `ai-collaboration-calibration/SKILL.md`
- `grill-me/SKILL.md`
- `decision-research/SKILL.md`
- `prd-architect/SKILL.md`
- `prd-review/SKILL.md`

## Problem

The current PRD Readiness Loop exists as a stateful extension under `prd-review`, but it does not describe the full multi-Skill workflow:

```text
problem framing -> solution pressure test -> optional decision research -> PRD drafting -> PRD review -> revision -> re-review -> readiness verdict
```

Without a first-class loop pattern, users and agents may treat PRD readiness as a single long `prd-review` run instead of a multi-Skill closed loop.

## What To Build

Create `loop-patterns/prd-readiness-loop.md` as a thin orchestration layer.

Minimum structure:

- Purpose
- When to use
- When not to use
- Node table:
  - `ai-collaboration-calibration` as Round 0 Framer / fallback
  - `grill-me` as solution Critic
  - optional `decision-research` for evidence-backed decisions
  - `prd-architect` as Maker / reviser
  - `prd-review` as Reviewer / readiness Gate
- Entry criteria
- Exit criteria
- State references
- Shared state directory convention, for example `.loop-state/prd-readiness/`
- Handoff payload fields
- Stop conditions
- Divergence protection:
  - maximum review rounds
  - blocker count not decreasing for N rounds -> human decision
- Relationship to existing parent contract

Do not move or rewrite `prd-review/references/prd-readiness-loop-contract.md`.

## Acceptance Criteria

- [ ] `loop-patterns/prd-readiness-loop.md` exists.
- [ ] It references but does not replace `prd-review/references/prd-readiness-loop-contract.md`.
- [ ] It includes all five relevant Skills with roles and entry/exit conditions.
- [ ] It defines a minimal Critic Handoff from `grill-me`.
- [ ] It defines readiness exits:
  - `Ready for writing-plans`
  - `Ready with assumptions`
  - `Not ready`
  - `Human decision required`
- [ ] It includes anti-over-looping guidance.

## Verification

Static checks:

```bash
test -f loop-patterns/prd-readiness-loop.md
rg -n "ai-collaboration-calibration|grill-me|decision-research|prd-architect|prd-review|Ready for writing-plans|Human decision" loop-patterns/prd-readiness-loop.md
```

Manual workflow check:

- [ ] Given a fuzzy idea, the loop starts with calibration.
- [ ] Given a concrete but risky solution, the loop can start with grill-me.
- [ ] Given a PRD draft, the loop can enter directly at prd-review.
- [ ] A PRD revision returns to prd-review for recheck.
- [ ] The loop has a hard stop when blockers do not converge.

## Blocked By

- Issue 002
- Issue 003

## Open Questions

- Should the shared state directory be `.loop-state/prd-readiness/` or a docs-local convention such as `docs/loop-state/prd-readiness/`?
