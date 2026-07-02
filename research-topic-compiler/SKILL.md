---
name: research-topic-compiler
description: >
  专题研究编译器 / Persona-Adaptive Research-to-Learning Compiler：当用户要围绕一个主题做系统学习、
  专题研究、行业调研、最佳实践提炼、轻量概念解读、概念源流、语义演化、PM 技术评审提问脚本或行业演进看板时使用。
  当用户只有大白话、模糊方向、业务愿望或 Roadmap/PRD 前置材料想法，需要先转成清晰研究目标、研究问题和输出要求时也使用。
  适合把研究转成 Research Project、学习报告、证据矩阵、PM 决策看板、候选池、模板、实践任务、业务判断、商业化输入或高门槛应用研究前置。适合“系统研究一个主题”
  “整理到 Obsidian”“做深度专题”“研究行业最佳实践”“概念解读”“概念源流”“PM 技术评审提问脚本”
  “行业演进看板”“这个主题对我的业务有什么用”。不适合创建 Skill、评审 SKILL.md、普通即时搜索或一次性摘要。
  当用户已经要在明确候选项中选一个、需要最终推荐和排除理由时，应使用 decision-research。
---

# 专题研究编译器（research-topic-compiler）

## 中文速查

- 中文名：专题研究编译器 / 系统学习与概念源流研究助手
- 英文稳定名：`research-topic-compiler`
- 分类：研究学习 / Obsidian 知识编译
- 你可以这样叫我：`系统研究这个主题`、`帮我整理到 Obsidian`、`做一个深度专题`、`研究行业最佳实践`、`概念解读`、`概念源流`、`PM 技术评审提问脚本`、`行业演进看板`、`把这个大白话拆成研究目标`
- 适合：围绕研究主题做多渠道证据收集、筛选、证据矩阵、阶段结论、概念源流、轻量 PM 决策看板、候选池、用户画像自适应学习报告和应用转化；也适合把用户的大白话、模糊主题或 Roadmap 前置想法转成研究目标、研究问题和输出要求
- 不适合：创建或评审 Skill；普通新闻搜索或一次性摘要；明确要“选一个 / 给最终推荐 / 排除其他方案”时改用 `decision-research`

## Overview

使用这个 Skill 把一个研究主题编译成可学习、可追溯、可继续扩展、并能按用户画像转化为实际工作判断的 Obsidian Research Project 或聊天内研究报告。

核心原则：

- 先把用户原话转成明确研究目标、研究问题和输出要求，再判断研究深度、渠道和样本量。
- 先解析用户画像，再决定解释方式、案例选择、实践任务和应用转化。
- Obsidian 是内部基线和默认沉淀位置，不是唯一研究渠道。
- 外部渠道动态选择，不默认全开；根据主题类型、证据缺口、时效性和可信度要求启用。
- 研究前可以先做 `Pre-Research Source Expansion`：用公开搜索、垂直 API、RSS、产品/市场目录等渠道扩充候选来源，再筛选进入正式证据矩阵。
- 结论必须能回到证据矩阵；`05_研究报告` 是第一阅读入口，`02_证据与卡片` 是按需深挖层。
- 系统学习不是重型课程仓库；默认保持轻量，只有触发条件满足时才建议独立学习包文件。
- 当研究会影响产品策略、商业化、工作台/连接器设计、企业 adoption 或其他高成本决策时，默认按高门槛应用研究处理，读取 `references/applied-business-research-contract.md`。
- 轻量概念解构属于本 Skill 的研究模式，不再单独使用独立概念看板 Skill；它适合快速建立概念源流、语义漂移、范式阶段和 PM 决策问题。
- 用户画像只影响解释深度、案例选择、输出结构和实践任务，不覆盖用户当前明确要求。
- 研究必须能转成行动：判断、方案、模板、任务、PRD、Workflow、Eval、Checklist、SOP、路线图或实践练习。
- 用户补充的新渠道可以进入渠道库，但要先判断适用主题、访问条件、证据强度和风险。
- 微信公众号、X、私域社区、付费库等渠道默认只能做公开候选发现；任何登录态读取、客户端转发、发送到 Obsidian 同步号或第三方服务的动作，都需要当前 run 的明确授权和可见确认点。

## Input / Context Intake

启动研究前先收集或推断这些上下文；不要问本地文件能发现的信息，只在答案会改变研究范围、访问权限或写回位置时追问：

