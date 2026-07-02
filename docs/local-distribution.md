# Local Distribution Notes

These notes are for maintainers who sync this public Skill catalog into local agent runtimes. They are not runtime instructions for public Skill execution.

## Source Of Truth

- Public repository default branch is the reviewable source for shared AI PM Skills.
- Local runtime folders should be treated as installation targets, not as the canonical editing surface.
- When a Skill is changed, update the repository first, validate, then sync to local targets.

## Suggested Sync Targets

Common local targets include:

- Codex Skills folder.
- Claude Code Skills folder.
- OpenCode / agents Skills folder, when configured.
- Skillshare-managed canonical folder, when the local machine uses Skillshare as the distribution layer.

Use local tooling or `rsync` only after verifying the destination is managed by the maintainer. Do not encode maintainer-only absolute paths in public `SKILL.md` files.

## Validation After Sync

Run the repository audit before sync:

```bash
python3 scripts/audit_skills.py .
```

After sync, verify target runtimes can see the updated Skill metadata and that no runtime points at a stale copy.
