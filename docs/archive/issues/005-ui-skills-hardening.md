# Issue 005: Harden UI Wireframe And Mockup Skills

Priority: P1
Type: AFK
Status: completed

## Source

- `docs/skill-audit-2026-07-02.md`
- `ui-wireframe-to-html/SKILL.md`
- `ui-mockup-desktop-workbench/SKILL.md`

## What To Build

For `ui-wireframe-to-html`:

- Replace public references to `~/.honeycomb-agent` templates with local reference templates.
- Add screen inventory, state model, ASCII layout, and wireframe handoff templates.
- Add a lightweight package checker.

For `ui-mockup-desktop-workbench`:

- Add output mode and verification references.
- Add a mockup package checker.

## Acceptance Criteria

- [x] No public UI Skill depends on `~/.honeycomb-agent` paths.
- [x] UI wireframe templates are bundled in `references/templates/`.
- [x] Checkers can validate minimum package structure for wireframe/mockup artifacts.
- [x] Existing evals still pass structural audit.

## Verification

```bash
python3 /Users/linctex/.config/skillshare/skills/skill-reviewer/scripts/check_skill.py ui-wireframe-to-html
python3 /Users/linctex/.config/skillshare/skills/skill-reviewer/scripts/check_skill.py ui-mockup-desktop-workbench
python3 scripts/audit_skills.py .
```

## Blocked By

Issue 001 is useful but not strictly required.

## Open Questions

None.
