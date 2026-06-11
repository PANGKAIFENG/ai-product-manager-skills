# Skill Boundary and Loop Pattern Audit

> Snapshot note: 本审计草稿记录的是实施前的边界判断，深审范围为 6 个核心 AI PM Skill；后续实施已将 public Skill surface 统一扩展到 8 个，并补齐 `ui-mockup-desktop-workbench` 与 `ai-work-assetization-diagnoser` 的 catalog / routing 边界。

## 1. Executive Summary

- 当前仓库本质上仍是一个 flat Skill Library：真实 Skill 目录位于仓库根目录，`README.md` 负责人类入口，`SKILL_REGISTRY.md` 负责 catalog/status，`SKILL_ROUTING.md` 负责相邻 Skill 分流。
- 仓库已经出现 Loop Extension 雏形：`decision-research`、`research-topic-compiler`、`prd-review` 分别内置了 Decision Research Loop、Research Radar Loop、PRD Readiness Loop contract。
- 但 Loop 仍被埋在各父 Skill 的 `references/` 中，尚未形成第一层可发现的 `loop-patterns/` 目录，也没有统一的 Loop State、Gate、handoff 约定。
- 本次深审覆盖 6 个 Public Skills：`ai-collaboration-calibration`、`research-topic-compiler`、`decision-research`、`prd-architect`、`prd-review`、`grill-me`。
- 审计时 public surface 已显示 7 个 Skill：`ui-mockup-desktop-workbench` 已出现在 `README.md`、`SKILL_REGISTRY.md`、`SKILL_ROUTING.md` 和根目录中；它超出本轮深审范围，应单独审查。实施后 public surface 已统一为 8 个 Skill。
- 最大 P0/P1 边界风险是 `research-topic-compiler` 的 `Product Candidate Research` 分支与独立 `decision-research` 重叠：二者都能做候选池、评分、推荐、handoff。
- `ai-collaboration-calibration` 与 `grill-me` 的高层边界基本成立：前者挑战问题定义，后者挑战已有方案；但 calibration 内部的 failure-premortem / asset-capture 模式需要加护栏，避免吞掉成熟方案压测职责。
- `prd-architect` 与 `prd-review` 边界基本清楚：前者生成 PRD，后者审查 PRD；但 `prd-review` 的修订草案输出应明确限制为最小 patch draft，不应变成完整 PRD 重写。
- 当前缺少 Router / Gate 层，用于判断任务应沉淀为 Prompt、Context Pack、Workflow、Skill、Loop 还是 System。建议新增 public-safe 版本的 `ai-work-assetization-diagnoser` 或等价 router 文档。
- 旧研究 Skill 命名未在本轮 targeted search 中发现；当前命名主要围绕 `decision-research`，但研究类内部模式命名仍需收敛。

## 2. Current Repository Model

当前仓库实际模型是：

```text
Flat Skill Library
  -> root-level public Skill folders
  -> README as human workflow entry
  -> SKILL_REGISTRY as catalog/status boundary
  -> SKILL_ROUTING as adjacent-Skill disambiguation
  -> examples/ as copyable prompt surface
  -> embedded Loop Extension contracts under parent Skill references/
```

这说明仓库已经从单个 Skill 集合进化到“带路由规则的 AI PM workflow library”，但还没有完全建立 Loop Pattern Layer。

现有 Loop 设计是“父 Skill 内的状态化扩展”：

- `decision-research/references/decision-loop-contract.md`
- `research-topic-compiler/references/research-radar-loop-contract.md`
- `prd-review/references/prd-readiness-loop-contract.md`

这种设计适合早期保持根目录简洁，但会带来三个问题：

- 跨 Skill Loop 不易被发现：例如 PRD Readiness Loop 实际需要 calibration、grill、architect、review 协作，但 contract 放在 `prd-review` 内。
- Loop State 不统一：Decision、Radar、PRD 各自定义 state files，没有共享的状态命名、resume、human gate、stop condition 规范。
- Router 缺位：当前只能从用户当前阶段路由到单个 Skill，不能先判断“这件事是否应该 Loop 化、是否值得资产化”。

本轮还观察到 public surface drift：根文档和 registry 已经把 `ui-mockup-desktop-workbench` 纳入公开 Skill，使 public count 从 6 变成 7；本报告按用户要求只深审 6 个原始 AI PM Skills，并把该新增 Skill 作为待审查 surface drift 记录。后续实施已补上 `ai-work-assetization-diagnoser`，当前发布口径为 8 个 public Skill。

## 3. Role Model

