# Asset Layer Rubric

Use this rubric when the right asset layer is ambiguous.

| Layer | Minimum Signal | Failure Signal |
| --- | --- | --- |
| Do Not Assetize | Low repeatability, no stable input/output, no reuse audience. | User cannot name when it would be reused. |
| Prompt | Reusable wording or checklist is enough. | Needs files, state, or deterministic verification. |
| Context Pack | Value comes from curated sources, examples, constraints, or glossary. | Steps and decisions are more important than context. |
| Workflow | Stable sequence with human checkpoints and handoff format. | Needs automatic routing, trigger contract, or packaged resources. |
| Skill | Frequent task with clear trigger, non-triggers, inputs, output contract, and verification. | Needs persistent state, retries, or scheduled updates. |
| Loop | Multi-round state, resumption, stop conditions, retries, or human gates. | Actually a product/system with permissions, audit, cost, or multiple agents. |
| System | Multiple Skills/Loops/agents with permissions, evaluation, governance, or UI/runtime needs. | Can be solved with a single Skill or Workflow. |

Prefer the smallest layer that creates durable reuse.
