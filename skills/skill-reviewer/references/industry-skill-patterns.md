# Industry Skill Patterns

Use this reference when a Skill review needs industry-grade standards, cross-harness compatibility, context-budget analysis, or concrete optimization patterns beyond the baseline team rubric.

## How to Use

- Treat these patterns as an overlay on top of the Codex baseline: `name`, `description`, concise `SKILL.md`, and progressive disclosure remain the default.
- Use the patterns to explain design risk and repair options, not to force every Skill into one ecosystem's file format.
- Prefer soft warnings for reasonable ecosystem metadata unless it hides or weakens the trigger contract.

## Transferable Patterns

| Pattern | What to Check | Why It Matters |
| --- | --- | --- |
| Trigger-only description | `description` says what the Skill does and when to use it; it does not summarize the full workflow. | The model may only see metadata before triggering. Bad metadata causes missed triggers or wrong triggers. |
| Fresh verification evidence | Completion claims are backed by newly observed command output, file inspection, test results, or explicit assumptions. | Prevents agents from claiming work is done based on intent or stale memory. |
| Context budget | `SKILL.md` is concise; details are in references; references are one level from `SKILL.md`; tool/schema exposure is bounded. | Skill ecosystems degrade when every turn pays for unnecessary metadata, instructions, or tool descriptions. |
| Workflow gates | The Skill says when to ask, continue with assumptions, stop, retry, escalate, or require confirmation. | Stable execution requires decision points, not only linear steps. |
| Eval taxonomy | Evaluation distinguishes smoke prompts, non-trigger prompts, capability evals, regression evals, deterministic graders, and model/human graders. | "Has tests" is too vague to prove a Skill works. |
| Cross-harness metadata | Fields such as `allowed-tools`, `triggers`, `version`, `argument-hint`, `handoffs`, `scripts`, `requires`, `tools`, `origin`, and `color` are recognized as ecosystem metadata. | A reviewer should not reject valid Claude/GSD/spec-kit/gstack artifacts just because they are not Codex-native. |
| Goal-backward review | Start from the Skill's goal and failure cost, then check trigger, inputs, workflow, tools, validation, and governance. | Avoids rewarding a well-structured document that cannot actually achieve the goal. |
| Deterministic downshift | Repeated, fragile, parsing-heavy, or format-exact operations are moved to scripts or tools. | Reduces drift and avoids repeatedly asking the model to recreate deterministic logic. |

## Source-Specific Lessons

### gstack

- Uses generated Skill documents, health checks, evals, e2e tests, and metadata such as `version`, `allowed-tools`, and `triggers`.
- Borrow the mechanisms: generation, checking, testing, and governance.
- Do not copy large runtime preambles into every team Skill.

### superpowers

- Treats Skill writing as process-document TDD: first observe what the agent fails to do, then teach only that durable behavior.
- Emphasizes that `description` is for triggering, not workflow summary.
- Requires verification before completion claims.

### everything-claude-code

- Makes eval harnesses, verification loops, context budgets, and security reviews first-class.
- Useful for reviewing high-value or high-risk Skills where regressions and context bloat matter.
- Encourages separating deterministic, model, and human graders.

### spec-kit

- Uses command metadata, handoffs, scripts, checklists, and stop/ask/continue gates.
- Limits clarification loops and requires measurable success criteria.
- Shows why a reviewer should distinguish incompatible format from valid ecosystem extension.

### GSD Redux

- Keeps orchestrators thin and pushes complex work into fresh-context agents, CLI tools, and state files.
- Uses goal-backward and adversarial review for plans.
- Reinforces that routing, state, and context reload strategy matter for complex Skills.

## Review Heuristics

- If `description` cannot answer "when should this trigger?", treat it as a trigger-contract issue even if the body is excellent.
- If a claim cannot be tied to deterministic, observed, inferred, or needs-context evidence, mark the evidence gap explicitly.
- If the Skill has many instructions but no completion gate, ask how the user will know the result is done.
- If the Skill grows past concise workflow guidance, move details into a one-level reference.
- If a script would be safer than prose, recommend a script suggestion rather than more instructions.
- If a file uses non-Codex metadata, identify the ecosystem and evaluate whether the metadata is useful, stale, or excessive.

## Anti-Patterns

- Copying an entire platform runtime preamble into a single Skill.
- Turning every good prompt into a Skill without repeated use or stable failure modes.
- Treating `README.md`, install guides, and changelogs as required Skill files.
- Failing a cross-ecosystem artifact solely because it has extra frontmatter fields.
- Requiring full eval harnesses for low-risk personal Skills.
- Allowing high-value team Skills to ship with no smoke prompts, no regression cases, and no deterministic checks.
