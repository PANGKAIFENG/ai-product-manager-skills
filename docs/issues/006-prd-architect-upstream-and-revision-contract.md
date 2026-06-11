# Issue 006 - Add prd-architect upstream and revision contract

## Title

Add upstream prerequisites and revision handoff contract to `prd-architect`

## Type

AFK

## Priority / Labels

P2

Suggested labels: `prd`, `skill-boundary`, `documentation`

## Source

- `docs/skill-boundary-and-loop-audit.md`
- `prd-architect/SKILL.md`
- `prd-review/SKILL.md`

## Problem

`prd-architect` correctly owns PRD creation and revision, but its upstream input maturity assumptions are not explicit enough.

It should make clear:

- fuzzy problem -> first use `ai-collaboration-calibration`
- concrete solution that needs pressure testing -> use `grill-me`
- major product / technical decision without evidence -> use `decision-research`
- revision feedback from `prd-review` can be consumed as a patch source

## What To Change

- In `prd-architect/SKILL.md`:
  - Add upstream prerequisites / transfer rules.
  - Add a section such as `Revision Input Contract`.
  - State that it can consume `prd-review` revision drafts, findings, and open questions.
  - State that it should not self-approve readiness; readiness verdict belongs to `prd-review`.

## Acceptance Criteria

- [ ] `prd-architect/SKILL.md` references `ai-collaboration-calibration`, `grill-me`, `decision-research`, and `prd-review` in boundary context.
- [ ] It states that `prd-review` owns readiness verdict.
- [ ] It defines how to use review feedback for PRD revision.
- [ ] It does not add heavy new workflow or duplicate `prd-review` responsibilities.

## Verification

```bash
rg -n "ai-collaboration-calibration|grill-me|decision-research|prd-review|readiness|revision" prd-architect/SKILL.md
```

Manual smoke tests:

- [ ] `帮我写 PRD，但我还没想清问题。` -> suggests calibration or asks minimal clarifications.
- [ ] `基于这份 review findings 修 PRD。` -> prd-architect accepts revision input.
- [ ] `这个 PRD 能不能进开发？` -> routes to prd-review for verdict.

## Blocked By

- Issue 005 is recommended first if the revision contract should align with loop-pattern terminology.

## Open Questions

None.