- 原始意图：用户原话、业务愿望、想产出的材料、隐含的后续动作。
- 研究主题：主题名称、用户要解决的决策或学习目标、是否已有种子资料。
- 预期产物：聊天内报告、Obsidian Research Project、更新已有专题、还是长期雷达。
- 深度约束：用户期望的速度、深度、样本量、是否需要 `L4/L5` 级外部扩展。
- 内部基线：是否扫描 Obsidian、哪些 Vault/目录可用、是否只读 `笔记同步助手`。
- 渠道偏好：必须看的渠道、明确排除的渠道、是否需要产品研究、GitHub、官方文档、论文、社区或 X。
- 访问边界：登录、API token、付费报告、私密社区、公司内部资料和引用限制。
- 写回边界：目标目录、命名规则、是否允许新增渠道到 `channel-registry.md`。
- 用户画像：角色、领域、技术深度、目标类型、输出偏好、应用场景和最终决策需求；先按 `User Context Resolution` 解析，不要默认每次追问。

默认假设：Obsidian 是内部基线，公开外部渠道可用于补证；封闭、付费、登录或私密渠道必须先取得用户授权。用户补充渠道时，先判断是本次临时使用还是值得进入渠道库；只有用户明确希望复用时才写入 `references/channel-registry.md`。

## Research Goal Framing Gate

当用户输入是大白话、宽泛方向、业务愿望、解法名称、Roadmap/PRD 前置材料想法，或没有明确研究问题与输出要求时，先读 `references/research-goal-framing-gate.md`。

这个 Gate 的职责是把用户原话转成可执行研究 brief：

- 保留用户原始意图。
- 推断真正研究目标。
- 判断目标类型：Concept Lens、Industry Evolution、Application Translation、Product Candidate、Roadmap Input、Learning Pack 或 Research Radar。
- 拆出主研究问题、子问题、out of scope 和证据标准。
- 明确读者、产物形态和研究结果要支持的下一步动作。
- 决定是否需要用户确认；能合理推断时带假设继续。

不要从用户第一句里的名词直接开始搜索。先确认这次研究是为了理解、判断、转译、候选发现、路线图输入、学习沉淀还是持续雷达。

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

按用户目标选择一种主模式，也可以组合使用。先读取 `references/mode-selection.md`；需要细则再读 `references/mode-routing-guide.md`。

| Mode | Use When | Primary Assets |
| --- | --- | --- |
| `Normal Research` | 普通专题研究、证据矩阵、阶段结论 | `research-depth-rubric.md`, `report-writing-standards.md` |
| `Lightweight Concept Lens` | 概念源流、语义演化、PM 技术评审提问脚本、HTML 决策看板 | `concept-lens-*` references |
| `Learning Pack` | 用户对陌生领域建立学习框架 | `learning-pack-standards.md` |
| `Application` | 研究要转成方案、PRD、Workflow、Eval、SOP 或路线图输入 | `applied-business-research-contract.md` |
| `Radar` | 长期变化主题、watchlist、更新日志 | `research-radar-loop-contract.md` |
| `Product Candidate` | 先发现候选、建候选池、为后续决策提供输入 | `product-decision-mode.md`, `candidate-backlog-schema.md` |

用户说“选一个”“给最终推荐”“为什么排除其他方案”“基于 Candidate Backlog 下结论”时，转交 `decision-research`。本 Skill 可以给 Top candidates 或排序表，但它们是决策输入，不是最终决策 authority。

## Pre-Research Source Expansion

当内部输入不足、主题依赖外部生态或用户要求扩源时，读取 `references/pre-research-source-expansion.md`。默认产物是 Candidate Source Table，不把搜索结果直接当结论。登录、付费、私密社区、客户端发送或同步动作都需要当前 run 的明确授权。

## Persona-Adaptive Output

按解析出的 `role` 调整输出重点。角色未知时先用通用解释，不要假设用户是工程师或产品经理；具体字段和追问规则见 `references/user-context-standards.md`。

## Workflow

