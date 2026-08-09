# Changelog

All notable changes to this project are documented here.

This project uses semantic-ish release tags for public snapshots. The current focus is usability and public discoverability rather than API stability.

## Unreleased

## [0.3.3] - 2026-08-10

### Added

- Added explicit-only Codex Runtime entrypoints for two Workflows, `$problem-to-solution` and `$solution-to-delivery`, and three Loops, `$decision-loop`, `$solution-loop`, and `$delivery-loop`.
- Added co-located runtime metadata and routing evals for all five composition entries while preserving their Workflow or Loop catalog kind.

### Changed

- Renamed the former v0.3 composition IDs to shorter, outcome-oriented names and recorded one-way migration aliases without keeping duplicate Runtime entrypoints.
- Bounded every Loop to three cycles, with a Human Gate after two consecutive cycles without a meaningful delta, and standardized recoverable state, preserved items, and resume points.
- Extended the v0.3 asset checker to validate composition Runtime adapters, stable IDs, explicit-only policy, eval schema/routes, and minimum trigger/non-trigger/risk coverage.
- Included requested version plans, issue drafts, and PRD coverage matrices in the Product Delivery Manifest fingerprint before independent Review.
- Bound every PRD, UI, and planning artifact to its producer identity, added a validator-enforced pre-split Review gate, and made the final Review cover every Package producer.
- Bound actor-scoped Reviewer and Human Approver writes to their persisted identities, and prevented `pre_split_review` from being added after planning artifacts already exist.
- Kept an independently reviewed Package at `package_ready` when a persisted publish approval is stale while preserving fail-closed Publisher authorization.
- Updated the core Pack, Registry, Routing, quickstart, install, distribution, migration, and Agent guidance for the new Runtime surface.

## [0.3.2] - 2026-08-09

### Changed

- Removed standalone module-level, overall, and equivalent acceptance sections from all three PRD templates; observable and verifiable outcomes now live beside the relevant feature logic, UI feedback, and failure or recovery behavior.
- Updated `prd-architect` and `prd-review` guidance and evals so reviews preserve testability without recreating a separate acceptance checklist.
- Updated the mirrored PRD shape checker to report legacy standalone acceptance headings, with regression coverage across every bundled PRD template.

## [0.3.1] - 2026-08-08

### Changed

- Simplified `prd-architect` around concise background, Draw.io when explicitly requested or justified by workflow complexity, and feature modules that pair target-state UI with functional logic.
- Replaced fixed-heading PRD checks with equivalent capability groups, added a 200-character background guard, and kept the mirrored `prd-review` checker compatible.
- Added regression coverage for chapter compression, simple-flow diagram suppression, complex Draw.io routing, and state semantics split by subject and scope.

## [0.3.0] - 2026-08-08

### Added

- A single public asset model: 15 atomic Skills, 3 Loops, 2 Workflows, 4 Tools, and 4 install Packs.
- `catalog/assets.yaml` plus a v0.3 checker that validates every asset ID, path, contract file, Pack reference, and retired install surface.
- Six on-demand Skills migrated into the public catalog: customer discovery, StyleWork requirement planning, Skill lifecycle governance, Skill review, trace diagnosis, and project context stewardship.
- `research-decision-loop`, `solution-challenge-loop`, and `prd-delivery-readiness-loop` with explicit state, return edges, stop conditions, and human gates.
- `product-discovery` and `product-delivery` stage workflows.
- Tool-owned side-effect boundaries for Product Delivery validation, DingTalk PRD publishing, Yunxiao work-item creation, and Yunxiao-to-DingTalk Sheet sync.

### Changed

- Converged the former public/private catalog split into `PANGKAIFENG/ai-product-manager-skills` as the single public authority; the old repository becomes a migration tombstone.
- Folded competitor evidence into `research-topic-compiler`, structure-only UI work into `ui-mockup-desktop-workbench`, StyleWork scoping into `customer-requirement-discovery`, and assetization judgment into `team-skill-creator`.
- Standardized all 15 Skill eval packages on the repository routing schema with trigger, non-trigger, and regression coverage.
- Updated Registry, Routing, quickstart, installation, distribution, and Agent guidance to the v0.3 asset model.
- Renamed ambiguous Python `root` identifiers in three installable packages so Skillshare's default security audit no longer misclassifies type annotations as system-prompt overrides.

### Removed From Active Discovery

- Retired `complex-exploration`, `competitive-analysis`, `ui-wireframe-to-html`, `ai-work-assetization-diagnoser`, and `stylework-solution-scoper` as standalone Skills. Historical content remains under `archive/` or in the old repository tombstone with migration aliases.
- Archived the B1-only catalog checker so v0.3 no longer locks the repository to the former 13-Skill surface.

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
