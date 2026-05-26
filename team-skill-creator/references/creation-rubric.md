# Creation Rubric

Use this rubric before creating a new Skill. The goal is to prevent Skill sprawl and choose the smallest durable mechanism that solves the user's repeatable need.

## Decision Rule

Ask three questions first:

- Can a general model handle this with no durable context or workflow?
- Does an existing Skill, script, workflow, plugin, or app already cover most of it?
- Is there a stable failure mode worth encoding for future reuse?

If the answer to the third question is no, do not create a Skill.

## Shape Selection

| Shape | Use when | Do not use when |
| --- | --- | --- |
| Prompt | One-off or low-risk request where ordinary instructions are enough | The task repeats, needs resources, or has known failure modes |
| Workflow | Multi-step process that coordinates human or agent actions but does not need a reusable Skill package | The process needs trigger metadata, bundled references, scripts, or portable reuse |
| Tool | Deterministic operation with clear input/output, especially parsing, conversion, generation, or validation | The task needs judgment, context intake, or flexible workflow decisions |
| Plugin | Capability needs installable integration, MCP/app wiring, persistent service behavior, or UI/runtime dependencies | The main value is procedural knowledge and local resources |
| App | Users need a persistent product surface, stateful UI, multi-user behavior, or non-agent interaction | The work is best done by Codex following instructions |
| Skill | Repeatable agent capability needs trigger contract, procedural guidance, domain context, bundled resources, tool boundaries, and evaluation | A prompt, tool, workflow, plugin, or app is simpler and more reliable |

## Strong Skill Signals

- Reuse frequency is high or expected to grow.
- Team members naturally ask for the capability in similar language.
- The task has stable inputs, outputs, and failure modes.
- The agent needs company, domain, repository, or workflow context.
- The task benefits from `references/`, `scripts/`, or `assets/`.
- Completion can be checked with smoke prompts, deterministic checks, or regression cases.
- The failure cost justifies encoding gates and validation.

## Weak Skill Signals

- The request is only a single deliverable.
- The task is just a style preference or temporary instruction.
- A small script can solve the whole problem deterministically.
- The intended scope overlaps heavily with an existing Skill.
- The team cannot name trigger examples or success criteria.
- The Skill would mostly contain generic advice the model already knows.

## Required Context Before Creation

Collect or infer these before recommending a Skill:

- Target users and whether the Skill is personal, team, or production-grade.
- Business or domain goal.
- Three to five trigger examples and two to three non-trigger examples.
- Required inputs, discoverable context, expected output, and Definition of Done.
- Required tools, scripts, APIs, permissions, and side effects.
- Failure cost and confirmation requirements.
- Minimum eval plan.

Ask at most 5 questions. If optional details are missing, proceed with explicit assumptions.

## Similarity and Reuse Gate

Before proposing a new Skill, scan:

- `/Users/linctex/.codex/skills`
- `/Users/linctex/.codex/skills/.system`
- `/Users/linctex/.agents/skills`

If an existing Skill covers at least 70% of the need, recommend updating or extending it instead of creating a new Skill.

## Creation Decision Checklist

The `Creation Decision` must include:

- Recommended shape.
- Whether to create a Skill.
- Candidate name.
- Similar existing Skills and overlap risk.
- Trigger and non-trigger examples.
- Resource plan for `SKILL.md`, `references/`, `scripts/`, and `assets/`.
- Minimum eval checklist.
- Risks and confirmation required before writes.
