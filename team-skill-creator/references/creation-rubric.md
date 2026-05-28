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

- The user's GitHub Skill online repository first. Use the refreshed local checkout only after checking remote URL, branch/upstream, ahead/behind, and dirty state.
- The GitHub catalog files in that checkout, including `SKILL_REGISTRY.md`, `categories/`, and same-name Skill directories.
- The target local `multica-skill` directory when the Skill should appear inside Multica.
- `/Users/linctex/.config/skillshare/skills`
- `/Users/linctex/.codex/skills`
- `/Users/linctex/.claude/skills`
- `/Users/linctex/.codex/skills/.system`
- `/Users/linctex/.agents/skills`
- Any import root from a Git clone, marketplace download, plugin, or local Skill source.

If an existing Skill covers at least 70% of the need, recommend updating or extending it instead of creating a new Skill.

## Catalog Placement Gate

Before creating or importing, choose the GitHub catalog placement:

- Source status: remote URL, branch/upstream, ahead/behind, dirty state, and whether fetch was attempted.
- GitHub action: optimize existing, add new, merge into another Skill, or keep local/private only.
- Category: existing category slug and Chinese label from `SKILL_REGISTRY.md`; if none fits, proposed new category slug, label, and boundary.
- Status: `core`, `active`, `keep`, `review`, or `private-only`.
- Discoverability updates: `中文速查`, `SKILL_REGISTRY.md`, `categories/README.md`, and the category README.

Keep English `name:` and folder slugs stable. Do not move real Skill directories under category folders; categories are reading/navigation metadata and should remain excluded from skill discovery when the catalog uses `.skillignore`.

## Import Decision Gate

When the source is an existing Skill from another repo or marketplace, decide whether to import, merge, replace, or reject it. Compare:

- Trigger contract and false-positive risk.
- Workflow completeness and missing gates.
- Resource split across `SKILL.md`, `references/`, `scripts/`, and `assets/`.
- Validation and eval readiness.
- Context budget and duplication.
- Maintainability and ownership.
- Provenance, license, and update path.

Prefer merging overlapping Skills over creating duplicates. Preserve the upstream name only for new imports; keep the existing local name when it is already the user-facing habit. Always record source repo, commit/version, plugin/package, original path, license status, import date, and merge notes.

## Runtime / App Sync Gate

When the target is a local app or managed workspace:

- Identify whether the app reads runtime local folders, a workspace database/API, or both.
- Prefer the confirmed local `multica-skill` directory or supported import/list command or UI/API over copying into an unknown internal store.
- Compare current app/workspace copy before overwriting same-name Skills.
- Record the exact distribution target: GitHub checkout, `multica-skill`, Codex path, Claude path, app workspace/API/UI import, or app-local Skill root.
- Verify with the narrowest available check: target directory listing, app CLI/API list, UI import result, or `skillshare sync --json` only if Skillshare is explicitly used.

## Creation Decision Checklist

The `Creation Decision` must include:

- Recommended shape.
- Whether to create a Skill.
- Candidate name.
- Similar existing Skills and overlap risk.
- Source candidate, best base, merge decision, borrowed strengths, provenance, and install/sync plan for import tasks.
- Category/status and GitHub action decision.
- Distribution targets and verification method, especially for Multica, Codex, Claude, or other app-backed Skill stores.
- Trigger and non-trigger examples.
- Resource plan for `SKILL.md`, `references/`, `scripts/`, and `assets/`.
- Minimum eval checklist.
- Risks and confirmation required before writes.
