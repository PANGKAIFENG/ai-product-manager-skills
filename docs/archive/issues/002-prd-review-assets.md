# Issue 002: Refactor `prd-review` Into Router Plus Assets

Priority: P1
Type: AFK
Status: completed

## Source

- `docs/skill-audit-2026-07-02.md`
- `prd-review/SKILL.md`

## What To Build

Reduce `prd-review/SKILL.md` into a router/workflow surface and move long rules into references:

- Review lenses.
- Severity rules.
- Diagram review.
- Output contract.
- Implementation-plan readiness.

Clean public-facing Honeycomb/local path references from the main Skill.

## Acceptance Criteria

- [x] `prd-review/SKILL.md` is materially shorter and points to references by trigger condition.
- [x] Honeycomb-only commands are removed from the public main flow.
- [x] `prd-review/evals/evals.json` covers readiness, diagram, over-technical PRD, missing PRD, and non-trigger cases.
- [x] PRD shape and Draw.io validation scripts remain available.

## Verification

```bash
python3 /Users/linctex/.config/skillshare/skills/skill-reviewer/scripts/check_skill.py prd-review
python3 scripts/audit_skills.py .
```

## Blocked By

Issue 001 is useful but not strictly required.

## Open Questions

Whether duplicate PRD scripts should be shared or kept as synced copies. This issue may document the strategy without moving them.
