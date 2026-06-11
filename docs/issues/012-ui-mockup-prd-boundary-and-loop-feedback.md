# Issue 012 - Clarify UI mockup PRD boundary and feedback loop

## Title

Clarify `prd-architect` vs `ui-mockup-desktop-workbench` boundary and PRD feedback path

## Type

AFK

## Priority / Labels

P3

Suggested labels: `ui-mockup`, `prd`, `routing`

## Source

- `docs/skill-boundary-and-loop-audit.md`
- `prd-architect/SKILL.md`
- `ui-mockup-desktop-workbench/SKILL.md`
- `SKILL_ROUTING.md`

## Problem

`prd-architect` can reference screenshots / HTML mockups while drafting PRDs, and `ui-mockup-desktop-workbench` generates real desktop HTML mockups from PRD + UI spec.

The boundary is mostly clear in practice, but not fully written into both Skills:

- `prd-architect`: light UI references and PRD-supporting diagrams/mockup notes.
- `ui-mockup-desktop-workbench`: formal multi-state desktop page mockup artifact.

The PRD feedback path is also not explicit: if a mockup exposes PRD gaps, the next step should usually be `prd-review` or `prd-architect`, not ad hoc production implementation.

## What To Change

- In `prd-architect/SKILL.md`:
  - Clarify it does not own formal desktop mockup generation.
  - Link to `ui-mockup-desktop-workbench` when PRD + UI spec are ready.
- In `ui-mockup-desktop-workbench/SKILL.md`:
  - Clarify required input maturity.
  - Add transfer rules:
    - PRD not mature -> `prd-architect`
    - PRD has conflicts / missing acceptance -> `prd-review`
- In `SKILL_ROUTING.md`:
  - Keep UI Mockup routing section aligned.

## Acceptance Criteria

- [ ] Both Skills reference each other where useful.
- [ ] `ui-mockup-desktop-workbench` is clearly downstream of PRD maturity.
- [ ] Mockup-discovered PRD gaps have a route back to PRD work.
- [ ] No production implementation workflow is implied.

## Verification

```bash
rg -n "ui-mockup-desktop-workbench|prd-architect|prd-review|mockup|PRD" prd-architect/SKILL.md ui-mockup-desktop-workbench/SKILL.md SKILL_ROUTING.md
```

Manual smoke tests:

- [ ] `帮我写 PRD，并说明后续页面怎么承接。` -> `prd-architect`
- [ ] `基于 PRD 和 UI 规范生成桌面端真实页面 mockup。` -> `ui-mockup-desktop-workbench`
- [ ] `mockup 做到一半发现 PRD 没写错误态。` -> route back to `prd-review` or `prd-architect`

## Blocked By

- Issue 005 if the feedback path should be described in PRD Readiness Loop pattern first.

## Open Questions

None.
