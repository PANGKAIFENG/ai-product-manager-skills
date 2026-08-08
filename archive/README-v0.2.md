# AI Product Manager Skills Library

[![Release](https://img.shields.io/github/v/release/PANGKAIFENG/ai-product-manager-skills?display_name=tag)](https://github.com/PANGKAIFENG/ai-product-manager-skills/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-13-2563eb.svg)](SKILL_REGISTRY.md)
[![Codex](https://img.shields.io/badge/Codex-skills-111827.svg)](docs/install-codex.md)
[![Claude Code](https://img.shields.io/badge/Claude_Code-skills-111827.svg)](docs/install-claude-code.md)

中文优先的 AI 产品经理 Agent Skill 库，用来把高频 PM 工作流沉淀成可复用的 Codex Skills、Claude Code Skills 和 Agent Skills。

它重点覆盖：AI 协作脑暴、复杂探索资产化、主题研究、竞品决策分析、决策调研、方案脑暴、PRD 起草、PRD 评审、PRD 到 GitHub issue 拆解、UI 线框/高保真 mockup、方案压测、AI 工作资产化诊断，以及把需求交给 Superpowers 开发计划前的交付准备。

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
$complex-exploration 先不要直接写方案，帮我判断这个复杂任务怎么探索并沉淀资产
$research-topic-compiler 系统研究这个主题，并转成 PM 决策输入
$competitive-analysis 研究这个竞品对我们的产品决策有什么启发
$decision-research 帮我比较这几个方案，给一个有立场推荐
$brainstorming 先不要写 PRD，帮我脑暴 2-3 个设计方案
$prd-architect 把这个想法整理成 PRD-lite
$prd-review 从研发和测试视角审一下这个 PRD
$prd-to-issues 把这个 PRD 拆成 GitHub implementation issues，先给我 draft
$ui-wireframe-to-html 先把 PRD 转成 UI 结构、状态模型和 ASCII 布局
$ui-mockup-desktop-workbench 基于 PRD、UI 规范和真实前端项目生成高保真 UI handoff / preview
$grill-me 拷问我的方案，找失败模式
$ai-work-assetization-diagnoser 判断这段 AI 工作该沉淀成 Prompt、Workflow、Skill 还是 Loop
```

Install paths:

- Codex: see [docs/install-codex.md](docs/install-codex.md)
- Claude Code: see [docs/install-claude-code.md](docs/install-claude-code.md)
- General walkthrough: see [docs/quickstart.md](docs/quickstart.md)

Quality gates:

- Repo audit: `python3 scripts/audit_skills.py .`
- Machine-readable catalog: [catalog/skills.yaml](catalog/skills.yaml)
- Eval schema: [docs/eval-schema.md](docs/eval-schema.md)
- Historical audits and completed work: [docs/archive/](docs/archive/)

## Who Should Use This

- AI 产品经理：需要把想法、调研、方案和 PRD 推进到可交付状态。
- 产品负责人或业务负责人：希望用 Codex、Claude Code 或其他 Agent 工具复用稳定工作流。
- 研发协作者：需要理解产品侧 Skill 如何与 Superpowers 的开发计划、TDD、执行和验证流程衔接。
- 需要中文优先 AI PM workflow 的团队：希望从脑暴、研究、PRD 到评审形成可复用流程。

## Public Skills

所有可安装 Skill 统一放在 `skills/<skill-id>/`。目录层级只负责安装边界，稳定的 `skill-id` 仍是公开调用名称；分类和状态由 [catalog/skills.yaml](catalog/skills.yaml) 管理。

| Skill | 中文名 | 主要用途 | Example |
| --- | --- | --- | --- |
| [`ai-collaboration-calibration`](skills/ai-collaboration-calibration/) | 协作校准 / 认知校准 | 问题还没定义清楚时，先挑战假设、澄清目标和判断标准。 | [example](docs/examples/ai-collaboration-calibration.md) |
| [`complex-exploration`](skills/complex-exploration/) | 复杂探索资产化 / 复杂探索协作 | 面对复杂、不确定、多轮迭代的 Roadmap、定价、定位、复盘或方法论任务时，先定题、探索、收敛，再沉淀五类可复用资产。 | [example](docs/examples/complex-exploration.md) |
| [`research-topic-compiler`](skills/research-topic-compiler/) | 专题研究编译器 / 概念源流研究助手 | 拥有证据覆盖与残余 gap；交付 Evidence Pack 或精确 Evidence Delta，但不做最终选择。 | [example](docs/examples/research-topic-compiler.md) |
| [`competitive-analysis`](skills/competitive-analysis/) | 竞品决策分析 / 竞品决策简报 | 围绕一个产品决策，把竞品、替代方案、市场信号和可选产品走查转成定位、路线图、定价、功能优先级、差异化或 Go/No-Go 输入。 | [example](docs/examples/competitive-analysis.md) |
| [`decision-research`](skills/decision-research/) | 决策调研 / 决策驱动调研 | 拥有最终推荐、排除理由、置信度和颠覆条件；只精确退回一个可关闭证据 gap。 | [example](docs/examples/decision-research.md) |
| [`brainstorming`](skills/brainstorming/) | 设计脑暴 / 实现前方案校准 | 作为 Maker 形成 Design Spec/Delta；不自批 Critic、PRD 或实现 readiness。 | [example](docs/examples/brainstorming.md) |
| [`prd-architect`](skills/prd-architect/) | PRD 架构师 / 需求文档起草 | 从想法或草稿起草 PRD，并在需要时补可编辑 Draw.io 图。 | [example](docs/examples/prd-architect.md) |
| [`prd-review`](skills/prd-review/) | PRD 评审 / 需求评审 | 评审已有 PRD/handoff，检查文字、流程、验收和图示是否能支撑交付；需要关闭阻断项时可进入 PRD Readiness Loop。 | [example](docs/examples/prd-review.md) |
| [`prd-to-issues`](skills/prd-to-issues/) | PRD 到研发 Issue 拆解 | 把 ready 的 PRD 拆成 vertical-slice GitHub implementation issues，先产出 draft，再按确认发布。 | [example](docs/examples/prd-to-issues.md) |
| [`ui-wireframe-to-html`](skills/ui-wireframe-to-html/) | PRD 到 UI 线框 / 结构阶段 | 从 PRD 先输出 screen inventory、状态模型、ASCII 布局和可选低保真 HTML，只确认结构和状态。 | [example](docs/examples/ui-wireframe-to-html.md) |
| [`ui-mockup-desktop-workbench`](skills/ui-mockup-desktop-workbench/) | 高保真 UI 交付对齐器 / 桌面工作台 UI Mockup 生成器 | PRD/UI 方向确认后，先承接结构阶段，再把桌面工作台 UI 转成可截图确认、可映射真实组件、可交给前端实现的 project-native preview / visual handoff / concept HTML。 | [example](docs/examples/ui-mockup-desktop-workbench.md) |
| [`grill-me`](skills/grill-me/) | 方案拷问 / 压力测试 | 作为 Critic 输出 Challenge/Critic Handoff，把一个 gap 返回最小责任节点。 | [example](docs/examples/grill-me.md) |
| [`ai-work-assetization-diagnoser`](skills/ai-work-assetization-diagnoser/) | AI 工作资产化诊断器 / 资产化路由器 | 判断重复 AI 工作应沉淀为 Prompt、Context Pack、Workflow、Skill、Loop、System，或不值得沉淀。 | [example](docs/examples/ai-work-assetization-diagnoser.md) |

## AI PM Workflow

| Stage | Current state | Say this | Skill | Next step |
| --- | --- | --- | --- | --- |
| 1. 脑暴校准 | 还没想清楚真正问题，担心方向错 | “先别执行，帮我看清问题”“挑战我的假设” | [`ai-collaboration-calibration`](skills/ai-collaboration-calibration/) | 明确问题、约束和判断标准 |
| 2. 复杂探索 | 任务复杂、不确定、多轮迭代，不能直接写最终方案 | “先不要直接写方案”“这个问题是不是问窄了”“这次探索要沉淀什么” | [`complex-exploration`](skills/complex-exploration/) | 得到任务类型、真正问题、探索路径、中间产物和五类资产 |
| 3. 主题/竞品/决策研究 | 需要理解领域、概念、行业演进、竞品启发，或要在多个方案间做选择 | “系统研究这个主题”“概念源流”“做竞品决策分析”“帮我选一个” | [`research-topic-compiler`](skills/research-topic-compiler/) / [`competitive-analysis`](skills/competitive-analysis/) / [`decision-research`](skills/decision-research/) | 得到证据、竞品决策简报、判断、推荐方案或 PM 决策看板 |
| 4. 方案脑暴 | 问题基本成立，但还没确定方案、范围、交互、视觉约束或技术切分 | “先脑暴几个方案”“先不要写 PRD，帮我设计几种路径” | [`brainstorming`](skills/brainstorming/) | 得到推荐方案、取舍、视觉约束摘要和设计 spec |
| 5. PRD 起草 | 要把想法、脑暴或草稿整理成需求文档 | “帮我写 PRD”“帮我选 PRD 模板”“PRD 里补 Draw.io 图” | [`prd-architect`](skills/prd-architect/) | 形成 PRD-lite、PRD-standard 或 PRD-ai-native |
| 6. PRD 评审 | 已有 PRD，需要找缺口、冲突和不可测试点 | “帮我审 PRD”“从研发测试视角挑问题” | [`prd-review`](skills/prd-review/) | 修订 PRD，关闭阻断项 |
| 7. PRD 拆 issue | PRD 已可交付，需要形成研发可领取 backlog | “把 PRD 拆成 issue”“生成 GitHub issues”“按 vertical slice 拆开发票” | [`prd-to-issues`](skills/prd-to-issues/) | 得到 draft issue plan、coverage matrix，确认后可发布到 GitHub |
| 8. UI 结构线框 | PRD 已可用，但还需要先确认页面结构、状态模型和布局骨架 | “先出 UI 结构”“先做 ASCII 布局”“不要高保真” | [`ui-wireframe-to-html`](skills/ui-wireframe-to-html/) | 得到 screen inventory、state model、ASCII layout 和结构确认问题 |
| 9. 高保真 UI 对齐 | PRD、UI 结构和 UI 规范已可用，需要确认桌面端真实页面并交给前端实现 | “基于 PRD 出高保真 mockup”“开发要复刻这个 UI” | [`ui-mockup-desktop-workbench`](skills/ui-mockup-desktop-workbench/) | 得到结构阶段产物、screen contract、component map、implementation notes 和 preview/handoff |
| 10. 方案压测 | 已有方案，但担心盲点和失败模式 | “拷问我的方案”“这个方案哪里会翻车” | [`grill-me`](skills/grill-me/) | 明确取舍、风险和前置条件 |
| 11. 资产化诊断 | 一段 AI 工作重复出现，不确定该沉淀到哪层 | “这个 prompt 应该做成 workflow 还是 Skill” | [`ai-work-assetization-diagnoser`](skills/ai-work-assetization-diagnoser/) | 得到最小资产建议和复用验证信号 |
| 12. 开发计划 | PRD 或 issue backlog 已可交付，需要拆实现步骤 | “基于这个 PRD 写开发计划”“基于这些 issues 写实现计划” | Superpowers `writing-plans` | 进入实现计划、测试策略和提交节奏 |

## Loop Extensions

Loop Extension 不新增 Skill，也不进入 `skills/`。它是在部分高价值 Skill 内增加的状态化工作合约，只有当用户明确需要多轮、可恢复、持续更新或交付准备度收敛时才启用。

| Loop Extension | Parent Skill | Use when | Contract | Pattern |
| --- | --- | --- | --- | --- |
| Decision Research Loop | [`decision-research`](skills/decision-research/) | 围绕同一个决策多轮收敛，跟踪假设、证据、反证、范围漂移和结论版本。 | [`decision-loop-contract.md`](skills/decision-research/references/decision-loop-contract.md) | [`decision-research-loop.md`](docs/workflows/decision-research-loop.md) |
| Research Radar Loop | [`research-topic-compiler`](skills/research-topic-compiler/) | 围绕持续变化主题维护 watchlist、证据更新、阶段结论 Diff 和更新日志。 | [`research-radar-loop-contract.md`](skills/research-topic-compiler/references/research-radar-loop-contract.md) | [`research-radar-loop.md`](docs/workflows/research-radar-loop.md) |
| PRD Readiness Loop | [`prd-review`](skills/prd-review/) | 围绕同一份 PRD 多轮 review、修订、关闭阻断项，并判断能否进入 `writing-plans`。 | [`prd-readiness-loop-contract.md`](skills/prd-review/references/prd-readiness-loop-contract.md) | [`prd-readiness-loop.md`](docs/workflows/prd-readiness-loop.md) |

四个核心节点保持可独立调用：Research 交 Evidence，Decision 做最终选择，`brainstorming` 作为 Maker 形成方案，`grill-me` 作为 Critic 返回 Challenge。跨节点只传一个可关闭 gap 的差量 handoff，已确认项必须保留；同一 gap 两轮未关闭或缩小即停止到 Human Gate。详细合同留在四个 Skill 各自的 handoff reference。

Product Work Graph 的方案发散固定路由到本仓 PUBLIC unqualified `brainstorming`。只有用户显式调用完整限定名 `superpowers:brainstorming` 时才选择 Superpowers plugin；本仓不修改或禁用该 plugin。

PRD 进入 Superpowers `writing-plans` 前，至少应满足：

- 目标用户、问题、范围边界和非目标已明确。
- 主流程、关键状态、输入输出、异常或人工接管点已写清。
- 验收标准能被测试或人工检查。
- 阻断性待确认项已经关闭，或被显式列为实现计划的前置假设。

See [docs/superpowers-comparison.md](docs/superpowers-comparison.md) for the product-to-engineering handoff model.

## Routing Rules

当多个 Skill 都可能被触发时，优先按用户当前阶段分流，而不是按关键词叠加：

- 问题还没定义清楚：用 `ai-collaboration-calibration`。
- 任务复杂、不确定、多轮迭代，需要先定题、探索路径、复盘并沉淀资产：用 `complex-exploration`。
- 需要把模糊研究想法拆成研究目标，或系统理解主题、概念源流、行业演进、PM 决策看板：用 `research-topic-compiler`。
- 需要把竞品、替代方案、定价、onboarding、公开评价或登录态走查转成产品决策简报：用 `competitive-analysis`。
- 明确具体决策、接入方式或方案选型：用 `decision-research`。
- 问题基本成立，但进入 PRD、mockup 或开发计划前还需要比较多个设计路径：用 `brainstorming`。
- 要从想法或草稿写 PRD：用 `prd-architect`。
- 已有 PRD 要找缺口、检查图示或判断能否交付：用 `prd-review`。
- PRD 已 ready，需要拆成可领取 GitHub implementation issues：用 `prd-to-issues`。
- PRD 已明确，但只想先确认 UI 结构、状态模型、ASCII 布局或低保真 HTML：用 `ui-wireframe-to-html`。
- PRD、UI 结构和 UI 规范已明确，要出高保真桌面工作台 UI handoff、项目原生 preview 或真实组件映射：用 `ui-mockup-desktop-workbench`。
- 已有方案要被追问和压测：用 `grill-me`。
- 重复 AI 工作要判断资产化层级：用 `ai-work-assetization-diagnoser`。

More details: [SKILL_ROUTING.md](SKILL_ROUTING.md)

## Repository Map

- [SKILL_REGISTRY.md](SKILL_REGISTRY.md): canonical catalog, Chinese names, status, and public boundaries.
- [SKILL_ROUTING.md](SKILL_ROUTING.md): adjacent-skill routing and handoff rules.
- [skills/](skills/): the only installable Skill root; each child directory owns one stable Skill ID.
- [catalog/skills.yaml](catalog/skills.yaml): machine-readable inventory, category, status, and example mapping.
- [docs/](docs/): install guides, quickstart, examples, workflows, PRDs, and release notes.
- [docs/archive/](docs/archive/): completed issues, historical audits, and promotion material.
- [docs/eval-schema.md](docs/eval-schema.md): shared eval file schema for routing and regression cases.
- [scripts/audit_skills.py](scripts/audit_skills.py): repository-level Skill quality gate.
- [docs/examples/](docs/examples/): copyable prompts and expected output shapes.
- [docs/workflows/](docs/workflows/): cross-Skill Loop orchestration documents; not installable Skills.
- [.github/assets/social-preview.svg](.github/assets/social-preview.svg): source artwork for GitHub social preview.

## Contributing

Contributions should keep this repo focused on public AI PM workflows. Before adding a new Skill, check:

1. Is it useful to AI product managers or product-facing operators?
2. Does it belong in one of the workflow stages above?
3. Does it avoid private company data, customer context, and internal-only process language?
4. Are `README.md`, `SKILL_REGISTRY.md`, and `SKILL_ROUTING.md` updated together when needed?

See [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License

MIT. See [LICENSE](LICENSE).