| Role | 定义 | 适合的输出 | 不适合的输出 |
|---|---|---|---|
| Framer | 定义问题、挑战前提、澄清目标、边界和判断标准 | 真实问题陈述、成功标准、约束、非目标、下一步入口 | 成熟方案、最终 PRD、完整调研结论 |
| Researcher | 围绕主题、决策、技术、行业或方案收集证据并形成判断 | Research Map、证据矩阵、有立场推荐、研究报告 | 没有证据的主观方案、无限资料堆砌 |
| Maker | 生成结构化交付物 | PRD、模板、流程图、handoff、修订草案 | 高风险方向拍板、脱离输入事实的终稿 |
| Critic | 对已有方案做压力测试，暴露失败模式和隐藏假设 | 决策记录、失败模式、被否掉选项、待确认问题 | 从零生成方案、标准化交付物验收 |
| Reviewer | 基于明确标准审查已有交付物是否可交付、可开发、可测试 | findings、blockers、readiness verdict、patch draft | 从零创作、开放式脑暴、方案层拷问 |
| Router / Gate | 判断任务应进入哪个 Skill、Loop Pattern 或资产化层级 | 路由决策、资产化建议、进入/退出条件 | 替代具体 Skill 执行主体工作 |

## 4. Skill-by-Skill Audit

### Overview Matrix

| Skill | 当前主角色 | 次角色 | 应调用场景 | 不应调用场景 | Loop 中角色 | 边界清晰度 1-5 | 主要问题 | 改造优先级 |
|---|---|---|---|---|---|---:|---|---|
| `ai-collaboration-calibration` | Framer | light Critic / Gate | 问题模糊、方向可能错、进入执行前需澄清问题 | 明确执行、小改、成熟方案专项压测 | Framer Node / Gate Node | 4 | 内部 failure-premortem / asset-capture 可能侵入 `grill-me` 和 Router | P1 |
| `research-topic-compiler` | Researcher | Maker / State Manager | 系统研究、概念源流、长期主题、Research Project、Radar | 明确单次决策、普通即时搜索、Skill 评审 | Research Radar Loop 主体 | 3 | Product Candidate Research 与 `decision-research` 明显重叠 | P0/P1 |
| `decision-research` | Researcher | Framer / Gate | 具体决策、选型、可行性、接入、产品方向推荐 | 长期知识沉淀、问题尚未定义、成熟方案压测 | Decision Research Loop 主体 | 4 | 自身边界清楚，但被 RTC Product Candidate 分支侵入 | P1 |
| `prd-architect` | Maker | Framer | 从想法、脑暴或草稿生成 PRD / 图示 / handoff | 已有完整 PRD 评审、直接编码、单纯 UI mockup | Maker Node | 4 | 有 readiness 判断，但不应承担 reviewer 角色 | P2 |
| `prd-review` | Reviewer | narrow Maker | 已有 PRD/handoff，需要 blockers、修订草案、readiness verdict | 从零写 PRD、纯润色、方案层开放压测 | Reviewer Node / Gate Node | 4 | 修订草案默认必选，需防止变成完整重写 | P1 |
| `grill-me` | Critic | Framer | 已有方案、架构、计划或决策，需要一问一答压力测试 | 从零写方案、标准 PRD review、不希望互动追问 | Critic Node | 4 | 没有明确接入 Loop Pattern 的 state/handoff 契约 | P1 |

### Skill: `ai-collaboration-calibration`

#### 1. 当前定位

该 Skill 用于问题还没定义清楚时，反转 AI 默认执行模式，先挑战假设、剥离解法、澄清真实任务、确认边界和判断标准。它区分 L4-fuzzy 脑暴与 L4-framed 结构化校准，并用 Done Signal 输出问题定义共识。

#### 2. 当前角色判断

主角色：Framer。

次角色：light Critic / Gate。它会挑战假设、识别反模式，也会判断是否退出校准进入执行、研究或方案阶段。

#### 3. 输入边界

应该在以下情况调用：

- 用户只有感受、现象、解法或模糊方向。
- 用户说“先聊一下”“帮我想想”“先别执行，帮我看清问题”。
- 用户直接要求做功能或接平台，但背景复杂，AI 判断可能存在过早执行风险。
- PRD / research / grill 之前，目标、成功标准、非目标还不稳定。

#### 4. 不应调用的情况

不应在以下情况调用：

- 明确翻译、摘要、格式整理、小改动。
- 已有成熟方案，用户明确要压力测试，此时优先 `grill-me`。
- 已有明确具体决策，需要证据收敛，此时优先 `decision-research`。
- 已有 PRD/handoff 要审查，此时优先 `prd-review`。

#### 5. 输出边界

应该输出：

- 真实问题陈述。
- 明确不解决的方向及原因。
- 核心未验证假设。
- 推荐下一步 Skill 或工作阶段。

不应该输出：

- 最终 PRD。
- 完整方案。
- 成熟方案的长篇压力测试报告。
- 未经研究支持的产品方向拍板。

#### 6. 与其他 Skill 的重叠

- 与 `grill-me` 重叠：都挑战用户假设。合理部分是 calibration 挑战“问题是否定义正确”，grill 挑战“已有方案为什么会失败”。风险在 calibration 的 `failure-premortem` 追加模式，容易侵入方案层压测。
- 与 `decision-research` 重叠：R00 framing gate 也会做问题层级判断。合理，因为 decision-research 需要轻量 framing；但若问题仍模糊，应先交回 calibration。
- 与 Router/Gate 重叠：`asset-capture` 暗示资产化判断，但目前不是系统化 Router。

#### 7. 在 Loop Pattern 中的角色

适合作为 Framer Node / Gate Node，不适合作为 Loop 主体。

