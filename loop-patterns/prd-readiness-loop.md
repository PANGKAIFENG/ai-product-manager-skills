# PRD Readiness Loop Pattern

This is a thin multi-Skill orchestration pattern. It does not replace `prd-review/references/prd-readiness-loop-contract.md`; that file remains the state contract owned by `prd-review`.

## Purpose

Use this loop when a product idea, solution, PRD draft, and review feedback must converge into a PRD that can safely enter Superpowers `writing-plans`.

The loop connects framing, pressure testing, optional decision research, PRD drafting, review, revision, and readiness gating.

## When To Use

- A fuzzy product idea must become a development-ready PRD.
- A concrete solution needs pressure testing before drafting or revision.
- A PRD draft has blockers that need multiple review and revision rounds.
- A major product or technical choice inside the PRD needs evidence before the PRD can be finalized.
- The user asks to close PRD blockers, resume a prior review, or decide whether the PRD can enter `writing-plans`.

## When Not To Use

- The user only wants a one-pass PRD review.
- The user only needs copyediting.
- The task is a simple factual lookup or a one-off UI mockup.
- There is no stable product goal and no willingness to clarify it.
- The blocker count is not decreasing and the remaining issues require owner judgment.

## Node Roles

| Node | Skill | Role | Enter When | Exit With |
| --- | --- | --- | --- | --- |
| Round 0 Framer | `ai-collaboration-calibration` | Clarify problem, goal, assumptions, and success criteria. | Problem, target user, or scope is fuzzy. | Problem statement, key assumptions, decision criteria. |
| Solution Critic | `grill-me` | Pressure-test a concrete solution or PRD-level product choice. | The problem is confirmed and there is a solution to challenge. | Critic Handoff: confirmed decisions, rejected options, open risks. |
| Evidence Owner | `decision-research` | Resolve a concrete product, technical, business, or platform decision. | A PRD blocker depends on evidence or option selection. | Recommendation, exclusion reasons, confidence, reversal condition. |
| Maker / Reviser | `prd-architect` | Draft or revise the PRD from inputs and review feedback. | Inputs are ready enough to write or patch the PRD. | PRD draft or revision patch, assumptions, open questions. |
| Reviewer / Gate | `prd-review` | Find blockers and issue the readiness verdict. | A PRD draft or revision exists. | Findings, revision draft, readiness verdict, next action. |

## Entry Criteria

At least one of these must exist:

- A fuzzy idea plus a product owner willing to clarify scope.
- A concrete solution that needs pressure testing before documentation.
- A PRD draft, handoff, or review findings.
- A Candidate Backlog or decision question blocking the PRD.

If none exist, do not start the loop. Ask for the smallest useful input.

## Shared State

Use `.loop-state/prd-readiness/` only when the user asks to save, resume, or manage loop state. Chat-only runs can keep the same sections in the response.

Suggested files:

| File | Purpose |
| --- | --- |
| `problem-frame.md` | Current problem, user, scope, assumptions, non-goals. |
| `critic-handoff.md` | `grill-me` output: confirmed decisions, rejected options, risks. |
| `decision-handoff.md` | `decision-research` output: recommendation, evidence, reversal condition. |
| `prd-revision-input.md` | Inputs for `prd-architect` revision. |
| `review-state.md` | Link or summary of `prd-review` loop state. |

For review state, prefer the parent contract: `prd-review/references/prd-readiness-loop-contract.md`.

## Handoff Payloads

### Critic Handoff From `grill-me`

- solution_under_test
- confirmed_problem
- confirmed_decisions
- rejected_options
- open_risks
- assumptions_to_validate
- recommended_next_skill

### Revision Handoff To `prd-architect`

- source_prd
- review_findings
- critic_handoff
- decision_handoff
- patch_scope
- facts_vs_assumptions
- open_questions

### Readiness Handoff From `prd-review`

- readiness_verdict: `Ready for writing-plans` / `Ready with assumptions` / `Not ready`
- open_blockers
- resolved_blockers
- assumptions_for_plan
- diagram_status
- suggested_writing_plans_prompt

## Loop Flow

1. Start at the earliest unstable node.
2. Use `ai-collaboration-calibration` if the problem is fuzzy.
3. Use `grill-me` if the problem is confirmed but the solution is risky.
4. Use `decision-research` only for concrete evidence-backed choices.
5. Use `prd-architect` to draft or patch the PRD.
6. Use `prd-review` to review the artifact and issue readiness.
7. If `Not ready`, route blockers back to the smallest owner:
   - unclear problem -> calibration
   - risky solution choice -> grill-me
   - evidence gap -> decision-research
   - missing PRD text -> prd-architect
8. Re-review the revised PRD with `prd-review`.

## Exit Criteria

The loop exits with one of:

- `Ready for writing-plans`: no open blockers remain.
- `Ready with assumptions`: planning can start, but assumptions must become plan prerequisites.
- `Not ready`: blockers remain and should not be hidden in implementation planning.
- `Human decision required`: the remaining issue is a business, scope, product, or resource decision.

## Anti-Over-Looping Rules

- Do not run every node by default; start where the current artifact is unstable.
- If blocker count does not decrease for two review rounds, stop and ask for a human decision.
- If the same missing context blocks two different nodes, stop and ask the owner instead of re-routing.
- Do not let `grill-me` hold loop state; it produces a Critic Handoff and exits.
- Do not let `prd-architect` self-approve readiness; `prd-review` owns the verdict.
