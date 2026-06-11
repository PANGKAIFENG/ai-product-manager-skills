---
name: research-topic-compiler
description: >
  专题研究编译器 / Persona-Adaptive Research-to-Learning Compiler：当用户要围绕一个主题做系统学习、
  专题研究、行业调研、最佳实践提炼、轻量概念解读、概念源流、语义演化、PM 技术评审提问脚本或行业演进看板时使用。
  适合把研究转成 Research Project、学习报告、证据矩阵、PM 决策看板、模板或实践任务。适合“系统研究一个主题”
  “整理到 Obsidian”“做深度专题”“研究行业最佳实践”“概念解读”“概念源流”“PM 技术评审提问脚本”
  “行业演进看板”“这个主题对我的业务有什么用”。不适合创建 Skill、评审 SKILL.md、普通即时搜索或一次性摘要。
---

# 专题研究编译器（research-topic-compiler）

## 中文速查

- 中文名：专题研究编译器 / 系统学习与概念源流研究助手
- 英文稳定名：`research-topic-compiler`
- 分类：研究学习 / Obsidian 知识编译
- 你可以这样叫我：`系统研究这个主题`、`帮我整理到 Obsidian`、`做一个深度专题`、`研究行业最佳实践`、`概念解读`、`概念源流`、`PM 技术评审提问脚本`、`行业演进看板`
- 适合：围绕研究主题做多渠道证据收集、筛选、证据矩阵、阶段结论、概念源流、轻量 PM 决策看板、用户画像自适应学习报告和应用转化
- 不适合：创建或评审 Skill；普通新闻搜索或一次性摘要

## Overview

使用这个 Skill 把一个研究主题编译成可学习、可追溯、可继续扩展、并能按用户画像转化为实际工作判断的 Obsidian Research Project 或聊天内研究报告。

核心原则：

- 先判断研究深度，再决定渠道和样本量。
- 先解析用户画像，再决定解释方式、案例选择、实践任务和应用转化。
- Obsidian 是内部基线和默认沉淀位置，不是唯一研究渠道。
- 外部渠道动态选择，不默认全开；根据主题类型、证据缺口、时效性和可信度要求启用。
- 研究前可以先做 `Pre-Research Source Expansion`：用公开搜索、垂直 API、RSS、产品/市场目录等渠道扩充候选来源，再筛选进入正式证据矩阵。
- 结论必须能回到证据矩阵；`05_研究报告` 是第一阅读入口，`02_证据与卡片` 是按需深挖层。
- 系统学习不是重型课程仓库；默认保持轻量，只有触发条件满足时才建议独立学习包文件。
- 轻量概念解构属于本 Skill 的研究模式，不再单独使用独立概念看板 Skill；它适合快速建立概念源流、语义漂移、范式阶段和 PM 决策问题。
- 用户画像只影响解释深度、案例选择、输出结构和实践任务，不覆盖用户当前明确要求。
- 研究必须能转成行动：判断、方案、模板、任务、PRD、Workflow、Eval、Checklist、SOP、路线图或实践练习。
- 用户补充的新渠道可以进入渠道库，但要先判断适用主题、访问条件、证据强度和风险。
- 微信公众号、X、私域社区、付费库等渠道默认只能做公开候选发现；任何登录态读取、客户端转发、发送到 Obsidian 同步号或第三方服务的动作，都需要当前 run 的明确授权和可见确认点。

## Input / Context Intake

启动研究前先收集或推断这些上下文；不要问本地文件能发现的信息，只在答案会改变研究范围、访问权限或写回位置时追问：

- 研究主题：主题名称、用户要解决的决策或学习目标、是否已有种子资料。
- 预期产物：聊天内报告、Obsidian Research Project、更新已有专题、还是长期雷达。
- 深度约束：用户期望的速度、深度、样本量、是否需要 `L4/L5` 级外部扩展。
- 内部基线：是否扫描 Obsidian、哪些 Vault/目录可用、是否只读 `笔记同步助手`。
- 渠道偏好：必须看的渠道、明确排除的渠道、是否需要产品研究、GitHub、官方文档、论文、社区或 X。
- 访问边界：登录、API token、付费报告、私密社区、公司内部资料和引用限制。
- 写回边界：目标目录、命名规则、是否允许新增渠道到 `channel-registry.md`。
- 用户画像：角色、领域、技术深度、目标类型、输出偏好、应用场景和最终决策需求；先按 `User Context Resolution` 解析，不要默认每次追问。

