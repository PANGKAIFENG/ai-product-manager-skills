# Research Topic Compiler 迭代研究循环 PRD v0.1

## 0. 文档信息

| 字段 | 内容 |
| --- | --- |
| 功能名 | Evidence-Driven Iterative Research Loop |
| 需求类型 | PRD-ai-native |
| 当前状态 | 已确认，可进入 Skill 实现与评测 |
| 关联模块 | `research-topic-compiler` |
| 更新时间 | 2026-07-12 |

本期只解决一件事：把 `research-topic-compiler` 从渠道驱动的一次性研究流程，升级为围绕证据缺口循环运行、能解释框架如何变化并能证明为何停止的研究 Skill。

本 PRD 描述的是 Skill 行为和状态，不包含用户界面，因此不产出页面 ASCII、HTML mockup 或截图；用研究状态机和逻辑对象图代替页面结构。

## 1. 背景与问题

现有 Skill 已具备研究深度、渠道选择、来源评级、Obsidian 输出、安全边界和 L1/L2 降级能力，但主流程仍是：

```text
定义目标 → 选模式/深度 → 选渠道 → 可选扩源
→ 内部扫描 → 外部发现 → 证据矩阵 → 报告
```

这套流程可以回答“看了哪些资料”，但不能稳定回答：

- 为什么下一步要查这个来源，而不是另一个来源？
- 一篇转述文章如何回溯到真正原文？
- 为什么从 Anthropic 扩展到 OpenAI 或其他主体？
- 为什么选择这些开源项目，它们分别验证什么？
- 新证据如何改变最初的研究框架？
- 什么时候已经足够支持用户目标，可以停止继续搜索？

### 1.1 旧版行为基线（RED）

同一测试输入要求从一篇转述 Anthropic Skill 实践的公众号文章，研究 Agent Skill 最佳实践。旧版输出表现为：

- 正确把公众号文章作为线索，并计划追溯 Anthropic 原文。
- 正确扩展 OpenAI、开源项目和其他框架。
- 但没有显式 `Framework V0`、Gap Ledger、Next Best Evidence 和 Framework Change Event。
- 开源项目检索以“高星仓库”为入口，缺少证据角色和独立性抽样。
- 停止条件主要是来源数量、问题覆盖数量、最佳实践条数和 `00-08` 文件完成度。
- L1 快查在用户已提供足够官方材料时能正确跳过扩源，此能力必须保留。

结论：问题不在“是否知道官方来源更强”，而在缺少统一的证据驱动研究控制面。

## 2. 模块定位

v0.1 只正式接入 Normal Research 和 Application，并为 L1/L2 提供轻量降级路径。Learning Pack、Product Candidate 和 Radar 本期只保证原有路由与产物兼容，不改造其 mode-specific 流程；后续版本可在独立回归覆盖后接入同一控制层。

输入：用户目标、Seed Corpus、已有结论、访问边界和研究预算。

输出：可追溯的当前框架、Claim/Evidence 关系、研究队列、框架变化、停止理由、残余风险和面向用户的研究报告。

下游：Obsidian Research Project、产品方案、PRD、Eval、候选池或 `decision-research`。

## 3. 用户场景

### 3.1 目标用户

- AI 产品经理：需要从碎片材料形成可用于产品优化的稳定判断。
- Skill/Agent 维护者：需要把官方规范、实现和失败案例转成可验证最佳实践。
- 技术负责人：需要理解结论的来源、边界和工程验证程度。
- 快查用户：只想基于已有权威材料得到轻量答案，不希望被迫进入重型研究。

### 3.2 核心场景

1. 用户提供一篇转述 Anthropic 的文章，AI 将其作为 Seed Corpus，抽取 Claim、回溯原始来源、扩展同类权威主体和实现证据，最终修订框架并停止。
2. 新官方证据推翻 Framework V0，AI 保留历史并用 `Challenge` / `Invalidate` / `Split` 显式修订，而不是静默覆盖或强行调和。
3. 用户已提供足够的官方资料并要求 L1/L2 快答，AI 在最小循环内完成，不扩源、不建重型状态文件。

## 4. 目标、成功标准与非目标

### 4.1 功能目标

