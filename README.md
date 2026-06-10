# AI Product Manager Skills Library

面向 AI 产品经理的中文优先 Agent Skill 仓库，用来沉淀可复用的 Codex Skills、Claude Skills 和 AI product management workflows。它重点覆盖需求创建、PRD 起草与评审、需求复盘、AI 协作脑暴、产品/技术主题研究、Agent trace 诊断和 Skill 治理。

这个仓库和 Superpowers 互补：Superpowers 更偏研发实现、测试驱动、计划执行和代码交付；本仓库更偏产品经理在进入研发交付前后的工作，包括把模糊想法变成可讨论需求、把主题研究转成产品判断、把 PRD 交付前的缺口暴露出来，以及把高频 AI 协作流程沉淀成可复用 Skill。

If you are searching for `AI product manager skills`, `Codex skills`, `Claude skills`, `PRD workflow`, `product research agent`, `AI collaboration brainstorming`, `requirements engineering`, or `Chinese AI workflow skills`, this repository is a curated Skill library for that use case.

当前仓库是 GitHub 管理的 Skill catalog，同时保持 `skillshare` 兼容结构：每个真实 Skill 都放在仓库根目录下的独立文件夹里。README 只提供“按工作流找能力”的导航，不作为运行时加载入口。

## 适合谁

- AI 产品经理：需要把想法、调研、方案和 PRD 推进到可交付状态。
- 使用 Codex、Claude 或其他 Agent 工具的产品/业务负责人：希望用自然语言稳定唤起一组可复用工作流。
- 正在搭建团队 Skill 资产的人：需要参考如何组织 `SKILL.md`、中文触发语、路由边界和 catalog。
- 研发协作者：需要理解产品侧 Skill 如何与 Superpowers 的开发计划、TDD、执行和验证流程衔接。

## 能解决什么

- 需求创建：从模糊想法、脑暴材料或功能说明进入 PRD 起草。
- 需求复盘：从 PM、研发、测试视角评审 PRD，找缺口、冲突和不可测试点。
- AI 协作脑暴：在执行前校准问题定义、挑战假设、压测方案。
- 主题研究：围绕产品、技术、行业或概念做结构化研究，并转成决策输入。
- 工程协作：诊断 agent trace、生成架构图、沉淀团队 Skill 和项目指南。

## 组织原则

真实 Skill 目录继续保持平铺，例如：

- `prd-architect/`
- `prd-review/`
- `skill-reviewer/`
- `team-skill-creator/`

这样做是为了保持 `name`、目录名、GitHub 历史、skillshare 同步路径和 Codex/Claude 触发名称稳定。不要为了视觉分类把真实 Skill 移到多层目录。

管理视图按“能力族 + 工作流阶段”组织：

- 产品需求工作流：从想清楚问题，到写 PRD、审 PRD、压测方案，再交给开发计划。
- Skill 治理工作流：判断一个能力要不要沉淀成 Skill，创建、评审和维护 Skill。
- 工程交付辅助：调试、编码规范、图示生成、上游提案。
- 研究学习：系统专题研究、概念源流研究和一次性技术调研。

## 产品需求工作流

这组 Skill 用来把模糊想法逐步推进到可交付研发的需求输入。它和 Superpowers 的开发流互补：这里负责产品需求成熟度，Superpowers `writing-plans` 负责后续实现计划。

| 阶段 | 你现在的状态 | 可以这样说 | 对应 Skill | 下一步 |
| --- | --- | --- | --- | --- |
| 1. 问题校准 | 还没想清楚真正问题，担心方向错 | “先别执行，帮我看清问题”“挑战我的假设” | [`ai-collaboration-calibration`](ai-collaboration-calibration/) | 明确问题、约束和判断标准 |
| 2. 概念解构 | 要理解复杂概念、行业演进或范式变化 | “帮我解构一个概念”“做行业演进看板” | [`concept-lens-dashboard`](concept-lens-dashboard/) | 形成概念地图和 PM 决策问题 |
| 3. 技术可行性 | 问题已定义，需要判断技术路线或现成方案 | “有没有现成方案”“技术上可行吗”“帮我选一个” | [`tech-research`](tech-research/) | 得到推荐方案、排除理由和风险 |
| 4. PRD 起草 | 要把想法、脑暴或草稿整理成需求文档 | “帮我写 PRD”“帮我选 PRD 模板” | [`prd-architect`](prd-architect/) | 形成 PRD-lite、PRD-standard 或 PRD-ai-native |
| 5. PRD 评审 | 已有 PRD，需要找缺口、冲突和不可测试点 | “帮我审 PRD”“从研发测试视角挑问题” | [`prd-review`](prd-review/) | 修订 PRD，关闭阻断项 |
| 6. 方案压测 | 已有方案，但担心盲点和失败模式 | “拷问我的方案”“这个方案哪里会翻车” | [`grill-me`](grill-me/) | 明确取舍、风险和前置条件 |
| 7. 开发计划 | PRD 已可交付，需要拆实现步骤 | “基于这个 PRD 写开发计划” | Superpowers `writing-plans` | 进入实现计划、测试策略和提交节奏 |

PRD 进入 Superpowers `writing-plans` 前，至少应满足：

- 目标用户、问题、范围边界和非目标已明确。
- 主流程、关键状态、输入输出、异常或人工接管点已写清。
- 验收标准能被测试或人工检查。
- 阻断性待确认项已经关闭，或被显式列为实现计划的前置假设。

## Skill 治理工作流

这组 Skill 用来维护本仓库自己的能力资产。