理由：它的价值是把模糊问题变成可进入下游 Skill 的稳定输入，输出 Done Signal 后应停止或交给 Researcher / Maker / Critic，而不是长时间自循环。

#### 8. 主要问题

- failure-premortem 模式边界不够强，可能和 `grill-me` 冲突。
- asset-capture 模式暗示资产化诊断，但缺少 Prompt / Context Pack / Workflow / Skill / Loop / System 的完整判断模型。
- 没有明确输出“下一步 Skill handoff payload”字段，跨 Loop 时需要人工解释。

#### 9. 改造建议

- 在 `SKILL.md` 中明确：已有成熟方案压测交给 `grill-me`，calibration 只做问题定义阶段的 failure suspicion。
- 把 `asset-capture` 下沉为“建议进入 Router/Gate”，不要在本 Skill 内判断完整资产化层级。
- 为 Loop 前置阶段新增标准输出：`problem_statement`、`non_goals`、`core_assumptions`、`success_criteria`、`recommended_next_skill`。

### Skill: `research-topic-compiler`

#### 1. 当前定位

该 Skill 用于围绕主题进行系统研究、概念源流、行业演进、学习报告、Research Project 和长期 Radar。它已经内置多种模式，包括 Normal Research、Lightweight Concept Lens、Learning Pack、Application、Radar、Product Candidate Research。

#### 2. 当前角色判断

主角色：Researcher。

次角色：Maker / State Manager。它会生成 Research Project、证据矩阵、报告、看板、学习包、更新日志，并在 Radar Mode 中维护长期研究状态。

#### 3. 输入边界

应该在以下情况调用：

- 用户要系统理解一个主题或领域。
- 用户要概念源流、语义演化、行业演进、PM 决策看板。
- 用户要整理到 Obsidian 或建立可持续扩展的 Research Project。
- 用户要长期雷达、持续更新、watchlist、更新日志。

#### 4. 不应调用的情况

不应在以下情况调用：

- 用户面对一个明确选项或路线，需要单次有立场推荐，应优先 `decision-research`。
- 用户只要简单事实查询或单篇摘要。
- 用户要创建或评审 Skill。
- 用户已有方案要拷问，应优先 `grill-me`。

#### 5. 输出边界

应该输出：

- Research Run Plan。
- 证据矩阵、阶段结论、研究报告。
- 概念源流、范式阶段、PM 问题脚本。
- Radar State：watchlist、证据变化、更新日志、阶段结论 diff。
- 若保持 Product Candidate Research，则输出候选池、评分、handoff，但这是当前争议点。

不应该输出：

- 对明确具体决策的单次最终推荐，除非仓库决定把 Product Candidate Research 保留在本 Skill。
- 无限扩张的资料堆砌。
- 未授权写入 Obsidian、automation 或私密渠道读取。

#### 6. 与其他 Skill 的重叠

- 与 `decision-research` 重叠最严重。`research-topic-compiler` 的 Product Candidate Research 可触发“选型、竞品分析、技术方案对比、市场策略验证”，并输出候选池、评分、Top 推荐、handoff；这些与 `decision-research` 的 concrete decision ownership 高度重合。
- 与 `prd-architect` 重叠：post-research exits 可输出 PRD Input。合理，但应停在 PRD 输入材料，不直接生成完整 PRD。
- 与 `ai-collaboration-calibration` 重叠：会解析研究目标，但如果“为什么研究”都不清楚，应转回 calibration。

#### 7. 在 Loop Pattern 中的角色

适合作为 Research Radar Loop 主体和 State Manager。

不适合作为所有研究 Loop 的唯一主体。具体决策收敛应由 `decision-research` 负责；RTC 更适合长期主题认知、证据变化和研究项目维护。

#### 8. 主要问题

- Product Candidate Research 与 `decision-research` 的职责边界冲突，是当前最影响整体路由的 P0/P1 问题。
- Research modes 太多，用户和 agent 容易把“研究为了理解”和“研究为了决策”混在一起。
- Radar Loop contract 已清楚，但被藏在 parent Skill references 中，不像 first-class loop pattern。

#### 9. 改造建议

- P0：明确 Product Candidate Research 的归属。建议把“具体决策推荐、候选排除、最终立场”交给 `decision-research`；RTC 只保留“候选发现、背景研究、长期 radar、PRD input 前材料”。
- 若保留 Product Candidate Research，应在 `SKILL_ROUTING.md` 写清：RTC 只在需要候选池和跨会话知识沉淀时使用，单次选择交给 `decision-research`。
- 将 Research Radar Loop 提升为 `loop-patterns/research-radar-loop.md`，父 Skill 只链接到它。
- 增加 non-trigger eval：`帮我对比 A/B 选一个` 应优先 `decision-research`，除非用户明确要长期候选池或 Research Project。

### Skill: `decision-research`

#### 1. 当前定位

该 Skill 用于围绕具体决策进行决策驱动调研。它先框定研究层级和问题类型，再锚定决策问题、枚举竞争假设、搜索反对证据，最后输出有立场推荐、排除理由、置信度和颠覆条件。

#### 2. 当前角色判断

主角色：Researcher。

