# Skill Routing

这个文件用于解决公开 AI PM Skill 的相邻触发边界。原则是先判断用户当前处在哪个工作阶段，再选择 Skill；不要因为关键词相似就叠加多个 Skill。

## 核心路由表

| 用户当前状态 | 优先 Skill | 触发信号 | 不要用它做什么 |
| --- | --- | --- | --- |
| 问题还没定义清楚，需要先看清真正问题 | `ai-collaboration-calibration` | “先聊一下”“帮我想想”“挑战我的假设”“方向是不是错了” | 不直接产出最终 PRD、方案或调研结论；成熟方案压力测试转 `grill-me` |
| 要围绕主题做系统学习、专题研究、概念源流、候选池或 PM 决策看板 | `research-topic-compiler` | “系统研究”“做深度专题”“整理到 Obsidian”“概念解读”“概念源流”“行业演进看板”“先沉淀候选池”“把大白话拆成研究目标” | 不替代单次最终方案选型，不创建或评审 Skill |
| 有明确具体决策，需要单次调研和推荐 | `decision-research` | “有没有现成方案”“怎么接入”“这个选择可行吗”“选 A 还是 B”“基于候选池给最终推荐” | 不做长期知识库沉淀，不替代问题脑暴 |
| 问题基本成立，但进入 PRD、mockup 或开发计划前需要比较设计路径 | `brainstorming` | “先脑暴几个方案”“先不要写 PRD，帮我设计几种路径”“把这个需求变成 design spec”“实现前先讨论设计” | 不替代问题定义校准，不直接写 PRD，不直接实现；涉及 UI/mockup 时必须先发现项目视觉规范，不直接套通用页面 |
| 要把想法、脑暴或需求草稿整理成 PRD | `prd-architect` | “帮我写 PRD”“选 PRD 模板”“把需求整理成 PRD”“PRD 里补 Draw.io 图” | 不评审已经成稿的 PRD，不直接写代码 |
| 已有 PRD/handoff，需要找缺口并修订 | `prd-review` | “帮我审 PRD”“从研发测试视角挑问题”“能不能交付开发”“检查图示是否可编辑” | 不从零生成 PRD，不做纯语言润色 |
| PRD 已 ready，需要拆成研发可领取的 GitHub issue backlog | `prd-to-issues` | “把 PRD 拆成 issue”“需求文档拆任务”“生成 GitHub issues”“按 vertical slice 拆开发票” | 不从零写 PRD，不评审 PRD 缺口，不替代 Superpowers `writing-plans` |
| PRD/UI 方向已确认，需要高保真 UI handoff 或项目原生 preview | `ui-mockup-desktop-workbench` | “基于 PRD 出高保真 mockup”“开发要复刻这个 UI”“做真实项目 preview”“输出 component map” | 不替代 PRD 起草/评审；不把 standalone HTML 当生产实现 |
| 已有方案，需要压力测试和追问 | `grill-me` | “拷问我的方案”“压力测试”“问 hard questions”“哪里会翻车” | 不从零写方案，不替代 PRD artifact/readiness 评审 |
| 重复 AI 工作需要判断资产化层级 | `ai-work-assetization-diagnoser` | “值得做成 Skill 吗”“workflow 还是 Skill”“该沉淀成 Prompt / Context / Loop 吗” | 不直接创建 Skill，不替代具体执行 Skill |

## 快速判别问题

遇到相邻触发词时，先问或推断下面几个问题：

| 判别问题 | 如果是 | 如果否 / 不清楚 |
| --- | --- | --- |
| 这个方案针对的问题是否已被确认？ | 已有具体方案、架构、计划或决策时用 `grill-me` 压测。 | 用 `ai-collaboration-calibration` 先校准问题定义。 |
| 用户是在问“先比较几个设计方案，再决定怎么写 PRD、mockup 或怎么实现”吗？ | 用 `brainstorming`，输出方案比较、推荐路径和设计 spec；涉及 UI 时先补项目视觉规范发现摘要。 | 如果已经要正式 PRD，转 `prd-architect`；如果方案已定要找漏洞，转 `grill-me`。 |
| 用户是在问“这份 PRD 是否可开发、可测试、可交付”吗？ | 用 `prd-review`，并输出 readiness verdict。 | 如果问的是“PRD 背后的方案是否会失败”，用 `grill-me`。 |
| 用户是在问“把 ready PRD 拆成 GitHub issues 或开发工单”吗？ | 用 `prd-to-issues`，默认先 draft-only，输出 coverage matrix 和 AFK / HITL 标注。 | 如果要的是文件级实现计划、测试策略和提交顺序，转 Superpowers `writing-plans`。 |
| 用户要的是候选池还是最终选择？ | 候选池、长期追踪、Research Project 用 `research-topic-compiler`。 | 最终推荐、排除理由、颠覆条件用 `decision-research`。 |