默认假设：Obsidian 是内部基线，公开外部渠道可用于补证；封闭、付费、登录或私密渠道必须先取得用户授权。用户补充渠道时，先判断是本次临时使用还是值得进入渠道库；只有用户明确希望复用时才写入 `references/channel-registry.md`。

## User Context Resolution

生成研究输出前先解析用户上下文。详细字段和追问规则见 `references/user-context-standards.md`。

优先级：

1. 当前用户消息中的显式要求，例如“我是后端工程师”“给我 PRD 视角”“不要太技术”。
2. 当前项目或目标 Research Project 附近的 `user-profile.md`。
3. 全局 `user-profile.md`，例如 Vault 根目录或用户明确指定的长期画像文件。
4. Skill 内置默认画像 `references/default-user-profile.md`，仅作为本地默认配置。
5. 如果仍缺少会显著影响输出质量的信息，最多问 3-5 个轻量问题。

处理规则：

- 不要每次都询问用户身份；能从当前消息、本地 profile 或默认 profile 推断时直接使用。
- 当前任务指令永远高于长期画像和默认画像。
- 用户画像只影响解释深度、案例选择、输出结构、实践任务和应用建议。
- 用户画像不能改变证据等级、不能绕过访问限制、不能把弱证据升级为稳定结论。
- 如果用户画像未知且主题不复杂，先用通用解释；只有主题复杂且目标不清时再追问。
- 只有当用户要求持久化、当前任务已经写入 Obsidian，或 profile 文件是本次明确产物时，才创建或更新 `user-profile.md`；否则画像只在本次研究中使用。

## Research Modes

按用户目标选择一种主模式，也可以组合使用：

- `Normal Research`：资料整理、证据矩阵、阶段结论、研究报告，适合普通专题研究。
- `Lightweight Concept Lens Mode`：轻量概念解读、概念源流、语义演化、行业演进、PM 技术评审提问脚本或 HTML 决策看板。
- `Learning Pack Mode`：用户对陌生领域要建立学习框架时启用；详细标准见 `references/learning-pack-standards.md`。
- `Application Mode`：用户问”对我/我们的业务有什么用””怎么落地””怎么做成方案/PRD/Workflow/Skill/Eval”时启用。
- `Radar Mode`：长期变化主题启用 `L5`，只形成 watchlist、更新日志和复盘建议；不默认创建 automation。
- `Product Decision Research`：用户需要做产品决策（选型、竞品分析、技术方案对比、市场策略验证）时启用。详细规则见 `references/product-decision-mode.md`。

### Radar Loop Extension

当用户明确要“长期雷达”“持续更新”“定期复盘”“更新已有研究项目”“维护活的知识库”或“下一轮继续扫描同一主题”时，读取 `references/research-radar-loop-contract.md`。

Research Radar Loop 是 `Radar Mode` 的状态化合约：

- 它维护演进主题的 watchlist、证据变化、阶段结论 Diff、更新日志和下一步。
- 它不等于普通新闻监控；每次扫描都要说明对用户当前学习、产品判断或决策有什么影响。
- 它不自动创建 Codex automation；只有用户明确要求创建、开启、设置或定期运行时，才进入 automation 流程。
- 弱信号只能进入更新日志或待复盘区，不能直接改写稳定阶段结论。
- 如果研究信号变成具体产品、技术、商业或战略选择，建议升级到 `decision-research`。

不要因为用户只是要一次性概念解释、单篇文章总结或固定知识学习就进入 Radar Loop。

Product Decision Research 触发信号：

