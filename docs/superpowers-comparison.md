# How This Complements Superpowers

This repository is not a replacement for Superpowers.

Superpowers is strongest once the problem is clear enough to plan, test, implement, verify, and finish development work. AI Product Manager Skills Library focuses on the product-side work before and around that handoff.

## Boundary

| Stage | This repository | Superpowers |
| --- | --- | --- |
| Fuzzy problem | Clarify assumptions, goals, constraints, and decision criteria. | Usually too early. |
| Topic research | Build PM decision input, evidence, concept lineage, and option framing. | Usually not the main job. |
| PRD drafting | Create PRD-lite, PRD-standard, or PRD-ai-native. | Consumes the PRD later. |
| PRD review | Find gaps, contradictions, untestable requirements, and handoff blockers. | May use the corrected PRD for implementation planning. |
| Plan pressure test | Challenge tradeoffs, dependencies, and failure modes. | Can then write or execute a plan. |
| Implementation plan | Provides readiness criteria and product context. | `writing-plans` owns file-level plan, tests, and commits. |
| Development execution | Out of scope. | TDD, debugging, executing plans, verification, and finishing branches. |

## Handoff Contract

Before handing work to Superpowers `writing-plans`, the PRD should make these clear:

- Target user and problem.
- Scope and non-goals.
- Main workflow and states.
- Inputs, outputs, and edge cases.
- Acceptance criteria.
- Known risks and open assumptions.
- Any diagrams or mockups required for engineering alignment.

If these are missing, use:

- `ai-collaboration-calibration` to clarify the problem.
- `research-topic-compiler` or `tech-research` to gather decision evidence.
- `prd-architect` to draft the PRD.
- `prd-review` to find blockers.
- `grill-me` to pressure-test the plan.

## Example Flow

```text
1. $ai-collaboration-calibration 先别写 PRD，帮我看清这个产品问题
2. $research-topic-compiler 系统研究这个主题，输出 PM 决策输入
3. $prd-architect 基于上面结论写 PRD-standard
4. $prd-review 从研发和测试视角审这个 PRD
5. $grill-me 拷问最终方案
6. Superpowers $writing-plans 基于修订后的 PRD 写实现计划
```

The key rule: product readiness here, implementation readiness there.
