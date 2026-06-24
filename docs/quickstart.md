# Quickstart

This guide helps you try AI Product Manager Skills Library in a local Agent workflow.

The repository contains root-level Skill folders. Each Skill folder has a `SKILL.md` file with a stable `name` and `description`.

## 1. Clone The Repository

```bash
git clone https://github.com/PANGKAIFENG/ai-product-manager-skills.git
cd ai-product-manager-skills
```

## 2. Pick A First Skill

Start with one workflow:

| Goal | Skill | Prompt |
| --- | --- | --- |
| Clarify a fuzzy product problem | `ai-collaboration-calibration` | `$ai-collaboration-calibration 先别执行，帮我看清这个问题` |
| Frame a complex multi-round exploration | `complex-exploration` | `$complex-exploration 先不要直接写方案，帮我判断这个复杂任务怎么探索并沉淀资产` |
| Frame or research a topic for PM decisions | `research-topic-compiler` | `$research-topic-compiler 把这个大白话拆成研究目标和输出要求，再做研究计划` |
| Turn competitor evidence into a product decision brief | `competitive-analysis` | `$competitive-analysis 研究这个竞品对我们的产品决策有什么启发` |
| Choose between options | `decision-research` | `$decision-research 帮我比较这几个方案，给一个有立场推荐` |
| Brainstorm a design before PRD or implementation | `brainstorming` | `$brainstorming 先不要写 PRD，帮我脑暴 2-3 个设计方案` |
| Draft a PRD | `prd-architect` | `$prd-architect 把这个想法整理成 PRD-lite` |
| Review a PRD | `prd-review` | `$prd-review 从研发和测试视角审一下这个 PRD` |
| Break a ready PRD into GitHub issues | `prd-to-issues` | `$prd-to-issues 把这个 PRD 拆成 GitHub implementation issues，先给我 draft` |
| Confirm UI structure and states | `ui-wireframe-to-html` | `$ui-wireframe-to-html 基于 PRD 先出 UI 结构、状态模型和 ASCII 布局` |
| Create a high-fidelity desktop UI handoff | `ui-mockup-desktop-workbench` | `$ui-mockup-desktop-workbench 基于 PRD、UI 规范和真实前端项目生成高保真 UI handoff` |
| Pressure-test a plan | `grill-me` | `$grill-me 拷问我的方案，找失败模式` |
| Diagnose assetization level | `ai-work-assetization-diagnoser` | `$ai-work-assetization-diagnoser 这个 prompt 应该沉淀成 workflow 还是 Skill？` |

## 3. Install Or Link The Skills

Recommended paths:

- Codex users: [install-codex.md](install-codex.md)
- Claude Code users: [install-claude-code.md](install-claude-code.md)
- skillshare users: use `skillshare install` and `skillshare sync`

If your tool supports manually loaded Agent Skills, copy or symlink the thirteen root-level Skill directories into the tool's Skills directory.

## 4. Verify Skill Discovery

Ask your agent to list available Skills or explicitly invoke one by name:

```text
$prd-architect 把“AI 会议纪要自动生成任务清单”整理成 PRD-lite
```

Expected signs:

- The agent recognizes `prd-architect`.
- It asks only necessary clarification questions.
- It produces a structured PRD rather than a generic brainstorm.
- It keeps product requirements separate from implementation planning.

## 5. Use The Workflow

A common AI PM path:

```text
$ai-collaboration-calibration 先帮我校准这个需求是不是值得做
$complex-exploration 先不要直接写方案，帮我判断这个复杂任务怎么探索并沉淀资产
$research-topic-compiler 把这个模糊方向拆成研究目标、研究问题和输出要求，再输出 PM 决策输入
$competitive-analysis 研究这个竞品对我们的产品决策有什么启发
$decision-research 帮我比较候选方案，给一个有立场推荐
$brainstorming 先不要写 PRD，帮我脑暴 2-3 个设计方案并推荐一个
$prd-architect 基于上面的结论写 PRD-standard
$prd-review 从研发和测试视角审这个 PRD
$prd-to-issues 把 ready PRD 拆成 vertical-slice GitHub issues，先 draft-only
$ui-wireframe-to-html 基于 PRD 先出 UI 结构、状态模型和 ASCII 布局
$ui-mockup-desktop-workbench 基于 PRD、UI 规范和真实前端项目生成高保真 UI handoff
$grill-me 拷问最终方案，找失败模式
$ai-work-assetization-diagnoser 判断这套重复 AI 工作要不要沉淀成 Skill 或 Loop
```

When the PRD is clear enough, use `prd-to-issues` for GitHub issue backlog or hand it to Superpowers `writing-plans` for file-level implementation planning.

## Troubleshooting

Skill not showing up:

- Check that each Skill folder contains `SKILL.md`.
- Check that the Skill folder is in a directory your Agent tool scans.
- Restart the Agent tool if it caches available Skills.
- Try explicit invocation with `$skill-name`.

Wrong Skill triggers:

- Read [SKILL_ROUTING.md](../SKILL_ROUTING.md).
- Make the prompt state the workflow stage: brainstorm, research, PRD draft, PRD review, or pressure test.
- Open an issue if the Skill descriptions need clearer boundaries.
