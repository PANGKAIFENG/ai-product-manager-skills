# Critic Handoff Contract

Use this contract when `grill-me` challenges a versioned solution, returns one blocker to the smallest responsible node, or rechecks a returned delta.

## Role Contract

Grill is the Critic. It owns challenge discovery, severity, recommended answer or assumption, closure criterion, primary return owner, and recheck of the original challenge. It does not own full evidence research, final option selection, complete solution rewriting, PRD or implementation-plan generation, or readiness/publication approval.

If no versioned solution exists, hand solution formation to `brainstorming`. Continue to ask one question at a time in interactive runs.

## Handoff Envelope

Every cross-Skill handoff or return must identify:

- `work_item_id`
- `source_owner` and exactly one `target_owner`
- `artifact_ref` and `artifact_version`
- one `outcome`
- one highest-priority `gap` with a stable challenge ID
- `why_it_matters`
- an executable `closure_criterion`
- `preserved_items`
- `return_to` and `resume_point`
- `cycle_count`
- one primary `next_owner` or `stop_reason`

Reject stale or missing artifact versions. When one finding affects several nodes, return it to the earliest causal gap and put downstream effects in notes; do not assign multiple primary owners.

## Challenge Record

Each Challenge contains:

- challenge ID and exact artifact/version/location;
- type: `dependency`, `assumption`, `evidence`, `failure-mode`, `tradeoff`, or `scope/boundary`;
- severity: `blocker`, `high`, `medium`, or `low`;
- current problem and why it matters;
- recommended answer or current assumption with rationale;
- closure criterion;
- exactly one primary return owner;
- passed and preserved items that must not reopen.

Critic has exactly three outcomes:

- `challenge-open`
- `clear-for-owner-confirmation`
- `human-decision-required`

`clear-for-owner-confirmation` means no blocker/high challenge remains. It is not PRD readiness, implementation readiness, release approval, or permission to execute.

## Smallest Responsible Return

Choose one primary target by the earliest causal gap:

| Gap | Primary target | Expected delta |
| --- | --- | --- |
| Missing/conflicting/stale evidence | `research-topic-compiler` | Evidence Delta |
| Choice criteria, exclusion logic, confidence, reversal condition | `decision-research` | Decision Delta |
| Scope, flow, state, interaction, failure recovery, reversibility | `brainstorming` | Design Delta |
| Local authority, organization commitment, budget, irreversible risk, hidden context | Human Gate | Explicit owner decision |

Emit only the Challenge and Critic Handoff. Do not write the target node's full artifact.

## Recheck

When a delta returns, verify the artifact/version, original challenge ID, closure criterion, and preserved items. Recheck only the affected challenge. Do not restart an unbounded full grill or reopen passed items without new evidence.

If the closure criterion passes, close that challenge and either move to the next queued challenge or return `clear-for-owner-confirmation`. If it fails but narrows, update the same challenge and cycle count.

## Stop and Human Gate

Stop after locating one primary return owner, after the current challenge closes, when no blocker/high challenge remains, or when local authority is required.

For the same stable challenge ID, if two completed cycles leave it open without narrowing the closure criterion, emit `cycle-limit-reached`, return `human-decision-required`, preserve the latest artifact/version, state the exact human decision needed, and do not emit a third automatic return edge.

## Compatibility

Existing conversational decision records remain valid. The structured Challenge Record is required only for cross-Skill return or resumable critique. Missing B1 fields in older artifacts are `unknown`, not implicit clearance.
