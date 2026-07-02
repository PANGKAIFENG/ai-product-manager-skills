# Issue 006: Add Evals And Checkers For Product Handoff Skills

Priority: P2
Type: AFK
Status: completed

## Source

- `docs/skill-audit-2026-07-02.md`
- `brainstorming/SKILL.md`
- `competitive-analysis/SKILL.md`
- `prd-to-issues/SKILL.md`

## What To Build

Add structured evals and minimal checkers for Skills that produce product handoff artifacts:

- `brainstorming`: design spec checker.
- `competitive-analysis`: decision brief checker.
- `prd-to-issues`: issue plan checker.

## Acceptance Criteria

- [x] Each Skill has `evals/evals.json`.
- [x] Each Skill has a lightweight checker for its core output shape.
- [x] Existing references remain discoverable.

## Verification

```bash
python3 /Users/linctex/.config/skillshare/skills/skill-reviewer/scripts/check_skill.py brainstorming
python3 /Users/linctex/.config/skillshare/skills/skill-reviewer/scripts/check_skill.py competitive-analysis
python3 /Users/linctex/.config/skillshare/skills/skill-reviewer/scripts/check_skill.py prd-to-issues
python3 scripts/audit_skills.py .
```

## Blocked By

Issue 001 is useful but not strictly required.

## Open Questions

None.
