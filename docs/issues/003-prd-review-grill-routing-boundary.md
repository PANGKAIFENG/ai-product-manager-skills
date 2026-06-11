# Issue 003 - Add prd-review and grill-me boundary handoff

## Title

Clarify `prd-review` vs `grill-me` routing and handoff

## Type

HITL

## Priority / Labels

P1

Suggested labels: `skill-boundary`, `prd`, `routing`

## Source

- `docs/skill-boundary-and-loop-audit.md`
- `prd-review/SKILL.md`
- `grill-me/SKILL.md`
- `SKILL_ROUTING.md`

## Problem

`prd-review` and `grill-me` both “find problems”, but at different levels:

- `prd-review`: standard review of a PRD / handoff artifact, with findings, severity, testability, and readiness verdict.
- `grill-me`: solution-level pressure test, with interactive questions and a decision record.

The difference is conceptually clear, but the files do not cross-reference strongly enough. A user prompt like “帮我挑挑这个 PRD 的毛病” can route incorrectly.

## What To Change

- In `prd-review/SKILL.md`:
  - Add non-trigger/transfer rule: if the core issue is solution viability rather than PRD artifact quality, recommend `grill-me`.
  - Keep revision draft scope as minimal patch draft, not full PRD rewrite.
- In `grill-me/SKILL.md`:
  - Add non-trigger/transfer rule: if the user needs a standard PRD readiness review, use `prd-review`.
  - Clarify that it does not produce `Implementation-Plan Readiness`.
- In `SKILL_ROUTING.md`:
  - Add a comparison rule:
    - “这份 PRD 是否可开发、可测试、可交付？” -> `prd-review`
    - “这份 PRD 背后的方案是否会失败？” -> `grill-me`

## Acceptance Criteria

- [ ] `prd-review/SKILL.md` references `grill-me` for solution-level doubts.
- [ ] `grill-me/SKILL.md` references `prd-review` for PRD artifact review.
- [ ] `SKILL_ROUTING.md` contains a PRD artifact vs solution viability判别.
- [ ] `prd-review` still owns readiness verdict.
- [ ] `grill-me` still owns interactive pressure testing.

## Verification

Routing smoke tests:

- [ ] `帮我挑挑这个 PRD 的毛病。` -> `prd-review`
- [ ] `这个需求文档能不能交付开发？` -> `prd-review`
- [ ] `这个 PRD 背后的方案能不能成？` -> `grill-me`
- [ ] `我不想要标准评审，问我 hard questions。` -> `grill-me`

Static check:

```bash
rg -n "grill-me|prd-review|readiness|方案" prd-review/SKILL.md grill-me/SKILL.md SKILL_ROUTING.md
```

## Blocked By

- Issue 002 is recommended first, because it defines the shared Critic boundary for `grill-me`.

## Open Questions

None.
