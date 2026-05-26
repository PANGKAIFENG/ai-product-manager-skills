---
name: skill-reviewer
description: Review, audit, and improve Codex/agent Skills for team standardization. Use when the user asks to check a Skill, review SKILL.md, decide whether a capability should become a Skill, find Skill design issues, produce concrete optimization suggestions, or validate trigger-only descriptions, input/output contracts, workflow gates, context budget, tool boundaries, progressive disclosure, bundled resources, evaluation readiness, evidence levels, and governance.
---

# Skill Reviewer

## Overview

Use this Skill as the team Skill reviewer. Treat a Skill as a reusable capability unit, not as a long prompt. Review from the target goal backward: trigger contract, input/output contract, workflow gates, tool boundary, bundled resources, context budget, evaluation loop, and governance must all support the intended outcome.

## Workflow

1. Locate the artifact. Prefer a Skill directory containing `SKILL.md`; if the user only provides text, review the text and state that directory/resource checks are unavailable.
2. Establish review context before final recommendations: target users, business/domain goal, expected trigger prompts, runtime environment, required tools, inputs/outputs, failure cost, reuse frequency, and current pain points.
3. If critical context is missing, ask at most 5 concrete questions. Do not block on optional context; if the user asks for a quick review, continue with explicit assumptions.
4. When a local Skill directory or `SKILL.md` path is available, run the deterministic check:

```bash
python3 <this-skill>/scripts/check_skill.py /path/to/skill-or-SKILL.md
```

5. Build an Evidence Summary as you inspect: files read, commands run, deterministic findings, observed facts, inferred judgments, and assumptions.
6. For team delivery, scoring, non-trivial optimization, context-budget concerns, or cross-ecosystem metadata, read `references/team-skill-rubric.md`.
7. For industry-grade review, cross-harness artifacts, or questions about best practices, read `references/industry-skill-patterns.md`.
8. Inspect `references/`, `scripts/`, `assets/`, eval files, or sample prompts only when needed to verify claims made by `SKILL.md`.
9. Output prioritized findings and concrete repair options. When the user asks for optimization, prefer executable patches, rewritten sections, script suggestions, or eval checklists over commentary alone.

## Context Intake

Confirm the following before final review, or write them as assumptions:

- Purpose: what repeatable task the Skill supports, and why it should be a Skill rather than a prompt, tool, workflow, plugin, or app.
- Users: who invokes it, how they naturally ask, and whether it is personal, team, or production-grade.
- Trigger examples: 3-5 requests that should trigger it and 2-3 that should not.
- Inputs and outputs: required user input, discoverable environment context, final deliverable, output format, and Definition of Done.
- Execution boundary: tools, scripts, APIs, permissions, side effects, sandbox constraints, confirmation requirements, and fallback behavior.
- Evaluation: success criteria, smoke prompts, non-trigger prompts, deterministic checks, capability evals, regression traces, grader type, and release requirements.

Only ask questions that materially affect the review. If the artifact already answers a question, do not ask it again.

## Evidence Levels

Use these labels for high-priority findings:

- `deterministic`: script output, file existence, frontmatter, command output, schema checks, or other mechanical evidence.
- `observed`: direct reading of `SKILL.md`, references, scripts, assets, evals, or sample artifacts.
- `inferred`: design judgment based on the Skill goal, structure, and likely failure modes.
- `needs context`: missing business goal, user profile, runtime environment, or failure cost prevents a final judgment.

Do not present inferred or needs-context findings as deterministic failures.

## Review Dimensions

Check these dimensions in order:

1. Necessity and boundary: repeated value, stable failure modes, clear scope, and not better handled by a deterministic tool or one-off prompt.
2. Trigger contract: `description` is trigger-first, covers natural-language use, and avoids being a workflow summary; non-trigger boundaries are clear when needed.
3. Input/output contract: required inputs, discoverable context, deliverables, output format, and Definition of Done are explicit.
4. Workflow gates and degrees of freedom: steps are actionable; the Skill says when to ask, assume, stop, retry, escalate, confirm, or verify.
5. Progressive disclosure and assets: `SKILL.md` stays concise; details go to `references/`; deterministic logic goes to `scripts/`; templates/static resources go to `assets/`.
6. Context budget: metadata, body, references, scripts, tools, and schema exposure are bounded and not duplicated.
7. Tool and safety boundary: permissions, side effects, destructive operations, credentials, network use, tool failures, and fallback behavior are clear.
8. Evaluation readiness: smoke prompts, non-trigger prompts, capability evals, regression evals, deterministic graders, and model/human graders are appropriate to risk.
9. Maintainability and governance: naming, ownership, compatibility, version/deprecation expectations, shared resources, and update path are clear.

## Definition of Done

A review is complete only when it includes:

- Verdict: `Ready`, `Needs revision`, or `Not a good Skill candidate`.
- Evidence Summary: what was inspected, what commands ran, what was not verified, and what assumptions were made.
- P0/P1/P2 findings sorted by severity, each with evidence level, evidence, impact, and repair.
- A scorecard covering the review dimensions.
- Explicit assumptions or blocking questions when context is incomplete.
- A concrete improvement artifact when useful: rewritten `description`, section structure, patch, script suggestion, or eval checklist.

## Output Format

Use this structure:

```markdown
**Evidence Summary**
- Files inspected: <paths or "not available">
- Commands run: <commands or "none">
- Evidence limits: <assumptions, missing context, or unavailable checks>

**Verdict**
<Ready / Needs revision / Not a good Skill candidate>，用 1-2 句话说明理由。

**Highest Priority Issues**
- [P0/P1/P2][deterministic/observed/inferred/needs context] <issue>: <why it matters>. Evidence: <file/line, command output, or cited observation>. Repair: <specific change>.

**Scorecard**
| Dimension | Score | Notes |
|---|---:|---|
| Necessity and boundary | 0-5 | ... |
| Trigger contract | 0-5 | ... |
| Input/output contract | 0-5 | ... |
| Workflow gates and degrees of freedom | 0-5 | ... |
| Progressive disclosure and assets | 0-5 | ... |
| Context budget | 0-5 | ... |
| Tool and safety boundary | 0-5 | ... |
| Evaluation readiness | 0-5 | ... |
| Maintainability and governance | 0-5 | ... |

**Recommended Patch**
<Include rewritten description, section outline, script suggestion, or patch when useful. Omit if not useful.>

**Eval Checklist**
<Minimum smoke prompts, non-trigger prompts, deterministic checks, or regression cases when useful.>

**Open Questions**
<Only questions that block a more certain judgment.>
```

Severity rules:

- `P0`: makes the Skill unusable, unsafe, or obviously mis-triggered in normal use.
- `P1`: causes unstable output, hidden failure, major context bloat, or poor team reuse.
- `P2`: maintainability, clarity, evaluation, or governance improvement that should be handled but does not block use.

## Resource Guide

- Use `scripts/check_skill.py` for deterministic structure, frontmatter, resource, and soft-warning checks.
- Use `references/team-skill-rubric.md` for detailed scoring anchors, evidence levels, common anti-patterns, and improvement patterns.
- Use `references/industry-skill-patterns.md` for trigger-only description, fresh verification evidence, context budget, workflow gates, eval taxonomy, cross-harness metadata, and goal-backward review.
