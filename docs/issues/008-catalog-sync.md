# Issue 008: Sync Registry, Routing, Metadata, And Changelog

Priority: P2
Type: AFK
Status: completed

## Source

- All previous optimization issues.
- `README.md`
- `SKILL_REGISTRY.md`
- `SKILL_ROUTING.md`
- `CHANGELOG.md`

## What To Build

Update catalog surfaces so new references, evals, checkers, and local issue backlog are discoverable:

- Mention the audit gate and eval schema.
- Align registry/routing descriptions with new router-plus-assets pattern.
- Add changelog entry.
- Keep OpenAI agent metadata strategy explicit; do not add metadata blindly if not used by runtime.

## Acceptance Criteria

- [x] Catalog docs mention repo-level audit and issue backlog.
- [x] Routing docs preserve current user-stage boundaries.
- [x] Changelog has a dated entry for this optimization pass.
- [x] `git diff --check` passes.

## Verification

```bash
python3 scripts/audit_skills.py .
git diff --check
```

## Blocked By

Issues 001-007.

## Open Questions

None.