- 用户说”这几个方案怎么选””帮我做竞品分析””对比一下 A 和 B””选型”。
- 用户说”这个方向值不值得做””市场上有没有类似的””我该怎么定位”。
- 用户描述的是一个需要在多个候选项之间做决定的场景。
- 用户目标是形成 PRD 输入、技术选型报告、Go/No-Go 决策或产品路线图。
- 调研后的预期产物是候选池（Candidate Backlog）而非单一结论。

Product Decision Research 与 Application Mode 的区别：Application Mode 是”研究完如何落地”，Product Decision Research 是”研究本身就是为了在多个选项间做决策”。两者可以组合：先用 Product Decision Research 形成候选池和评分，再用 Application Mode 将最终选择转化为落地方案。

Lightweight Concept Lens Mode 触发信号：

- 用户说“概念解读”“概念源流”“概念透镜”“语义演化”“行业演进看板”。
- 用户要 PM 技术评审提问脚本、反模式诊断、概念债务识别或供应商/方案评估问题。
- 用户不需要完整 Obsidian Research Project，但需要带来源的结构化理解和可操作判断。
- 用户要求生成本地 HTML 决策看板、Tailwind + Alpine.js 看板或可验证的概念演进 dashboard。

Lightweight Concept Lens Mode 工作规则：

- 先追溯概念源流：提出背景、原始问题、原始用户、原始用途、主要语义漂移和当前误用。
- 再归纳范式阶段：从证据中推导 3-6 个阶段，不强套固定四阶段，也不把简单时间线当结构。
- 每个阶段必须写清用户需求、底层矛盾、成熟解法、PM 视角操作逻辑、证据依据和 1-2 个评审问题。
- 输出默认是聊天内 PM 决策看板；只有用户明确要文件或 HTML dashboard 时才生成本地 `dashboard.html`。
- 生成 HTML dashboard 前读取 `references/concept-lens-output-contract.md`、`references/concept-lens-html-dashboard-template.md` 和 `references/concept-lens-design-quality.md`。
- 冷启动或事实敏感主题先读取 `references/concept-lens-source-and-factuality.md` 并浏览验证；用到历史来源时区分证据和模型推断。
- 生成 HTML 后运行 `python3 scripts/validate_html_artifact.py <path-to-dashboard.html>`，并在可用时做浏览器视觉检查。

Learning Pack Mode 触发信号：

- 用户说“陌生领域”“系统学习”“学习路线”“教程式理解”。
- 用户说“不要只给证据卡片”“不要太表面”。
- 用户说“像 Agent-Learning-Hub，但轻一点”。
- 用户希望建立一个主题的长期认知框架。

Learning Pack 默认写进 `05_研究报告`、`03_阶段结论`、`07_行业案例对照` 和 `08_最佳实践与应用模板`。不要默认新增 `10-12` 文件；只有用户明确要求独立学习包、主题复杂度达到 `L4/L5` 且内容过长、研究项目要复用给他人学习，或 `05_研究报告` 过长影响阅读时，才建议新增 `10_学习路线.md`、`11_概念地图.md`、`12_实践任务.md`。

Application Mode 必须把核心结论转成用户当前工作中的至少一种产物：

- 判断：是否值得做、边界在哪里、风险是什么、何时不适合。
- 方案：模块拆解、路线图、资源投入、关键取舍。
- 模板：PRD 片段、Workflow 表、Eval 指标、接口草案、SOP、风险矩阵。
- 任务：最小实践、验证动作、下一步调研、团队分工。

## Pre-Research Source Expansion

在 Obsidian 内部基线扫描之前，先判断是否需要扩充前置来源。详细规则见 `references/pre-research-source-expansion.md`。

启用信号：

- 用户资料不足、`笔记同步助手` 中没有足够种子文章，或用户明确希望“不要依赖我提前收集输入”。
- 主题高度依赖中文实践文章、产品案例、市场反馈、近期趋势或封闭平台内容。
- 研究目标是系统学习、产品判断、竞品/行业调研或应用转化，需要先扩大候选面再筛选。

默认产物是 `Candidate Source Table`，不要直接把搜索结果当结论：

```markdown
| Title | Channel | Author/account | Date | URL/access | Snippet | Relevance | Quality | Recommended action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
```

