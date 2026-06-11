# Issue 007 - Promote cross-skill comparison into routing

## Title

Promote the cross-Skill comparison matrix into `SKILL_ROUTING.md`

## Type

AFK

## Priority / Labels

P2

Suggested labels: `routing`, `documentation`, `catalog`

## Source

- `docs/skill-boundary-and-loop-audit.md`
- `decision-research/SKILL.md`
- `SKILL_ROUTING.md`

## Problem

`decision-research/SKILL.md` contains one of the clearest cross-Skill comparison tables in the repo. It distinguishes calibration, decision research, research-topic-compiler, and grill-me by premise, time scale, output, and stop condition.

This knowledge belongs in the repository-level routing surface, not only inside one Skill.

## What To Change

- Add a compact cross-Skill comparison section to `SKILL_ROUTING.md`.
- Keep it as routing guidance, not a new governance document.
- Include at least:
  - `ai-collaboration-calibration`
  - `research-topic-compiler`
  - `decision-research`
  - `grill-me`
  - `prd-architect`
  - `prd-review`
  - `ui-mockup-desktop-workbench`
- Preserve the rule: route by current workflow stage, not keyword alone.

## Acceptance Criteria

- [ ] `SKILL_ROUTING.md` includes a compact comparison matrix.
- [ ] The matrix does not duplicate the full `SKILL_REGISTRY.md`.
- [ ] README and Registry responsibilities remain unchanged.
- [ ] Ambiguous prompts can be routed by stage and desired output.

## Verification

```bash
rg -n "comparison|对比|前提|输出|终止|ai-collaboration-calibration|decision-research|grill-me" SKILL_ROUTING.md
```

Manual smoke tests:

- [ ] `帮我想想。` -> calibration unless a more concrete stage is provided.
- [ ] `帮我选一个。` -> decision-research.
- [ ] `系统研究一下。` -> research-topic-compiler.
- [ ] `拷问我的方案。` -> grill-me.
- [ ] `帮我审 PRD。` -> prd-review.

## Blocked By

- Issue 002
- Issue 003
- Issue 004

## Open Questions

None.
