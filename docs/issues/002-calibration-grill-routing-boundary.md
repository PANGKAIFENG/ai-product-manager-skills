# Issue 002 - Add calibration and grill-me boundary handoff

## Title

Clarify `ai-collaboration-calibration` vs `grill-me` routing and handoff

## Type

HITL

## Priority / Labels

P1

Suggested labels: `skill-boundary`, `routing`, `documentation`

## Source

- `docs/skill-boundary-and-loop-audit.md`
- `ai-collaboration-calibration/SKILL.md`
- `grill-me/SKILL.md`
- `SKILL_ROUTING.md`

## Problem

Both Skills can be triggered by “挑战假设”, “方案是不是想错了”, “压力测试”, or “哪里不对劲”.

The intended boundary is valid:

- `ai-collaboration-calibration`: challenge problem definition before the solution is stable.
- `grill-me`: pressure-test an existing solution, plan, architecture, or decision.

But the boundary is not encoded strongly enough in the Skill files. `ai-collaboration-calibration` currently routes “已有方案，想压力测试” into its own failure-premortem mode, which can steal work from `grill-me`.

## What To Change

- In `ai-collaboration-calibration/SKILL.md`:
  - Clarify that failure-premortem is only for problem-definition risk sensing.
  - Add a transfer rule: if the problem is defined and the user has a concrete solution, use `grill-me`.
  - Tighten trigger wording around “挑战假设” so it means problem-level assumptions.
- In `grill-me/SKILL.md`:
  - Add a non-trigger rule: if the user does not yet know the real problem, use `ai-collaboration-calibration`.
  - Add a Context Intake rule: ask or infer whether the problem has already been confirmed before starting pressure testing.
- In `SKILL_ROUTING.md`:
  - Add a shared decision question: “这个方案针对的问题是否已被确认？”
  - Route “否 / 不清楚” to `ai-collaboration-calibration`.
  - Route “是，已有具体方案” to `grill-me`.

## Acceptance Criteria

- [ ] `ai-collaboration-calibration/SKILL.md` explicitly references `grill-me`.
- [ ] `grill-me/SKILL.md` explicitly references `ai-collaboration-calibration`.
- [ ] `SKILL_ROUTING.md` includes the shared判别规则.
- [ ] No Skill claims ownership of both problem-definition calibration and mature solution pressure testing.

## Verification

Run routing smoke tests manually against `SKILL_ROUTING.md`:

- [ ] `帮我想想这个方案。` routes based on whether the problem is confirmed.
- [ ] `压力测试一下这个设计，我感觉哪里不对劲。` routes to `grill-me` when design is concrete.
- [ ] `挑战我这个方案的假设。` routes to `grill-me` if方案已成形, otherwise calibration.
- [ ] `这个方案是不是想错了？` asks/infers problem maturity before picking.

Optional static check:

```bash
rg -n "grill-me|ai-collaboration-calibration|方案针对的问题" ai-collaboration-calibration/SKILL.md grill-me/SKILL.md SKILL_ROUTING.md
```

## Blocked By

None.

## Open Questions

- Should `06-failure-premortem.md` remain as an internal calibration mode, or should it be renamed to avoid mature方案压测 ambiguity?
