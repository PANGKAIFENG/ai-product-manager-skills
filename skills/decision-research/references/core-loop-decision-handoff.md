# Core Loop Decision Handoff Contract

Use this contract when `decision-research` consumes a Research Evidence Pack, returns one evidence gap to `research-topic-compiler`, hands a settled Decision constraint to `brainstorming`, or receives a choice/criteria gap from `grill-me`.

## Role Contract

Decision owns the final recommendation, exclusions, confidence, assumptions, reversal conditions, and the choice of `recommendation`, `research-return`, `poc-needed`, `human-decision-required`, or `low-roi-stop`. It does not own an open-ended knowledge project, the returned evidence acquisition, solution design, Critic clearance, or readiness approval.

A single-Skill request stops after one Decision outcome. A downstream handoff is offered unless the user or caller has already authorized the chain.

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

Reject stale or mismatched artifact versions, changed decision questions, and ambiguous multi-owner returns. Never silently change the decision frame.

## Decision Record

A Decision Record contains the stable decision question, owner and window, current options or competing hypotheses, recommendation, confidence, excluded options with reasons, assumptions, evidence references, reversal conditions, non-blocking open items, one outcome, and the next gate.

When handing a settled decision to `brainstorming`, pass the Decision Record reference/version and only the constraints that the Maker must preserve. Do not create the Solution Candidate Set or Design Spec.

## Research Return Request

Return to Research only when the gap is material, researchable, and closable, with all of the following true:

1. One gap can materially change the recommendation, exclusion, or confidence.
2. Research evidence can close or narrow it; it is not a local-owner, authorization, or PoC question.
3. The request names the affected option/hypothesis, expected evidence role, closure criterion, effort budget, preserved items, and resume point.
4. The current Evidence Pack does not already answer it.

Emit one `research-return` request for one stable gap ID. Research returns an Evidence Delta; resume the same Decision artifact at the saved point and do not reopen preserved items.

If these conditions do not hold, use `poc-needed`, `human-decision-required`, or `low-roi-stop` instead of a vague "research more" handoff.

## Critic Return

Consume a Critic return only when its primary gap concerns choice criteria, exclusion logic, confidence, or reversal conditions. Update only the affected part of the Decision Record, preserve evidence and unaffected decisions, and return a Decision Delta to the referenced challenge. Grill, not Decision, decides whether that challenge is cleared.

## Stop and Human Gate

Stop after a recommendation, when PoC is cheaper, when more research has low decision value, when the question changes, or when a local/high-risk choice requires its owner.

For the same stable gap ID, if two completed cross-Skill cycles have not closed or narrowed it, emit `cycle-limit-reached`, set `human-decision-required`, preserve the last artifact/version, and do not emit a third automatic return edge.

## Compatibility

Existing Decision Loop files remain readable. Missing B1 fields in older artifacts are `unknown`, not implicit success. Add fields at the next conclusion, handoff, or delta; do not rewrite historical state in bulk.