次角色：Framer / Gate。R00 Research Framing Gate 会先判断用户给的是问题、现象还是解法，并确认终止条件。

#### 3. 输入边界

应该在以下情况调用：

- 用户要在 A/B/C 中选择。
- 用户问“有没有现成方案”“怎么接入”“技术上可行吗”。
- 用户要产品方向、定位、版本分层、商业判断、竞品判断的有立场结论。
- 同一决策需要多轮证据收敛，并需要 Research Map、Assumption Ledger、Scope Drift。

#### 4. 不应调用的情况

不应在以下情况调用：

- 问题还没定义清楚，应先 `ai-collaboration-calibration`。
- 目标是长期知识沉淀或系统学习，应优先 `research-topic-compiler`。
- 已有方案要压力测试，应优先 `grill-me`。
- 已有 PRD 要审查，应优先 `prd-review`。

#### 5. 输出边界

应该输出：

- Research Map。
- 竞争假设与证据状态。
- 支持证据和反对证据。
- 有立场推荐、置信度、排除理由、颠覆条件。
- 需要 PoC / 用户决策 / 停止的 next gate。

不应该输出：

- 长期 Research Project。
- 完整 PRD。
- 无立场方案矩阵作为最终结论。
- 未标注 Evidence / Inference / Judgment / Open 的关键判断。

#### 6. 与其他 Skill 的重叠

- 与 `research-topic-compiler` Product Candidate Research 重叠：当前最需要处理。
- 与 `ai-collaboration-calibration` 重叠：R00 framing gate 是必要轻量前置，但不是完整问题脑暴。
- 与 `grill-me` 重叠：二者都处理决策。区别应是：decision-research 用外部证据和反证收敛，grill-me 用一问一答挑战方案内部逻辑。

#### 7. 在 Loop Pattern 中的角色

适合作为 Decision Research Loop 主体。

理由：它已经具备 Research Map、竞争假设、反证搜索、Scope Drift、Assumption Ledger、结论版本和停止条件。

#### 8. 主要问题

- 自身设计较完整，但整体路由被 RTC Product Candidate 分支削弱。
- `check_skill.py` 提示它应补充或明确 input/context intake，这说明 deterministic structure 上还有轻微缺口。
- Decision Research Loop contract 没有明确接入 `grill-me` 作为挑战研究设计或阶段结论的 Critic Node。

#### 9. 改造建议

- 明确 `decision-research` 拥有“具体决策最终推荐”。
- 增补 Input / Context Intake 小节，列出 decision owner、deadline、candidate options、constraints、local context、stop condition。
- 在 future `loop-patterns/decision-research-loop.md` 中加入 `grill-me` 作为可选 Critic Node：调研前挑战 Research Map，调研后挑战阶段结论。

### Skill: `prd-architect`

#### 1. 当前定位

该 Skill 用于把产品想法、需求草稿、脑暴结果或功能说明整理为 PRD，并根据需求复杂度选择 PRD-lite、PRD-standard 或 PRD-ai-native。它也承担 PRD 起草阶段的 Draw.io 图示和 handoff 接口设计。

#### 2. 当前角色判断

主角色：Maker。

次角色：Framer。它会判断需求复杂度、文档深度、PRD 类型、当前成熟度和下一步 handoff。

#### 3. 输入边界

应该在以下情况调用：

- 用户要写 PRD、选 PRD 模板、整理需求草稿。
- calibration / research / grill 后已有较稳定输入，需要转成 PRD。
- 需要 PRD 内正式流程图、架构图或 AI 协作链路图。
- 需求仍在成型，但已有足够信息能形成第一版结构。

#### 4. 不应调用的情况

不应在以下情况调用：

- 已有完整 PRD 要审查，应优先 `prd-review`。
- 只是 UI mockup，应优先 UI mockup 相关 Skill。
- 直接编码或写 implementation plan。
- 关键产品方向尚未定义，应先 `ai-collaboration-calibration` 或 `decision-research`。

#### 5. 输出边界

应该输出：

- PRD-lite / standard / AI-native。
- 当前状态：草稿 / 讨论中 / 已确认。
- 事实、假设、边界、不做项。
- UI / handoff / writing-plans 的承接接口。
- 必要 Draw.io 图示及验证状态。

不应该输出：

- 标准化 PRD review findings。
- 对已成稿 PRD 的完整评审报告。
- 开发文件边界、测试步骤、提交计划。

#### 6. 与其他 Skill 的重叠

- 与 `prd-review` 重叠：都会判断是否可进入 writing-plans。合理部分是 architect 在起草时给下一步建议；但 readiness verdict 的权威应属于 reviewer。
- 与 `ai-collaboration-calibration` 重叠：都会澄清目标和边界。若输入仍是 fuzzy，应先 calibration。
- 与 `research-topic-compiler` 重叠：RTC 可能输出 PRD Input，architect 才应生成 PRD。

#### 7. 在 Loop Pattern 中的角色

适合作为 Maker Node，不适合作为 Reviewer Node 或 Loop 主体。

在 PRD Readiness Loop 中，它负责根据 critic/reviewer feedback 修订 PRD，但不应自行宣布 Ready。