1. 捕获用户原话、主题和目标。若输入不够明确，先执行 `Research Goal Framing Gate`，输出 `Research Goal Framing`，把大白话转成研究目标、研究问题、输出要求和 out-of-scope。若用户只要求整理研究 brief、先不要搜资料或先不要开始研究，停在 framing 产物，不继续生成 `Research Run Plan`。
2. 解析用户画像。按 `User Context Resolution` 选择通用解释或 persona-adaptive 输出。
3. 判断研究模式和深度。非平凡主题先读 `references/research-depth-rubric.md`，推荐 `L1-L5`，并说明是否启用 Lightweight Concept Lens、Learning Pack、Application Mode、Applied Business Research 或 Product Candidate Research。
4. 选择渠道。读取 `references/channel-selection-rubric.md` 和 `references/channel-registry.md`，根据主题动态选择 Obsidian 之外的渠道。
5. 判断是否启用 `Pre-Research Source Expansion`。当内部输入不足、主题依赖外部生态或用户要求扩源时，先生成候选来源表和筛选建议。
6. 先输出 `Research Run Plan`。包含推荐深度、研究模式、用户画像摘要、主题类型、核心问题、渠道选择、前置扩源渠道、每个渠道启用或不启用的理由、样本量、写入位置、凭据或访问限制。
7. 做 Obsidian 内部基线扫描。查 `笔记同步助手`、`03_Resources`、已有 Research Project、主题卡片、规则和模板，确认已有沉淀、证据缺口和重复研究风险。
8. 做外部发现与筛选。只读取公开或用户授权内容；GitHub 仅读文档、源码、配置、issues 和 discussions，默认不执行第三方代码。
9. 建立证据矩阵。按”研究问题 × 来源 × 结论 × 证据强度 × 对当前用户的启发 × 扩展阅读”组织。
10. 写入或更新 Obsidian Research Project。默认输出 `00_研究定义` 到 `05_研究报告`；深度专题可增加 `06_外部渠道研究`、`07_行业案例对照`、`08_最佳实践与应用模板`、`09_更新日志`；只在触发条件满足时建议 `10-12` 学习包文件。Lightweight Concept Lens 默认不写入 Obsidian，除非用户要求沉淀。
11. 输出最终摘要。给出研究报告入口、用户画像适配方式、核心结论、关键证据、应用转化、仍需验证、下一步建议和新增渠道候选。

### Product Candidate Research 分支步骤

当步骤 3 判定为 Product Candidate Research 模式时，步骤 6-11 替换为以下流程：

6. 输出 `Research Run Plan`（同上），额外包含：决策维度（见 `references/product-decision-mode.md`）、候选池初始边界、评分权重草案。
7. 读取项目上下文。按 `references/project-context-intake.md` 获取项目阶段、约束、已有决策和用户优先级。
8. 做内部基线扫描 + 外部发现。与 Normal Research 一致，但聚焦于形成候选列表而非单一结论。
9. 形成 Candidate Backlog。按 `references/candidate-backlog-schema.md` 的 17 字段 schema 填充每个候选项，通过 Quality Gate 5 项检查。
10. 评分与排序。按用户确认的维度权重打分，输出排序表和关键差异点。
11. Taxonomy 转译（可选）。若候选项来自外部体系，按 `references/taxonomy-translation.md` 转译为项目内部分类。
12. 输出阶段产物：
    - Candidate Backlog（完整表格）
    - Candidate Summary（Top candidates + 理由 + 风险，标注为决策输入）
    - Cross-Session Handoff（按 `references/cross-session-handoff.md` 格式，供后续会话或 `decision-research` 继续）
13. 判断 Post-Research Exit。按 `references/post-research-exits.md` 推荐下一步出口（PRD Input / Starter Scenes / Demo Beachhead / Eval 等），不强制执行。

## L5 Automation Handling

`L5` 表示长期雷达，不等于默认创建自动化。只有用户明确要求创建、开启、设置、定期运行或持续自动更新时，才进入 automation 流程。创建前读取 `references/research-radar-loop-contract.md`，并说明频率、写入范围、禁止动作和人工确认点。

## Research Run Plan

开始研究前输出：

