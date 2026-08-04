---
name: prd-readiness-loop-contract
description: PRD Readiness Loop contract for repeated review, revision, and implementation readiness checks
---

# PRD Readiness Loop Contract

## Purpose

PRD Readiness Loop is used to move a PRD from draft status to development-ready status through repeated review, revision, and readiness checks.

The loop does not replace product judgment. It makes blockers, assumptions, revisions, and implementation readiness explicit so a PRD can safely move into Superpowers `writing-plans`.

## When to Use

Use this contract when at least one of these is true:

1. A PRD draft needs multiple review rounds.
2. Existing findings or blockers need to be tracked until closed.
3. The user wants to know whether a PRD can enter development planning.
4. The PRD includes AI-native flows, exception paths, human takeover, or diagrams.
5. Revision drafts must be generated and re-reviewed.

Do not use this contract for:

1. Writing a PRD from scratch.
2. Pure copyediting.
3. A vague idea with no product goal.
4. A major decision that should be researched before drafting.

## Required Inputs

- PRD draft
- Product goal
- Target user
- Scope boundary and non-goals
- Main workflow
- Key states
- Input and output definitions
- Exception paths
- Acceptance criteria
- Existing review findings, if any
- Diagrams or diagram expectations, if relevant

If the PRD draft is missing or too vague, hand off to `prd-architect` or `ai-collaboration-calibration` instead of forcing a review loop.

## State Files

Use these files when the user asks to save, resume, or manage a readiness loop. In chat-only runs, keep the same sections in the answer.

| File | Purpose |
| --- | --- |
| `review_round.md` | Current round, review scope, reviewed artifact versions, and summary. |
| `open_blockers.md` | Unresolved blocker and major findings. |
| `resolved_blockers.md` | Closed blockers, resolution notes, and evidence. |
| `revision_draft.md` | Text that can be pasted back into the PRD. |
| `readiness_status.md` | `Ready`, `Ready with assumptions`, or `Not ready` with reasons. |
| `open_questions.md` | Questions requiring user, business, design, or engineering judgment. |
| `diagram_status.md` | Diagram necessity, editability, validation results, and gaps. |
| `handoff_decision.md` | Whether to continue review, enter `writing-plans`, or pause. |

## Loop Steps

1. Read the PRD and related handoff or prior review state.
2. Identify PRD type and current maturity.
3. Review from PM perspective.
4. Review from engineering perspective.
5. Review from QA/testing perspective.
6. Check diagrams when diagrams are present or required.
7. Classify findings by severity.
8. Generate revision suggestions and PRD patch draft.
9. Update blocker state.
10. Run Implementation-Plan Readiness.
11. Decide `Ready`, `Ready with assumptions`, or `Not ready`.
12. Recommend the next action.

## Finding Severity

| Severity | Meaning |
| --- | --- |
| `Blocker` | Cannot enter development planning. |
| `Major` | Should be fixed before implementation or written as a clear assumption. |
| `Minor` | Improves clarity but does not block planning. |
| `Suggestion` | Optional improvement. |

Use the existing Chinese severity labels in user-facing output when helpful, but keep the state model clear enough to resume across rounds.

## Readiness Verdict

Use the same three verdicts as `implementation-plan-readiness.md`:

| Verdict | Meaning |
| --- | --- |
| `Ready for writing-plans` | No open blockers; PRD can enter development planning. |
| `Ready with assumptions` | Planning can start, but assumptions must be listed as plan prerequisites. |
| `Not ready` | Blockers remain; development planning would create rework or false certainty. |

## Stop Conditions

Stop the loop when:

1. No open blockers remain.
2. Acceptance criteria are testable.
3. Core flow and exception flow are clear.
4. Scope and non-goals are explicit.
5. Required diagrams are present, validated, or explicitly unnecessary.
6. Open questions are either resolved or converted into explicit implementation assumptions.
7. The PRD is ready for `writing-plans`.

## Pause Conditions

Pause and ask the user when:

1. A key business decision is missing.
2. Scope conflict cannot be resolved from the PRD.
3. A trade-off requires product owner judgment.
4. Requirement feasibility depends on unavailable engineering constraints.
5. The PRD needs a new product direction rather than revision.

## Human Gate

Ask the user before:

1. Marking a PRD as ready when major assumptions remain.
2. Removing, deprioritizing, or changing product scope.
3. Treating missing business context as a stable requirement.
4. Moving into `writing-plans`.
5. Rewriting large sections beyond the requested revision scope.

## Output Template

Use this template after each loop run:

```markdown
# PRD Readiness Loop Update

## 1. Review Round

Round X

## 2. Current Readiness

Ready for writing-plans / Ready with assumptions / Not ready

## 3. Open Blockers

| Issue | Severity | Why it blocks | Suggested revision |
| --- | --- | --- | --- |

## 4. Resolved Blockers

...

## 5. Recommended Revisions This Round

...

## 6. PRD Patch Draft

...

## 7. Can Enter writing-plans?

Yes / Not yet

Reason: ...

## 8. Next Step

Continue revision / Enter development planning / Wait for user decision
```

## Handoff

When the loop stops, leave enough state for planning:

1. Final readiness verdict
2. Remaining assumptions
3. Known non-goals
4. Validation and diagram status
5. Suggested `writing-plans` entry prompt
