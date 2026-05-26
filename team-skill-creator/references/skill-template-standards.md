# Skill Template Standards

Use this standard when drafting or updating the generated `SKILL.md`.

## Minimum Structure

A team-ready Skill should provide:

- YAML frontmatter with `name` and `description`.
- Overview that states the repeatable capability.
- Workflow with ordered executable steps.
- Context intake or missing-information gates.
- Resource guide for `references/`, `scripts/`, and `assets/`.
- Output format or deliverable contract.
- Definition of Done.
- Evaluation readiness through smoke prompts, checks, or regression cases.

The headings do not need to match exactly, but the behavior must be present.

## Frontmatter

Use only required Codex fields unless there is a product-specific reason:

```yaml
---
name: skill-name
description: Use when Codex needs to...
---
```

Rules:

- `name` must match the folder name.
- `name` must use lowercase letters, digits, and hyphens.
- `description` is the trigger contract, not a body summary.
- Put all "when to use" information in `description`, because body loads only after triggering.
- Do not put long workflow steps in `description`.

## Description Quality

A strong description says:

- What the Skill does.
- When user requests should trigger it.
- Relevant domains, objects, file types, systems, or task language.
- Typical natural-language expressions users will use.
- Important adjacent cases when useful.

Avoid:

- Vague noun phrases like `Review skills`.
- Generic claims like `Help with AI tasks`.
- Slash-command-only triggers.
- Full procedural summaries.

## Body Quality

Keep `SKILL.md` focused on what the agent must know after trigger:

- Core workflow.
- Key judgment rules.
- Safety and side-effect boundaries.
- Resource loading conditions.
- Output contract.
- Completion criteria.

Move detailed background, long examples, policies, rubrics, and domain references into `references/`.

Move fragile, repeated, format-exact, or deterministic logic into `scripts/`.

Move templates, boilerplate, images, fonts, and static resources into `assets/`.

## Context Budget

Treat context budget as a quality gate:

- Keep the body concise and preferably under 500 lines.
- Keep references one level away from `SKILL.md`.
- Mention when each reference should be read.
- Avoid repeating the same checklist in metadata, body, and references.
- Avoid exposing large tool or schema catalogs before they are needed.

## Workflow Gates

Specify:

- What missing information must be asked.
- Maximum number of questions.
- When to continue with assumptions.
- When to stop.
- When writes, destructive actions, network calls, credentials, or production effects require confirmation.
- What to do when verification fails.
- What evidence is required before saying work is complete.

## Evaluation Checklist

At minimum, include:

- Smoke prompts for normal trigger behavior.
- Non-trigger prompts for likely false positives.
- Capability checks for the core workflow.
- Deterministic checks for files, schema, generated artifacts, or commands when possible.
- Regression prompts for historical failures when available.

Low-risk personal Skills may use a small checklist. Team-critical Skills should include deterministic or regression checks.

## Completion Bar

A generated Skill is not ready while it contains:

- TODO placeholders.
- Missing or vague `description`.
- No Definition of Done.
- No output format for non-trivial tasks.
- References or scripts that are not mentioned in `SKILL.md`.
- Claims of validation without command output or observed evidence.
