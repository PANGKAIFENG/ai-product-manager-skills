# Contributing

Thanks for helping improve AI Product Manager Skills Library.

This repository is intentionally narrow: public, Chinese-first Agent Skills for AI product managers and product-facing operators. It is not a dump of every useful prompt, private workflow, or engineering-only Skill.

## What Belongs Here

Good contributions usually fit one of these stages:

- AI collaboration brainstorming and problem calibration.
- Product, technology, industry, or concept research for PM decisions.
- Technical feasibility or option selection.
- PRD drafting, PRD review, and requirements handoff.
- Plan pressure testing and decision risk review.

Out of scope:

- Private company workflows, customer data, internal system names, or confidential business logic.
- Generic coding standards, low-level implementation helpers, or project-specific engineering rules.
- One-off prompts that do not define a reusable workflow.
- Skills whose trigger boundary overlaps heavily with an existing Skill without a routing update.

## Before Opening a PR

1. Check [SKILL_REGISTRY.md](SKILL_REGISTRY.md) for existing Skills.
2. Check [SKILL_ROUTING.md](SKILL_ROUTING.md) for adjacent boundaries.
3. Decide whether the change updates an existing Skill or introduces a new one.
4. Remove private context, secrets, customer names, and internal-only terminology.
5. Add or update an example in [examples/](examples/) when the workflow changes.

## Adding a New Skill

Use a root-level directory with a stable English slug:

```text
new-skill-name/
  SKILL.md
  references/
  scripts/
  evals/
```

Required checklist:

- `SKILL.md` has frontmatter with `name` and `description`.
- The `description` says when to use and when not to use the Skill.
- The Skill has a Chinese quick reference section.
- The workflow is specific enough to be reusable.
- `README.md` is updated if it belongs to the public AI PM workflow.
- `SKILL_REGISTRY.md` is updated.
- `SKILL_ROUTING.md` is updated if adjacent triggers could conflict.
- `examples/<skill-name>.md` is added or updated.

## Editing an Existing Skill

Keep changes focused. Prefer improving trigger boundaries, workflow steps, output contracts, and examples over adding broad prose.

If behavior changes, update:

- The Skill's `description`.
- The relevant example.
- `SKILL_REGISTRY.md`.
- `SKILL_ROUTING.md` if routing changes.
- `CHANGELOG.md`.

## Commit Style

Use short, descriptive commit messages:

```text
Improve PRD review trigger boundaries
Add example for research topic compiler
Document Codex install path
```

## Review Standard

A good PR makes the repo easier to use, easier to discover, and safer to share publicly.

Maintainers may reject contributions that are useful personally but not broadly useful to AI product managers.
