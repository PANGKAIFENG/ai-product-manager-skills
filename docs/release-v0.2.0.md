# Release v0.2.0

v0.2.0 gives the AI Product Manager Skills Library one canonical installable root and a machine-readable catalog, while keeping all 13 public Skill IDs stable.

## Highlights

- Moved every installable Skill from `<skill-id>/` to `skills/<skill-id>/`.
- Added `catalog/skills.yaml` as the canonical machine-readable inventory.
- Added repository-level structure, canonical-root, catalog, eval, checker, link, duplicate-drift, and regression gates in GitHub Actions.
- Organized examples under `docs/examples/`, workflow contracts under `docs/workflows/`, and completed maintenance material under `docs/archive/`.
- Added migration and local-distribution guidance for copied installs, symlinks, and Skillshare metadata.

## Included Skills

- `ai-collaboration-calibration`
- `ai-work-assetization-diagnoser`
- `brainstorming`
- `competitive-analysis`
- `complex-exploration`
- `decision-research`
- `grill-me`
- `prd-architect`
- `prd-review`
- `prd-to-issues`
- `research-topic-compiler`
- `ui-mockup-desktop-workbench`
- `ui-wireframe-to-html`

## Upgrade Notes

The public Skill IDs and invocation names did not change. Only their source paths moved.

- Existing copied Skills continue to work until explicitly replaced.
- Direct repository symlinks must change from `<repo>/<skill-id>` to `<repo>/skills/<skill-id>` after the checkout moves to v0.2.0.
- Existing Skillshare single-Skill metadata that uses `subdir: <skill-id>` must be rebound to `skills/<skill-id>` before a future metadata-driven update.
- Review and preserve local modifications before any forced reinstall or broad sync.

See `docs/migration-v0.2.md` for the complete migration matrix and safe dry-run commands.

## Install

Full catalog:

```bash
skillshare install PANGKAIFENG/ai-product-manager-skills --all
```

Single Skill:

```bash
skillshare install \
  PANGKAIFENG/ai-product-manager-skills/skills/prd-architect \
  --name prd-architect
```

Codex and Claude Code users can follow `docs/install-codex.md` and `docs/install-claude-code.md`.

## Verification

- Repository audit discovered all 13 cataloged Skills without hard errors.
- PRD regression suite: 13 tests.
- Research Dashboard regression suite: 28 tests.
- Skillshare release-candidate dry-run discovered and selected all 13 Skills.
- All 13 Skill packages passed the deterministic `skill-reviewer` structure checks; five indirect Concept Lens reference warnings remain non-blocking.

## Known Limitations

- Plugin packaging is not included.
- The project remains Chinese-first.
- This release does not automatically rewrite local Skillshare metadata or overwrite locally modified Skills.
