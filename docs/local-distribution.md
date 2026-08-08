# Local Distribution Notes

These notes are for maintainers who sync this public Skill catalog into local agent runtimes. They are not runtime instructions for public Skill execution.

## Source Of Truth

- Public repository default branch is the reviewable source for shared AI PM Skills.
- Installable atomic Skills live only under `skills/<skill-id>/`; `loops/` and `workflows/` contain orchestration guidance, not installable Skills. Tool compatibility adapters are explicitly located under `tools/*/*/runtime-adapter/`.
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

## v0.1 To v0.2 Source Rebinding

The v0.2 repository migration changes source subdirectories from `<skill-id>` to `skills/<skill-id>`. It does not rename the local runtime directory or the public Skill ID.

Before changing an existing Skillshare-managed Skill:

1. Inspect its entry in `$HOME/.config/skillshare/skills/.metadata.json`.
2. Check whether `source` or `subdir` still points at the v0.1 repository-root path.
3. Diff the local Skill against the v0.2 source and preserve any local-only changes.
4. Preview the direct v0.2 path without writing:

   ```bash
   skillshare install \
     PANGKAIFENG/ai-product-manager-skills/skills/prd-architect \
     -b v0.2.0-restructure \
     --name prd-architect \
     --force \
     --dry-run
   ```

5. Stop if the destination contains modifications that have not been preserved.

For an existing destination, Skillshare v0.20.22 requires `--force` to reach the overwrite preview. The paired `--dry-run` prevents writes; verify that it remains present before running the command. Skillshare v0.20.22 does not expose a metadata-only source-rebind command. A later direct install with `--force` but without `--dry-run` may replace content while updating metadata; do not treat it as a harmless path edit.

After a reviewed reinstall, run:

```bash
skillshare sync --dry-run
```

Do not run an unrestricted real sync if the preview includes unrelated Skills or unexpected copy-target changes. See [`migration-v0.2.md`](migration-v0.2.md) for user-facing migration guidance.