- Seed Corpus 是研究线索和初始假设来源，不是默认权威证据。
- 每轮研究围绕最高价值未知问题选择下一最佳证据动作。
- 来源回溯、同行扩展、实现验证和反例搜索均可解释。
- 每条关键新证据都能追踪其对 Claim 和 Framework 的影响。
- 停止依据是信息饱和或已满足当前目的，不是搜索渠道或样本数耗尽。
- L1-L5 使用同一逻辑，但按风险和任务深度裁剪状态与持久化。

### 4.2 发布成功标准

- 核心回归、框架推翻、伪官方降级、饱和停止全部通过。
- 原有 5 条 trigger/routing 回归全部保持。
- L1/L2 边界用例不被升级成完整研究工程。
- 独立 holdout 能迁移同一方法，不依赖 Anthropic/Skill 示例词汇。
- 主 `SKILL.md` 保持为触发与主控制面，细节通过 progressive disclosure 下沉到 reference。

### 4.3 非目标

- 不构建搜索引擎、爬虫、RSS 平台或来源数据库。
- 不保证穷尽全网或绝对完整。
- 不绕过登录、付费墙、验证码、反爬、API 限制或私密访问边界。
- 不替代 `decision-research` 做最终方案选择。
- 不强制 L1/L2 创建 Obsidian 项目或完整状态文件。
- 不重构 Concept Lens、Product Candidate 或 Radar 的独立业务产物。

## 5. 目标研究状态机

```text
FRAME
  ↓
IDENTIFY GAP
  ↓
PLAN NEXT BEST EVIDENCE
  ↓
ACQUIRE
  ↓
EVALUATE
  ↓
UPDATE FRAMEWORK
  ↓
CHECK SATURATION
  ├─ Continue ─────────────→ IDENTIFY GAP
  ├─ Stop ─────────────────→ SYNTHESIZE
  ├─ Pause ────────────────→ CHECKPOINT
  └─ Escalate ─────────────→ USER / L4 / L5 / decision-research
```

| 状态 | AI 动作 | 用户可见或可恢复结果 | 退出条件 |
| --- | --- | --- | --- |
| FRAME | 将目标和 Seed Claims 转成可修订的 Framework V0 | 研究问题、Must/Should/Could Claim、证据标准 | 知道要回答什么和什么最重要 |
| IDENTIFY GAP | 找出未知、冲突、缺失来源和泛化风险 | Ranked Gap Ledger | 每个重要 Claim 已满足或有 Gap |
| PLAN NBE | 选择降低当前不确定性最大的下一动作 | NBE Action + 选择理由 | 一个可执行动作就绪 |
| ACQUIRE | 获取原文、同主体、同类主体、实现或反例 | Source + Source Graph 边 | 获取成功或明确 blocked |
| EVALUATE | 提取 Evidence，判断支持、挑战或仅作背景 | Evidence → Claim 关系与质量 | Evidence 可定位且完成质量判断 |
| UPDATE | 更新 Claim 和 Framework 版本 | Framework Change Event | before/after/evidence/rationale 已记录 |
| SATURATION | 判断继续的边际价值 | Continue/Stop/Pause/Escalate | 四选一，不允许模糊结束 |

## 6. 核心对象与产品规则

这些是逻辑状态，不等于每次运行必须创建同名文件。v0.1 的 Core 对象是 Framework Node、Claim、Gap、NBE Action、Source/Evidence、Change Event 和 Saturation Check；Run 与 Checkpoint 是运行辅助对象。完整字段只在 L4 或跨会话恢复时启用。

| 对象 | 最小字段 |
| --- | --- |
| Run | goal, mode, depth, scope, evidence contract, effort budget, authorization, framework version, status |
| Framework Node | question, importance, claim IDs, current status |
| Claim | statement, type, decision impact, required evidence, status, confidence, evidence IDs, open gaps |
| Gap | type, why it matters, closure criterion, priority, status |
| NBE Action | target Gap, action type, target, expected information gain, source role, independence target, cost/access risk, selection reason |
| Source | owner, URL/path, source type, primary/secondary, evidence level, lineage root, access status |
| Evidence | source ID, claim ID, locator/excerpt, support/challenge/context, directness, freshness, independence group, limitations |
| Change Event | from/to version, type, affected nodes/claims, evidence, before, after, rationale |
| Saturation Check | Must gaps, contradictions, marginal yield, counterexample status, budget, decision, stop reason, residual risk |
| Checkpoint | last completed state, current Gap, ranked queue, completed/blocked actions, next exact action, artifact paths |

