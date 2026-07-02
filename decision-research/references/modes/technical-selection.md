# Technical Selection Mode

Use when the decision is about libraries, frameworks, services, models, runtime architecture, deployment paths, or implementation feasibility.

## Required Checks

- Candidate options and the "do nothing / existing stack" baseline.
- Project constraints: language, runtime, security, deployment, license, team familiarity, maintenance cost.
- Evidence channels: official docs, changelog, GitHub issues/discussions, package metadata, dependent repos, production examples, benchmark caveats.
- Anti-signals: abandoned releases, unresolved security issues, weak docs, license mismatch, hidden paid dependency, vendor lock-in.

## Decision Output

Include:

- Recommendation with confidence.
- Excluded options and why.
- Minimum spike or proof path.
- Rollback or migration cost.
- Overturn conditions, especially project constraints that would change the choice.

Do not use stars as the primary quality signal. Treat benchmark claims as weak until tied to the user's workload.
