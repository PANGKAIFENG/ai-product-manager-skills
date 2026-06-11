# Issue 001 - Fix skill request template old Skill reference

## Title

Fix old research Skill reference in Skill request template

## Type

AFK

## Priority / Labels

P1

Suggested labels: `documentation`, `skill-request`, `good first issue`

## Source

- `docs/skill-boundary-and-loop-audit.md`
- `.github/ISSUE_TEMPLATE/skill_request.md`

## Problem

The public Skill request template still lists an old research Skill reference, but the current stable public Skill is `decision-research`.

This is externally visible and can confuse contributors proposing adjacent Skill changes.

## What To Change

- Replace the old research Skill reference with `decision-research` in `.github/ISSUE_TEMPLATE/skill_request.md`.
- Check whether the template should also include `ui-mockup-desktop-workbench` and `ai-work-assetization-diagnoser`, because the public catalog currently has 8 Skills.

## Acceptance Criteria

- [ ] Targeted search across `.github`, docs, README, Registry, and Routing returns no stale public Skill reference.
- [ ] `.github/ISSUE_TEMPLATE/skill_request.md` lists the current public Skill names.
- [ ] No unrelated template wording changes are made.

## Verification

```bash
rg -n "decision-research|ui-mockup-desktop-workbench|ai-work-assetization-diagnoser" .github/ISSUE_TEMPLATE/skill_request.md
```

## Blocked By

None.

## Open Questions

None.
