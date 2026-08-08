# Maintenance Rules

Use these rules when updating an existing `PROJECT_CONTEXT.md` or equivalent project context document.

## Update Triggers

Update global context when:

- product positioning changes in a way that affects future requirements;
- a repo, module, runtime, or ownership boundary changes;
- a new recurring workflow or user type becomes important;
- a durable domain term is introduced or renamed;
- a repeated pitfall caused wrong exploration, wrong edits, or wasted work;
- an entry route, verification command, or first-read path changes.

## Do-Not-Update Cases

Do not update global context for:

- a one-off feature plan that belongs in a PRD;
- temporary debug state or a single trace;
- speculative competitor analysis;
- unfinished options that have not become accepted project knowledge;
- local machine quirks that are not part of the project workflow;
- large pasted excerpts from source files or docs.

## Update Decision Tree

1. Is the fact useful before any specific feature discussion begins?
   - Yes: it may belong in global context.
   - No: route it to PRD, research, decision, runbook, or handoff.
2. Is it verified, inferred, or open?
   - Verified: label it as verified if the section needs evidence quality.
   - Inferred: label it as current judgment.
   - Open: add it under open research points, not as a decision.
3. Does the update make the document harder to read at session start?
   - Yes: summarize and link to the detailed artifact.
   - No: keep the text concise.

## Anti-Bloat Rules

- Prefer route maps over long explanations.
- Prefer links and file paths over copied content.
- Keep requirement-specific detail out of global sections.
- Merge duplicate pitfalls into one durable prevention rule.
- Remove stale wording when adding new facts.
- Keep future AI entry routes short and actionable.

## Pitfall Format

Use this format:

```text
Symptom: what went wrong or what the agent/team was tempted to do.
Cause: why the mistake was likely.
Prevention rule: the durable rule future sessions should follow.
Evidence: optional short path or command that confirms the rule.
```

## Review Checklist

Before finishing an update, check:

- All referenced paths exist, or the document marks them as unverified.
- The document does not confuse sibling repositories or checkouts.
- Product facts, current judgments, and open questions are not mixed together.
- PRD, research, ADR, runbook, and handoff content is routed rather than pasted.
- The first-read route tells a future AI where to start for product, frontend, backend, runtime, and tests.
- The document answers: what product, who uses it, where to read next, how modules connect, and what not to assume.