## Cross-Skill Comparison

| Skill | 前提 | 主要输出 | 终止条件 |
| --- | --- | --- | --- |
| `ai-collaboration-calibration` | 问题、目标或约束还不稳定 | 真实问题陈述、关键假设、判断标准 | Done Signal 三问或用户确认进入执行 |
| `research-topic-compiler` | 需要理解主题、沉淀知识、扩展候选池或长期雷达 | Research Project、证据矩阵、PM 决策看板、Candidate Backlog | 信息饱和、用户确认或转交决策 |
| `decision-research` | 决策问题已定义或可快速框定 | 最终推荐、排除理由、置信度、颠覆条件 | 三角收敛、信息饱和、PoC 更便宜或用户决策 |
| `brainstorming` | 问题基本成立，但方案、范围、交互、视觉约束或技术切分未定 | 2-3 个方案、推荐路径、视觉约束摘要、设计 spec、下游 handoff | 用户确认设计或明确待确认项 |
| `prd-architect` | 要把想法、草稿或 review feedback 整理成 PRD | PRD-lite / standard / ai-native、图示或 UI 承接接口 | PRD 草稿达到当前阶段目标 |
| `prd-review` | 已有 PRD/handoff artifact | Findings、Revision Draft、Implementation-Plan Readiness | Ready / Ready with assumptions / Not ready |
| `prd-to-issues` | PRD 已可交付，且用户要 issue backlog 或 GitHub issues | Issue Breakdown Draft、AFK / HITL 标注、Coverage Matrix、可选发布结果 | 用户确认粒度、依赖、标签和是否发布 |
| `ui-mockup-desktop-workbench` | PRD 和 UI 规范足够明确，且需要 UI 可确认、可验收、可交给前端实现 | `project-native-preview`、`visual-handoff` 或 `concept-html`，包含状态说明、组件映射、实现说明和截图/验证备注 | UI contract 可验收，迁移边界明确 |
| `grill-me` | 方案、架构、计划或决策已成形 | 决策记录、被否选项、未解问题、推荐下一步 | 关键分支已探索或需要用户决策 |
| `ai-work-assetization-diagnoser` | 重复 AI 工作、prompt、流程或团队场景需要沉淀判断 | 推荐资产层、相邻层排除理由、最小下一步 artifact、复用信号 | 得到明确资产化建议或不沉淀结论 |

## 研究类分流规则

`research-topic-compiler` 和 `decision-research` 的边界取决于用户要的是“学习/理解/沉淀/候选池”还是“选择/接入/最终决策”。

| 用户目标 | 优先 Skill | 说明 |
| --- | --- | --- |
| 用户只有大白话、模糊方向、业务愿望或 Roadmap/PRD 前置材料想法，需要先拆研究目标 | `research-topic-compiler` 的 `Research Goal Framing Gate` | 先输出 Research Goal Framing：原始意图、研究目标、主问题、子问题、输出要求、out-of-scope 和推荐模式；不要直接搜索。 |
| 轻量概念解读、概念源流、语义演化、范式阶段、PM 技术评审提问脚本 | `research-topic-compiler` 的 `Lightweight Concept Lens Mode` | 输出 PM 决策看板、概念源流、阶段矩阵、反模式和评审问题；默认不写入 Obsidian。 |
| 系统学习、深度专题、长期沉淀、Obsidian Research Project | `research-topic-compiler` 的深度研究模式 | 输出研究计划、证据矩阵、研究报告、学习包或长期雷达。 |
| 候选发现、候选池、竞品池、跨会话 handoff | `research-topic-compiler` 的 Product Candidate Research | 输出 Candidate Backlog、Candidate Summary、评分输入和 handoff；这些是最终决策输入。 |
| 明确决策路线、平台接入、工具选型、可行性判断、最终推荐 | `decision-research` | 输出有立场推荐、排除理由、接入风险、验证路径、置信度和颠覆条件。 |
| 用户还没定义清楚为什么研究这个主题 | `ai-collaboration-calibration` | 先校准问题、决策目标和约束，再进入研究。 |

典型分流：

- “帮我轻量解构一下 MCP 的概念源流，输出 PM 决策看板。” -> `research-topic-compiler` Lightweight Concept Lens Mode。
- “我想研究 Agent 从聊天到做事，后面要做 Roadmap，先帮我把研究目标拆清楚。” -> `research-topic-compiler` Research Goal Framing Gate。
- “系统研究 MCP 安全最佳实践，整理到 Obsidian。” -> `research-topic-compiler` 深度研究模式。
- “研究市面上的 AI 视频生成方案，先沉淀候选池，后续继续补。” -> `research-topic-compiler` Product Candidate Research。
- “我们应该选 MCP 还是自研工具协议？” -> `decision-research`。
- “基于这个 Candidate Backlog 给我一个最终推荐。” -> `decision-research`。

