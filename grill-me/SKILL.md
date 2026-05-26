---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when the user wants to stress-test a plan, get grilled on a design, pressure-test tradeoffs, or mentions "grill me".
---

# Grill Me

## Overview

Use this Skill to pressure-test a plan or design through a focused interview. The goal is shared understanding, not a long list of disconnected questions.

## Workflow

1. Restate the plan or design being grilled in one sentence.
2. Identify the main decision branches, dependencies, assumptions, and likely failure modes.
3. Ask one question at a time. Wait for the user's answer before continuing unless the answer can be discovered locally.
4. For each question, provide your recommended answer or current hypothesis so the user can accept, reject, or refine it.
5. If a question can be answered by exploring the codebase or local docs, inspect them instead of asking.
6. Resolve branches in dependency order. Do not jump to downstream choices while upstream constraints are still unstable.
7. Summarize settled decisions, remaining open questions, and any plan changes when the grilling session ends or pauses.

## Context Intake

Use available artifacts first: PRDs, issues, code, docs, ADRs, diagrams, logs, and prior user messages. Ask only for missing information that changes a real decision.

## Output

The live output is one question at a time with a recommended answer. The closing output is a concise decision log:

- Settled decisions.
- Rejected options and why.
- Open questions.
- Recommended next step.

## Definition of Done

- Important branches have been explored in a sensible order.
- Each asked question had a reason and a recommended answer.
- Codebase-answerable questions were answered by inspection.
- The user has a decision log or a clear next unresolved question.

## Evaluation

Smoke prompts:

- `Grill me on this architecture plan.`
- `Pressure-test my proposal before I send it.`
- `Ask me hard questions about this design.`

Non-trigger prompts:

- `Write the final proposal for this plan.`
- `Summarize this PRD without interviewing me.`

## Resources

- `references/provenance.md` records the upstream source, local overlap, and merge notes.
