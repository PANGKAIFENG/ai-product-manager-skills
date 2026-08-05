# Core Loop Research Handoff Contract

Use this contract when `research-topic-compiler` hands evidence to `decision-research`, or when it consumes one bounded evidence gap returned by `decision-research` or `grill-me`.

## Role Contract

Research owns evidence coverage, provenance, contradictions, candidate input, confidence, and residual gaps. It does not own final recommendation, exclusion logic, solution design, Critic clearance, or downstream readiness.

A normal single-Skill request ends after the Research artifact and one terminal status. A `next_owner` is an offer, not permission to run another Skill.

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

Do not use "continue researching" as a gap or closure criterion. Do not consume a handoff whose target, artifact version, decision question, or scope does not match; stop and request correction instead.

## Evidence Pack

When evidence is fit for a decision, emit a complete Evidence Pack containing the research goal and scope, Evidence Contract, current Framework or Candidate Backlog version, Must Claims and competing candidates, evidence lineage, closed/open/blocked/deferred gaps, contradictions, confidence, residual risks, one Research terminal status, and a stable `decision_question_id`.

An Evidence Pack may offer `next_owner: decision-research`. It must not contain a final choice or silently execute Decision.

## Evidence Delta

When consuming a Research Return Request, work only on its named gap and return:

- the original gap ID and request artifact/version;
- new, invalidated, or conflicting evidence and its Change Event;
- `closed`, `narrowed`, `blocked`, or `deferred` gap status;
- impact on candidates, hypotheses, confidence, and reversal conditions;
- the original Decision or Critic resume point.

Do not rewrite the full research report or reopen `preserved_items` to hide whether the gap closed.

## External Write Boundary

A handoff or chain is not authorization for external writes. Runtime sync, Skillshare/Multica publishing, and DingTalk/Yunxiao writes are outside Research and the B1 contract. Stop before any such write and hand it to a specialist publisher/operation under separate explicit authorization.

## Stop and Human Gate

Stop with the existing unique Research terminal state when evidence is fit for purpose, access or budget blocks progress, the goal changes to final selection, or the next fact requires local authority. Use `escalated` only with a consumable handoff.

For the same stable gap ID, if two completed cross-Skill cycles have not closed or narrowed the gap, emit `cycle-limit-reached`, set the next outcome to `human-decision-required`, preserve the last artifact/version, and do not emit a third automatic return edge.

## Compatibility

Existing Candidate Backlog, Cross-Session Handoff, iterative loop state, and chat-only output remain valid. Missing B1 fields in an older artifact are `unknown`, never inferred as complete. Add the fields on the next handoff or delta; do not batch-rewrite historical files.
