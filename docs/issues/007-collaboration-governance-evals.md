# Issue 007: Add Evals And Assets For Collaboration/Governance Skills

Priority: P2
Type: AFK
Status: completed

## Source

- `docs/skill-audit-2026-07-02.md`
- `ai-collaboration-calibration/SKILL.md`
- `ai-work-assetization-diagnoser/SKILL.md`
- `complex-exploration/SKILL.md`
- `grill-me/SKILL.md`

## What To Build

Improve lower-risk but frequently used collaboration and governance Skills:

- Convert `ai-collaboration-calibration` CSV evals into unified JSON while preserving the CSV.
- Add asset-layer rubric and checker for `ai-work-assetization-diagnoser`.
- Add mode-selection reference and evals for `complex-exploration`.
- Add question-patterns reference and evals for `grill-me`.

## Acceptance Criteria

- [x] Each Skill has `evals/evals.json`.
- [x] Assetization diagnosis has at least one reference and one checker.
- [x] Grill / complex exploration have references for reusable patterns, not only inline prose.

## Verification

```bash
python3 /Users/linctex/.config/skillshare/skills/skill-reviewer/scripts/check_skill.py ai-collaboration-calibration
python3 /Users/linctex/.config/skillshare/skills/skill-reviewer/scripts/check_skill.py ai-work-assetization-diagnoser
python3 /Users/linctex/.config/skillshare/skills/skill-reviewer/scripts/check_skill.py complex-exploration
python3 /Users/linctex/.config/skillshare/skills/skill-reviewer/scripts/check_skill.py grill-me
python3 scripts/audit_skills.py .
```

## Blocked By

Issue 001 is useful but not strictly required.

## Open Questions

None.