#### 8. 主要问题

- 具备 readiness/handoff 判断，容易被误用为 PRD 评审入口。
- Draw.io 生成职责合理，但与 `prd-review` 的图示检查 reference 重复，后续可能造成模板漂移。
- 没有显式定义“接收 grill / review feedback 后如何修订”的 loop input contract。

#### 9. 改造建议

- 在 PRD Loop Pattern 中明确：`prd-architect` 负责 create/revise，`prd-review` 负责 readiness verdict。
- 把 “Ready for writing-plans” 判断留给 `prd-review`；architect 只给 “建议进入 review / handoff / UI / plan”。
- 合并或共享 Draw.io reference，避免 architect/review 双份模板长期分叉。

### Skill: `prd-review`

#### 1. 当前定位

该 Skill 用于审查已有 PRD、handoff、需求文档或产品方案，从 PM、研发、测试视角找缺口、冲突、不可实现点、不可测试点和图示问题，并输出修订建议与 readiness verdict。

#### 2. 当前角色判断

主角色：Reviewer。

次角色：narrow Maker。它会输出可回填 PRD 的 revision draft，但应限制在最小替换块、补充段落、验收/边界列表。

#### 3. 输入边界

应该在以下情况调用：

- 已有 PRD/handoff。
- 用户要从研发和测试视角挑问题。
- 用户要判断 PRD 能否交给 writing-plans。
- 需要多轮关闭 blockers 并跟踪 readiness。

#### 4. 不应调用的情况

不应在以下情况调用：

- 从零生成 PRD，应优先 `prd-architect`。
- 只是语言润色。
- 方案还没写成交付物，只是想法或方向，应先 calibration / grill / decision-research。
- 要压力测试方案战略，不是审查文档交付质量，应优先 `grill-me`。

#### 5. 输出边界

应该输出：

- Review Scope。
- Executive Summary。
- 按严重程度排序的 Findings。
- PM / 研发 / 测试 Lens Summary。
- Revision Draft。
- Open Questions。
- Implementation-Plan Readiness：Ready for writing-plans / Ready with assumptions / Not ready。

不应该输出：

- 凭空生成完整 PRD。
- 未经要求重写整份 PRD 成终稿。
- 替代 writing-plans 拆文件、测试、提交节奏。

#### 6. 与其他 Skill 的重叠

- 与 `prd-architect` 重叠：revision draft 是必要的修复建议，但不应变成 full PRD generation。
- 与 `grill-me` 重叠：都能发现问题。区别是 review 按交付标准审文档，grill 按方案失败模式拷问思路。
- 与 `decision-research` 重叠：如果 PRD 缺的是重大产品方向选择，review 应暂停并建议 decision-research，而不是自己做研究结论。

#### 7. 在 Loop Pattern 中的角色

适合作为 Reviewer Node / Gate Node，也可以承载 PRD Readiness Loop 的状态管理。

理由：它已经定义 open blockers、resolved blockers、revision draft、readiness status、open questions、diagram status、handoff decision 和停止条件。

#### 8. 主要问题

- Revision Draft 默认必选，容易鼓励 reviewer 过度生成。
- PRD Readiness Loop contract 放在 `prd-review` 内，导致 cross-skill loop 看起来像单 Skill 长跑。
- 停止条件较完整，但没有明确“回到 `prd-architect` 修订后再复查”的跨 Skill handoff 格式。

#### 9. 改造建议

- 明确 revision draft 只能是 patch draft / minimal replacement blocks；完整重写交给 `prd-architect`。
- 将 PRD Readiness Loop 提升为 `loop-patterns/prd-readiness-loop.md`，定义 `prd-architect` 修订节点和 `prd-review` 复查节点。
- 增加 non-trigger examples：`拷问这个方案是否会失败` 应走 `grill-me`，`从零写 PRD` 应走 `prd-architect`。

### Skill: `grill-me`

#### 1. 当前定位

该 Skill 用于对已有产品方案、架构设计、计划或决策做聚焦访谈式压力测试。它通过一问一答澄清依赖、隐含假设、分支、取舍和失败模式，并在结束时输出决策记录。

#### 2. 当前角色判断

主角色：Critic。

次角色：Framer。它会在上游约束不稳定时阻止跳到下游细节，并把未解决问题暴露出来。

#### 3. 输入边界

应该在以下情况调用：

- 用户已经有一个方案、设计、计划、路线或决策草案。
- 用户要 hard questions、压力测试、失败模式、哪里会翻车。
- PRD 前需要先挑战方案思路。
- Research Map 或阶段结论需要被反方挑战。

#### 4. 不应调用的情况

不应在以下情况调用：

- 用户要直接写最终方案。
- 用户要标准 PRD review。
- 用户不希望互动追问，只要一次性总结。
- 问题还没定义清楚，此时先 calibration。

#### 5. 输出边界

应该输出：

- 一问一答过程，每个问题附推荐答案或当前假设。
- 已确认决策。
- 被否掉的选项及原因。
- 仍未解决的问题。
- 推荐下一步。

不应该输出：