关系必须明确：

```text
Source ─extracts→ Evidence ─supports/challenges→ Claim ─belongs_to→ Framework Node
```

转载、转述和摘要若来自同一原始来源，必须共享 lineage root，不能重复计算为多个独立证据。

## 7. 人工与 AI 交互逻辑

- 用户提供研究目标、Seed Corpus、时间/成本约束和访问授权。
- AI 内部维护与深度匹配的最小研究状态；L1 不向用户展示 Ledger、Change Event、Source Graph 等控制面术语。
- AI 每轮只执行一个 Next Best Evidence Action；若跳过排名最高的 Gap，必须说明访问、成本、范围或授权原因。
- AI 在范围扩大、访问受限、预算耗尽或目标转为最终选型时暂停、升级深度或 handoff，不把这些动作混成一种 Escalate。
- 用户可修改研究范围、证据标准和预算；AI 保留修改前后的 Framework 版本。

### 7.1 双轨协作定义

| 阶段 | 人工动作 | AI 动作 | 系统反馈 | 边界 |
| --- | --- | --- | --- | --- |
| 启动 | 提供目标、Seed、预算和授权 | 形成 brief、Framework V0 与证据标准 | 显示研究范围、深度、关键假设和待确认项 | L1/L2 范围清楚时可压缩为内部判断 |
| 研究 | 调整范围或补充材料 | 逐轮选择一个 NBE，获取并评估证据 | 更新当前 Gap、Framework 版本和阻塞原因 | 未授权来源不得读取；不得机械扩源 |
| 变更 | 对高影响冲突或范围扩大做判断 | 记录 Change Event，必要时暂停或升级 | 显示 before/after、证据、理由与影响 | AI 不静默覆盖旧结论，不代替用户做高风险决策 |
| 结束 | 接受结果、补授权或转下游决策 | 执行 Saturation Check 并输出唯一终态 | 显示停止理由、残余 Gap、风险和下一动作 | 最终选型转 `decision-research`；持续监控需用户明确授权 |

### 7.2 状态反馈

| 状态 | 用户应看到的信息 | 可执行下一步 |
| --- | --- | --- |
| `running` | 当前 Framework 版本、最高优先级 Gap、本轮 NBE 和选择理由 | 继续、调整范围或预算 |
| `blocked-authorization` | 所需授权、证据价值、无公开替代的原因 | 授权或结束本轮 |
| `partial-access` / `partial-budget` | 未关闭的 Must Gap、对结论的影响和已尝试替代方案 | 补访问/预算或接受部分结果 |
| `escalated` | 升级原因、handoff 对象和已保留状态 | 进入人工判断或 `decision-research` |
| `complete-saturated` / `complete-fit-for-purpose` | 唯一终态、停止理由、证据边界、残余风险和未解决问题 | 使用研究结果进入学习、产品或决策流程 |

L1/L2 的状态反馈保持自然语言和紧凑输出，不展示内部枚举或完整 Ledger；L3+、暂停、交接和审计场景才显示完整状态。

## 8. 功能需求

| ID | 需求 | 验收标准 |
| --- | --- | --- |
| FR-01 | Seed Corpus Intake | 提取 Seed Claims、来源主体、疑似原始出处和证据角色；二手转述不得直接形成最高等级核心结论 |
| FR-02 | Framework V0 | 重要研究问题具有初始假设、重要性、证据标准、状态和置信度 |
| FR-03 | Gap Ledger | 每轮明确未知、冲突、缺失证据、关闭条件和优先级 |
| FR-04 | Next Best Evidence | 下一动作说明目标 Gap、预期信息增益、来源角色、独立性、成本/访问风险和选择理由；排序默认遵循 Must > Should > Could、原始来源追溯优先、高决策影响与高不确定性优先 |
| FR-05 | Source Graph | 支持 `derived_from`、`cites`、`same_publisher_as`、`implementation_of`、`fork_of`、`responds_to` |
| FR-06 | 权威主体扩展 | 仅在 Claim 需要跨平台泛化时扩展同类主体，并说明比较维度；不按品牌知名度机械列举 |
| FR-07 | 开源项目抽样 | 项目标注 Canonical/Independent/Production/Contrast/Counterexample 角色、Gap、可观察材料、独立性和局限；Stars 不得作为主要理由 |
| FR-08 | Framework Update | 使用 `Fill / Refine / Split / Merge / Challenge / Invalidate / Expand / No change`；保留 before/after/evidence/rationale |
| FR-09 | Saturation Gate | 同时检查 Must Claim、来源回溯、独立验证/反例、关键矛盾、边际信息增益、预算和残余风险 |
| FR-10 | 分级运行 | L1/L2 内联轻量状态；L3+ 或用户要求保存/续跑时才持久化完整状态 |
| FR-11 | Checkpoint/Resume | 下一会话能恢复 Framework 版本、当前 Gap、队列、阻塞项和下一动作；恢复时按来源身份去重 |
| FR-12 | Evidence-based Merge | 新结论不能仅因时间更晚自动覆盖旧结论；必须显式 supersedes 或由更强、更直接、更新且独立的 Evidence 支持 |

