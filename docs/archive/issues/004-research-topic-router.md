# Issue 004: Refactor `research-topic-compiler` Router And Cleanup Runtime Notes

Priority: P1
Type: AFK
Status: completed

## Source

- `docs/skill-audit-2026-07-02.md`
- `research-topic-compiler/SKILL.md`

## What To Build

Make `research-topic-compiler` more router-like:

- Add a mode-selection reference.
- Add evals for framing, normal research, product candidate, radar loop, and non-trigger cases.
- Move local distribution/runtime notes out of `SKILL.md` into a docs-only maintainer note.

## Acceptance Criteria

- [x] Main `SKILL.md` no longer includes maintainer-only local runtime paths.
- [x] `references/mode-selection.md` defines when to load major research modes.
- [x] `evals/evals.json` covers the high-risk routing boundaries with `decision-research` and `competitive-analysis`.
- [x] Existing references remain discoverable from `SKILL.md`.

## Verification

```bash
python3 /Users/linctex/.config/skillshare/skills/skill-reviewer/scripts/check_skill.py research-topic-compiler
python3 scripts/audit_skills.py .
```

## Blocked By

Issue 001 is useful but not strictly required.

## Open Questions

None.
