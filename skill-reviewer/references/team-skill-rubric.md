# Team Skill Review Rubric

Use this rubric to review team Skills as reusable capability units. A Skill is not a long prompt; it is a trigger contract plus execution guidance, resource loading, tool boundaries, evaluation, and governance.

## Scoring

Score each dimension from 0 to 5.

- `0`: Missing or actively harmful.
- `1`: Vague mention only.
- `2`: Partially described but not stable enough for team reuse.
- `3`: Usable for ordinary cases with clear gaps.
- `4`: Team-ready with minor improvement opportunities.
- `5`: Concrete, testable, maintainable, and robust.

Recommended verdict:

- `Ready`: No P0/P1 issues and average score >= 4.
- `Needs revision`: Any P1 issue, or average score from 2.5 to 4.
- `Not a good Skill candidate`: Better as a prompt, deterministic tool, workflow, plugin, or app, or average score < 2.5.

## Evidence Levels

Use evidence levels when writing issues.

- `deterministic`: From script output, file existence, frontmatter, command output, schema checks, or other mechanical evidence.
- `observed`: From reading `SKILL.md`, references, scripts, assets, evals, or sample artifacts.
- `inferred`: A design judgment derived from the Skill goal, structure, and known failure modes.
- `needs context`: Business goal, user profile, runtime environment, or failure cost is missing, so the judgment cannot be final.

## Dimension 1: Necessity and Boundary

A good Skill needs repeated use, stable failure modes, and a clear reason not to be a one-off prompt or deterministic tool.

Check:

- The task is repeated, not a one-time request.
- The failure modes are stable enough to encode.
- The capability is not better handled entirely by a script, CLI, workflow, plugin, or app.
- The intended level is clear: personal, team, or production-grade.
- The Skill does not overlap heavily with an existing Skill.

Common issues:

- The Skill is only a long prompt.
- A single deterministic operation is wrapped in agent instructions.
- The boundary is so broad that it competes with many existing Skills.

## Dimension 2: Trigger Contract

YAML `description` is the primary trigger contract. It must say what the Skill does and when to use it.

Check:

- `name` matches the folder name and uses lowercase letters, digits, and hyphens.
- Codex-native Skills include required `name` and `description`.
- `description` includes concrete "Use when..." semantics, user intent, domains, file types, objects, or keywords.
- `description` covers natural-language user requests, not only slash commands.
- `description` is trigger-first, not a workflow summary.
- The body states non-trigger boundaries when confusion is likely.
- Extra ecosystem metadata does not replace a clear `description`.

Common issues:

- `description` is only a noun phrase.
- Trigger examples only appear in the body, which loads too late.
- `description` is bloated with step-by-step workflow.
- The Skill relies on explicit commands and misses natural-language usage.

## Dimension 3: Input and Output Contract

The Skill must define the interaction contract clearly enough for another agent to execute consistently.

Check:

- Required user inputs are explicit.
- Discoverable environment context is separated from information the user must provide.
- Missing-context behavior is clear: ask, assume, or stop.
- Final deliverable and output format are explicit.
- Definition of Done is concrete and checkable.

Common issues:

- It says "ask clarifying questions" without saying which information is essential.
- The output is only described as a "report" or "suggestions".
- Completion depends on subjective confidence instead of observable criteria.

## Dimension 4: Workflow Gates and Degrees of Freedom

The workflow should guide execution without over-constraining judgment.

Check:

- Steps are ordered and executable.
- The Skill distinguishes judgment-heavy work from deterministic work.
- Fragile, repeated, or format-exact operations are moved to scripts or tools.
- It says when to ask, continue with assumptions, stop, retry, escalate, or require confirmation.
- Verification failure has a defined response.
- Completion claims require fresh evidence when evidence is possible.

Common issues:

- The body reads like an essay, not an executable workflow.
- It adds rigid rules for judgment-heavy tasks.
- It gives too much freedom for exact formats, schemas, or file generation.
- It says to verify but not what to do when verification fails.

## Dimension 5: Progressive Disclosure and Assets

