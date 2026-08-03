# PRD Readiness Checklist

Use this before splitting a PRD into implementation issues.

## Pass Signals

A PRD is ready enough to split when it contains:

- Clear target user or operator.
- Problem statement and desired outcome.
- In-scope and out-of-scope boundaries.
- Main flow or job flow.
- User stories, requirements, or equivalent requirement items.
- Acceptance criteria or measurable done signals.
- Known constraints: permissions, data sources, dependencies, compliance, rollout, or migration.
- Open questions separated from confirmed requirements.

## Blockers

Stop and ask clarification, or route to `prd-review`, when:

- The goal is ambiguous enough that an issue could pass while the product still fails.
- The PRD mixes conflicting scope versions.
- Acceptance criteria are subjective only.
- Critical inputs, outputs, states, or ownership are missing.
- AI-native flows omit human confirmation, fallback, or failure handling.
- The requested issues would require product or architecture decisions that have not been made.

## Handling Missing Information

Ask at most five questions. Prefer questions that unblock slicing:

1. Which repository should receive the issues?
2. Is the desired output draft-only or publish after approval?
3. Which parts of the PRD are in scope for this release?
4. Which decisions must stay HITL?
5. Are there existing labels, milestones, issue templates, or parent issue conventions?

If optional details are missing, continue with explicit assumptions and mark affected issues as HITL or lower confidence.

## Readiness Output

Use one of:

- `pass`: enough confirmed detail to draft issues.
- `needs clarification`: draft possible, but some issues must stay HITL or contain open questions.
- `blocked`: issue splitting would create misleading or unimplementable work.