推荐动作只能是：

- `read now`：公开可读、质量足够，进入证据卡片。
- `sync to Obsidian`：适合进入 `笔记同步助手` 或 Research Project，但需要授权的同步动作。
- `verify later`：有价值但受登录、API、反爬、付费或来源不明限制。
- `skip`：重复、低质、SEO、疑似转载或与研究问题弱相关。

微信公众号处理边界：

- 可默认尝试公开候选发现，例如搜狗微信、Web 搜索、OpenCLI Weixin adapter 或已授权的第三方 API。
- 搜狗微信适合发现候选标题、摘要、时间和跳转线索；它可能触发反爬，不能假设可稳定抓全文。
- 第三方公众号 API 只在用户提供 token 或明确允许使用时启用；标注服务商、访问时间、字段范围和可靠性限制。
- WeWe RSS/RSSHub 类工具适合已知公众号的持续订阅，不适合无边界全网搜索。
- 打开微信客户端、搜索公众号文章、转发给 `Obsidian @笔记同步科技` 或其他同步号属于有副作用的发送/同步动作；即使用户偏好自动化，也要在当前 run 明确授权，且默认在发送前停下确认。不要静默发送。

## Persona-Adaptive Output

按解析出的 `role` 调整输出重点。角色未知时先用通用解释，不要假设用户是工程师或产品经理。

- 产品经理：强调产品判断、业务映射、能力边界、PRD 输入、Workflow 设计、Eval 标准和落地路径；技术解释要转译成产品语言；每个关键结论说明“对产品设计有什么影响”。
- 工程师：强调架构、接口、数据结构、状态管理、权限、安全、测试、可观测性和实现风险；每个关键结论说明“实现上需要注意什么”。
- 设计师：强调用户场景、交互流程、信息架构、认知负担、视觉表达和用户决策路径；每个关键结论说明“界面和体验上怎么体现”。
- 运营：强调 SOP、执行流程、内容生产、增长指标、转化效率和复盘机制；每个关键结论说明“怎么变成可执行动作”。
- 管理者/创始人：强调战略价值、成本、风险、组织分工、ROI、路线图和资源投入；每个关键结论说明“是否值得投、怎么分阶段投”。
- 研究员/分析师：强调概念边界、方法论、证据强度、反例、研究缺口和可复现性；每个关键结论说明“还需要怎样验证”。

## Catalog / Distribution Notes

- Catalog source：GitHub Skill 仓库 `git@github.com:PANGKAIFENG/ai-product-manager-skills.git` 的默认分支是标准源。
- Category/status：中文分类“研究学习 / 产品研究”，状态 `active`。
- Public/private decision：这是公开 AI PM Skill；涉及个人 Obsidian 路径、私密资料、登录渠道或客户资料时必须在具体 run 中显式授权并标注边界。
- Distribution targets：保持 GitHub checkout、Multica 确认的 `multica-skill` 目录、`/Users/linctex/.codex/skills` 和 `/Users/linctex/.claude/skills` 一致；当前 Codex/Claude 可通过 Skillshare 管理的 symlink 使用。
- Sync rule：`skillshare sync` 是可选分发方式，不是本 Skill 的事实来源；使用前先确认目标路径确实由 Skillshare 管理。

## Workflow