- 完整 PRD。
- 标准化 readiness verdict。
- 长篇无交互问题清单。
- 证据型调研报告。

#### 6. 与其他 Skill 的重叠

- 与 `ai-collaboration-calibration` 重叠：都挑战前提。边界应是“问题没定义清楚 -> calibration；已有方案 -> grill”。
- 与 `prd-review` 重叠：都发现问题。边界应是“方案层失败模式 -> grill；交付物层可开发可测试 -> review”。
- 与 `decision-research` 重叠：都能处理决策。边界应是“需要外部证据 -> decision-research；需要内部逻辑压测 -> grill”。

#### 7. 在 Loop Pattern 中的角色

适合作为 Critic Node，不适合作为 Loop 主体。

理由：它的职责是插入到 PRD、Decision Research、Research Radar 等 Loop 中挑战设计或结论，输出问题和决策记录后交回 Maker / Researcher / Reviewer。

#### 8. 主要问题

- 没有状态文件或 loop handoff contract。
- 没有明确和 PRD Readiness / Decision Research / Research Radar 的接入点。
- 输出结构适合单次访谈，但不足以作为多轮 Loop 的可恢复状态。

#### 9. 改造建议

- 增加 `Critic Handoff` 模板：`challenged_artifact`、`validated_assumptions`、`rejected_options`、`open_risks`、`return_to_skill`。
- 在 future loop-pattern docs 中明确 grill 的插入点：PRD 初稿前、PRD 修订后、Research Map 后、阶段结论后。
- 增加 non-trigger examples：`帮我审 PRD 是否可交付开发` 应走 `prd-review`。

## 5. Boundary Conflicts

### 5.1 `ai-collaboration-calibration` vs `grill-me`

当前文件基本体现了目标差异：

- `ai-collaboration-calibration`：问题未定义时，挑战问题本身、剥离解法、输出真实问题陈述。
- `grill-me`：已有方案后，按依赖、假设、分支、失败模式逐个追问。

主要缺口是 calibration 的追加模式包含 `failure-premortem`，而 grill 的核心也是失败模式压测。建议把 calibration 的 failure-premortem 限定为“问题定义阶段的风险嗅探”，一旦已有明确方案，应转交 `grill-me`。

### 5.2 `decision-research` vs `research-topic-compiler`

根文档和 routing 已经写出正确原则：

```text
decision-research = 调研是为了做一个决定
research-topic-compiler = 调研是为了建立认知或长期沉淀
```

但 `research-topic-compiler` 内部 Product Candidate Research 分支破坏了这一原则。它触发“这几个方案怎么选”“选型”“这个方向值不值得做”，并输出 Candidate Backlog、评分、Top candidates、Candidate Summary、Cross-Session Handoff。这些与 `decision-research` 的具体决策、竞争假设、反证搜索、有立场推荐高度重合。

建议：

- P0：决定 Product Candidate Research 最终归属。
- 推荐方案：`decision-research` 拥有具体决策结论；RTC 只做主题认知、候选发现、长期雷达和 PRD input material。
- 若保留 RTC Product Candidate Research，则必须把它定义为“长周期候选池研究”，不输出最终单一推荐；最终推荐转交 `decision-research`。

### 5.3 `prd-architect` vs `prd-review`

当前边界总体清楚：

- `prd-architect`：生成或修订 PRD。
- `prd-review`：审查 PRD 是否可交付、可开发、可测试。

风险点：

- `prd-architect` 也会判断是否可以进入 UI / handoff / writing-plans。
- `prd-review` 默认输出 Revision Draft，且要求“可直接回填”。

建议把边界写得更硬：

- `prd-architect` 可以说“建议进入 review / handoff”，但最终 readiness verdict 由 `prd-review` 给出。
- `prd-review` 的 Maker 权限仅限 patch draft，不做完整 PRD 重写。

### 5.4 `grill-me` vs `prd-review`

当前差异存在，但还可以更明确：

- `grill-me` = 方案层压力测试，关注依赖、前提、取舍、失败模式。
- `prd-review` = 交付物层标准化评审，关注 blocker、冲突、验收、可开发、可测试。

建议在两边都补 non-trigger:

- `grill-me` 不做 `Implementation-Plan Readiness`。
- `prd-review` 不做开放式方案拷问，除非问题已落在 PRD blockers 中。

### 5.5 是否缺少 Router / Gate

缺少。

当前 `SKILL_ROUTING.md` 解决的是“相邻 Skill 分流”，但没有解决“这个工作应该沉淀到哪一层资产”的问题：

```text
Prompt / Context Pack / Workflow / Skill / Loop / System
```

建议新增 public-safe `ai-work-assetization-diagnoser` 或等价 Router/Gate：

- 输入：AI 协作会话、任务流程、prompt、工作流描述、团队场景。
- 输出：当前成熟度、推荐资产层、是否适合 Skill、是否适合 Loop、下一步最小沉淀动作。
- 边界：只做诊断和路由，不替代具体 Skill 执行。

## 6. Loop Pattern Readiness

### 6.1 PRD Readiness Loop

目标链路：

