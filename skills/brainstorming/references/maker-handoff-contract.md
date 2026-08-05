# Maker Handoff Contract

Use this contract when `brainstorming` produces a solution for optional critique, or when it consumes a design gap returned by `grill-me`.

## Role Contract

Brainstorming is the solution Maker. It owns real alternatives, recommendation and tradeoffs, scope/non-goals, flow, states, risks, challenge targets, and focused Design Deltas. It does not own evidence collection, final option authority, Critic clearance, PRD readiness, implementation readiness, or publication approval.

The public Product Work Graph solution-divergence node routes to the unqualified `brainstorming` Skill. Never infer `superpowers:brainstorming`; that route is valid only when the user explicitly invokes the fully qualified name. Do not modify, disable, or hide either Skill.

## Entry and Single-Call Stop

Enter only when the problem, goal, judgment criteria, and material constraints are stable enough to compare solutions. Otherwise offer a minimal handoff to `ai-collaboration-calibration` and stop without creating a Design Spec.

For a single-Skill request, produce the requested Solution Candidate Set or Design Spec and stop at exactly one Maker outcome:

- `design-confirmation-needed`
- `critic-ready`
- `revision-required`
- `owner-confirmed`

`owner-confirmed` records user confirmation only. It is not Critic, PRD, implementation, or release readiness.

## Handoff Envelope

Every cross-Skill handoff or return must identify:

- `work_item_id`
- `source_owner` and exactly one `target_owner`
- `artifact_ref` and `artifact_version`
- one `outcome`
- one highest-priority `gap` with a stable ID, when returning work
- `why_it_matters`
- an executable `closure_criterion`
- `preserved_items`
- `return_to` and `resume_point`
- `cycle_count`
- one primary `next_owner` or `stop_reason`

A `next_owner: grill-me` is an offer. Do not run Critic, PRD, issues, code, or implementation planning without explicit chain authorization.

## Solution Candidate Set and Design Spec

Include the confirmed problem, goals, criteria and constraints; 2-3 real alternatives or a reason only one is viable; recommendation, sacrificed optimization goals and reversal conditions; scope/non-goals; core flow, states and failure recovery; assumptions, risks, open items; version; user-confirmation status; and challenge targets.

Do not label a Maker artifact `clear`, `ready`, `approved`, or "passed pressure testing" based on Maker self-review.

## Design Delta

Consume a Critic Handoff only when it targets `brainstorming`, references the exact Design Spec version, supplies one design gap, closure criterion, preserved items, and resume point.

Return a Design Delta that identifies the challenge, changes only the affected scope/flow/state/boundary, explains the effect, and preserves everything else. Keep unresolved challenges visible. "Revised" does not mean "cleared"; return to the original Critic resume point for recheck.

## Stop and Human Gate

Stop when the user confirms or rejects the recommendation, the artifact is ready to offer to Critic, the blocker belongs to Research/Decision/Human, or the user requested only this layer.

For the same stable challenge ID, if two completed return cycles have not closed or narrowed the blocker, emit `cycle-limit-reached`, set `human-decision-required`, preserve the last artifact/version, and do not emit a third automatic return edge.

## Compatibility

Existing lightweight summaries and Design Specs remain valid. Missing B1 fields are `unknown`; add them only on the next handoff or revision. No persistent state file is required for ordinary one-pass brainstorming.
