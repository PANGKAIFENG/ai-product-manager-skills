# Decision Research Loop Pattern

This is a thin multi-Skill orchestration pattern. It does not replace `decision-research/references/decision-loop-contract.md`; that file remains the state contract owned by `decision-research`.

## Purpose

Use this loop when one concrete decision needs more than one pass of evidence, challenge, and convergence.

`decision-research` remains the loop owner and final recommendation owner. `grill-me` is an optional Critic checkpoint, not a mandatory step.

## When To Use

- The decision question is concrete but cannot be closed in one pass.
- There are competing options or hypotheses.
- A high-risk product, technical, business, or platform decision needs challenge before execution.
- The user wants the decision state saved, resumed, or updated across rounds.
- A Candidate Backlog from `research-topic-compiler` needs final recommendation and exclusion logic.

## When Not To Use

- The user wants a broad learning project or long-term watchlist; use `research-topic-compiler`.
- The user has not clarified the problem or decision question; start with `ai-collaboration-calibration`.
- The question is a simple factual lookup or one-pass docs search.
- The decision has no owner, deadline, consequence, or stop condition.

## Node Roles

| Node | Skill | Role | Enter When | Exit With |
| --- | --- | --- | --- | --- |
| Optional Framer | `ai-collaboration-calibration` | Clarify decision frame when the question is fuzzy. | Decision question, target level, or success criteria are unclear. | Decision question candidate, assumptions, constraints. |
| Loop Owner | `decision-research` | Maintain Research Map, evidence, hypothesis matrix, and recommendation. | A concrete decision question exists. | Recommendation, confidence, reversal condition, next gate. |
| Optional Critic A | `grill-me` | Challenge the Research Map before search deepens. | High-risk decision, weak framing, or expensive downstream cost. | Critic Handoff: missing hypotheses, weak assumptions, scope risks. |
| Optional Critic B | `grill-me` | Challenge the interim or final recommendation before handoff. | Recommendation has material product, business, legal, or engineering impact. | Critic Handoff: challenged assumptions, failure modes, unresolved risks. |

## State Reference

Use `decision-research/references/decision-loop-contract.md` for state files:

- `research_map.md`
- `hypothesis_matrix.md`
- `evidence_table.md`
- `assumption_ledger.md`
- `scope_drift_log.md`
- `conclusion_version.md`

If a shared folder is needed, use `.loop-state/decision-research/`.

## Critic Checkpoints

### After Research Map

Use `grill-me` only when:

- The decision is high-risk.
- The Research Map has only one plausible hypothesis.
- The user has strong prior bias.
- A wrong decision would trigger significant rework, spend, customer impact, or compliance risk.

Skip this checkpoint when:

- The decision is low-risk and reversible.
- The Research Map already has clear competing hypotheses.
- The user only needs a fast factual selection.

### Before Final Recommendation

Use `grill-me` only when:

- The recommendation will drive roadmap, hiring, purchase, production integration, or public positioning.
- Confidence is medium or low but the user still wants to act.
- The strongest option has meaningful reversal cost.

Skip this checkpoint when:

- The next step is explicitly a PoC or spike.
- Evidence is strong, decision is reversible, and user asked for speed.
- More critique would not change the decision or next gate.

## Critic Handoff Fields

- decision_question
- recommendation_or_map_under_review
- strongest_assumptions
- missing_hypotheses
- likely_failure_modes
- evidence_to_recheck
- user_decision_needed

## Stop Conditions

Stop with one of:

- `recommendation`: one option is strongest under current constraints.
- `poc-needed`: a spike, prototype, or technical validation is now cheaper than more research.
- `insufficient-evidence`: public evidence cannot close the decision.
- `user-decision-required`: the remaining uncertainty is local, strategic, or value-based.
- `low-roi-stop`: additional research will not materially change the next action.

## Guardrails

- Do not force `grill-me` into every research run.
- Do not let `research-topic-compiler` own the final recommendation for a concrete decision.
- Do not continue researching only because more sources exist.
- Do not convert weak evidence into a stable conclusion without a Human Gate.
- Do not move from recommendation into execution without user confirmation when impact is high.
