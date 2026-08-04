# Evidence-Driven Iterative Research Loop

Normal Research 和 Application 使用本合同，把研究从一次性渠道扫描改为可恢复的证据循环。它定义逻辑状态，不要求每轮都创建同名文件；持久化程度由 `research-depth-rubric.md` 决定。

## Contents

1. [Core Invariants](#core-invariants)
2. [State Machine](#state-machine)
3. [State Objects](#state-objects)
4. [FRAME](#frame)
5. [IDENTIFY GAP](#identify-gap)
6. [PLAN NEXT BEST EVIDENCE](#plan-next-best-evidence)
7. [ACQUIRE](#acquire)
8. [EVALUATE](#evaluate)
9. [UPDATE FRAMEWORK](#update-framework)
10. [CHECK SATURATION](#check-saturation)
11. [Failure and Recovery](#failure-and-recovery)
12. [Checkpoint and Resume](#checkpoint-and-resume)

## Core Invariants

- 把 Seed Corpus 当作线索、术语表和 Seed Claims 的来源，不默认当作权威证据。
- 每轮只执行一个 Next Best Evidence（NBE）Action；动作必须关闭或缩小一个已排序 Gap。
- 先选择 Gap 和证据角色，再选择渠道与具体来源。不要先打开所有渠道再寻找用途。
- 把 `Source`、`Evidence` 和 `Claim` 分开：来源不是证据，证据也不是结论。
- 二手材料、转载和摘要若来自同一原始材料，必须共享 `lineage_root`，不能冒充独立验证。
- 新证据通过 Change Event 改变 Framework；不得静默覆盖、不强行调和冲突。
- 停止由 fit-for-purpose 或饱和门禁决定，不由来源数、搜索结果数或文件完成度决定。
- 若访问、预算、授权或决策边界阻止继续，返回唯一终态并留下可执行 Checkpoint。

## State Machine

```text
FRAME
  -> IDENTIFY GAP
  -> PLAN NEXT BEST EVIDENCE
  -> ACQUIRE
  -> EVALUATE
  -> UPDATE FRAMEWORK
  -> CHECK SATURATION
       Continue -> IDENTIFY GAP
       Stop     -> SYNTHESIZE
       Pause    -> CHECKPOINT
       Escalate -> USER / DEPTH UPGRADE / decision-research
```

不允许在 ACQUIRE 后直接写最终结论。即使一次获取没有改变 Framework，也要记录 `No change` 并经过饱和检查。

## State Objects

字段是语义契约。L1/L2 可内联维护最小子集；L3+ 按 Obsidian 映射持久化。

### Run

```yaml
run:
  goal: "研究要支持的理解、判断或应用动作"
  mode: "Normal Research | Application"
  depth: "L1 | L2 | L3 | L4 | L5"
  scope: { in: [], out: [] }
  evidence_contract: "Must Claim 达到什么标准"
  effort_budget: "时间、动作数或成本边界"
  authorization: { public: true, restricted: [] }
  framework_version: "v0"
  status: "active"
```

### Framework Node and Claim

```yaml
framework_node:
  id: "FN-01"
  question: "需要回答的问题"
  importance: "Must | Should | Could"
  claim_ids: ["C-01"]
  current_status: "open | supported | contested | invalidated | deferred"

claim:
  id: "C-01"
  statement: "可被证据支持或挑战的陈述"
  type: "definition | mechanism | practice | transfer | risk | trend"
  decision_impact: "high | medium | low"
  required_evidence: "所需来源角色、直接性和独立性"
  status: "seed | provisional | supported | contested | invalidated | unverified"
  confidence: "high | medium | low"
  evidence_ids: []
  open_gap_ids: []
```

### Gap and NBE Action

```yaml
gap:
  id: "G-01"
  claim_id: "C-01"
  type: "origin | authority | implementation | independence | counterexample | contradiction | transfer | freshness"
  why_it_matters: "不关闭会怎样影响用户目标"
  closure_criterion: "什么证据足以关闭或降级此 Gap"
  priority: "Must | Should | Could"
  status: "open | narrowed | closed | blocked | deferred"

nbe_action:
  id: "A-01"
  target_gap: "G-01"
  action_type: "trace-origin | inspect-authority | compare-peer | inspect-implementation | seek-independent-validation | seek-counterexample | resolve-conflict"
  target: "主体、文档族、项目或可验证问题"
  expected_information_gain: "预期支持、挑战或区分什么"
  source_role: "Primary | Peer Authority | Canonical | Independent | Production | Contrast | Counterexample"
  independence_target: "期望的新 lineage 或实现路径"
  cost_access_risk: "low | medium | high + 说明"
  selection_reason: "为何它比队列中其他动作更值得先做"
  status: "planned | acquired | evaluated | blocked | abandoned"
```

### Source, Evidence, and Source Graph

```yaml
source:
  id: "S-01"
  owner: "可验证的发布主体或作者"
  url_or_path: "稳定 URL 或本地路径"
  source_type: "official-doc | standard | paper | repository | issue | case | article | community"
  provenance: "primary | secondary | unverified-origin"
  evidence_level: "按 source-quality-rules.md"
  lineage_root: "原始材料或独立实现族的稳定标识"
  independence_group: "应视作一个 corroboration unit 的发布/数据/实现组"
  access_status: "available | partial | blocked | requires-authorization"
  published_or_updated_at: "已知日期或 unknown"
  accessed_at: "本轮访问日期"

evidence:
  id: "E-01"
  source_id: "S-01"
  claim_id: "C-01"
  locator_or_excerpt: "章节、行号、时间戳或可定位摘录"
  relation: "supports | challenges | context"
  directness: "direct | inferred | anecdotal"
  freshness: "日期与时效风险"
  independence_group: "用于避免重复计票的 lineage/实现组"
  limitations: "不能证明什么"
```

Source Graph 使用以下边：

- `derived_from`：转述、翻译、摘要或镜像来自某源。
- `cites`：来源明确引用另一来源。
- `same_publisher_as`：同一发布主体，不默认算独立验证。
- `implementation_of`：实现某规范、方法或参考项目。
- `fork_of`：代码或内容分支，默认共享实现血缘。
- `responds_to`：反驳、修订或讨论另一来源。

关系保持为：

```text
Source -extracts-> Evidence -supports/challenges-> Claim -belongs_to-> Framework Node
```

### Framework Change Event

```yaml
change_event:
  id: "CE-01"
  from_version: "v0"
  to_version: "v1"
  type: "Fill | Refine | Split | Merge | Challenge | Invalidate | Expand | No change"
  affected_node_or_claim_ids: ["C-01"]
  evidence_ids: ["E-01"]
  before: "更新前状态或陈述"
  after: "更新后状态或陈述"
  rationale: "证据为何支持此变化"
```

### Saturation Check and Checkpoint

```yaml
saturation_check:
  must_gaps: []
  unresolved_contradictions: []
  marginal_yield: "high | medium | low"
  counterexample_status: "not-required | not-searched | none-found | found-and-handled | blocked"
  budget_status: "available | exhausted"
  decision: "Continue | Stop | Pause | Escalate"
  terminal_status: "仅在终止时填写"
  stop_reason: "为什么继续研究不会显著改善当前目标"
  residual_risks: []

checkpoint:
  last_completed_state: "CHECK SATURATION"
  framework_version: "vN"
  current_gap: "G-xx"
  ranked_nbe_queue: []
  completed_actions: []
  blocked_actions: []
  next_exact_action: "恢复后第一个动作"
  artifact_paths: []
```

## FRAME

1. 保留用户原始意图，并写清研究要支持的下一步动作。
2. 从 Seed Corpus 抽取 Seed Claims、来源主体、疑似原始出处、术语和证据角色。
3. 标记 Seed 的 provenance。标题、自称“官方”、转述中的品牌名都不能替代可验证发布主体与原始 URL。
4. 建立 Framework V0：将问题拆为 Framework Nodes，并为每个 Must/Should/Could Claim 定义 required evidence。
5. 明确 scope、out-of-scope、预算、授权和 Evidence Contract。

Framework V0 是可被推翻的研究假设，不是报告目录。若用户已提供足够权威材料，仍建立最小 Claim/Gap 判断，但不要为了展示流程而扩源。

## IDENTIFY GAP

从以下缺口中创建 Gap：

- `origin`：二手 Claim 尚未追溯原始材料。
- `authority`：发布主体、作者身份或规范地位不可验证。
- `implementation`：规范主张缺少实现行为或失败证据。
- `independence`：多个材料共享同一 lineage，尚无独立验证。
- `counterexample`：高影响泛化 Claim 尚未测试适用边界。
- `contradiction`：证据或权威来源彼此冲突。
- `transfer`：从一个平台、案例或行业推广到另一个场景的依据不足。
- `freshness`：时效敏感结论依赖过期资料。

排序先看 `Must > Should > Could`，再看 decision impact、不确定性、可关闭性和获取成本。每轮重排；新证据产生的 Must Gap 可以插到队首。

## PLAN NEXT BEST EVIDENCE

对排名靠前的 Gap 生成少量候选动作，再选一个 NBE：

1. 判断什么证据角色能真正关闭或缩小 Gap。
2. 估计动作的信息增益：它能区分哪些相互竞争的解释？
3. 检查独立性：新来源是否只是已有材料的转载、同发布者内容或 fork？
4. 检查成本、访问风险、范围与授权。
5. 记录 selection reason；若跳过最高优先 Gap，说明 blocked、超预算或授权原因。

推荐排序启发式：原始来源追溯优先；高影响且高不确定的 Must Claim 优先；能同时区分多个解释的证据优先；独立 lineage 优先于重复共识。

## ACQUIRE

先根据 NBE 的 source role 选择渠道，再获取具体来源。`pre-research-source-expansion.md` 是候选发现策略，不是固定前置阶段。

### Authority Expansion

只有当 Claim 需要跨平台或跨主体泛化时才扩展同类权威主体。先写比较维度与目标 Gap，再选同行；不得因品牌知名度机械罗列公司。

### Open-source Sampling

先指定证据角色，再选择项目：

| Role | What it tests |
| --- | --- |
| Canonical | 规范或方法的参考实现是否兑现其主张 |
| Independent | 不同 lineage 是否独立复现同一机制 |
| Production | 真实运行约束、维护与失败模式 |
| Contrast | 替代设计如何处理同一问题 |
| Counterexample | Claim 在何种条件下失效 |

为每个项目记录 target Gap、可观察材料、lineage、局限和选择理由。Stars、下载量或热度只能作为发现/活跃度信号，不能作为主要证据理由。默认只读 README、文档、源码、配置、issues、discussions、releases 和测试；不要执行第三方代码。

### Access Boundary

只读取公开或当前 run 已授权的来源。登录、付费、私密、客户数据或客户端转发需要明确授权。若必要证据受限，记录其预期价值并寻找公开替代 NBE；没有充分替代时进入 Pause/partial 终态。

## EVALUATE

1. 解析 canonical identity、owner、日期、source type、provenance 和 lineage root。
2. 抽取可定位 Evidence；没有 locator/excerpt 的材料不能进入稳定结论。
3. 标注 Evidence 对 Claim 是 `supports`、`challenges` 还是仅为 `context`。
4. 按 `source-quality-rules.md` 评估直接性、新鲜度、独立性和局限。
5. 标题声称“官方”但无可验证发布主体、作者身份或原始材料时，降级为 `unverified-origin`；不得形成最高等级核心结论。
6. 矛盾不是失败：把 Claim 标为 `contested`，生成 contradiction Gap。

## UPDATE FRAMEWORK

每个已评估 NBE 必须创建一个 Change Event：

| Type | Use when |
| --- | --- |
| `Fill` | 新证据填补既有 Claim 的证据缺口，不改变边界 |
| `Refine` | 收窄、澄清或增加条件 |
| `Split` | 一个 Claim 实际包含多个条件不同的 Claim |
| `Merge` | 多个重复 Claim 可由同一机制解释 |
| `Challenge` | 新证据显著降低信心或形成争议 |
| `Invalidate` | Claim 不再成立，需保留历史而非删除 |
| `Expand` | 发现原框架遗漏的重要节点或 Must Gap |
| `No change` | 有效获取但未提供新信息；仍记录边际产出 |

`before`、`after`、`evidence_ids` 和 `rationale` 不得缺失。`Challenge` / `Invalidate` / `Split` 优先保留冲突与条件差异，不得为获得整齐结论而强行调和。

## CHECK SATURATION

每轮只返回 `Continue / Stop / Pause / Escalate` 之一：

- `Continue`：仍有可执行的高价值 Must/Should Gap，且预算与授权允许。
- `Stop`：达到 fit-for-purpose，或 L4 同时达到信息饱和。
- `Pause`：下一必要动作等待授权、访问恢复或新预算。
- `Escalate`：目标转为最终选型、范围显著扩大、需要高风险人工判断或应升级深度。

### Completion Gate

任何 `complete-*` 必须同时满足：

- 所有 Must Claim 达到 Evidence Contract，或明确降级为无法验证并披露影响。
- 核心二手 Claim 已追溯原始来源，或披露无法追溯造成的可信度损失。
- L4 的高影响泛化 Claim 已进行独立验证和反例搜索。
- 没有未处理的关键矛盾。
- 剩余 Gap 不阻碍用户下一步。

`complete-saturated` 额外要求：在已 fit-for-purpose 的前提下，L4 最近两个来自不同 lineage 的高质量 NBE 只产生 `Fill` 或 `No change`，且没有产生新 Must Gap。L1-L3 不为获得该状态而机械扩源。

### Unique Terminal Status

按以下顺序自上而下判定，命中即停止；不得同时返回多个终态：

1. `blocked-authorization`：下一必要动作需要授权，且没有公开替代 NBE。
2. `partial-access`：必要证据不可访问、替代来源不足，仍影响 Must Gap。
3. `partial-budget`：预算耗尽且仍有 Must Gap；披露对结论的影响。
4. `escalated`：目标转为最终决策、范围显著扩大或需要高风险人工判断，并已 handoff。
5. `complete-saturated`：通过 Completion Gate，并满足 L4 连续两个独立 lineage 低增益条件。
6. `complete-fit-for-purpose`：通过 Completion Gate，允许不阻碍下一步的 Should/Could Gap。

不能仅因“已看 N 个来源”“候选池已读完”“所有文件已生成”而完成。最终输出必须包含 terminal status、stop reason、未解决问题和 residual risks。

## Failure and Recovery

| Condition | Required behavior |
| --- | --- |
| 工具或网络瞬时失败 | 最多一次合理重试；仍失败则记录 blocked action，选择替代 NBE |
| 原始来源不存在或无法验证 | 标记 `unverified-origin`，降级相关 Claim，保留 origin Gap |
| 来源需要授权 | 不绕过；记录价值与影响，寻找公开替代，否则 `blocked-authorization` |
| 来源不可访问 | 记录 access 状态与替代尝试；Must Gap 未关闭则 `partial-access` |
| 预算耗尽 | 停止获取，保留队列与影响说明，返回 `partial-budget` |
| 新证据冲突 | Claim -> `contested`，生成 contradiction Gap，不吞掉冲突 |
| 范围显著扩大 | 暂停并确认新 scope；必要时升级深度 |
| 用户要求最终选择 | 生成 handoff，转 `decision-research`，返回 `escalated` |

## Checkpoint and Resume

L3+、跨会话或中断前写 Checkpoint。至少保存 framework version、最后完成状态、当前 Gap、已排序 NBE 队列、已完成/阻塞动作、下一精确动作和 artifact paths。

恢复时：

1. 读取 Evidence Contract、最新 Framework 版本和 Checkpoint。
2. 以 canonical URL/path/repository identity 和 `lineage_root` 去重，不以标题去重。
3. 检查来源 freshness、访问状态和用户是否修改 scope、预算或授权。
4. 对旧 Claim 与新 Evidence 逐条合并；时间更晚不是覆盖理由。
5. 只有显式 Change Event 或证据驱动的 `supersedes` 才能替换旧判断。
6. 从 `next_exact_action` 恢复；若环境已变，先重排 NBE queue 并记录原因。

跨会话交接格式和证据驱动合并规则见 `cross-session-handoff.md`；Obsidian 文件映射见 `obsidian-output-contract.md`。
