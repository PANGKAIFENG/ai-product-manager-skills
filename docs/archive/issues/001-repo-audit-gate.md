# Issue 001: Add Repo Audit Gate And Eval Schema

Priority: P1
Type: AFK
Status: completed

## Source

- `docs/skill-audit-2026-07-02.md`
- Global findings: eval inconsistency, local path leakage, script duplication, lack of repo-level gate.

## What To Build

Add a repository-level quality gate that checks every public Skill for:

- Valid `SKILL.md` location and line budget.
- Local/private path leakage.
- Honeycomb legacy references.
- Missing `evals/evals.json`.
- Missing scripts for high-risk output-producing Skills.
- Duplicated PRD scripts drifting between `prd-architect` and `prd-review`.

Also document the canonical eval schema.

## Acceptance Criteria

- [x] `docs/eval-schema.md` documents the repo-level eval format.
- [x] `scripts/audit_skills.py` runs from repo root.
- [x] Audit output is readable and returns non-zero only for configured hard failures.
- [x] Existing known gaps are warnings, not blockers, until fixed by later issues.

## Verification

```bash
python3 scripts/audit_skills.py .
```

## Blocked By

None.

## Open Questions

None.
