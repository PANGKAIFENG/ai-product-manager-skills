# v0.2 Directory Migration Guide

v0.2 moves every installable Skill from a repository-root folder into one canonical installable root: `skills/<skill-id>/`.

This is a source-layout migration. It does not rename the 13 public Skill IDs or intentionally change how they are invoked.

## What Changed

| v0.1 source path | v0.2 source path | Stable Skill ID |
| --- | --- | --- |
| `<skill-id>/` | `skills/<skill-id>/` | `<skill-id>` |
| `prd-architect/` | `skills/prd-architect/` | `prd-architect` |
| `research-topic-compiler/` | `skills/research-topic-compiler/` | `research-topic-compiler` |

The same mapping applies to all 13 entries in [`catalog/skills.yaml`](../catalog/skills.yaml). Examples moved to `docs/examples/`, Loop orchestration moved to `docs/workflows/`, and historical maintenance material moved to `docs/archive/`; those directories are not installable Skill roots.

## What Did Not Change

- Public invocation names such as `$prd-architect` remain stable.
- Every installable directory still contains its own `SKILL.md`, references, scripts, and eval assets.
- A local copied Skill continues to work from its existing runtime folder until it is explicitly replaced.
- A local symlink continues to work if its target still exists. A symlink to a v0.1 repository-root path must be repointed after that checkout switches to v0.2.
- This migration does not require an immediate broad runtime sync.

## Impact By Installation Type

| Existing installation | Immediate runtime impact | Upgrade action |
| --- | --- | --- |
| Copied Skill directory | None. The local copy remains in place. | Compare local changes, then copy from `skills/<skill-id>/` when ready. |
| Symlink to a canonical local Skillshare folder | None while the canonical folder remains unchanged. | Update the canonical source first; runtime links normally do not need renaming. |
| Symlink directly to `<repo>/<skill-id>` | The link breaks only after that checkout adopts v0.2. | Repoint it to `<repo>/skills/<skill-id>`. |
| Skillshare whole-repository install | No change until an update is requested. | Preview the v0.2 branch/release and confirm 13 discovered Skills before installing. |
| Skillshare single-Skill metadata with `subdir: <skill-id>` | Current files remain usable, but a later metadata-based update still points to the old source path. | Rebind the source to `skills/<skill-id>` after preserving or reconciling local modifications. |

## Preview The v0.2 Branch

Before v0.2 is merged or released, preview discovery without changing local files:

```bash
skillshare install PANGKAIFENG/ai-product-manager-skills \
  -b v0.2.0-restructure \
  --dry-run \
  --all
```

The expected result is exactly 13 discovered and selected Skills.

To preview one Skill through its new source path:

```bash
skillshare install \
  PANGKAIFENG/ai-product-manager-skills/skills/prd-architect \
  -b v0.2.0-restructure \
  --name prd-architect \
  --force \
  --dry-run
```

For an existing destination, Skillshare v0.20.22 requires `--force` before it will show the dry-run overwrite preview. The paired `--dry-run` keeps this command read-only. Never run the same `--force` command without `--dry-run` until local modifications have been reviewed and preserved.

## Upgrade After v0.2 Is Released

For a fresh full-catalog installation:

```bash
skillshare install PANGKAIFENG/ai-product-manager-skills --all
```

For a fresh single-Skill installation:

```bash
skillshare install \
  PANGKAIFENG/ai-product-manager-skills/skills/prd-architect \
  --name prd-architect
```

For an existing locally modified Skill:

1. Record its current metadata and diff it against the v0.2 source.
2. Preserve the local changes in a patch, branch, or separate directory.
3. Run the direct new-path command with `--force --dry-run`; for an existing destination, `--dry-run` alone exits before showing the overwrite preview.
4. Use `--force` only after deciding which local changes should survive.
5. Run `skillshare sync --dry-run` and inspect unrelated target changes before any actual sync.

There is no metadata-only rebind command in Skillshare v0.20.22. A real reinstall from the new path can update both content and metadata, so it must be treated as a content replacement operation.

## Rollback

If a v0.2 install is not ready for local use, keep the current runtime directory unchanged and continue using the existing local copy. Repository layout changes do not require deleting a working local Skill. For direct repository symlinks, temporarily point back to a v0.1 checkout or release tag.