1. 捕获主题和目标，用一句话复述研究对象、用户要解决的问题和预期产物。
2. 解析用户画像。按 `User Context Resolution` 选择通用解释或 persona-adaptive 输出。
3. 判断研究模式和深度。非平凡主题先读 `references/research-depth-rubric.md`，推荐 `L1-L5`，并说明是否启用 Lightweight Concept Lens、Learning Pack、Application Mode 或 Product Decision Research。
4. 选择渠道。读取 `references/channel-selection-rubric.md` 和 `references/channel-registry.md`，根据主题动态选择 Obsidian 之外的渠道。
5. 判断是否启用 `Pre-Research Source Expansion`。当内部输入不足、主题依赖外部生态或用户要求扩源时，先生成候选来源表和筛选建议。
6. 先输出 `Research Run Plan`。包含推荐深度、研究模式、用户画像摘要、主题类型、核心问题、渠道选择、前置扩源渠道、每个渠道启用或不启用的理由、样本量、写入位置、凭据或访问限制。
7. 做 Obsidian 内部基线扫描。查 `笔记同步助手`、`03_Resources`、已有 Research Project、主题卡片、规则和模板，确认已有沉淀、证据缺口和重复研究风险。
8. 做外部发现与筛选。只读取公开或用户授权内容；GitHub 仅读文档、源码、配置、issues 和 discussions，默认不执行第三方代码。
9. 建立证据矩阵。按”研究问题 × 来源 × 结论 × 证据强度 × 对当前用户的启发 × 扩展阅读”组织。
10. 写入或更新 Obsidian Research Project。默认输出 `00_研究定义` 到 `05_研究报告`；深度专题可增加 `06_外部渠道研究`、`07_行业案例对照`、`08_最佳实践与应用模板`、`09_更新日志`；只在触发条件满足时建议 `10-12` 学习包文件。Lightweight Concept Lens 默认不写入 Obsidian，除非用户要求沉淀。
11. 输出最终摘要。给出研究报告入口、用户画像适配方式、核心结论、关键证据、应用转化、仍需验证、下一步建议和新增渠道候选。

### Product Decision Research 分支步骤

当步骤 3 判定为 Product Decision Research 模式时，步骤 6-11 替换为以下流程：

6. 输出 `Research Run Plan`（同上），额外包含：决策维度（见 `references/product-decision-mode.md`）、候选池初始边界、评分权重草案。
7. 读取项目上下文。按 `references/project-context-intake.md` 获取项目阶段、约束、已有决策和用户优先级。
8. 做内部基线扫描 + 外部发现。与 Normal Research 一致，但聚焦于形成候选列表而非单一结论。
9. 形成 Candidate Backlog。按 `references/candidate-backlog-schema.md` 的 17 字段 schema 填充每个候选项，通过 Quality Gate 5 项检查。
10. 评分与排序。按用户确认的维度权重打分，输出排序表和关键差异点。
11. Taxonomy 转译（可选）。若候选项来自外部体系，按 `references/taxonomy-translation.md` 转译为项目内部分类。
12. 输出阶段产物：
    - Candidate Backlog（完整表格）
    - Decision Summary（Top 3 推荐 + 理由 + 风险）
    - Cross-Session Handoff（按 `references/cross-session-handoff.md` 格式，供后续会话继续）
13. 判断 Post-Research Exit。按 `references/post-research-exits.md` 推荐下一步出口（PRD Input / Starter Scenes / Demo Beachhead / Eval 等），不强制执行。

## L5 Automation Handling

`L5` 表示长期雷达，不等于默认创建自动化。默认行为是先形成 watchlist、更新日志格式、复盘节奏和 automation proposal。

只有当用户在当前任务中明确要求创建、开启、设置、定期运行、持续自动更新或调用 Codex automation 时，才调用 Codex 的 automation 能力创建 `cron` automation。不要把“L5”“长期雷达”“持续研究”单独解释为创建授权。

创建自动化前先检查是否已有同主题 automation，优先更新已有任务，避免重复。自动化任务应使用 `cron`，不使用 thread heartbeat；L5 研究雷达是独立周期任务，不是当前对话稍后继续。

L5 automation 的默认安全边界：

- 只读取公开来源、用户授权来源、当前 Research Project、对应 Context Pack 和允许读取的 Obsidian 目录。
- 只追加或更新 Research Project 内的雷达型内容，例如 `09_更新日志.md` 的候选信号、待复盘更新、来源状态和下一步。
- 不自动修改 `03_阶段结论.md`、Theme、Area、长期规则、权限策略、Skill 或项目级 instructions，除非用户在该次 automation run 后再次确认。
- 不移动、删除、覆盖 `笔记同步助手` 或其他来源层原文。
- 不绕过登录、付费墙、私密社区或访问限制；需要凭据时把它记录为 blocked/needs authorization。
- 弱信号只能进入待复盘区，不能直接升级为稳定结论。

