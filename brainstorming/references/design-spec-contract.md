# Design Spec Contract

Use this reference when `brainstorming` needs to produce a written design spec instead of a short conversational summary.

## Choose The Right Weight

Use a lightweight spec when:

- The change affects one feature, one page, one workflow, or one decision.
- The user mainly needs to compare options and choose a direction.
- The next step is a PRD-lite, mockup, or pressure test.

Use a standard spec when:

- The design spans multiple user roles, states, systems, or artifacts.
- The next step is implementation planning.
- The decision has meaningful trade-offs, failure modes, or sequencing concerns.

Avoid a heavyweight spec when the problem itself is still unstable. Route back to `ai-collaboration-calibration`.

## Lightweight Spec

```markdown
# <Topic> Design Spec

## Current Problem

## Design Goal

## Recommended Approach

## Alternatives Considered

## Scope

### In Scope

### Out of Scope

## Core Flow

## States / Edge Cases

## Risks And Open Questions

## Next Step
```

## Standard Spec

```markdown
# <Topic> Design Spec

## 1. Background

## 2. Problem And Goal

## 3. Users / Roles

## 4. Constraints

## 5. Options Compared

## 6. Recommended Design

## 7. Core Flow

## 8. Data / Content / Artifact Model

## 9. UI / Interaction Notes

## 10. Error, Edge And Human-Review States

## 11. Non-Goals

## 12. Validation / Acceptance

## 13. Risks

## 14. Open Questions

## 15. Handoff Recommendation
```

## Self-Review

Before saying the spec is ready, check:

1. No unresolved placeholders, marker text or fake certainty.
2. The recommended approach matches the stated goal.
3. Alternatives are real alternatives, not weak straw options.
4. Scope and non-goals are explicit.
5. Important states and failure paths are not omitted.
6. Open questions are separated from confirmed decisions.
7. The next step names the correct downstream Skill or artifact.
