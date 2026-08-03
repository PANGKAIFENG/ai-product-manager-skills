# Provenance

## Sources Reviewed

- `mattpocock/skills`, `skills/engineering/to-issues/SKILL.md`
  - URL: https://github.com/mattpocock/skills/blob/main/skills/engineering/to-issues/SKILL.md
  - Repository: https://github.com/mattpocock/skills
  - License: MIT
  - Main branch commit observed during creation: `694fa30311e02c2639942308513555e61ee84a6f`
  - Borrowed concepts: tracer-bullet vertical slices, AFK / HITL split, dependency order, approval before publishing, parent issue preservation.

- Prior local variant used during adaptation
  - Borrowed concepts: PRD issue lookup, GitHub issue body sections, user-story coverage, dependency order.
  - Note: not treated as an upstream public source and not redistributed as-is.

- GitHub `awesome-copilot` issue creation Skills
  - URL: https://github.com/github/awesome-copilot
  - Borrowed concepts: issue template awareness, duplicate checks, and separating issue operation concerns from planning concerns.

## Merge Decision

Decision: public AI PM Skill with borrowed patterns, not a direct import.

Reason:

- The upstream Skills are strong at generic engineering issue slicing.
- This Skill needs Chinese discoverability, PM-to-engineering handoff boundaries, PRD readiness checks, `prd-architect` / `prd-review` routing, and explicit GitHub publish confirmation.
- V1 avoids scripts because the highest-value behavior is judgment: readiness, slice granularity, AFK / HITL classification, and coverage.

## Public Ownership

This Skill is maintained in `PANGKAIFENG/ai-product-manager-skills` as a public AI PM workflow. Future updates should preserve the trigger contract and update this provenance file when upstream patterns are materially imported.
