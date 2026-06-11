# Provenance

## Source

- Source Skill: Superpowers `brainstorming`
- Local source path: `/Users/linctex/.codex/plugins/cache/openai-curated/superpowers/c6ea566d/skills/brainstorming`
- Plugin/package: `superpowers` from `openai-curated`
- License: MIT License, copyright Jesse Vincent, 2025
- Import date: 2026-06-11

## Merge Decision

Decision: `new`, adapted rather than copied verbatim.

The upstream Skill is optimized for implementation flow: brainstorm -> write design doc -> commit -> user review -> invoke Superpowers `writing-plans`. This repository is an AI PM Skill library, so the local `brainstorming` Skill keeps the design-before-execution discipline but adapts the downstream handoff to PM artifacts:

- `prd-architect` for formal PRD drafting.
- `grill-me` for pressure testing a selected design.
- `prd-review` for PRD readiness review.
- `ui-mockup-desktop-workbench` for desktop UI mockups.
- `prd-to-issues` or Superpowers `writing-plans` only after PRD/design readiness.

## Borrowed Strengths

- Explore context before proposing.
- Ask one clarifying question at a time.
- Present 2-3 approaches with trade-offs.
- Get design confirmation before implementation.
- Use visual aids only when the question benefits from seeing rather than reading.
- Self-review the design spec for placeholders, contradictions, ambiguity and scope drift.

## Local Boundary

This Skill does not replace:

- `ai-collaboration-calibration`, which handles unclear problem framing and assumption calibration.
- `grill-me`, which pressure tests an already formed plan.
- `prd-architect`, which writes formal PRDs.
- `prd-review`, which decides whether a PRD/handoff can be developed and tested.

## License Note

The local Skill is an adaptation for this catalog. If copying substantial upstream text or resources in future edits, preserve the MIT license notice and this provenance record.
