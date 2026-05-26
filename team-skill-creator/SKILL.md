---
name: team-skill-creator
description: Plan and create team-standard Codex Skills. Use when the user has a repeatable capability request and wants to decide whether it should be a Prompt, Workflow, Tool, Plugin, App, or Skill; check for similar existing Skills; clarify requirements; produce a Creation Decision; create a new Skill only after user confirmation; and validate the result with system and team Skill checks.
---

# Team Skill Creator

## Overview

Use this Skill as the team Skill factory. It adds team gates around the system `skill-creator`: first decide whether a request should become a Skill, then clarify only what matters, create only after confirmation, and validate the result with both system and team checks.

Do not replace the system `.system/skill-creator`. Use it as the baseline for Codex Skill structure and scaffolding.

## Workflow

1. Capture the request and restate the intended repeatable capability in one sentence.
2. Run the similarity scan before recommending a new Skill:

```bash
python3 <this-skill>/scripts/inspect_existing_skills.py --name "<candidate-name>" --description "<request summary>"
```

3. Classify the best implementation shape. For non-trivial or ambiguous requests, read `references/creation-rubric.md`.
4. If critical context is missing, ask at most 5 concrete questions. Do not ask for information that can be discovered from local files.
5. Produce a `Creation Decision` before writing files. Include the recommended shape, whether to create a Skill, trigger examples, non-trigger examples, resource plan, eval checklist, risks, and the exact confirmation needed.
6. Create a Skill only after explicit user confirmation. Use:

```bash
python3 <this-skill>/scripts/create_team_skill.py --name "<skill-name>" --description "<trigger description>" --resources scripts,references --path /Users/linctex/.codex/skills
```

7. Replace scaffold placeholders, validate with both checks, and use `skill-reviewer` for a final review before calling a team-facing or high-value Skill ready:

```bash
python3 /Users/linctex/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/linctex/.codex/skills/<skill-name>
python3 -B /Users/linctex/.codex/skills/skill-reviewer/scripts/check_skill.py /Users/linctex/.codex/skills/<skill-name>
```

## Decision Gates

Prefer a Skill when the task is repeated, has stable failure modes, needs domain or team context, benefits from bundled resources, and can be evaluated with smoke prompts or deterministic checks.

Do not create a Skill when the request is a one-off answer, a simple prompt, a purely deterministic command-line operation, a full product surface that should be an app, or an integration better packaged as a plugin.

Use `references/skill-template-standards.md` when writing or reviewing the generated `SKILL.md`.

## Context Intake

Confirm these inputs before recommending creation, or record them as assumptions:

- Target users, reuse frequency, and failure cost.
- Trigger examples, non-trigger examples, and similar existing Skills.
- Required user inputs, discoverable local context, expected output, and Definition of Done.
- Tool, API, file-write, credential, network, and production side effects.
- Minimum validation path: smoke prompts, non-trigger prompts, deterministic checks, and regression cases when needed.

Ask only for missing information that changes the creation decision or generated Skill structure.

## Confirmation Rule

Before writing a new Skill under `/Users/linctex/.codex/skills`, get explicit confirmation that includes either the approved Skill name or clear approval of the `Creation Decision`.

If the user asks to skip confirmation, still show the `Creation Decision` first unless they already supplied all of these: final name, install path, trigger description, required resources, and acceptance checks.

## Output Format

For planning, use:

```markdown
**Creation Decision**
- Recommended shape: <Prompt / Workflow / Tool / Plugin / App / Skill>
- Create a Skill: <Yes / No / Needs clarification>
- Candidate name: `<skill-name>`
- Similar existing Skills: <findings from inspect_existing_skills.py>
- Trigger examples: <3-5 examples>
- Non-trigger examples: <2-3 examples>
- Required context: <known / missing>
- Resource plan: <SKILL.md / references / scripts / assets>
- Eval checklist: <smoke, non-trigger, deterministic, regression if needed>
- Risks: <context budget, overlap, side effects, maintenance>
- Confirmation needed: <exact approval needed before file writes>
```

After creation, use:

```markdown
**Creation Result**
- Created path: <path>
- Key files: <SKILL.md, references, scripts, agents/openai.yaml>
- Commands run: <init, validate, reviewer checks>
- Validation result: <pass/fail with key output>
- Remaining work: <missing references, scripts, evals, review items>
- Next regression: <real prompts or sample artifacts>
```

## Definition of Done

A team Skill creation task is complete only when one of these is true:

- The request is classified as not needing a Skill, with a concrete alternative.
- A `Creation Decision` is delivered and awaits confirmation.
- A confirmed Skill is created, placeholders are removed, system validation passes, team checker results are reported, and remaining review or regression work is explicit.

## Resource Guide

- Use `references/creation-rubric.md` for the Prompt / Workflow / Tool / Plugin / App / Skill decision.
- Use `references/skill-template-standards.md` for the generated `SKILL.md` structure and quality bar.
- Use `scripts/inspect_existing_skills.py` before proposing a new Skill.
- Use `scripts/create_team_skill.py` only after confirmation.
