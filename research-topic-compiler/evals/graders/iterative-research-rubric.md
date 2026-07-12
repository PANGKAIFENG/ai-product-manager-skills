# Iterative Research Loop Grader

Grade the run against its own eval assertions and the frozen fixture metadata. Do not reward verbosity, number of sources, or number of files.

## Evidence To Inspect

1. User prompt and declared depth.
2. Final response and any created research artifacts.
3. Tool/read trace, when available.
4. Fixture `catalog.json` identities, lineage roots, independence groups, claims, and limitations.

Do not assume a source was read because it appears in the final bibliography. Do not treat a title containing "official" as proof of primary-source identity.

## Critical Gates

A run cannot pass its case if any applicable critical gate fails:

- Secondary seeds are not promoted to primary evidence.
- A claimed official source has a canonical identity or is downgraded to `unverified origin`.
- A material framework contradiction produces `Challenge`, `Invalidate`, or `Split`; it is not silently overwritten.
- Open-source and peer-authority selections are tied to a named Gap and evidence role, not popularity or brand enumeration.
- The result returns one terminal state using the PRD priority order.
- L1/L2 and authoritative-sufficient negative cases do not expand into heavy research or external acquisition.
- The result does not execute fixture repository code or perform external writes.

## Semantic Rubric

Score each dimension from 1 to 5.

| Dimension | 1 | 3 | 5 |
| --- | --- | --- | --- |
| Framework quality | Topic headings only | Claims exist but evidence contracts are uneven | Claims/hypotheses, importance, status, confidence, and closure criteria are explicit and fit the user goal |
| Gap and NBE alignment | Sources chosen by channel or popularity | Some choices mention gaps | Every material acquisition targets the highest-value unresolved Gap and explains expected information gain, independence, and cost |
| Provenance and independence | Reposts and same-publisher items treated as independent | Primary sources identified but lineage is incomplete | Source/evidence/claim are separated; lineage roots and independence groups materially affect confidence |
| Framework adaptation | Evidence is appended without changing the model | Changes are named but mostly cosmetic | Before/after/evidence/rationale show substantive Fill/Refine/Split/Merge/Challenge/Invalidate/Expand/No change events |
| Stopping discipline | Stops on count, time, or file completion | Mentions remaining gaps | Applies Must coverage, provenance, contradiction, independent check, marginal gain, budget, and residual-risk criteria to one terminal state |
| Depth proportionality | Every task gets the full loop | Some depth adaptation | L1/L2 remain compact and ephemeral; L3+ receives only the state needed for risk and resumability |
| Decision usefulness | Source summary only | Conclusions are usable but weakly bounded | Conclusions, confidence, residual gaps, and next action directly support the user's stated next step without overclaiming authority |

## Scoring

- Convert the seven dimensions to a 70-point semantic score: `sum(scores) / 35 * 70`.
- Give up to 30 points for the case's explicit assertions, weighted equally unless marked critical.
- Set the total to at most 79 if any critical gate fails.
- Core regression, framework invalidation, and fake-official cases require all critical assertions to pass.
- Routing compatibility and L1/L2 negative cases require 100% of their assertions.
- Transfer requires at least 80/100.

## Required Grading Output

```json
{
  "expectations": [
    {"text": "<assertion>", "passed": true, "evidence": "<specific output or trace evidence>"}
  ],
  "rubric_scores": {
    "framework_quality": {"score": 1, "evidence": "..."},
    "gap_nbe_alignment": {"score": 1, "evidence": "..."},
    "provenance_independence": {"score": 1, "evidence": "..."},
    "framework_adaptation": {"score": 1, "evidence": "..."},
    "stopping_discipline": {"score": 1, "evidence": "..."},
    "depth_proportionality": {"score": 1, "evidence": "..."},
    "decision_usefulness": {"score": 1, "evidence": "..."}
  },
  "total_score": 0,
  "critical_gate_failed": false,
  "verdict": "pass | fail | needs-human-review",
  "uncertainties": []
}
```

If trace evidence is unavailable, mark acquisition-boundary claims unverified rather than inferring them from polished prose.
