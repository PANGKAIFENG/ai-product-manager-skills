# Dashboard Artifact Grader

Use this rubric for `research-dashboard-html` behavior runs. Grade the generated files and the run trace; do not infer compliance from the final chat response alone.

## Critical Gate

Set `critical_gate_failed: true` if any condition holds:

- `dashboard.html` or `summary.md` is missing.
- The dashboard uses the wrong root family, mixes both roots, or fails `scripts/validate_html_artifact.py`.
- A multi-persona dashboard loses persona switching when the Alpine.js CDN is unavailable.
- A Normal Research/Application dashboard is rendered without one unique terminal status, an evidence-bearing latest Framework, and a locatable claim-to-evidence link.
- A partial/blocked run renders without explicit user acceptance after limitations are visible, or an `escalated` run renders before the receiving owner decides the artifact.
- A material contradiction, weak evidence state, or residual Gap that could change the conclusion is hidden or upgraded to certainty.
- The artifact claims final decision authority that belongs to `decision-research`.
- The run uses network access when the prompt limits evidence to the supplied offline pack.

## Scoring

Score each dimension from 0 to 5, then convert the total to 100.

| Dimension | Weight | Full-credit evidence |
| --- | ---: | --- |
| Routing and boundary | 15 | Correct research mode plus `research-dashboard-html`; no Concept Lens or decision-owner confusion. |
| Research-state integrity | 20 | Latest Framework, material Change Events, unique terminal status, residual Gaps/risks, and stop reason survive projection. |
| Evidence fidelity | 20 | Evidence map separates source-backed facts, weak signals, inferences, contradictions, and unknowns with visible sources. |
| Artifact contract | 15 | Both files exist, required real-element markers are present, static validator passes, and no backend call/build dependency exists. |
| Persona and action value | 15 | Reader-specific implications and concrete next actions support the requested business/product/engineering use. |
| Visual and interaction quality | 15 | First viewport contract, desktop/mobile fit, no overlap or horizontal overflow, working persona interaction, no console error. |

## Verdict

- `pass`: score >= 80 and no critical gate failure.
- `needs_revision`: score 60-79 and no critical gate failure.
- `fail`: score < 60 or any critical gate failure.

Every finding must cite a file fragment, validator output, browser observation, or trace event. Mark visual claims unverified when no browser evidence exists.

For the offline interaction check, intercept Tailwind and Alpine requests with a local `HTTP 200 empty stub`. Confirm the native fallback remains functional and require zero console errors; a blocked request or tolerated CDN load error is not equivalent evidence.
