# Research Topic Compiler Evals

This suite separates routing compatibility from research-behavior quality.

## Running Comparisons

- Snapshot the old Skill before editing it.
- Run old and new versions with the same model, prompt, fixture files, and grader.
- Treat the fixture summaries as frozen eval evidence, not as current public documentation.
- Do not use network access for deterministic old/new comparison.
- Run live source retrieval only as a separate smoke test.
- Capture the final output and tool/read trace. A final answer alone cannot prove that a boundary case avoided unnecessary acquisition.

## Holdout Boundary

The independent holdout is intentionally absent from this directory. Reveal it only after the candidate Skill version is frozen.

## Grading

Use `graders/iterative-research-rubric.md`. Objective assertions may be checked against fixture IDs and paths. Gap quality, source independence, framework change, and stopping sufficiency require model or human review.