```markdown
**Research Run Plan**
- Topic: <研究主题>
- User goal: <用户要学会、判断或沉淀什么>
- Framed from raw intent: <yes/no; if yes, summarize interpreted research goal>
- Research mode: <Normal Research / Lightweight Concept Lens / Learning Pack / Application / Radar / Product Candidate>
- User context: <role, domain, technical_depth, goal_type, output_preference, application_context, decision_need>
- Recommended depth: <L1 / L2 / L3 / L4 / L5, with reason>
- Topic type: <平台能力 / 开源工程 / 产品竞品 / 学术方法 / 政策合规 / 市场趋势 / 其他>
- Core questions: <按理解型 / 判断型 / 设计型 / 实践型 / 复盘型组织>
- Output requirements: <读者 / 产物 / 必须支持的下一步 / 不做什么>
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

默认不是“所有渠道全开”，而是按主题选择渠道。读取 `references/channel-selection-rubric.md` 和 `references/channel-registry.md`；封闭、付费、登录或私密渠道只在用户授权并说明引用限制后使用。

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
- Research mode: <Normal / Lightweight Concept Lens / Learning Pack / Application / Radar / Product Candidate>
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

### Product Candidate Research 输出格式

当使用 Product Candidate Research 模式时，额外输出：

```markdown
**Product Candidate Result**
- Decision question: <用户要做什么决策>
- Candidate count: <候选池总数 / 通过 Quality Gate 数>
- Top candidates: <Top 3 候选 + 一句话理由，作为决策输入而非最终推荐>
- Key differentiators: <候选间核心差异点>
- Scoring dimensions: <使用的评分维度和权重>
- Confidence level: <High / Medium / Low + 原因>
- Handoff file: <跨会话 handoff 文件路径，或 chat-only>
- Recommended exit: <decision-research / PRD Input / Starter Scenes / Demo Beachhead / Eval / Registry / Review / Roadmap / none>
- Open questions for next session: <仍需下一轮研究验证的问题>
```

## Definition of Done

任务完成必须满足至少一种情况：

- `L1` 快查：给出直接答案、来源和证据局限。
- `Lightweight Concept Lens`：给出概念源流、语义演化、范式阶段、PM 决策问题、反模式或概念债务判断；如果生成 HTML，静态验证已通过或明确说明限制。
- `L2`：给出主题地图、核心概念、基础案例、来源和下一步阅读。
- `L3`：Research Project 或聊天报告已覆盖问题清单、证据矩阵、阶段结论和第一阅读入口式 `05_研究报告`，能帮助陌生领域入门。
- `L4`：额外形成外部渠道研究、行业案例对照、最佳实践或应用模板，能指导方案设计、选型、商业化、企业 adoption、workflow 设计或 PRD 输入；若是高门槛应用研究，还应给出迁移判断、矩阵、风险和分阶段路径。
- `L5`：形成 watchlist、更新日志、稳定/候选/待验证/废弃结论分层和后续自动化建议；若用户明确确认创建 automation，则调用 Codex `cron` automation，并保留低风险写入边界与人工确认点。
- Product Candidate Research：候选池通过 Quality Gate（至少 3 个候选项有完整 schema 填充）、评分表输出、Candidate Summary 包含 Top candidates 和风险、Cross-Session Handoff 文件可被后续会话或 `decision-research` 直接消费。
- Persona-adaptive 输出：关键结论已说明对当前用户画像、业务目标或应用场景的影响。
- Application 输出：至少给出一个可执行动作、模板、实践任务或判断框架，除非用户只要求快查；当研究是高门槛应用研究时，还要包含决策上下文、证据覆盖、迁移判断、判断矩阵、分阶段建议、风险与待验证假设。
- 如果渠道受限，必须说明未使用的渠道、限制原因和对结论可信度的影响。

## Resource Guide

- `references/mode-selection.md`：主模式选择、相邻 Skill 边界和最小加载规则。
- `references/research-depth-rubric.md`：判断 `L1-L5` 深度、样本量和确认门禁。
- `references/research-goal-framing-gate.md`：把用户大白话、模糊方向或 Roadmap 前置想法转成研究目标、研究问题、输出要求和 out-of-scope。
- `references/applied-business-research-contract.md`：高门槛应用研究、商业化/企业 adoption/workflow 决策的证据覆盖、迁移判断和决策产物要求。
- `references/research-radar-loop-contract.md`：Research Radar Loop 的状态文件、信号分类、更新规则、暂停条件和升级规则。
- `references/mode-routing-guide.md`：Research Modes 的触发细则、Concept Lens、Learning Pack、Application 和 Product Candidate 规则。
- `references/user-context-standards.md`：解析用户画像和 persona-adaptive 输出边界。
- `references/default-user-profile.md`：本地默认用户画像；仅作为默认配置，不写死主逻辑。
- `evals/evals.json`：结构化 trigger / non-trigger / routing 回归样例。
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
- `references/product-decision-mode.md`：产品候选研究模式、评分维度、候选池默认输出；最终推荐转 `decision-research`。
- `references/project-context-intake.md`：项目上下文读取规范、必填字段和输出分层。
- `references/taxonomy-translation.md`：外部模式→内部分类转译规则和市场分类模板。
- `references/candidate-backlog-schema.md`：候选池 17 字段 schema、Quality Gate 5 项检查和评分规则。
- `references/cross-session-handoff.md`：跨会话 handoff 模板、合并规则和 Research Run Metadata。
- `references/post-research-exits.md`：研究到 PRD/Starter/Demo/Eval/Registry/Review/Roadmap 7 种出口。