```text
ai-collaboration-calibration
  -> grill-me
  -> decision-research optional
  -> prd-architect
  -> grill-me
  -> prd-architect revision
  -> prd-review
  -> prd-architect regression fix
  -> prd-review recheck
  -> Ready for writing-plans / Not ready / Human decision required
```

当前支持度：中高，但需要 first-class loop doc。

判断：

- 应该先挑战方案思路，再输出 PRD，尤其是 AI-native、跨模块、涉及商业/定位/技术选型的需求。
- 前置阶段分工应为：calibration 澄清真实问题；grill-me 压测已有方案；decision-research 在关键决策缺证据时介入。
- `prd-review` 停止条件已经较明确：无 open blockers、验收可测试、流程清楚、scope/non-goals 明确、图示状态明确、open questions 已解决或转成 assumptions。
- 需要维护 `PRD Loop State`，否则 review / revision / re-review 会退化成单次报告。
- 建议新增 `loop-patterns/prd-readiness-loop.md`，并把现有 `prd-review/references/prd-readiness-loop-contract.md` 作为父 Skill 内引用或迁移来源。

建议 `PRD Loop State` 最小字段：

- `problem_definition`
- `solution_assumptions`
- `prd_version`
- `critic_findings`
- `open_blockers`
- `resolved_blockers`
- `revision_draft`
- `readiness_verdict`
- `human_decisions_required`
- `next_skill`

### 6.2 Decision Research Loop

目标链路：

```text
ai-collaboration-calibration
  -> decision-research Research Map
  -> grill-me challenge research design
  -> decision-research evidence and counter-evidence
  -> grill-me challenge interim conclusion
  -> decision-research revised conclusion
  -> recommendation / PoC / stop / user handoff
```

当前支持度：高，但 grill-me 插入点缺失。

判断：

- `decision-research` 已具备 Framing、假设、反证、Scope Drift、Assumption Ledger、终止条件和有立场输出。
- `grill-me` 应该前后都能使用：调研前挑战 Research Map，调研后挑战阶段结论。
- 需要维护 `Decision Research State`，现有 loop contract 已定义 `research_map.md`、`hypothesis_matrix.md`、`evidence_table.md`、`assumption_ledger.md`、`scope_drift_log.md`、`conclusion_version.md`。
- 建议新增 `loop-patterns/decision-research-loop.md`，把跨 Skill 调用顺序写出来，而不是只写在 `decision-research` 内部。

建议 `Decision Research State` 最小字段：

- `decision_question`
- `decision_owner`
- `constraints`
- `current_options`
- `competing_hypotheses`
- `supporting_evidence`
- `counter_evidence`
- `scope_drift`
- `assumption_ledger`
- `current_recommendation`
- `confidence`
- `reversal_condition`
- `next_gate`

### 6.3 Research Radar Loop

目标链路：

```text
research-topic-compiler establish research project
  -> grill-me challenge research map
  -> research-topic-compiler scan new material
  -> update Evidence Matrix / Update Log
  -> grill-me challenge interim conclusions
  -> decision-research if decision needed
  -> continue / pause / stop
```

当前支持度：中高。

判断：

- `research-topic-compiler` 适合长期主题跟踪，尤其是 evolving topic、watchlist、阶段结论 diff、更新日志。
- Radar Mode 已较清晰：它不是新闻监控，不默认创建 automation，弱信号不能直接改写稳定结论。
- 需要新增或外显 `Research Radar State`，当前 contract 已有 state files，但缺少和 grill / decision handoff 的统一入口。
- 建议新增 `loop-patterns/research-radar-loop.md`。

建议 `Research Radar State` 最小字段：

- `research_topic`
- `why_it_matters`
- `watchlist`
- `source_scope`
- `stable_conclusions`
- `candidate_conclusions`
- `weak_signals`
- `contradictory_evidence`
- `update_log`
- `decision_implications`
- `next_action`

### 6.4 AI Work Assetization Loop

当前仓库不具备完整支持。

需要一个 Router / Gate 先判断：

```text
一次性 Prompt
-> 可复用 Context Pack
-> SOP / Workflow
-> Skill
-> Loop
-> System
```

这个 Loop 不应由现有 6 个 Skill 任意承担。建议新增 `ai-work-assetization-diagnoser` 或轻量 router doc，先用作 Gate，再决定是否创建 Skill、Loop Pattern 或 System 设计。

## 7. Recommended Repository Structure

建议后续结构演进为：

```text
README.md
SKILL_REGISTRY.md
SKILL_ROUTING.md
AGENTS.md                         # P2, runtime orientation after routing is stable

ai-collaboration-calibration/
research-topic-compiler/
decision-research/
prd-architect/
prd-review/
grill-me/
ui-mockup-desktop-workbench/       # detected public surface; audit separately

loop-patterns/                     # P1, first-class Loop Pattern layer
  prd-readiness-loop.md
  decision-research-loop.md
  research-radar-loop.md

ai-work-assetization-diagnoser/     # P0/P1 decision; public-safe Router/Gate if added

docs/
examples/
```

判断：

