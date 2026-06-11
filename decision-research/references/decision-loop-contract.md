---
name: decision-loop-contract
description: Decision Research Loop contract for stateful, bounded decision convergence
---

# Decision Research Loop Contract

## Purpose

Decision Research Loop is used when a decision cannot be closed in one pass, but the work still has one clear decision question.

The loop exists to help the user converge toward a defensible product, technical, business, or strategy decision. It should not become open-ended topic research. If the goal becomes long-term knowledge tracking, hand off to `research-topic-compiler` Radar Mode.

## When to Use

Use this contract when at least one of these is true:

1. The user needs multiple rounds of evidence before choosing.
2. The decision has competing hypotheses that need to be tracked over time.
3. New evidence or user corrections may change the recommendation.
4. The user wants the research state saved so the decision can resume later.
5. The decision has a deadline, owner, reversal condition, or PoC gate.

Do not use this contract for:

1. A simple factual lookup.
2. A one-pass API or docs search.
3. A broad learning topic without a decision owner.
4. A long-running watchlist without a concrete choice to make.

## Required Inputs

- Decision question
- Decision owner, if known
- Deadline or decision window, if known
- Current options or candidate hypotheses
- Known local context
- Constraints
- Current assumptions
- What happens if no decision is made
- Stop condition for this loop run

If these inputs are missing, run `R00 Research Framing Gate` and ask only the questions that change the decision frame.

## State Files

Use these files when the user asks to save, resume, or continue a decision loop. In chat-only runs, keep the same sections in the answer.

| File | Purpose |
| --- | --- |
| `research_map.md` | Current decision frame, scope, hypotheses, sources, and stop conditions. |
| `hypothesis_matrix.md` | Competing hypotheses, supporting evidence, counter-evidence, and status. |
| `evidence_table.md` | Evidence records with source level, relevance, and interpretation. |
| `assumption_ledger.md` | User corrections, changed assumptions, and decision impact. |
| `scope_drift_log.md` | Scope Drift Checkpoint results across rounds. |
| `conclusion_version.md` | Versioned recommendation, confidence, reversal condition, and next gate. |

## Loop Steps

1. Frame the decision with `R00 Research Framing Gate`.
2. Confirm the decision question and stop condition.
3. Build or update `Research Map`.
4. Enumerate competing hypotheses.
5. Search for supporting evidence.
6. Search for counter-evidence.
7. Run `Scope Drift Checkpoint`.
8. Update `Assumption Ledger` when the user corrects the frame.
9. Compare hypotheses and downgrade weak options.
10. Decide whether to continue, stop, ask the user, or move to PoC.
11. Output a versioned conclusion with confidence and reversal condition.

## Hypothesis Status

Use these statuses in `hypothesis_matrix.md`:

| Status | Meaning |
| --- | --- |
| `active` | Still plausible under current evidence. |
| `weakened` | Still possible, but weaker than before. |
| `excluded` | Ruled out for a concrete reason. |
| `needs-user-context` | Cannot be resolved without local or business context. |
| `needs-poc` | Needs a real-world spike, prototype, or technical validation. |

## Stop Conditions

Stop the loop when one condition is met:

1. One option is clearly stronger under the current constraints.
2. Multiple independent sources support the same conclusion.
3. New evidence has low decision value for 3 consecutive items.
4. The unresolved uncertainty is local context that only the user can answer.
5. A PoC, spike, or business validation is now the cheapest next step.
6. The ROI fuse triggers because more research will not change the decision.
7. The user changes the decision frame.

## Human Gate

Ask the user before:

1. Changing the core decision question.
2. Treating weak or single-source evidence as a stable conclusion.
3. Making a high-risk recommendation with material business, legal, or engineering impact.
4. Continuing research after the ROI fuse triggers.
5. Moving from research into execution, purchase, integration, or implementation.

## Output Template

Use this template after each loop run:

```markdown
# Decision Research Loop Update

## 1. Current Decision Question

...

## 2. Strongest Hypothesis

...

## 3. New Supporting Evidence

| Evidence | Source level | Supports | Notes |
| --- | --- | --- | --- |

## 4. New Counter-Evidence

| Evidence | Source level | Weakens | Notes |
| --- | --- | --- | --- |

## 5. Weakened or Excluded Hypotheses

...

## 6. Scope Drift Check

- Drifted from original question: Yes / No
- Explanation: ...
- Research Map update needed: Yes / No

## 7. Assumption Ledger Updates

...

## 8. Current Conclusion

- Recommendation: ...
- Confidence: High / Medium / Low
- Reversal condition: ...

## 9. Next Step

Continue research / Enter PoC / Ask user / Stop
```

## Handoff

When the loop stops, leave enough state for another run to resume:

1. Current recommendation
2. Confidence and reversal condition
3. Open assumptions
4. Evidence still missing
5. Next gate: user decision, PoC, PRD input, or no action