## 9. 深度分级

| 深度 | 循环与持久化 |
| --- | --- |
| L1 | 内部执行一次 ephemeral 压缩循环，只处理一个核心 Claim/Gap；通常一个充分权威来源即可；不建文件、不强制扩源、不向用户输出控制面术语 |
| L2 | 3-5 个框架节点，最多两个 NBE acquisition action；默认无文件、无完整图谱；最终只输出紧凑结论、来源和未解决问题，出现重要冲突再建议升级 |
| L3 | 使用现有 `00-05`；所有 Must Claim 有状态；核心二手 Claim 至少尝试一次原始来源追溯 |
| L4 | 完整 Claim/Evidence/Source Graph；覆盖权威定义、实现、独立验证和反例；保留 Change Log 并正式执行饱和门禁 |
| L5 | 首轮建立 L4 基线，后续只做 delta；记录 No change；连续低增益后暂停；自动化仍需用户明确授权 |

深度控制研究风险和状态完整度。样本量只作为预算参考，不能作为完成定义。

## 10. 信息饱和与停止

`complete-*` 终态必须满足：

- 所有 Must Claim 达到预设证据标准，或明确降级为无法验证。
- 原始来源已追溯，或已披露无法追溯导致的可信度损失。
- L4 的重要泛化 Claim 已做独立验证和反例搜索。
- 没有未处理的关键矛盾。
- 剩余 Gap 不阻碍用户下一步。
- `complete-saturated` 还要求 L4 最近两个不同来源血缘的高质量动作只产生 `Fill` / `No change`，且未产生新的 Must Gap。

终态按下表自上而下判定，命中后停止，不允许同时返回多个状态：

| 优先级 | 终态 | 唯一判定 | 是否完成 |
| --- | --- | --- | --- |
| 1 | `blocked-authorization` | 下一必要动作需要用户授权，且没有公开替代 NBE | 否 |
| 2 | `partial-access` | 必要证据不可访问，替代来源不足，仍存在受影响 Must Gap | 否 |
| 3 | `partial-budget` | 时间/成本预算耗尽，仍存在 Must Gap；必须披露对结论的影响 | 否 |
| 4 | `escalated` | 目标转为最终决策、范围显著扩大或需要高风险人工判断 | 否，已 handoff |
| 5 | `complete-saturated` | 已 fit-for-purpose，且 L4 满足连续两个独立血缘低增益、无新 Must Gap | 是 |
| 6 | `complete-fit-for-purpose` | 所有 Must Claim 达到当前用户目标所需标准，无阻断矛盾；允许不影响下一步的 Should/Could Gap | 是 |

不得使用“来源数达到 N”“文件写完”“候选池读完”作为单独停止理由。

## 11. 状态持久化映射

| 现有 Research Project 文件 | 新逻辑状态 |
| --- | --- |
| `00_研究定义.md` | Run、Framework V0、Evidence Contract、预算与授权 |
| `01_问题清单.md` | Framework Map、Claim Ledger、Gap Ledger |
| `02_证据与卡片.md` | Source Ledger、Evidence Ledger、Source Graph |
| `03_阶段结论.md` | 当前结论、Assumption Ledger、Framework Change Log |
| `04_下一步.md` | Ranked NBE Queue、阻塞项、继续/停止判断 |
| `05_研究报告.md` | 综合结论、停止理由、残余风险 |
| `09_更新日志.md` | L5 delta、No change 和 cycle checkpoint |

历史 Research Project 不强制迁移；后续更新时按需增量补字段。

## 12. 人工接管、异常与安全边界