## Loop Extension 分流规则

Loop Extension 不是新的 Skill 入口，而是现有 Skill 的状态化运行模式。只有用户明确需要多轮、可恢复、持续更新或准备度收敛时才启用；普通一次性任务仍按核心路由表处理。

| 用户目标 | 优先 Skill / Mode | 说明 |
| --- | --- | --- |
| 围绕同一个决策持续收敛，下一轮继续更新证据和结论 | `decision-research` 的 Decision Research Loop | 读取 `references/decision-loop-contract.md`，维护 Research Map、假设矩阵、证据表、Assumption Ledger、Scope Drift 和结论版本。 |
| 围绕长期变化主题维护认知雷达 | `research-topic-compiler` 的 Research Radar Loop | 读取 `references/research-radar-loop-contract.md`，维护 watchlist、证据变化、阶段结论 Diff 和 `09_更新日志.md`；不默认创建 automation。 |
| 围绕同一份 PRD 多轮关闭阻断项并判断能否进入开发计划 | `prd-review` 的 PRD Readiness Loop | 读取 `references/prd-readiness-loop-contract.md`，维护 open blockers、revision draft、readiness status 和 handoff decision。 |
| 只是一次性调研、一次性研究报告或一次 PRD review | 原 Skill 普通模式 | 不启用 Loop contract，不创建状态文件。 |

如果任务仍然模糊、没有稳定目标、没有状态、没有验证口径或没有停止条件，先回到 `ai-collaboration-calibration`，不要强行 Loop 化。

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

## UI Mockup / 高保真 UI 交付分流规则

`ui-mockup-desktop-workbench` 只在 PRD 或页面需求已经足够明确，并且用户要的是可确认、可截图、可交付前端实现的桌面端真实页面时使用。

| 用户目标 | 优先 Skill | 说明 |
| --- | --- | --- |
| 从 PRD、UI 规范和真实前端项目生成可开发复刻的桌面工作台 UI | `ui-mockup-desktop-workbench` 的 `project-native-preview` | 先做 Design Discovery Gate，读取真实路由、组件、token、图标和样式，再输出 preview route/component、screen contract、component map 和 implementation notes。 |
| 不改真实项目，但需要开发能准确还原 UI | `ui-mockup-desktop-workbench` 的 `visual-handoff` | 输出高保真 HTML/React 视觉参考、截图、组件映射、状态清单、实现说明和迁移边界。 |
| 早期只想快速讨论布局或信息架构 | `ui-mockup-desktop-workbench` 的 `concept-html` 或 `ui-wireframe-to-html` | concept HTML 只作为视觉讨论稿；低保真结构优先用 `ui-wireframe-to-html`。 |
| PRD 还没成型，需要先补目标、流程、验收 | `prd-architect` | 先把需求写清楚，不直接画页面。 |
| 已有 PRD，但担心缺口、冲突、不可测试 | `prd-review` | 先 review 并关闭阻断项，再生成 mockup。 |
| mockup 过程中发现 PRD 缺状态、验收或流程冲突 | `prd-review` / `prd-architect` | 冲突和 readiness 问题走 `prd-review`；缺章节或缺描述走 `prd-architect`。 |
| 只需要低保真结构、ASCII 布局或线框 | `ui-wireframe-to-html` 或 `prd-architect` 内的 UI 结构步骤 | 不强求视觉 polish。 |
| 要生产级前端实现、接入真实路由和测试 | Superpowers `writing-plans` 后进入实现 | mockup 不是生产代码。 |

不要把 standalone HTML 当生产实现。如果用户要求“开发复刻”，必须同时产出 `screen-contract.md`、`component-map.md`、`implementation-notes.md`、截图/验证结果和迁移边界。

## PRD 到 Issue / 开发计划的衔接

`prd-architect` 和 `prd-review` 的边界止于产品需求交付准备度。只有当 PRD 已经满足以下条件，才适合进入 `prd-to-issues` 或 Superpowers `writing-plans`：

- 目标用户、问题、范围边界和非目标已明确。
- 主流程、关键状态、输入输出、异常或人工接管点已写清。
- 验收标准能被测试或人工检查。
- 阻断性待确认项已经关闭，或被显式列为 issue / implementation plan 的前置假设。

分流规则：

- 用户要 GitHub issues、开发工单、implementation tickets、可领取 backlog、AFK / HITL 标注或 coverage matrix：用 `prd-to-issues`。
- 用户要文件边界、测试策略、实现步骤、提交节奏或本地开发计划：用 Superpowers `writing-plans`。
- `prd-to-issues` 可以作为 `writing-plans` 的输入，但不替代实现计划；`writing-plans` 可以消费 PRD 或 issue backlog，但不负责 PRD readiness review。