High-quality Skills use three loading layers: metadata, `SKILL.md`, and on-demand bundled resources.

Check:

- `SKILL.md` is concise enough to load on every trigger.
- Detailed policies, domain knowledge, examples, and rubrics are in `references/`.
- Deterministic reusable logic is in `scripts/`.
- Templates, images, fonts, boilerplate, and static files are in `assets/`.
- `SKILL.md` explains when to read or use each resource.
- References are one level away from `SKILL.md`.
- Longer references include a short table of contents.
- Content is not duplicated between `SKILL.md` and references.

Common issues:

- Everything is placed in `SKILL.md`.
- References exist but are not discoverable from the workflow.
- Scripts exist without usage guidance or tests.

## Dimension 6: Context Budget

Context budget is a first-class quality dimension for team Skill ecosystems.

Check:

- `description` is not so long that it becomes body content.
- `SKILL.md` does not approach 500 lines unless there is a strong reason.
- Large details are moved into references with clear load conditions.
- Reference chains are shallow.
- Tool, script, MCP, and schema descriptions are not eagerly exposed without need.
- Similar guidance is not repeated across metadata, body, and references.
- Complex systems use routing or namespaces when listing cost becomes material.

Common issues:

- The Skill is technically correct but too expensive to load.
- Multiple references repeat the same checklist.
- A large tool/schema catalog is exposed before the task requires it.

## Dimension 7: Tool, Permission, and Safety Boundary

The Skill should prevent accidental side effects and unsafe tool use.

Check:

- Required tools, CLIs, MCPs, APIs, or browsers are named when material.
- File writes, destructive operations, network access, credentials, and approvals have boundaries.
- Tool-missing and command-failure fallback behavior is clear.
- The Skill says whether it can edit files directly or should only output findings.
- Production systems default to read-only or explicit confirmation.

Common issues:

- Credentials or local paths are assumed with no discovery or fallback.
- It says to run tests, deploy, or delete without safety gates.
- Side effects are not modeled.

## Dimension 8: Evaluation Readiness

Evaluation should be designed with the Skill, not bolted on after a vague draft.

Check:

- Success criteria are explicit.
- Non-trivial Skills include smoke prompts or realistic examples.
- Non-trigger prompts cover likely false positives.
- Capability evals prove the Skill can perform the target task.
- Regression evals cover known historical failures.
- Deterministic graders cover file, schema, format, command, or invariant checks.
- Model or human graders cover semantic quality, style, and judgment.
- Release gates or trace review guidance exist for high-value Skills.

Common issues:

- There are no examples for trigger or behavior validation.
- Testing only asks whether the final answer "looks good".
- Future versions cannot be compared to current behavior.

## Dimension 9: Maintainability and Governance

Team Skills need ownership and change discipline.

Check:

- Naming is stable and discoverable.
- Compatibility assumptions are documented.
- Important Skills describe version, deprecation, migration, or rollback expectations when relevant.
- Shared references or scripts are reused rather than duplicated.
- Updating the Skill does not require rereading unrelated background.

Common issues:

- A team-critical Skill has no owner or domain boundary.
- Local paths or team assumptions are hard-coded with no explanation.
- It duplicates another Skill's resources or workflow.

## Common Improvement Patterns

- Rewrite `description` as a trigger contract: `Use when Codex needs to...`.
- Add context intake with essential questions and safe assumptions.
- Add output format with a concrete Markdown or JSON skeleton.
- Move detailed background into `references/` and explain when to load it.
- Move fragile repeated logic into `scripts/` and document the command.
- Add a mechanical Definition of Done.
- Add smoke prompts for happy path, missing context, edge case, and non-trigger case.
- Add deterministic checks for YAML, schema, filenames, generated files, or required sections.
- Add side-effect gates: default read-only, ask before writing, never deploy without confirmation.

## Quick Review Questions

Ask only questions that materially change the review:

- What user requests should trigger this Skill, and what requests should not?
- What information must the user provide before the Skill can work?
- What exact artifact should the Skill produce?
- Which parts should be scripts or tools instead of prose instructions?
- How will the team know a new version is better than the current one?