- 新范围显著超出原 brief：暂停并确认范围。
- 需要登录、付费、私密、敏感来源：记录 Gap 和访问价值，获得当前 run 明确授权前不得继续。
- 找不到所谓“官方原文”：不得根据标题升级为官方证据，标记 `unverified origin`。
- 矛盾证据：Claim 转为 contested 并生成验证 Gap，不视为执行失败。
- 网络/工具瞬时错误：最多一次合理重试，然后记录 blocked 并选择替代 NBE。
- Evidence 无可定位片段：不得进入稳定结论。
- 用户要求最终选一个：执行 `Handoff decision-research`。
- 用户要求持续监控：才进入 L5 Radar；不默认创建 automation。
- 权威冲突或决策风险超出当前深度：执行 `Upgrade depth`，说明升级理由和新增预算。
- 需要授权：执行 `Pause for authorization`，不把它记录为普通研究失败。

## 13. 评测与发布门禁

### 13.1 核心回归

```text
公众号转述 Anthropic Skill 实践
→ 标记为 Seed/Secondary
→ 抽取 Claims 并形成 Framework V0
→ 追溯 Anthropic 原文
→ 针对 Gap 扩展 OpenAI/其他同类主体
→ 按证据角色选择开源项目
→ 记录至少一个 Framework Change Event
→ 输出停止理由、状态和未解决问题
```

### 13.2 可重复评测契约

版本比较使用冻结的离线 source pack，不依赖实时搜索结果：

- Seed：一篇转述 Anthropic Agent Skill 实践的二手文章。
- Primary：与 Seed Claims 对应的 Anthropic 官方摘录和稳定 URL。
- Peer authority：OpenAI/其他同类主体的官方摘录，用于验证平台通用 Claim。
- Implementation candidates：包含 Canonical、Independent、Contrast/Counterexample 候选及其 README/Issue/Release 摘录。
- Fake official：标题声称“Google 官方”但无官方原文或可验证作者身份的材料。
- Saturation pack：后续多个来源与同一 lineage 重复已有 Claim。

同一 source pack、模型、提示和 grader 用于 old/new 对比。联网 smoke 只验证真实来源可访问性与追溯动作，不参与确定性版本胜负。

### 13.3 评测矩阵

| 类型 | 用例 | 必须行为 |
| --- | --- | --- |
| Regression | 核心回归 | 来源回溯、NBE、角色化抽样、框架变化、停止理由全部出现 |
| Regression | 框架推翻 | 使用 Challenge/Invalidate/Split，不能静默覆盖或强行调和 |
| Regression | 伪 Google 官方 | 降级为待验证/弱证据，不形成核心结论 |
| Regression | 饱和停止 | 重复来源连续低增益后停止，不机械读完候选池 |
| Negative | L1 快答 | 不输出完整状态工程，不扩源、不写文件 |
| Negative | 权威材料充分 | 没有影响结论的关键 Gap 时不外部搜索 |
| Transfer | MCP 安全 | 同样围绕 Gap 选择规范、实现、独立验证和反例 |
| Holdout | 独立技术规范与互操作问题 | 冻结实现后揭示，验证方法可迁移而非记忆 Agent Skill 示例 |
| Compatibility | 原 5 条 routing eval | 全部保持 |

### 13.4 评审方式与阈值

- 确定性检查：字段、source pack 中的 canonical URL/path/repo identity、框架变更结构、终态结构、L1/L2 重型产物边界。真实性、血缘和独立性判断仍需语义评审。
- 模型/人工评审：Gap 对齐、NBE 是否真能降低高价值不确定性；来源血缘是否合理；横向主体和开源项目是否选得合理；框架变化是否实质；终态是否符合判定表。
- 新旧版本必须使用同一模型、同一输入和同一 grader 对照。
- 本期按 L2 Skill 变更门禁：旧版基线、回归、迁移、负例、独立 holdout、确定性检查和人工/模型评审。
- 发布阈值：核心回归、框架推翻和伪官方用例关键断言 100% 通过；原 5 条 routing 与 L1/L2 negative 100% 通过；transfer/独立 holdout 的语义评分不低于 80/100。

## 14. 实现范围

### 14.1 必改

