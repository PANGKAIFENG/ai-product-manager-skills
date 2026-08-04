# Changelog

All notable changes to this project are documented here.

This project uses semantic-ish release tags for public snapshots. The current focus is usability and public discoverability rather than API stability.

## Unreleased

### Added

- `stylework-yunxiao-workitem-submitter` for turning StyleWork discussions and investigation evidence into confirmed Yunxiao requirements or defects, with attachment validation and readback verification.

## [0.2.0] - 2026-08-04

### Added

- A single installable root at `skills/`, backed by the machine-readable `catalog/skills.yaml` inventory.
- A v0.2 migration guide covering stable Skill IDs, old-to-new source paths, direct symlinks, copied installs, and Skillshare metadata rebinding.
- GitHub Actions checks for catalog consistency, repository links, self-contained duplicate drift, and existing regression tests.
- Repository-level Skill audit gate: `scripts/audit_skills.py`.
- Shared eval schema in `docs/eval-schema.md`; the completed optimization issue backlog is archived under `docs/archive/issues/`.
- `evals/evals.json` coverage for all 13 public Skills.
- Lightweight checker scripts for high-risk output Skills, including decision reports, issue plans, UI wireframe/mockup packages, design specs, competitive briefs, and assetization reports.
- `complex-exploration` Skill for complex, multi-round product strategy, Roadmap, pricing, positioning, review, and methodology tasks that need task typing, problem reframing, exploration planning, and reusable asset extraction.
- `prd-to-issues` Skill for turning ready PRDs into draft GitHub implementation issue backlogs with vertical slices, AFK / HITL labels, and coverage matrix.
- `ui-wireframe-to-html` Skill for turning PRDs into UI structure, state models, ASCII layouts, and optional low-fidelity HTML wireframes.
- `competitive-analysis` Skill for turning competitor, alternative-product, pricing, onboarding, review, and optional walkthrough evidence into Product Decision Briefs.

### Changed

- Moved all 13 public Skills from the repository root to `skills/<skill-id>/` without changing Skill behavior.
- Moved examples to `docs/examples/`, Loop orchestration to `docs/workflows/`, social preview sources to `.github/assets/`, and completed maintenance material to `docs/archive/`.
- Updated `prd-architect` with an explicit UI source-resolution gate, screenshot/reference fallback rules, and a durable mockup evidence manifest that invalidates stale screenshots after HTML or baseline changes.
- Refactored `prd-review`, `decision-research`, and `research-topic-compiler` toward router-plus-assets structure with detailed rules in `references/`.
- Replaced public UI wireframe references to local templates with bundled `references/templates/`.
- Documented maintainer-only runtime sync guidance in `docs/local-distribution.md` instead of public Skill bodies.
- Updated Codex and Claude Code installation guidance for nested Skill discovery, single-Skill source paths, dry-run checks, and locally modified v0.1 installs.
- Updated catalog, routing, install docs, quickstart, examples, and promotion copy for the complex-exploration workflow.
- Updated catalog, routing, install docs, and Superpowers handoff docs for the PRD-to-issue workflow.
- Updated catalog, routing, install docs, quickstart, and examples for the competitive-analysis workflow.
- Updated `ui-mockup-desktop-workbench` so high-fidelity handoff starts with a wireframe-stage review gate before visual output.
- Updated UI mockup catalog, routing, examples, install docs, and promotion copy to distinguish low-fidelity structure from high-fidelity implementation handoff.

## [0.1.0] - 2026-06-11

### Added

- Public AI PM Skill library positioning.
- Six public Skills for AI collaboration brainstorming, research, technical decisions, PRD drafting, PRD review, and plan pressure testing.
- Quickstart and install documentation for Codex, Claude Code, and skillshare-based workflows.
- Example prompts for each public Skill.
- Community health files: license, contribution guide, code of conduct, security policy, issue templates, and PR template.
- Promotion assets for GitHub social preview and external launch copy.

### Changed

- Refocused the repository around public AI product manager workflows.
- Clarified how this project complements Superpowers: product-side preparation here, engineering-side planning and execution there.
- Kept public Skill folders flat at the repository root for stable names and tool discovery.

### Known Limitations

- Plugin packaging is not included in this release.
- Install steps may differ by each user's Codex, Claude Code, or skillshare setup.
- The repository is Chinese-first; English descriptions are provided mainly for discoverability.
