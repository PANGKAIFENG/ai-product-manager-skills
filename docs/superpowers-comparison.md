# How This Complements Superpowers

This repository is not a replacement for Superpowers.

Superpowers is strongest once the problem is clear enough to plan, test, implement, verify, and finish development work. AI Product Manager Skills Library focuses on the product-side work before and around that handoff.

## Boundary

| Stage | This repository | Superpowers |
| --- | --- | --- |
| Fuzzy problem | Clarify assumptions, goals, constraints, and decision criteria. | Usually too early. |
| Topic research | Build PM decision input, evidence, concept lineage, and option framing. | Usually not the main job. |
| Design brainstorming | Compare 2-3 product/design paths, recommend one, align UI/mockup work with local visual standards, and produce a design spec before PRD or implementation planning. | Use implementation brainstorming after the product/design direction is confirmed and ready for file-level planning. |
| PRD drafting | Create PRD-lite, PRD-standard, or PRD-ai-native. | Consumes the PRD later. |
| PRD review | Find gaps, contradictions, untestable requirements, and handoff blockers. | May use the corrected PRD for implementation planning. |
| Implementation issue backlog | `prd-to-issues` breaks a ready PRD into GitHub implementation issue drafts with coverage and AFK / HITL labels. | May consume the issue backlog as planning input, but does not own GitHub issue publishing. |
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
- `research-topic-compiler` to build topic understanding, `x-public-signal-research` to turn X public conversation into PM evidence, or `decision-research` to choose between concrete options.
- `brainstorming` to compare design paths and confirm the design before writing PRD or implementation plan.
- `prd-architect` to draft the PRD.
- `prd-review` to find blockers.
- `prd-to-issues` to create a GitHub issue backlog after the PRD is ready.
- `grill-me` to pressure-test the plan.

## Example Flow

```text
1. $ai-collaboration-calibration 先别写 PRD，帮我看清这个产品问题
2. $research-topic-compiler 系统研究这个主题，输出 PM 决策输入
3. $x-public-signal-research 用 X 公开内容补证用户痛点和反证
4. $decision-research 比较候选方案，给一个有立场推荐
5. $brainstorming 先比较 2-3 个设计路径，确认推荐方案
6. $prd-architect 基于上面结论写 PRD-standard
7. $prd-review 从研发和测试视角审这个 PRD
8. $prd-to-issues 把 ready PRD 拆成 GitHub implementation issues，先给 draft
9. $grill-me 拷问最终方案
10. Superpowers $writing-plans 基于修订后的 PRD 或 issue backlog 写实现计划
```

The key rule: product readiness here, implementation readiness there.
