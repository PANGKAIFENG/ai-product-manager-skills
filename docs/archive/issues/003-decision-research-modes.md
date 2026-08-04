# Issue 003: Refactor `decision-research` Modes And Checks

Priority: P1
Type: AFK
Status: completed

## Source

- `docs/skill-audit-2026-07-02.md`
- `decision-research/SKILL.md`

## What To Build

Move detailed decision-research modes and templates into references while keeping `SKILL.md` as the trigger/router:

- Technical selection.
- Platform integration.
- Product strategy.
- Business model.
- Research map template.
- Conclusion template.

Add evals and a lightweight output checker.

## Acceptance Criteria

- [x] Main `SKILL.md` keeps the R00/R01/R04/R08/R11 logic but delegates detailed mode rules.
- [x] `evals/evals.json` includes trigger, non-trigger, loop, and handoff-from-candidate-backlog cases.
- [x] `scripts/check_decision_report.py` checks for decision question, hypotheses, evidence, recommendation, exclusions, confidence, and overturn conditions.

## Verification

```bash
python3 /Users/linctex/.config/skillshare/skills/skill-reviewer/scripts/check_skill.py decision-research
python3 scripts/audit_skills.py .
```

## Blocked By

Issue 001 is useful but not strictly required.

## Open Questions

None.
