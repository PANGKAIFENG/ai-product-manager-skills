# AI Product Manager Skills Library

[![Release](https://img.shields.io/github/v/release/PANGKAIFENG/ai-product-manager-skills?display_name=tag)](https://github.com/PANGKAIFENG/ai-product-manager-skills/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-9-2563eb.svg)](SKILL_REGISTRY.md)
[![Codex](https://img.shields.io/badge/Codex-skills-111827.svg)](docs/install-codex.md)
[![Claude Code](https://img.shields.io/badge/Claude_Code-skills-111827.svg)](docs/install-claude-code.md)

中文优先的 AI 产品经理 Agent Skill 库，用来把高频 PM 工作流沉淀成可复用的 Codex Skills、Claude Code Skills 和 Agent Skills。

它重点覆盖：AI 协作脑暴、主题研究、决策调研、PRD 起草、PRD 评审、PRD 到 GitHub issue 拆解、UI mockup、方案压测、AI 工作资产化诊断，以及把需求交给 Superpowers 开发计划前的交付准备。

## Why This Exists

Superpowers 更偏研发实现、TDD、计划执行和代码交付。本仓库补的是产品经理侧的空位：

- 把模糊想法变成可以讨论的产品问题。
- 把产品/技术/行业主题研究转成 PM 判断。
- 把 PRD 起草、评审、复盘和交接变成稳定流程。
- 在进入研发计划前暴露缺口、风险和不可测试点，并把 ready 的 PRD 拆成可领取的 implementation issues。
- 用中文自然语言稳定唤起这些流程，而不是每次重写提示词。

If you are searching for `AI product manager skills`, `Codex skills`, `Claude Code skills`, `PRD workflow`, `product research agent`, `AI collaboration brainstorming`, `requirements review`, or `Chinese AI workflow skills`, this repository is a curated Skill library for that use case.

## Quick Start

```bash
git clone https://github.com/PANGKAIFENG/ai-product-manager-skills.git
cd ai-product-manager-skills
```

Recommended first prompts:

```text
$ai-collaboration-calibration 先别执行，帮我看清这个产品问题
$research-topic-compiler 系统研究这个主题，并转成 PM 决策输入
$decision-research 帮我比较这几个方案，给一个有立场推荐
$prd-architect 把这个想法整理成 PRD-lite
$prd-review 从研发和测试视角审一下这个 PRD
$prd-to-issues 把这个 PRD 拆成 GitHub implementation issues，先给我 draft
$ui-mockup-desktop-workbench 基于 PRD 和 UI 规范生成桌面端真实页面 mockup
$grill-me 拷问我的方案，找失败模式
$ai-work-assetization-diagnoser 判断这段 AI 工作该沉淀成 Prompt、Workflow、Skill 还是 Loop
```

Install paths:

- Codex: see [docs/install-codex.md](docs/install-codex.md)
- Claude Code: see [docs/install-claude-code.md](docs/install-claude-code.md)
- General walkthrough: see [docs/quickstart.md](docs/quickstart.md)

## Who Should Use This

- AI 产品经理：需要把想法、调研、方案和 PRD 推进到可交付状态。
- 产品负责人或业务负责人：希望用 Codex、Claude Code 或其他 Agent 工具复用稳定工作流。
- 研发协作者：需要理解产品侧 Skill 如何与 Superpowers 的开发计划、TDD、执行和验证流程衔接。
- 需要中文优先 AI PM workflow 的团队：希望从脑暴、研究、PRD 到评审形成可复用流程。

## Public Skills

真实 Skill 目录保持在仓库根目录，确保 GitHub 历史、运行时分发和 Skill 触发名称稳定。

| Skill | 中文名 | 主要用途 | Example |
| --- | --- | --- | --- |
| [`ai-collaboration-calibration`](ai-collaboration-calibration/) | 协作校准 / 认知校准 | 问题还没定义清楚时，先挑战假设、澄清目标和判断标准。 | [example](examples/ai-collaboration-calibration.md) |
| [`research-topic-compiler`](research-topic-compiler/) | 专题研究编译器 / 概念源流研究助手 | 把大白话或模糊方向转成研究目标、研究问题和输出要求，再做系统研究、概念源流、行业演进和 PM 决策看板；需要持续更新时可进入 Research Radar Loop。 | [example](examples/research-topic-compiler.md) |
| [`decision-research`](decision-research/) | 决策调研 / 决策驱动调研 | 明确具体决策、接入可行性、方案选型和一次性决策调研；需要多轮收敛时可进入 Decision Research Loop。 | [example](examples/decision-research.md) |
| [`prd-architect`](prd-architect/) | PRD 架构师 / 需求文档起草 | 从想法或草稿起草 PRD，并在需要时补可编辑 Draw.io 图。 | [example](examples/prd-architect.md) |
| [`prd-review`](prd-review/) | PRD 评审 / 需求评审 | 评审已有 PRD/handoff，检查文字、流程、验收和图示是否能支撑交付；需要关闭阻断项时可进入 PRD Readiness Loop。 | [example](examples/prd-review.md) |
| [`prd-to-issues`](prd-to-issues/) | PRD 到研发 Issue 拆解 | 把 ready 的 PRD 拆成 vertical-slice GitHub implementation issues，先产出 draft，再按确认发布。 | [example](examples/prd-to-issues.md) |
| [`ui-mockup-desktop-workbench`](ui-mockup-desktop-workbench/) | 桌面工作台 UI Mockup 生成器 | 基于 PRD、UI 规范和桌面 Agent 工作台模式，生成可打开、可截图、可交付讨论的真实页面 mockup。 | [example](examples/ui-mockup-desktop-workbench.md) |
| [`grill-me`](grill-me/) | 方案拷问 / 压力测试 | 对已有方案连续追问，暴露盲点、失败模式和前置条件。 | [example](examples/grill-me.md) |
| [`ai-work-assetization-diagnoser`](ai-work-assetization-diagnoser/) | AI 工作资产化诊断器 / 资产化路由器 | 判断重复 AI 工作应沉淀为 Prompt、Context Pack、Workflow、Skill、Loop、System，或不值得沉淀。 | [example](examples/ai-work-assetization-diagnoser.md) |

## AI PM Workflow

| Stage | Current state | Say this | Skill | Next step |
| --- | --- | --- | --- | --- |
| 1. 脑暴校准 | 还没想清楚真正问题，担心方向错 | “先别执行，帮我看清问题”“挑战我的假设” | [`ai-collaboration-calibration`](ai-collaboration-calibration/) | 明确问题、约束和判断标准 |
| 2. 主题/决策研究 | 需要理解领域、概念、行业演进，或要在多个方案间做选择 | “系统研究这个主题”“概念源流”“帮我选一个” | [`research-topic-compiler`](research-topic-compiler/) / [`decision-research`](decision-research/) | 得到证据、判断、推荐方案或 PM 决策看板 |
| 3. PRD 起草 | 要把想法、脑暴或草稿整理成需求文档 | “帮我写 PRD”“帮我选 PRD 模板”“PRD 里补 Draw.io 图” | [`prd-architect`](prd-architect/) | 形成 PRD-lite、PRD-standard 或 PRD-ai-native |
| 4. PRD 评审 | 已有 PRD，需要找缺口、冲突和不可测试点 | “帮我审 PRD”“从研发测试视角挑问题” | [`prd-review`](prd-review/) | 修订 PRD，关闭阻断项 |
| 5. PRD 拆 issue | PRD 已可交付，需要形成研发可领取 backlog | “把 PRD 拆成 issue”“生成 GitHub issues”“按 vertical slice 拆开发票” | [`prd-to-issues`](prd-to-issues/) | 得到 draft issue plan、coverage matrix，确认后可发布到 GitHub |
| 6. UI Mockup | PRD 和 UI 规范已可用，需要桌面端真实页面 | “基于 PRD 和 UI 规范出桌面端 mockup” | [`ui-mockup-desktop-workbench`](ui-mockup-desktop-workbench/) | 得到可打开、可截图、可讨论的页面 mockup |
| 7. 方案压测 | 已有方案，但担心盲点和失败模式 | “拷问我的方案”“这个方案哪里会翻车” | [`grill-me`](grill-me/) | 明确取舍、风险和前置条件 |
| 8. 资产化诊断 | 一段 AI 工作重复出现，不确定该沉淀到哪层 | “这个 prompt 应该做成 workflow 还是 Skill” | [`ai-work-assetization-diagnoser`](ai-work-assetization-diagnoser/) | 得到最小资产建议和复用验证信号 |
| 9. 开发计划 | PRD 或 issue backlog 已可交付，需要拆实现步骤 | “基于这个 PRD 写开发计划”“基于这些 issues 写实现计划” | Superpowers `writing-plans` | 进入实现计划、测试策略和提交节奏 |

## Loop Extensions

Loop Extension 不新增 Skill，也不改变根目录结构。它是在部分高价值 Skill 内增加的状态化工作合约，只有当用户明确需要多轮、可恢复、持续更新或交付准备度收敛时才启用。

| Loop Extension | Parent Skill | Use when | Contract | Pattern |
| --- | --- | --- | --- | --- |
| Decision Research Loop | [`decision-research`](decision-research/) | 围绕同一个决策多轮收敛，跟踪假设、证据、反证、范围漂移和结论版本。 | [`decision-loop-contract.md`](decision-research/references/decision-loop-contract.md) | [`decision-research-loop.md`](loop-patterns/decision-research-loop.md) |
| Research Radar Loop | [`research-topic-compiler`](research-topic-compiler/) | 围绕持续变化主题维护 watchlist、证据更新、阶段结论 Diff 和更新日志。 | [`research-radar-loop-contract.md`](research-topic-compiler/references/research-radar-loop-contract.md) | [`research-radar-loop.md`](loop-patterns/research-radar-loop.md) |
| PRD Readiness Loop | [`prd-review`](prd-review/) | 围绕同一份 PRD 多轮 review、修订、关闭阻断项，并判断能否进入 `writing-plans`。 | [`prd-readiness-loop-contract.md`](prd-review/references/prd-readiness-loop-contract.md) | [`prd-readiness-loop.md`](loop-patterns/prd-readiness-loop.md) |

PRD 进入 Superpowers `writing-plans` 前，至少应满足：

- 目标用户、问题、范围边界和非目标已明确。
- 主流程、关键状态、输入输出、异常或人工接管点已写清。
- 验收标准能被测试或人工检查。
- 阻断性待确认项已经关闭，或被显式列为实现计划的前置假设。

See [docs/superpowers-comparison.md](docs/superpowers-comparison.md) for the product-to-engineering handoff model.

## Routing Rules

当多个 Skill 都可能被触发时，优先按用户当前阶段分流，而不是按关键词叠加：

- 问题还没定义清楚：用 `ai-collaboration-calibration`。
- 需要把模糊研究想法拆成研究目标，或系统理解主题、概念源流、行业演进、PM 决策看板：用 `research-topic-compiler`。
- 明确具体决策、接入方式或方案选型：用 `decision-research`。
- 要从想法或草稿写 PRD：用 `prd-architect`。
- 已有 PRD 要找缺口、检查图示或判断能否交付：用 `prd-review`。
- PRD 已 ready，需要拆成可领取 GitHub implementation issues：用 `prd-to-issues`。
- PRD 与 UI 规范已明确，要出桌面工作台真实页面 mockup：用 `ui-mockup-desktop-workbench`。
- 已有方案要被追问和压测：用 `grill-me`。
- 重复 AI 工作要判断资产化层级：用 `ai-work-assetization-diagnoser`。

More details: [SKILL_ROUTING.md](SKILL_ROUTING.md)

## Repository Map

- [SKILL_REGISTRY.md](SKILL_REGISTRY.md): canonical catalog, Chinese names, status, and public boundaries.
- [SKILL_ROUTING.md](SKILL_ROUTING.md): adjacent-skill routing and handoff rules.
- [docs/](docs/): install guides, quickstart, Superpowers comparison, and release notes.
- [examples/](examples/): copyable prompts and expected output shapes.
- [promotions/](promotions/): launch copy for Chinese and English channels.
- [assets/social-preview.svg](assets/social-preview.svg): source artwork for GitHub social preview.

## Contributing

Contributions should keep this repo focused on public AI PM workflows. Before adding a new Skill, check:

1. Is it useful to AI product managers or product-facing operators?
2. Does it belong in one of the workflow stages above?
3. Does it avoid private company data, customer context, and internal-only process language?
4. Are `README.md`, `SKILL_REGISTRY.md`, and `SKILL_ROUTING.md` updated together when needed?

See [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License

MIT. See [LICENSE](LICENSE).
