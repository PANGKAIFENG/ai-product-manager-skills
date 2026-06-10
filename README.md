# AI Product Manager Skills Library

面向 AI 产品经理的中文优先 Agent Skill 仓库，用来沉淀可复用的 Codex Skills、Claude Skills 和 AI product management workflows。

这个仓库和 Superpowers 互补：Superpowers 更偏研发实现、测试驱动、计划执行和代码交付；本仓库更偏产品经理在进入研发交付前后的工作，包括把模糊想法变成可讨论需求、把主题研究转成产品判断、把 PRD 交付前的缺口暴露出来，以及把方案交给 Superpowers 开发计划。

If you are searching for `AI product manager skills`, `Codex skills`, `Claude skills`, `PRD workflow`, `product research agent`, `AI collaboration brainstorming`, `requirements review`, or `Chinese AI workflow skills`, this repository is a curated Skill library for that use case.

当前仓库是公开 AI PM Skill catalog。个人 trace 诊断、编码规范、Skill 治理、项目治理和内部工程类 Skill 不在本仓库维护。

## 适合谁

- AI 产品经理：需要把想法、调研、方案和 PRD 推进到可交付状态。
- 使用 Codex、Claude 或其他 Agent 工具的产品/业务负责人：希望用自然语言稳定唤起一组可复用工作流。
- 研发协作者：需要理解产品侧 Skill 如何与 Superpowers 的开发计划、TDD、执行和验证流程衔接。
- 需要中文优先 AI PM workflow 的团队：希望从脑暴、研究、PRD 到评审形成可复用流程。

## 能解决什么

- 脑暴校准：在执行前校准问题定义、挑战假设、重新定义目标。
- 主题/技术研究：把产品、技术、行业或概念研究转成 PM 判断、证据矩阵和决策输入。
- PRD 起草：从想法、脑暴材料或功能说明进入 PRD-lite、PRD-standard 或 PRD-ai-native。
- PRD 评审：从 PM、研发、测试视角找缺口、冲突、不可实现点和不可测试点。
- 方案压测：对已有方案做反方挑战、失败模式识别和取舍收敛。
- 开发计划衔接：当 PRD 足够清楚时，把需求交给 Superpowers `writing-plans`。

## 公开 Skill

真实 Skill 目录保持在仓库根目录，确保 GitHub 历史、运行时分发和 Skill 触发名称稳定。

| Skill | 中文名 | 主要用途 |
| --- | --- | --- |
| [`ai-collaboration-calibration`](ai-collaboration-calibration/) | 协作校准 / 认知校准 | 问题还没定义清楚时，先挑战假设、澄清目标和判断标准。 |
| [`research-topic-compiler`](research-topic-compiler/) | 专题研究编译器 / 概念源流研究助手 | 系统研究、主题学习、轻量概念解构、概念源流、行业演进和 PM 决策看板。 |
| [`tech-research`](tech-research/) | 技术调研 / 决策驱动调研 | 明确技术决策、接入可行性、方案选型和一次性调研。 |
| [`prd-architect`](prd-architect/) | PRD 架构师 / 需求文档起草 | 从想法或草稿起草 PRD，并在需要时补可编辑 Draw.io 流程图/架构图。 |
| [`prd-review`](prd-review/) | PRD 评审 / 需求评审 | 评审已有 PRD/handoff，检查文字、流程、验收和图示是否能支撑交付。 |
| [`grill-me`](grill-me/) | 方案拷问 / 压力测试 | 对已有方案连续追问，暴露盲点、失败模式和前置条件。 |

## AI PM 主工作流

| 阶段 | 你现在的状态 | 可以这样说 | 对应 Skill | 下一步 |
| --- | --- | --- | --- | --- |
| 1. 脑暴校准 | 还没想清楚真正问题，担心方向错 | “先别执行，帮我看清问题”“挑战我的假设” | [`ai-collaboration-calibration`](ai-collaboration-calibration/) | 明确问题、约束和判断标准 |
| 2. 主题/技术研究 | 需要理解领域、概念、行业演进或技术路线 | “系统研究这个主题”“概念源流”“技术上可行吗” | [`research-topic-compiler`](research-topic-compiler/) / [`tech-research`](tech-research/) | 得到证据、判断、推荐方案或 PM 决策看板 |
| 3. PRD 起草 | 要把想法、脑暴或草稿整理成需求文档 | “帮我写 PRD”“帮我选 PRD 模板”“PRD 里补 Draw.io 图” | [`prd-architect`](prd-architect/) | 形成 PRD-lite、PRD-standard 或 PRD-ai-native |
| 4. PRD 评审 | 已有 PRD，需要找缺口、冲突和不可测试点 | “帮我审 PRD”“从研发测试视角挑问题” | [`prd-review`](prd-review/) | 修订 PRD，关闭阻断项 |
| 5. 方案压测 | 已有方案，但担心盲点和失败模式 | “拷问我的方案”“这个方案哪里会翻车” | [`grill-me`](grill-me/) | 明确取舍、风险和前置条件 |
| 6. 开发计划 | PRD 已可交付，需要拆实现步骤 | “基于这个 PRD 写开发计划” | Superpowers `writing-plans` | 进入实现计划、测试策略和提交节奏 |

PRD 进入 Superpowers `writing-plans` 前，至少应满足：

- 目标用户、问题、范围边界和非目标已明确。
- 主流程、关键状态、输入输出、异常或人工接管点已写清。
- 验收标准能被测试或人工检查。
- 阻断性待确认项已经关闭，或被显式列为实现计划的前置假设。

## 路由优先级

当多个 Skill 都可能被触发时，优先按用户当前阶段分流，而不是按关键词叠加：

- 问题还没定义清楚：用 `ai-collaboration-calibration`。
- 需要系统理解主题、概念源流、行业演进或 PM 决策看板：用 `research-topic-compiler`。
- 明确技术决策、接入方式或方案选型：用 `tech-research`。
- 要从想法或草稿写 PRD：用 `prd-architect`。
- 已有 PRD 要找缺口、检查图示或判断能否交付：用 `prd-review`。
- 已有方案要被追问和压测：用 `grill-me`。

更细的相邻能力边界见 [`SKILL_ROUTING.md`](SKILL_ROUTING.md)。

## 命名原则

`name` 和目录名是 Skill 的稳定 ID，会被 Codex、Claude、skillshare、GitHub 历史和触发名称引用。仓库采用：

- 英文 slug 保持稳定，例如 `prd-architect`。
- `description` 使用中文触发优先的写法。
- 每个 `SKILL.md` 顶部保留“中文速查”。
- README/Registry 提供中文目录、中文别名和自然语言唤起语。

## 管理原则

- GitHub 线上仓库是公开 AI PM Skill 的标准源，不是本机所有 Skill 的原样倾倒。
- 相邻 Skill 的触发边界统一维护在 [`SKILL_ROUTING.md`](SKILL_ROUTING.md)，优先按用户当前工作阶段路由。
- 常用/收藏 Skill 应通过目标工具白名单控制，而不是把私有或工程类 Skill 混入公开仓库。
- 发布前必须检查许可证、敏感信息、适用边界和 README 说明。