- 建议新增 `loop-patterns/`，因为当前 Loop 已经跨 Skill，继续藏在 parent Skill references 会让用户误以为 Loop 是单 Skill 长时间运行。
- 建议新增 `AGENTS.md`，但优先级低于 Loop / Router 决策。它适合稳定后告诉 agent：先看 routing，何时启用 Loop，何时禁止写文件，如何交给 Superpowers。
- 建议新增或公开化 `ai-work-assetization-diagnoser`，但需要先决定是否把私有治理语言公开化，避免把内部成熟度框架直接暴露。

## 8. Recommended Changes

### P0

- 决定 Product Candidate Research 的 ownership：推荐由 `decision-research` 拥有具体决策推荐，`research-topic-compiler` 保留长期认知、候选发现、Research Project 和 Radar。
- 决定是否新增 Router / Gate：推荐新增 public-safe `ai-work-assetization-diagnoser` 或 `AI Work Assetization Gate` 文档。
- 决定 Loop Pattern 是否 first-class：推荐新增 `loop-patterns/`，至少覆盖 PRD Readiness、Decision Research、Research Radar。

### P1

- 新增 `loop-patterns/prd-readiness-loop.md`，明确 calibration / grill / decision-research / prd-architect / prd-review 的顺序和 PRD Loop State。
- 新增 `loop-patterns/decision-research-loop.md`，明确 grill-me 挑战 Research Map 和阶段结论的插入点。
- 新增 `loop-patterns/research-radar-loop.md`，明确 Radar State、weak signal handling、升级到 decision-research 的条件。
- 更新 `README.md`、`SKILL_REGISTRY.md`、`SKILL_ROUTING.md` 时必须同步，包含 7-skill public surface 和新 loop layer。
- 为 `grill-me` 增加 Critic Handoff 输出，方便进入 Loop。

### P2

- 给 `decision-research` 补明确 Input / Context Intake 小节。
- 给 `prd-review` 明确 revision draft 是 minimal patch draft，不是 full PRD rewrite。
- 整理 `prd-architect` 与 `prd-review` 的 Draw.io reference 复用策略。
- 为四组边界冲突增加 smoke / non-trigger eval。
- 在 routing 中记录 `ui-mockup-desktop-workbench` 是 PRD 之后的 UI artifact Maker，不参与本轮 6-skill role model。

### P3

- 暂不重写所有 `SKILL.md`。
- 暂不删除 flat root Skill directories。
- 暂不强制迁移到 `skills/` 子目录。
- 暂不创建 automation。
- 暂不把所有 references 拆成统一框架。

## 9. Do Not Change Yet

本轮不建议直接改：

- 不要重写所有 `SKILL.md`。当前问题主要是边界和 loop layer，而不是每个 Skill 都失效。
- 不要新增 `loop-patterns/` 前同时大改父 Skill。先让 loop docs 成为 thin orchestration layer。
- 不要新增 `AGENTS.md` 作为第一步。没有 Router / Loop 决策前，AGENTS 容易固化错误路由。
- 不要删除或移动根目录 Skill。历史、触发名称、分发路径都依赖 flat root layout。
- 不要把 `research-topic-compiler` 的所有 Product Candidate 内容立即删除。先决定 ownership，再迁移或降级为候选发现模式。
- 不要把 `prd-review` 改成只评论不修订。修订草案有价值，问题是需要限制生成边界。
- 不要把 Loop 理解为单个 Skill 长时间运行。Loop 应是多 Skill、有状态、有 Gate、有停止条件的闭环。

## 10. Next Step Proposal

建议下一步按小批量改造：

1. P0 决策小会：确定 Product Candidate Research 归属、Router/Gate 是否公开、`loop-patterns/` 是否新增。
2. 新增 `loop-patterns/` 三份薄文档：只编排已有 Skills，不重写 Skill 主体。
3. 给 `grill-me` 增加 Critic Handoff 模板，支持 PRD / Decision / Radar Loop 插入。
4. 收敛研究类边界：把 RTC Product Candidate 改为候选发现 / 长期沉淀，或明确只有跨会话候选池才走 RTC。
5. 同步更新 `README.md`、`SKILL_REGISTRY.md`、`SKILL_ROUTING.md`，把 Skill Library、Loop Pattern Layer、Router/Gate 三层讲清楚。
6. 单独审查 `ui-mockup-desktop-workbench`，确认它在 public catalog 中的角色、边界和是否进入某个 PRD-to-UI Loop。

## Verification Notes

- 本轮 deterministic check：6 个深审 Skill 中，`ai-collaboration-calibration`、`research-topic-compiler`、`prd-architect`、`prd-review`、`grill-me` 未发现确定性结构问题；`decision-research` 有 P2 建议：补充或明确 `input/context intake`。
- Targeted search 未发现旧研究 Skill 命名；当前研究命名主要是 `decision-research`、`research-topic-compiler` 和 RTC 内部 `Product Candidate Research`。
- Targeted search 发现 public surface 已包含 `ui-mockup-desktop-workbench`；这与用户本轮要求深审 6 个 Skill 不冲突，但需要后续 catalog 一致性审查。
- 当前未发现根目录 `loop-patterns/` 或 `AGENTS.md`；Loop contract 仍位于 parent Skill 的 `references/` 下。
