# Assetization Gate

Use this gate before creating another Skill. The goal is to preserve repeated
business value without turning every useful conversation into a discoverable
runtime entry.

## 1. Is It Worth Persisting?

Persist only when at least two of these signals are present:

- the work recurs or is expected to recur across projects;
- the same omission or failure happens more than once;
- durable domain context, a checker, template, or state contract changes quality;
- another person or runtime should reproduce the behavior;
- the output has a stable Definition of Done.

If the request is one-off, low-risk, and ordinary model instructions are enough,
keep it as a prompt or document example.

## 2. Choose The Smallest Shape

| Shape | Owns | Typical signal |
| --- | --- | --- |
| Skill | One reusable judgment-heavy responsibility with its own trigger and output contract | Users ask for the same atomic capability in natural language |
| Loop | Repeated handoff between existing Skills with explicit state, return edges, and stop conditions | Research and decision must converge over multiple rounds |
| Workflow | Stage-level composition of Skills, Loops, human gates, and Tools | A medium or large product request spans discovery through delivery |
| Tool | Deterministic operation or external side effect with exact inputs, authorization, and read-back | Publish a DingTalk document or create a Yunxiao item |
| Context Pack | Reusable facts or templates without an independent trigger | A domain baseline is loaded only by an owning Skill |

Do not create a Skill solely to name a Workflow, wrap one deterministic command,
or expose a low-frequency template. Packs are install recommendations, not a new
runtime behavior kind.

## 3. Reuse And Overlap Gate

Before adding a stable ID:

1. Search the public catalog, local Skillshare source, system Skills, and current project.
2. Compare trigger language, primary responsibility, input/output contract, resources, and evals.
3. If an existing Skill covers most of the responsibility, extend it with a mode, reference, script, or regression case.
4. Create a new Skill only when the owner, trigger, output, and non-trigger boundary remain independently useful.

## 4. Over-Engineering Check

Reject or simplify the proposal when it introduces any of these without evidence:

- a mega Skill that owns research, decisions, PRD, UI, review, and publication;
- an orchestrator that duplicates Workflow composition;
- a new Loop with no recoverable state or real return edge;
- a Tool described as prose even though its operation can be validated deterministically;
- a Pack treated as a trigger or business workflow;
- a new stable ID for a single customer, report, template, or temporary workaround.

The final decision should state: `do-not-persist`, `extend-existing`,
`create-skill`, `create-loop`, `create-workflow`, `create-tool`, or
`context-pack-only`, with the evidence that supports the choice.