| 阶段 | 你现在的状态 | 可以这样说 | 对应 Skill | 产出 |
| --- | --- | --- | --- | --- |
| 1. 判断是否沉淀 | 有一个可重复能力，不确定该做成 Prompt、Workflow、Tool 还是 Skill | “这个能力要不要沉淀成 Skill”“帮我创建一个 Skill” | [`team-skill-creator`](team-skill-creator/) | Skill 候选判断、目录结构、catalog 更新清单 |
| 2. 评审和优化 | 已有 `SKILL.md` 或 Skill 目录，需要检查质量 | “帮我 review 这个 Skill”“优化 Skill 触发描述” | [`skill-reviewer`](skill-reviewer/) | 问题清单、修复建议、触发边界和验证建议 |
| 3. 项目级参考 | 想看项目专属 Skill 应该怎么组织 | “给我一个项目 Skill 模板”“项目指南型 Skill 怎么组织” | [`project-guidelines-example`](project-guidelines-example/) | 项目级 Skill 示例结构 |

新增一个 Skill 时，至少同步检查：

- 新增根目录 `<skill-name>/SKILL.md`。
- 更新 [`SKILL_REGISTRY.md`](SKILL_REGISTRY.md)。
- 如果会和相邻 Skill 抢触发，更新 [`SKILL_ROUTING.md`](SKILL_ROUTING.md)。
- 如果它属于某条核心工作流，更新本 README。
- 如额外维护 GitHub 浏览索引目录或专题 README，再同步对应索引。
- 如果要立即在 Codex、Claude 或其他目标工具里使用，再执行对应的 skillshare 同步或白名单更新。

## 工程交付辅助

这组 Skill 不直接负责产品需求本身，而是辅助开发、诊断、表达和治理。

| 我想做什么 | 可以这样说 | 对应 Skill | 状态 |
| --- | --- | --- | --- |
| 从 trace、日志或执行记录定位根因 | “看下这个 trace”“根据日志定位根因”“只说明问题不要改文件” | [`agent-trace-diagnoser`](agent-trace-diagnoser/) | active |
| 按工程规范写、改或审代码 | “按编码规范实现”“检查代码有没有工程坏味道” | [`coding-standards`](coding-standards/) | keep |
| 生成可编辑架构图或流程图 | “画一张架构图”“生成 Draw.io”“输出 .drawio 文件” | [`generate-drawio-diagram`](generate-drawio-diagram/) | active |
| 把共享模板或 managed path 问题写成上游提案 | “整理成 Honeycomb 上游提案”“判断这是共享问题还是本地问题” | [`honeycomb-change-proposer`](honeycomb-change-proposer/) | keep |

## 研究学习

研究类 Skill 的区别主要看目标是“单次决策”还是“长期沉淀”。

| 研究目标 | 可以这样说 | 对应 Skill | 用法边界 |
| --- | --- | --- | --- |
| 单次技术调研、可行性判断、方案选型 | “这个怎么接”“有没有现成方案”“选 A 还是 B” | [`tech-research`](tech-research/) | 给出有立场推荐和排除理由，不做长期知识库沉淀 |
| 系统学习一个主题，整理证据和研究报告 | “系统研究这个主题”“整理到 Obsidian”“做一个深度专题” | [`research-topic-compiler`](research-topic-compiler/) | 适合多渠道研究、证据矩阵和研究项目沉淀 |
| 追溯概念源流、语义演化和范式变化 | “帮我解构一个概念”“PM 技术评审提问脚本” | [`concept-lens-dashboard`](concept-lens-dashboard/) | 适合复杂概念进入产品或战略判断前的结构化理解 |

## 路由优先级

当多个 Skill 都可能被触发时，优先按用户当前阶段分流，而不是按关键词叠加：

- 问题还没定义清楚：用 `ai-collaboration-calibration`。
- 已有方案要被追问和压测：用 `grill-me`。
- 明确技术决策需要调研：用 `tech-research`。
- 要系统理解一个主题并沉淀材料：用 `research-topic-compiler`。
- 要从想法或草稿写 PRD：用 `prd-architect`。
- 已有 PRD 要找缺口：用 `prd-review`。
- 要创建或导入 Skill：用 `team-skill-creator`。
- 要评审或优化已有 Skill：用 `skill-reviewer`。

更细的相邻能力边界见 [`SKILL_ROUTING.md`](SKILL_ROUTING.md)。

## 为什么名称仍保留英文

`name` 和目录名是 Skill 的稳定 ID，会被 Codex、Claude、skillshare、GitHub 历史和分类入口引用。直接改成中文有同步断链、重复安装、历史追踪丢失的风险。

所以本仓库采用：

- 英文 slug 保持稳定，例如 `prd-architect`。
- `description` 使用中文触发优先的写法。
- 每个 `SKILL.md` 顶部增加“中文速查”。
- README/Registry 提供中文目录、中文别名和自然语言唤起语。

## 管理原则

- GitHub 线上仓库是精选 Skill 的标准源，不是本机所有 Skill 的原样倾倒。
- `skillshare` 可以作为把这些 Skill 分发到 Codex、Claude 等目标工具的实现方式，但不是唯一同步机制。
- 相邻 Skill 的触发边界统一维护在 [`SKILL_ROUTING.md`](SKILL_ROUTING.md)，优先按用户当前工作阶段路由。
- 常用/收藏 Skill 应通过 `skillshare target include` 白名单控制，而不是删除低频 Skill。
- 含公司流程、业务数据、客户数据或内部系统语义的 Skill 默认标记为 `private-only`。
- 发布到 ClawHub 前必须单独检查许可证、敏感信息、适用边界和 README 说明。

## 状态说明

- `core`: 高频、稳定、应长期维护。
- `active`: 常用，可进入 Codex/Claude 白名单。
- `keep`: 低频但有明确价值，保留在仓库中。
- `review`: 来源、质量或用途还需要复核。
- `archive`: 历史能力或已被替代，不进入常用白名单。
- `private-only`: 不能公开发布。