如果用户确认创建 automation，最终摘要要说明 automation 名称、频率、写入范围、禁止动作和后续人工确认点。

## Research Run Plan

开始研究前输出：

```markdown
**Research Run Plan**
- Topic: <研究主题>
- User goal: <用户要学会、判断或沉淀什么>
- Research mode: <Normal Research / Lightweight Concept Lens / Learning Pack / Application / Radar>
- User context: <role, domain, technical_depth, goal_type, output_preference, application_context, decision_need>
- Recommended depth: <L1 / L2 / L3 / L4 / L5, with reason>
- Topic type: <平台能力 / 开源工程 / 产品竞品 / 学术方法 / 政策合规 / 市场趋势 / 其他>
- Core questions: <按理解型 / 判断型 / 设计型 / 实践型 / 复盘型组织>
- Pre-research expansion: <是否启用 + 候选渠道 + 预期候选数 + 是否需要授权同步>
- Channels selected: <渠道 + 启用理由 + 样本量>
- Channels skipped: <未启用渠道 + 原因>
- Access needs: <GitHub token / X token / login / paywall / none>
- Obsidian output: <chat-only / new Research Project / update existing project>
- Expected files: <00-05, optional 06-09, only suggest 10-12 when triggered>
- Confirmation needed: <only if L4/L5, closed channels, credentials, or broad writes>
```

如果用户已经明确要求写入 Obsidian，`L1-L3` 可以在输出计划后继续执行。`L4/L5`、封闭渠道、付费资料、需要登录或凭据、自动化持续跟踪、跨多个项目的大范围写入，都要先取得明确确认。若用户明确确认创建 L5 automation，按 `L5 Automation Handling` 调用 Codex automation。

## Channel Selection Rules

默认不是“所有渠道全开”，而是先判断主题，再选择渠道。

- 平台能力、API、机制、最佳实践：优先官方文档、公司工程博客、release notes、cookbook、SDK 示例。
- 开源实现、工程模式、工具链：启用 GitHub、包管理器、issues、discussions、示例项目。
- 产品研究、竞品、市场反馈：启用 Product Hunt、G2、Capterra、AlternativeTo、App Store、Chrome Web Store、VS Code Marketplace、定价页、changelog、用户评论。
- 学术方法、算法、评测、benchmark：启用论文、技术报告、Papers with Code、OpenReview、arXiv、Semantic Scholar。
- 趋势、近期发布、作者观点：启用 X、社区讨论、HN、Reddit、新闻稿和 newsletter；这些默认标为弱证据，除非能被官方或实现证据交叉验证。
- 政策、合规、安全：启用官方监管文件、标准组织、CVE/NVD、vendor advisories、security docs。
- 封闭或半封闭渠道：只在用户授权、提供访问方式且研究目标需要时使用；不要绕过登录、付费墙或访问限制。

## Obsidian Output Contract

写入 Obsidian 前读 `references/obsidian-output-contract.md`。

默认 Research Project 结构：

- `00_研究定义.md`
- `01_问题清单.md`
- `02_证据与卡片.md`
- `03_阶段结论.md`
- `04_下一步.md`
- `05_研究报告.md`

深度专题可补：

- `06_外部渠道研究.md`
- `07_行业案例对照.md`
- `08_最佳实践与应用模板.md`
- `09_更新日志.md`

仅在触发条件满足时建议独立学习包文件：

- `10_学习路线.md`
- `11_概念地图.md`
- `12_实践任务.md`

`笔记同步助手` 是来源层，只读。不要移动、删除、覆盖原始同步文章。新 Resource、Theme 更新或长期 Area 结论只在规则允许时写回。

## Channel Registry Update

当用户补充新的研究渠道时，先判断它是否值得进入渠道库。

记录字段：

```markdown
| Channel | Best for | Access | Evidence level | Query method | Risks | Notes |
| --- | --- | --- | --- | --- | --- | --- |
```

处理规则：