- `research-topic-compiler/SKILL.md`：增加 Normal/Application 共用循环、深度裁剪和停止门禁摘要，替换这两条路径的线性 Workflow 控制逻辑。
- 新增 `references/iterative-research-loop.md`：承载完整状态模型、NBE、Source Graph、变更分类、停止和恢复规则。
- `pre-research-source-expansion.md`：从一次性前置阶段改为 ACQUIRE 的候选发现策略。
- `channel-selection-rubric.md`：由主题到渠道映射升级为 Gap 驱动的动态选择，并增加开源抽样规则。
- `source-quality-rules.md`：补 Source/Evidence/Claim、来源血缘、独立性和伪官方降级。
- `research-depth-rubric.md`：补 L1-L5 循环裁剪和停止门槛。
- `obsidian-output-contract.md`、`cross-session-handoff.md`：补状态映射、checkpoint 和证据驱动合并；`research-radar-loop-contract.md` 只声明兼容边界，不在 v0.1 改造为通用循环。
- `evals/evals.json`：保留原路由用例并增加行为回归、负例和迁移用例。

### 14.2 不改

- 不改变 Skill 名称和目录名。
- 不改变与 `decision-research`、`competitive-analysis` 的公开路由边界。
- 不改无关 Skill 和根目录 catalog，除非确定性检查证明引用发现性需要修复。
- 不改变 Learning Pack、Product Candidate、Radar 的 mode-specific 主流程；只验证路由兼容。

### 14.3 实现顺序与文件所有权

1. Eval Agent：冻结行为用例、grader 和离线 source pack，不修改 `SKILL.md`。
2. Core Agent：修改 `SKILL.md`、新增 loop reference，并更新 depth/Obsidian/handoff 适配。
3. Evidence Agent：修改 expansion、channel selection 和 source quality references。
4. 总控串行整合，处理 cross-file 术语、运行回归、holdout 和最终 CR。

任意时刻只有一个 Agent 修改 `SKILL.md` 或 `evals.json`。

## 15. 风险与控制

| 风险 | 控制 |
| --- | --- |
| 研究循环失控 | 深度预算、单次 NBE、饱和门禁、Pause/Escalate |
| 状态文件膨胀 | 逻辑对象映射现有 `00-05`，L1/L2 内联 |
| 上下文与 Token 增长 | 主文件只留控制面，完整字段与模板下沉 reference |
| 框架频繁漂移 | 所有变化保留 before/after/evidence/rationale |
| 同源材料被当独立证据 | lineage root 与 independence group 去重 |
| 来源选择变成品牌清单 | 每个主体和项目必须绑定 Gap、证据角色和选择理由 |
| 旧能力回归 | 保留原 5 条路由评测和 L1 负例 |

## 16. 待确认事项

当前无阻断实现的待确认项。v0.1 已确定：只接入 Normal/Application；离线 source pack 用于版本比较；终态按第 10 节优先级唯一判定。

## 17. Improvement Record

- Observed failure：旧版会追溯来源，但按渠道和数量推进；没有统一 Framework/Gap/NBE/Change/Saturation 控制面。
- User-visible impact：研究看似丰富，却无法说明为何查、如何变、为何停，难以复盘和复用。
- Evidence：旧版核心行为基线、现有 `SKILL.md` Workflow、扩源/深度/source-quality references、现有 5 条 routing eval。
- Responsible layer：Skill instruction + research state contract + behavior eval。
- General principle：复杂研究应围绕当前最高价值未知问题迭代，并用证据显式修订框架。
- Best Practice Delta：execution reliability、resources/context、evaluation loop。
- Deterministic checks：状态结构、来源身份、Change Event、Saturation、负例产物边界。
- Human-review criteria：NBE 价值、来源选择逻辑、实质框架变化、停止充分性。
- Regression eval：Anthropic Seed 主用例、框架推翻、伪官方、饱和停止。
- Transfer eval：MCP 安全。
- Negative eval：L1/L2、权威资料充分。
- Independent holdout：独立技术规范与互操作问题，冻结实现后揭示具体主题。
- Trace/time/token evidence：发布前记录同模型的新旧输出长度、耗时和用例结果；联网能力单独 smoke，不混入确定性版本比较。
- Release decision：通过本 PRD 第 13 节后 release，否则 experiment 或 block。
- Research/meta-skill feedback：将“已有资料是 Seed，不是结论；框架需随证据版本化；完成是 fit-for-purpose saturation”反馈到后续通用 Skill 创建/评审实践。
