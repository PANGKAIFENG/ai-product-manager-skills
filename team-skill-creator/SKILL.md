---
name: team-skill-creator
description: Plan and create team-standard Codex Skills. Use when the user has a repeatable capability request and wants to decide whether it should be a Prompt, Workflow, Tool, Plugin, App, or Skill; check for similar existing Skills; clarify requirements; produce a Creation Decision; create a new Skill only after user confirmation; and validate the result with system and team Skill checks.
---

# Team Skill Creator

## Overview

Use this Skill as the team Skill factory. It adds team gates around the system `skill-creator`: first decide whether a request should become a Skill, then clarify only what matters, create or import only after confirmation, and validate the result with both system and team checks.

It also handles import-style creation where the proposed new Skill comes from a Git repository, marketplace download, local clone, or another agent's Skill directory. In that case, treat the upstream Skill as a source candidate, not as an automatically accepted final artifact.

Do not replace the system `.system/skill-creator`. Use it as the baseline for Codex Skill structure and scaffolding.

## Workflow

1. Capture the request and restate the intended repeatable capability in one sentence.
2. Run the similarity scan before recommending a new Skill. Scan Skillshare canonical source, Codex, Claude, `.agents`, system Skills, and any import source root:

```bash
python3 <this-skill>/scripts/inspect_existing_skills.py --name "<candidate-name>" --description "<request summary>"
python3 <this-skill>/scripts/inspect_existing_skills.py --name "<candidate-name>" --description "<request summary>" --import-root /path/to/imported/skills --json
```

3. Classify the best implementation shape. For non-trivial or ambiguous requests, read `references/creation-rubric.md`.
4. If critical context is missing, ask at most 5 concrete questions. Do not ask for information that can be discovered from local files.
5. Produce a `Creation Decision` before writing files. Include the recommended shape, whether to create or import a Skill, trigger examples, non-trigger examples, resource plan, eval checklist, risks, and the exact confirmation needed. For import candidates, also include the source candidate, best base, merge decision, borrowed strengths, provenance, and install/sync plan.
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

## Import / Clone / Marketplace Skill Intake

Use this flow when the user wants to add Skills from another repository, marketplace, local clone, downloaded bundle, plugin, or another agent's Skill folder.

1. Identify the import root and list every `SKILL.md` under it. Record the upstream repo URL, commit or version, plugin/package name, original relative path, and license when discoverable.
2. Run `inspect_existing_skills.py` with `--import-root` for each candidate. Include roots for any special local source the user mentions.
3. Build a comparison matrix for exact-name and high-overlap candidates:

| Dimension | Existing Skill | Source candidate | Judgment |
|---|---|---|---|
| Trigger contract |  |  |  |
| Workflow completeness |  |  |  |
| Resource split |  |  |  |
| Validation/eval ability |  |  |  |
| Context budget |  |  |  |
| Maintainability |  |  |  |
| Source/license/provenance |  |  |  |

4. Choose one of four merge decisions:
   - `new`: no meaningful overlap; import as a new team Skill.
   - `merge-into-existing`: overlap exists and the local Skill is the stable user-facing entry.
   - `replace-with-source`: source candidate has the better architecture; keep local name only if it avoids breaking existing users.
   - `do-not-import`: capability is already covered or is better absorbed into another Skill.
5. Default policy: preserve the upstream name for new imports; when similar Skills exist, merge rather than duplicate; retain the local name if renaming would break existing Skillshare habits.
6. Preserve provenance in a concise `references/provenance.md` or a `metadata.provenance` frontmatter object. At minimum include source repo, commit/version, plugin/package, original path, license status, import date, and merge notes.
7. Copy all required upstream resources (`references/`, `scripts/`, `assets/`, templates, and directly linked markdown files). Rewrite paths only when needed to keep references one level away and mentioned from `SKILL.md`.
8. After import or merge, run system validation and `skill-reviewer`; fix P0/P1, record P2 if intentionally deferred; sync through Skillshare only after validation is acceptable.

## Context Intake

Confirm these inputs before recommending creation, or record them as assumptions:

- Target users, reuse frequency, and failure cost.
- Trigger examples, non-trigger examples, and similar existing Skills.
- Required user inputs, discoverable local context, expected output, and Definition of Done.
- Tool, API, file-write, credential, network, and production side effects.
- Minimum validation path: smoke prompts, non-trigger prompts, deterministic checks, and regression cases when needed.
- For imports: source repo, commit/version, original path, license, exact-name overlaps, similar Skills, chosen base, borrowed strengths, and sync targets.

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
- Source candidate: <repo/path/version, or none>
- Best base: <existing Skill / source Skill / new scaffold>
- Merge decision: <new / merge-into-existing / replace-with-source / do-not-import>
- Borrowed strengths: <what will be absorbed from each source>
- Provenance: <repo, commit/version, plugin/package, original path, license>
- Install/sync plan: <canonical source path and targets>
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
- Imported from: <repo, commit/version, plugin/package, original paths, license>
- Merge decision: <new / merge-into-existing / replace-with-source / do-not-import>
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
- An imported Skill is either merged, rejected with reason, or installed into canonical Skillshare source with required resources, provenance, validation results, and sync plan.

## Resource Guide

- Use `references/creation-rubric.md` for the Prompt / Workflow / Tool / Plugin / App / Skill decision.
- Use `references/skill-template-standards.md` for the generated `SKILL.md` structure and quality bar.
- Use `scripts/inspect_existing_skills.py` before proposing a new Skill.
- Use `scripts/create_team_skill.py` only after confirmation.