- 如果用户明确说“以后也用这个渠道”或“补录进 Skill”，将它加入 `references/channel-registry.md` 的合适分区。
- 如果只是本次研究临时提供，把它记录到当前 Research Project 的 `02_证据与卡片` 或 `04_下一步`。
- 新渠道涉及登录、付费、私密社区、客户数据或内部资料时，必须标明访问条件和引用限制。
- 渠道库更新后，最终结果里说明新增了什么、适合什么主题、证据强度是什么。

## Output Format

完成后输出：

```markdown
**Research Result**
- Project/report: <Obsidian path or chat-only>
- Depth used: <L1-L5>
- Research mode: <Normal / Lightweight Concept Lens / Learning Pack / Application / Radar / Product Decision>
- Persona adaptation: <role/domain/depth/goal used, or generic>
- Channels used: <channels and sample counts>
- Core conclusions: <3-7 bullets>
- Application outputs: <judgment, template, task, PRD/Workflow/Eval/SOP/roadmap, or none>
- Strongest evidence: <top sources>
- Weak or trend evidence: <sources that need caution>
- Added channel candidates: <new registry entries or none>
- Still uncertain: <evidence gaps>
- Next actions: <what to read or do next>
```

### Product Decision Research 输出格式

当使用 Product Decision Research 模式时，额外输出：

```markdown
**Product Decision Result**
- Decision question: <用户要做什么决策>
- Candidate count: <候选池总数 / 通过 Quality Gate 数>
- Top recommendations: <Top 3 候选 + 一句话理由>
- Key differentiators: <候选间核心差异点>
- Scoring dimensions: <使用的评分维度和权重>
- Confidence level: <High / Medium / Low + 原因>
- Handoff file: <跨会话 handoff 文件路径，或 chat-only>
- Recommended exit: <PRD Input / Starter Scenes / Demo Beachhead / Eval / Registry / Review / Roadmap / none>
- Open questions for next session: <仍需下一轮研究验证的问题>
```

## Definition of Done

任务完成必须满足至少一种情况：

- `L1` 快查：给出直接答案、来源和证据局限。
- `Lightweight Concept Lens`：给出概念源流、语义演化、范式阶段、PM 决策问题、反模式或概念债务判断；如果生成 HTML，静态验证已通过或明确说明限制。
- `L2`：给出主题地图、核心概念、基础案例、来源和下一步阅读。
- `L3`：Research Project 或聊天报告已覆盖问题清单、证据矩阵、阶段结论和第一阅读入口式 `05_研究报告`，能帮助陌生领域入门。
- `L4`：额外形成外部渠道研究、行业案例对照、最佳实践或应用模板，能指导方案设计、选型或 PRD 输入。
- `L5`：形成 watchlist、更新日志、稳定/候选/待验证/废弃结论分层和后续自动化建议；若用户明确确认创建 automation，则调用 Codex `cron` automation，并保留低风险写入边界与人工确认点。
- Product Decision Research：候选池通过 Quality Gate（至少 3 个候选项有完整 schema 填充）、评分表输出、Decision Summary 包含 Top 推荐和风险、Cross-Session Handoff 文件可被后续会话直接消费。
- Persona-adaptive 输出：关键结论已说明对当前用户画像、业务目标或应用场景的影响。
- Application 输出：至少给出一个可执行动作、模板、实践任务或判断框架，除非用户只要求快查。
- 如果渠道受限，必须说明未使用的渠道、限制原因和对结论可信度的影响。

## Resource Guide

