# Skill Routing

这个文件用于解决公开 AI PM Skill 的相邻触发边界。原则是先判断用户当前处在哪个工作阶段，再选择 Skill；不要因为关键词相似就叠加多个 Skill。

## 核心路由表

| 用户当前状态 | 优先 Skill | 触发信号 | 不要用它做什么 |
| --- | --- | --- | --- |
| 问题还没定义清楚，需要先看清真正问题 | `ai-collaboration-calibration` | “先聊一下”“帮我想想”“挑战我的假设”“方向是不是错了” | 不直接产出最终 PRD、方案或调研结论 |
| 要围绕主题做系统学习、专题研究、概念源流或 PM 决策看板 | `research-topic-compiler` | “系统研究”“做深度专题”“整理到 Obsidian”“概念解读”“概念源流”“行业演进看板” | 不替代单次方案选型，不创建或评审 Skill |
| 有明确具体决策，需要单次调研和推荐 | `decision-research` | “有没有现成方案”“怎么接入”“这个选择可行吗”“选 A 还是 B” | 不做长期知识库沉淀，不替代问题脑暴 |
| 要把想法、脑暴或需求草稿整理成 PRD | `prd-architect` | “帮我写 PRD”“选 PRD 模板”“把需求整理成 PRD”“PRD 里补 Draw.io 图” | 不评审已经成稿的 PRD，不直接写代码 |
| 已有 PRD/handoff，需要找缺口并修订 | `prd-review` | “帮我审 PRD”“从研发测试视角挑问题”“能不能交付开发”“检查图示是否可编辑” | 不从零生成 PRD，不做纯语言润色 |
| 已有方案，需要压力测试和追问 | `grill-me` | “拷问我的方案”“压力测试”“问 hard questions”“哪里会翻车” | 不从零写方案，不替代 PRD 评审 |

## 研究类分流规则

`research-topic-compiler` 和 `decision-research` 的边界取决于用户要的是“学习/理解/沉淀”还是“选择/接入/决策”。

| 用户目标 | 优先 Skill | 说明 |
| --- | --- | --- |
| 轻量概念解读、概念源流、语义演化、范式阶段、PM 技术评审提问脚本 | `research-topic-compiler` 的 `Lightweight Concept Lens Mode` | 输出 PM 决策看板、概念源流、阶段矩阵、反模式和评审问题；默认不写入 Obsidian。 |
| 系统学习、深度专题、长期沉淀、Obsidian Research Project | `research-topic-compiler` 的深度研究模式 | 输出研究计划、证据矩阵、研究报告、学习包或长期雷达。 |
| 明确决策路线、平台接入、工具选型、可行性判断 | `decision-research` | 输出有立场推荐、排除理由、接入风险、验证路径和下一步决策。 |
| 用户还没定义清楚为什么研究这个主题 | `ai-collaboration-calibration` | 先校准问题、决策目标和约束，再进入研究。 |

典型分流：

- “帮我轻量解构一下 MCP 的概念源流，输出 PM 决策看板。” -> `research-topic-compiler` Lightweight Concept Lens Mode。
- “系统研究 MCP 安全最佳实践，整理到 Obsidian。” -> `research-topic-compiler` 深度研究模式。
- “我们应该选 MCP 还是自研工具协议？” -> `decision-research`。

## PRD 图示分流规则

Draw.io 图示不再作为独立公开 Skill；它是 PRD 起草和 PRD 评审的一部分。

| 用户目标 | 优先 Skill | 说明 |
| --- | --- | --- |
| 从想法/草稿写 PRD，并补核心流程图、架构图或 AI 协作链路图 | `prd-architect` | 在 PRD 起草阶段生成可编辑 `.drawio` 或 `*.drawio.svg`，并运行 `scripts/validate_drawio.py`。 |
| 已有 PRD，需要检查图示是否缺失、不可编辑、引用错误或无法支撑研发评审 | `prd-review` | 把图示作为 review finding，区分文本要求缺失、文件校验失败和未能验证。 |
| 只想要视觉稿、不可编辑 PNG、静态海报或 UI 设计稿 | 不走 PRD 图示流程 | 这不是公开 AI PM PRD Skill 的职责。 |

PRD 图示判断：

- `PRD-lite`：简单局部改动不强制 Draw.io，优先文字步骤、表格、Mermaid 草稿、真实页面截图或 HTML mockup。
- `PRD-standard`：多阶段链路、模块依赖、上下游输入输出时，应考虑核心流程图或结构图。
- `PRD-ai-native`：人工动作、AI 动作、状态反馈、记忆写入、失败回退形成闭环时，应考虑一体化总图或核心流程图。

## PRD 到开发计划的衔接

`prd-architect` 和 `prd-review` 的边界止于产品需求交付准备度。只有当 PRD 已经满足以下条件，才适合进入 Superpowers `writing-plans`：

- 目标用户、问题、范围边界和非目标已明确。
- 主流程、关键状态、输入输出、异常或人工接管点已写清。
- 验收标准能被测试或人工检查。
- 阻断性待确认项已经关闭，或被显式列为 implementation plan 的前置假设。

进入 `writing-plans` 后，开发计划应负责文件边界、测试、实现步骤和提交节奏；PRD Skill 不替代开发计划 Skill。