- `references/research-depth-rubric.md`：判断 `L1-L5` 深度、样本量和确认门禁。
- `references/research-radar-loop-contract.md`：Research Radar Loop 的状态文件、信号分类、更新规则、暂停条件和升级规则。
- `references/user-context-standards.md`：解析用户画像和 persona-adaptive 输出边界。
- `references/default-user-profile.md`：本地默认用户画像；仅作为默认配置，不写死主逻辑。
- `references/learning-pack-standards.md`：轻量系统学习包标准。
- `references/pre-research-source-expansion.md`：研究前扩源、候选来源筛选和微信公众号/同步渠道边界。
- `references/channel-selection-rubric.md`：按主题选择渠道。
- `references/channel-registry.md`：预置渠道库和后续补录位置。
- `references/source-quality-rules.md`：证据强度、来源筛选、引用和封闭渠道处理规则。
- `references/obsidian-output-contract.md`：Obsidian 写回结构和 Vault 规范。
- `references/report-writing-standards.md`：`05_研究报告` 写作标准。
- `references/concept-lens-source-and-factuality.md`：概念源流、历史来源、引用和不确定性处理。
- `references/concept-lens-paradigm-framework.md`：范式阶段归纳、PM 矩阵维度和反模板规则。
- `references/concept-lens-output-contract.md`：轻量概念解构的 Markdown 与文件产物结构。
- `references/concept-lens-html-dashboard-template.md`：Tailwind + Alpine.js HTML 决策看板要求和验证标记。
- `references/concept-lens-design-quality.md`：HTML dashboard 的视觉质量与移动端检查。
- `scripts/validate_html_artifact.py`：HTML dashboard 的确定性结构校验脚本。
- `references/product-decision-mode.md`：产品决策型研究模式、评分维度、候选池默认输出。
- `references/project-context-intake.md`：项目上下文读取规范、必填字段和输出分层。
- `references/taxonomy-translation.md`：外部模式→内部分类转译规则和市场分类模板。
- `references/candidate-backlog-schema.md`：候选池 17 字段 schema、Quality Gate 5 项检查和评分规则。
- `references/cross-session-handoff.md`：跨会话 handoff 模板、合并规则和 Research Run Metadata。
- `references/post-research-exits.md`：研究到 PRD/Starter/Demo/Eval/Registry/Review/Roadmap 7 种出口。

## Evaluation Checklist

- Smoke：`帮我系统研究一下 AI Agent Memory，并整理到 Obsidian。`
- Smoke：`研究一下 MCP 安全最佳实践，需要看官方文档、GitHub 和行业案例。`
- Smoke：`快速了解 Claude Skills 的设计机制，不需要写入 Vault。`
- Smoke：`帮我轻量解构一下 MCP 的概念源流，输出 PM 决策看板。`
- Smoke：`分析向量数据库的概念源流、行业演进和 PM 技术评审提问脚本。`
- Smoke：`我对 Agent Harness 完全陌生，帮我系统学习并整理到 Obsidian。`
- Smoke：`研究 Harness 对我们推款智能体有什么用。`
- Smoke：`我是后端工程师，研究 Agent Harness 的权限和 Trace 机制。`
- Product Decision：`帮我对比 Electron vs Tauri vs Flutter Desktop，选一个做桌面端。` → 应触发 Product Decision Research 模式，输出候选池和评分表。
- Product Decision：`研究一下市面上的 AI 视频生成方案，我需要选一个集成到产品里。` → 应形成 Candidate Backlog，通过 Quality Gate。
- Product Decision：`这个方向值不值得做？市场上有没有类似的？` → 应输出竞品候选池 + Go/No-Go 判断框架。
- Product Decision Handoff：研究跨多个会话时，后续会话应能从 handoff 文件继续，不重复已有候选。
- Channel selection：学术型主题应启用论文/技术报告。
- Channel selection：开源工具型主题应启用 GitHub。
- Channel selection：产品竞品型主题应考虑 Product Hunt、G2、marketplace、定价页、changelog 和用户评论。
- Channel selection：趋势型主题可启用 X/社区，但必须标注弱证据。
- Persona：产品经理、工程师、设计师、运营、管理者/创始人应看到不同解释重点和实践任务。
- Learning pack：只有明确学习包需求或复杂度触发时才建议 `10-12`。
- Application：研究结论必须能转成判断、方案、模板、任务或实践。
- Non-trigger：`帮我创建一个 Skill。` 不属于公开 AI PM 研究工作流。
- Non-trigger：`帮我 review 这个 SKILL.md。` 不属于公开 AI PM 研究工作流。
- Non-trigger：`搜一下今天某条新闻。` 不应触发本 Skill，除非用户要求沉淀成专题研究。
