# Skill Boundary and Loop Pattern Audit

> 审查对象：`PANGKAIFENG/ai-product-manager-skills`（审计快照：v0.1.0，7 个 Public Skills；后续实施已扩展到 8 个）
> 审查日期：2026-06-11
> 审查范围：README.md、SKILL_REGISTRY.md、SKILL_ROUTING.md、审计快照中的 7 个 Skill 的 SKILL.md 与 references/、docs/、examples/
> 本轮约束：只做审查报告，不修改任何现有文件。
> 实施后状态：本报告建议已拆成 12 个 issue 并落地，当前 public Skill surface 已统一为 8 个。

---

## 1. Executive Summary

1. **仓库整体边界质量高于预期。** 7 个 Skill 在 README / SKILL_REGISTRY / SKILL_ROUTING 三份顶层文档中名称、描述、状态完全一致；多数 Skill 有显式的"不适合场景"声明和跨 Skill 升级路径。
2. **仓库已经有一个"单 Skill Loop 层"，但还没有"多 Skill 编排层"。** 3 个 Loop Extension 合约（Decision Research Loop / Research Radar Loop / PRD Readiness Loop）已存在于各 Skill 的 references/ 中，定义了状态文件、停止条件和升级规则——但它们都是单 Skill 的有状态运行模式，没有任何合约把 grill-me 或 ai-collaboration-calibration 作为 loop 内节点编排进来。
3. **最清晰的边界是 decision-research vs research-topic-compiler**（双向显式声明 + 对比表 + 双向升级路径），可作为其他 Skill 边界写法的范本。
4. **最需要补的边界是 ai-collaboration-calibration vs grill-me**：问题层 vs 方案层的区分在各自文件内部已体现，但两边 SKILL.md 互不引用、无 handoff 协议，触发词（"挑战我的假设"等）存在真实路由歧义。
5. **存在一处隐性功能重叠**：research-topic-compiler 的 Product Candidate Research mode 与 decision-research 的 Top-Down Product Research Mode 都做"多源竞品 → 候选池"，分工只靠时间尺度区分，需要显式收敛。
6. **grill-me 是全仓库唯一的纯 Critic，但它被排除在所有 Loop 合约之外。** PRD Readiness Loop 内部用"PM/研发/测试三视角"自评，没有引入 grill-me 作为独立 Critic 节点——这是 Loop Pattern 升级的最大缺口。
7. **缺少 Router / Gate 角色。** SKILL_ROUTING.md 是一张静态路由表（按工作阶段分流，质量不错），但没有任何 Skill 负责"这个任务值不值得资产化、应该沉淀到 Prompt / Workflow / Skill / Loop / System 哪一层"的判断。建议新增 `ai-work-assetization-diagnoser`。
8. **发现一处命名残留**：`.github/ISSUE_TEMPLATE/skill_request.md` 仍引用旧研究 Skill 名（应为 `decision-research`），列为 P1。除此之外未发现 README / REGISTRY / ROUTING 不一致。
9. **三个目标 Loop Pattern 的就绪度排序：Decision Research Loop（最就绪）> PRD Readiness Loop（基础闭环可运行，缺前置链）> Research Radar Loop（机制清晰，缺 Critic 约定）。**
10. **建议的改造路径是"增量升级"而非重构**：保留现有 3 个 references/ 内合约作为单 Skill 层，新增 `loop-patterns/` 作为多 Skill 编排层，新增 `AGENTS.md` 作为编排入口说明——本轮均不实施，只给方案。

---

## 2. Current Repository Model

当前仓库的实际形态是 **Skill Library + 部分 Loop Extension，尚未建立 Loop Pattern Layer**。

```text
当前三层结构：

  Layer 1: Skill Library（已完整）
    审计快照中的 7 个独立 Skill，各自有 SKILL.md + references/
    README / SKILL_REGISTRY / SKILL_ROUTING 提供注册与静态路由

  Layer 2: Loop Extension（部分实现）
    3 个单 Skill 有状态合约：
      decision-research/references/decision-loop-contract.md
      research-topic-compiler/references/research-radar-loop-contract.md
      prd-review/references/prd-readiness-loop-contract.md
    定位明确：SKILL_ROUTING.md 写明 "Loop Extension 不是新的 Skill 入口，
    而是现有 Skill 的状态化运行模式"

  Layer 3: Loop Pattern Layer（缺失）
    没有 loop-patterns/ 目录
    没有 AGENTS.md
    没有任何文件把多个 Skill 组织成
    "定义问题 → 生成/研究 → 挑战 → 修正 → 评审 → 停止/交还人" 的有状态闭环
```

跨 Skill 协作目前只有两种弱形式：

1. **顺序 handoff 建议**：docs/superpowers-comparison.md 演示了 7 步线性链（calibration → research-topic-compiler → decision-research → prd-architect → prd-review → grill-me → writing-plans），examples/ 每个示例末尾有"推荐后续"一句话。
2. **升级边（escalation edges）**：Research Radar Loop 合约写明"出现具体决策时转 decision-research"；PRD Readiness Loop 合约写明"PRD 太模糊时转 prd-architect 或 ai-collaboration-calibration"。

这些是**交接**，不是**闭环**：没有共享状态、没有回边（修正后回到上游节点复查）、没有统一的停止/交还人协议。

另一个值得注意的防御性设计：SKILL_ROUTING.md 明确写了反过度 Loop 化规则——"如果任务仍然模糊、没有稳定目标、没有状态、没有验证口径或没有停止条件，先回到 ai-collaboration-calibration，不要强行 Loop 化"。这条规则应在未来的 loop-patterns/ 中保留为第一条 Gate。

---

## 3. Role Model

本审查使用以下六种角色类型：

| 角色 | 定义 | 关键判据 |
|---|---|---|
| **Framer** | 定义问题、挑战前提、澄清目标/边界/判断标准；防止 AI 过早进入执行 | 工作对象是"问题定义"，产出是问题共识而非方案 |
| **Researcher** | 围绕主题/决策收集证据与反证，形成结构化判断 | 工作对象是"外部信息"，产出是结论 + 证据链 |
| **Maker** | 生成结构化交付物（PRD、图、mockup、模板） | 工作对象是"交付物"，产出可直接交付的草稿；不擅自决定高风险方向 |
| **Critic** | 对已有方案做压力测试，暴露失败模式、隐藏假设、替代路径 | 工作对象是"方案"，产出是问题清单/决策记录，不产出新方案 |
| **Reviewer** | 基于明确标准审查交付物，判断 ready / not ready | 工作对象是"交付物质量"，产出是判决 + 修订建议 |
| **Router / Gate** | 判断任务应进入哪个 Skill / 哪个 Loop / 沉淀到哪一层 | 工作对象是"任务本身"，产出是路由决定 |

Critic 与 Reviewer 的区别（本仓库中容易混淆）：Critic 挑战的是**方案为什么会失败**（开放式、对抗式、无固定清单）；Reviewer 检查的是**交付物是否满足标准**（封闭式、清单式、有判决）。grill-me 是 Critic，prd-review 是 Reviewer。

---

## 4. Skill-by-Skill Audit

### Skill: ai-collaboration-calibration

#### 1. 当前定位

在问题还没定义清楚时介入：通过 L1-L4 协作层级判断，对模糊感受做 JTBD 追问、假设显化和判断表达（L4-fuzzy 脑暴模式），或对已框定问题做六步校准（L4-framed），在 Done Signal 满足前阻止进入方案讨论。

#### 2. 当前角色判断

**混合角色：主 Framer，次 Critic（L3 挑战模式）+ 隐性 Gate（L1-L4 层级判断本身就是一个轻量路由器）。**

L4-fuzzy / L4-framed 是典型 Framer。L3 Challenger 单点挑战假设，带 Critic 性质但仍作用于问题层。L1-L4 分层判断实际上承担了"这个任务需要多深的协作"的 Gate 职能——这是仓库中最接近 Router 的现存机制，但它只路由协作深度，不路由 Skill。

#### 3. 输入边界

- 用户有模糊感受说不清问题；方案越补越复杂；想挑战假设、重新定义问题
- 用户直接说"帮我做 X 功能"但背景复杂、或对话早期方向可能跑偏
- 任何 Loop 启动前任务仍模糊、无稳定目标时（SKILL_ROUTING.md 的回退规则）

#### 4. 不应调用的情况

- 简单改写/翻译/摘要/格式转换 → L1 直接执行
- 用户明确说"直接做" → 尊重选择
- **方案已成形、问题定义已确认，用户想压测方案** → 应调用 grill-me（当前文件未写这条转出规则，见第 8 节）
- 校准完成或用户说"够了开始做" → 退出进入执行

#### 5. 输出边界

应输出：问题定义共识块（真问题陈述 + 显式排除方向 + 核心未验证假设）、结构化校准结果（隐藏假设表、问题分类、领域定位、下一步、现在不该做什么）。
不应输出：方案候选（L4-fuzzy 有"延迟方案硬约束"明确禁止）、PRD、研究报告、最终决策。

#### 6. 与其他 Skill 的重叠

- **与 grill-me**：触发词重叠（"挑战我的假设""这个方案是不是想错了" vs "拷问我的方案"）。意图边界（问题层 vs 方案层）在各自文件内部成立，但**两边互不引用**，详见第 5 章冲突 1。重叠本身合理（都是对抗式协作），需要的是显式 handoff 而非拆分。
- **与 decision-research**：decision-research 的 R00 Research Framing Gate（问题/现象/解法判别）是 calibration 思路的内嵌轻量版。这种内嵌是合理的（避免每次调研都强制先跑 calibration），但应在文档中承认这种关系。

#### 7. 在 Loop Pattern 中的角色

**Framer Node + 循环入口 Gate。不适合作为 Loop 主体。**

理由：它的产出（问题共识）是一次性收敛物，Done Signal 达成后职责即终止；它没有也不应有跨轮状态。在三个目标 Loop 中它都应是 Round 0 的入口节点，外加一个回退目标（loop 中途发现问题定义崩塌时回到它）。PRD Readiness Loop 合约已经把它列为升级目标（"PRD needs new product direction rather than revision"时转出），这个用法正确。

#### 8. 主要问题

1. SKILL.md 没有任何对 grill-me 的引用；"校准完成"之后的去向只写了"进入执行"，没写"如果产物是一个待压测的方案方向 → grill-me"。
2. 触发词列表中"这个方案是不是想错了"会吸入本应路由到 grill-me 的请求。
3. L1-L4 层级判断的 Gate 能力没有被仓库级路由复用（SKILL_ROUTING.md 与它各自为政）。

#### 9. 改造建议

- 在 SKILL.md 边界规则中新增一条转出规则："问题定义已清晰且用户持有具体方案 → 转 grill-me"，并在 grill-me 侧加对称引用（P1）。
- 在触发词描述中给"挑战假设"类短语加限定语（"挑战问题层面的假设"），把"方案哪里会翻车"类短语显式让渡给 grill-me（P1）。
- 未来 loop-patterns/ 中将其固定为所有 loop 的 Round 0 入口 + 回退节点（P1，随 loop-patterns 一起做）。

---

### Skill: research-topic-compiler

#### 1. 当前定位

面向长期主题的研究编译器：把系统学习、专题研究、概念源流、行业演进等需求转成 Research Project（00-09 文件结构）、证据矩阵、PM 决策看板或学习报告；含 5 种模式（Normal / Lightweight Concept Lens / Learning Pack / Application / Radar），L5 Radar Mode 支持长期追踪。

#### 2. 当前角色判断

**混合角色：主 Researcher，次 Maker。**

研究主体是 Researcher；但 Lightweight Concept Lens 输出 HTML 决策看板、Learning Pack 输出学习框架、Application Mode 输出模板/任务——这些是 Maker 行为。Maker 次角色是合理的（研究产物需要载体），但 Product Candidate Research mode 越界进入了 decision-research 的领地（见下文第 6 点）。

#### 3. 输入边界

- 围绕一个主题做系统学习、行业调研、最佳实践提炼、概念源流、语义演化
- 需要长期沉淀（Obsidian Research Project）或持续更新（Radar Mode）
- 输出需要跨会话复用

#### 4. 不应调用的情况

- 调研是为了做一个具体决定、不需要沉淀文档 → decision-research（双方文件均有显式声明）
- 还没定义清楚"为什么研究这个主题" → ai-collaboration-calibration（SKILL_ROUTING.md 有此规则）
- 创建/评审 Skill、普通即时搜索、一次性摘要（frontmatter 显式排除）

#### 5. 输出边界

应输出：Research Project（00-09 文件）、证据矩阵、阶段结论、决策看板、更新日志；弱信号只能进待复盘区。
不应输出：有立场的单次决策推荐（那是 decision-research 的产物）、候选池终选结论、PRD。

#### 6. 与其他 Skill 的重叠

- **与 decision-research**：宏观边界是全仓库最佳实践（双向声明 + 升级路径，见第 5 章冲突 2）。**但存在一处具体重叠**：本 Skill 的 Product Candidate Research mode（多源竞品研究 → 候选池评分 → handoff）与 decision-research 的 Top-Down Product Research Mode（行业叙事 → … → 商业包装六层递进）做的是同一类事。当前的区分（前者强调跨会话持久化，后者强调单次收敛）过于微妙，路由器无法稳定区分。
- 重叠不合理，需要收敛：要么把 Product Candidate Research mode 降级为"为 decision-research 准备输入的预研模式"，要么明确"候选池属于 compiler、终选属于 decision-research"的接力分工并在两边互相引用。

#### 7. 在 Loop Pattern 中的角色

**Loop 主体（Research Radar Loop 已有合约支撑）。**

理由：它有完整的跨轮状态（00-09 文件 + 更新日志 + watchlist）、信号分级（strong / weak / contradictory / no-meaningful-update）、防漂移规则（弱信号不能直接改写稳定结论）和暂停条件（连续 N 轮无信号、来源重复、主题失效）。这是天然的长周期 loop 主体。

#### 8. 主要问题

1. 模式过多（5 种模式 + 多档 Definition of Done），单文件认知负担重，路由进入正确模式依赖较长的判断链——这是它边界清晰度 3 分（其余多为 4 分）的主因。
2. Product Candidate Research mode 与 decision-research 重叠（见上）。
3. Radar Mode 缺少"研究地图被挑战"的环节：watchlist 和研究问题一旦建立，没有机制质疑它们本身是否还成立（Critic 缺位）。

#### 9. 改造建议

- 收敛 Product Candidate Research mode 的职责，与 decision-research 建立显式接力分工（P1）。
- 考虑把 Lightweight Concept Lens / Learning Pack 拆为 references/ 内的子文档，主 SKILL.md 只保留模式路由表，降低单文件复杂度（P2）。
- Research Radar Loop pattern 中加入可选的 grill-me 节点（挑战研究地图与阶段结论），见第 6 章（P2）。

---

### Skill: decision-research

#### 1. 当前定位

决策驱动调研：先用 R00 Research Framing Gate 框定问题层级与类型，再锚定决策问题、枚举竞争假设、主动搜反证、三角收敛，最终给出有立场结论 + 置信度 + 排除理由 + 颠覆条件；配有完整的 Decision Research Loop 合约（6 个状态文件、7 条停止条件、Human Gate）。

#### 2. 当前角色判断

**混合角色：主 Researcher，次 Critic（内置反证机制）+ 轻量 Framer（R00 Gate）。**

反证搜索（R06）、竞争假设枚举（R04）、Scope Drift Checkpoint 是把 Critic 职能内化到研究流程中——这是合理的内嵌，不构成与 grill-me 的冲突（grill-me 挑战的是用户的方案，decision-research 的反证挑战的是自己的研究假设）。R00 的问题/现象/解法判别是 Framer 职能的轻量内嵌，同样合理。

#### 3. 输入边界

- 面对一个具体决策需要找信息："有没有现成方案""怎么接入 X""选 A 还是 B""这个可行吗"
- 问题已定义清楚或可被 R00 快速框定
- 调研完不需要沉淀成长期文档，只要得出决策结论

#### 4. 不应调用的情况

- 问题还没定义清楚 → ai-collaboration-calibration
- 需要长期知识沉淀、建立系统认知 → research-topic-compiler（SKILL.md L11-12 有显式声明）
- 方案已成形、要的是压测而非调研 → grill-me（SKILL.md 内的四技能对比表已覆盖）

#### 5. 输出边界

应输出：有立场结论 + 置信度 + 排除理由 + 颠覆条件；证据/解读分离标注（L1-L4 证据等级）；Loop 模式下的 6 个状态文件。
不应输出：长期研究项目、PRD、执行计划；弱证据不得升级为稳定结论（合约有显式禁令）。

#### 6. 与其他 Skill 的重叠

- **与 research-topic-compiler**：见上文及第 5 章冲突 2，宏观清晰、Product Candidate mode 局部重叠。
- **与 grill-me**：SKILL.md 内嵌的四技能对比表（calibration / decision-research / research-topic-compiler / grill-me，含前提、时间尺度、输出、终止条件四个维度）是全仓库唯一的跨 Skill 对比矩阵——这个写法应推广到其他 Skill 或上提到仓库级文档。

#### 7. 在 Loop Pattern 中的角色

**Loop 主体（Decision Research Loop 已有合约支撑），是全仓库 loop-readiness 最高的 Skill。**

理由：框定（R00）、假设矩阵、反证、漂移检查（scope_drift_log）、假设状态机（active / weakened / excluded / needs-user-context / needs-poc）、三类收敛条件（三角收敛 / 信息饱和 / 暗知识缺口）、ROI fuse、Human Gate 全部齐备。其他 loop 合约应向它看齐。

#### 8. 主要问题

1. 几乎没有结构性问题。仅有的缺口：Loop 合约未约定 grill-me 的可选介入点（挑战 Research Map 设计、挑战阶段结论）——当前由内置反证机制承担，但内置自评和外部 Critic 不是同一种保障。
2. Top-Down Product Research Mode 与 research-topic-compiler 的重叠（责任在两边，见冲突 2）。

#### 9. 改造建议

- 在未来的 loop-patterns/decision-research-loop.md 中把 grill-me 定义为两个可选 Critic 检查点（Research Map 建立后、结论收敛前），不改现有合约（P2）。
- 把 SKILL.md 内的四技能对比表上提（或复制）到 SKILL_ROUTING.md，作为仓库级路由依据（P2）。

---

### Skill: prd-architect

#### 1. 当前定位

把想法/草稿/脑暴结果整理成 PRD：在 PRD-lite（6 章）/ PRD-standard（12 章）/ PRD-ai-native（17 章）中选择模板，维护文档成熟度状态（草稿/讨论中/已确认）和待确认项，可生成可编辑的 Draw.io 图（含 validate_drawio.py 验证）和基于真实项目页面的截图。

#### 2. 当前角色判断

**主 Maker，次轻度 Gate。**

任务方关心的问题——"prd-architect 是否承担了过多评审职责"——审查结论是**没有**。它的 readiness 判断（待确认项 ≥3 或存在阻断性待确认 → 不推荐进入 ui-mockup，继续深化）是**流程把控**（决定自己产物的下一站），不是多视角质量评审；它没有 findings、没有严重度分级、没有三视角清单。SKILL.md 明确写了"已有完整 PRD 要评审 → 改用 prd-review"。这条边界是干净的。

#### 3. 输入边界

- 从想法、脑暴、需求草稿进入 PRD 结构
- 需要判断模板档位、文档成熟度、是否需要正式图示
- prd-review 评审后回填修订（修订职责属于 architect，review 只给补丁草案）

#### 4. 不应调用的情况

- 已有完整 PRD 要评审 → prd-review（双向均有声明）
- 直接编码、单纯画 UI → ui-mockup-desktop-workbench 或开发工具
- 问题/方向还没确认 → ai-collaboration-calibration（当前文件未显式写这条，建议补）

#### 5. 输出边界

应输出：PRD 文档 + 当前状态字段 + 待确认项列表 + .drawio 源/svg + 必要时 HTML mockup 引用。
不应输出：评审报告、readiness 判决（那是 prd-review 的）、生产代码、未经确认就拍板的高风险产品方向（待确认项机制保障了这点）。

#### 6. 与其他 Skill 的重叠

- **与 prd-review**：生成 vs 评审分工清晰（见第 5 章冲突 3）。唯一的灰区是双方都有"质量检查点"语言（architect 的冗余控制/事实假设分离 vs review 的三视角），但前者是写作纪律、后者是评审标准，性质不同，可接受。
- **与 ui-mockup-desktop-workbench**：architect 的"真实项目截图规则"与 mockup Skill 的产物有表面相似，但 architect 只引用既有页面截图，mockup Skill 生成新页面，边界成立。

#### 7. 在 Loop Pattern 中的角色

**Maker Node。不适合作为 Loop 主体。**

理由：PRD Readiness Loop 的状态（blockers、readiness verdict）天然由 Reviewer 持有；architect 在 loop 中的职责是"接收 revision_draft → 回填 → 提交复查"，是被驱动的节点。它自带的"当前状态"字段是文档元数据，不是 loop 状态。

#### 8. 主要问题

1. 缺少上游引用：没写"想法仍模糊时先 calibration"、没提"方案方向有重大不确定时先 grill-me 或 decision-research"——作为 Maker 它假设输入已成熟，但没有声明这个前提的检查方式。
2. 17 章的 PRD-ai-native 模板较重，依赖冗余控制规则防止过度升档，这条规则的执行效果依赖模型自律。

#### 9. 改造建议

- 在 SKILL.md 增加上游前提声明与转出规则（方向未定 → calibration / grill-me / decision-research）（P2）。
- 在未来 PRD Readiness Loop pattern 中明确它作为 Maker Node 的回填义务与输入格式（直接消费 prd-review 的 revision_draft.md）（P1，随 loop-patterns 一起做）。

---

### Skill: prd-review

#### 1. 当前定位

对已有 PRD/handoff 做 PM / 研发 / 测试三视角评审：输出按严重度排序的 findings（阻断/重要/优化）、视角汇总、最小可替换块形式的修订草案、open questions，最终给出三态判决（Ready for writing-plans / Ready with assumptions / Not ready）；配有 PRD Readiness Loop 合约（8 个状态文件）。

#### 2. 当前角色判断

**主 Reviewer，次轻度 Maker（修订补丁）+ Gate（readiness 判决）。**

任务方关心的问题——"prd-review 是否承担了过多生成职责"——审查结论是**受控的、合理的**。它生成的是"最小可替换块"补丁（建议新增章节结构 / 替换段落草案 / 补充验收列表），且 SKILL.md 显式禁止"未经要求直接重写整份 PRD 成终稿"和"在没有 handoff/PRD 的情况下凭空生成完整方案"。Reviewer 给出可直接回填的修订建议属于"怎么改"而非"代写"，边界守住了。

它的三态判决 + "能否进 writing-plans" 判断使它同时是 PRD 工作流的**出口 Gate**——这是仓库中第二个现存的 Gate 机制。

#### 3. 输入边界

- 已有 PRD 初稿 / handoff / 需求文档，需要找阻断项、冲突、不可实现点、不可测试点
- 需要判断能否交付开发（进入 writing-plans）
- 多轮关闭阻断项 → 启用 PRD Readiness Loop

#### 4. 不应调用的情况

- 从零写 PRD → prd-architect
- 只做语言润色
- PRD 太模糊以至于评审无从下手 → prd-architect 或 ai-collaboration-calibration（Loop 合约已有此升级规则）
- 要挑战的是产品方案思路本身而非文档质量 → grill-me（当前文件未显式写这条）

#### 5. 输出边界

应输出：Review Scope、Executive Summary、按严重度排序的 findings、三视角汇总、最小可替换块修订草案、open questions、三态 readiness 判决。
不应输出：整份重写的 PRD、新的产品方向决策、把未确认业务事实伪装成已确认结论（均有显式禁令）。

#### 6. 与其他 Skill 的重叠

- **与 prd-architect**：见冲突 3，分工干净。
- **与 grill-me**：见冲突 4。交付物层标准化评审 vs 方案层压测的区分客观成立（清单式三视角 + 判决 vs 开放式追问 + 决策记录），但文件层面零互引；评审中发现"方案本身可能是错的"时没有转出到 grill-me 的协议——当前只能靠"Pause and ask the user: PRD needs new product direction"间接覆盖。

#### 7. 在 Loop Pattern 中的角色

**Reviewer Node + 出口 Gate Node，同时是 PRD Readiness Loop 的主体（状态持有者）。**

理由：loop 的核心状态（open_blockers / resolved_blockers / readiness_status / handoff_decision）天然归属评审方；三态判决就是 loop 的停止条件。它是三个 Loop 主体中唯一"以 Gate 判决为停止条件"的，这个设计正确。

#### 8. 主要问题

1. PRD Readiness Loop 合约的"挑战"环节全部由自身三视角承担，没有独立 Critic（grill-me）介入点——自评视角再多也是同一个评审者。
2. 停止条件 7 条已较完整，但缺"最大轮数 / 连续 N 轮 blocker 不下降则强制升级人工"的发散保护。
3. 与 grill-me 零互引（见上）。

#### 9. 改造建议

- 未来 loop-patterns/prd-readiness-loop.md 中：第一轮评审前或重大修订后插入可选 grill-me 节点；增加轮数上限 / blocker 不收敛升级规则（P1）。
- SKILL.md 增加转出规则："评审发现根本问题在方案思路 → 建议先走 grill-me 再回评审"（P1）。

---

### Skill: grill-me

#### 1. 当前定位

对已有方案/架构/计划/决策做一问一答式压力测试：一次只问一个问题、每问附推荐答案或当前假设、可查证的问题先查代码/文档再问人、按依赖顺序推进，最终输出决策记录（已确认决策 + 已排除选项及理由 + 未解决问题 + 下一步）。

#### 2. 当前角色判断

**纯 Critic。** 全仓库唯一的纯单一角色 Skill。它不生成方案（显式拒绝"直接帮我写最终方案"）、不做标准化判决、不做研究——角色纯度是它的核心价值，应当保持。

#### 3. 输入边界

- 用户已有成形的方案、设计、计划或决策，担心盲点
- 需要互动式追问（一问一答）而非一次性输出
- 在 PRD 起草前挑战方案思路，或 PRD 重大修订后挑战新方向

#### 4. 不应调用的情况

- 问题还没定义清楚、用户说不清要什么 → ai-collaboration-calibration（当前文件未显式写）
- 要的是对文档的标准化评审与 ready 判决 → prd-review（当前文件未显式写）
- 要的是补充外部证据来支持决策 → decision-research
- 直接写最终方案、泛泛总结、不希望互动追问（frontmatter 已排除）

#### 5. 输出边界

应输出：追问过程（每问带推荐答案）+ 决策记录。
不应输出：新方案、修订稿、readiness 判决、研究报告。决策记录是"压测后的共识快照"，不是交付物评审结论。

#### 6. 与其他 Skill 的重叠

- **与 ai-collaboration-calibration**：见冲突 1。语义重叠（都挑战）、范围正交（方案 vs 问题），需要显式 handoff。
- **与 prd-review**：见冲突 4。层次不同（方案 vs 交付物），但用户视角下"帮我挑 PRD 的毛病"可能误路由到 grill-me——prd-review 的清单评审才是正解；反之"这个 PRD 背后的方案能不能成"应到 grill-me。
- **与 decision-research 的内置反证**：不冲突——decision-research 挑战自己的研究假设，grill-me 挑战用户的方案。

#### 7. 在 Loop Pattern 中的角色

**Critic Node。明确不适合作为 Loop 主体。**

理由：它是无状态的单次决策树遍历——没有跨轮状态文件、没有收敛度量（它的 Definition of Done 是"关键分支已探索"，这是单会话条件）、没有合约。让它当 loop 主体会变成"无限拷问"，违背其设计。但它是三个目标 Loop Pattern 都需要的关键插件节点：在 PRD Loop 中挑战方案思路、在 Decision Loop 中挑战研究设计与阶段结论、在 Radar Loop 中挑战研究地图。

**当前最大的结构性问题就是：仓库唯一的纯 Critic 被排除在全部三个 Loop 合约之外。**

#### 8. 主要问题

1. 零跨 Skill 引用：不引用 calibration（上游）也不被任何 Loop 合约引用（下游）。
2. 作为 Loop 节点缺一个轻量"输出接口"约定：决策记录目前是自由格式，loop 中的下游节点（如 prd-architect 修订）无法机械消费。
3. 触发词与 calibration 部分重叠（见冲突 1）。

#### 9. 改造建议

- SKILL.md 增加双向边界：上游（问题没定义清 → calibration）与平行（要标准化评审 → prd-review）（P1）。
- 为 loop 场景定义最小输出契约（决策记录的固定字段：confirmed / rejected+rationale / unresolved / next），不改变交互式风格（P1，随 loop-patterns 一起做）。
- 三个 loop-patterns 文件中将其注册为可选 Critic 节点并写明介入时机（P1/P2）。

---

### Skill: ui-mockup-desktop-workbench

#### 1. 当前定位

基于已明确的 PRD + UI 规范 + 页面状态清单，生成可打开、可截图的桌面工作台 HTML/CSS mockup（四区壳布局），附 README 假设说明、screen-contract 可追溯映射和验证截图。

#### 2. 当前角色判断

**纯 Maker。** 无评审/挑战行为；其 smoke test 和回归清单是生成质量门，不是 Reviewer 职能。

#### 3. 输入边界

- PRD 和 UI 规范已明确，需要可落地的真实桌面页面 mockup
- 需要覆盖关键状态（空态/加载/错误等）的可讨论交付物

#### 4. 不应调用的情况

- 问题还没定义清楚、PRD 还没成型 → prd-architect 在前（SKILL_ROUTING.md 有此规则）
- 只写 PRD、移动端或营销页、直接实现生产代码（frontmatter 显式排除）

#### 5. 输出边界

应输出：独立 HTML/CSS mockup、README（假设）、screen-contract.md（PRD 条目 → 页面元素映射）、截图、handoff note。
不应输出：生产代码、PRD 修订、UI 规范本身。

#### 6. 与其他 Skill 的重叠

- **与 prd-architect**：architect 的 PRD-lite 可附 HTML mockup、有真实项目截图规则——存在轻微产物重叠。当前可用"architect 只引用/轻量示意，mockup Skill 负责正式多状态页面"区分，但两边都没写这条分界。

#### 7. 在 Loop Pattern 中的角色

**Maker Node（PRD Readiness Loop 的下游可选节点）。不适合进入 Loop 主体。**

理由：单次生成型，无跨轮状态。在 PRD Loop 达到 Ready 后作为可视化交付节点最自然；mockup 暴露的 PRD 缺口可作为回边反馈给 prd-review（当前无此约定）。

#### 8. 主要问题

1. 与 prd-architect 的 mockup/截图职责分界未成文。
2. 任务方给定的 6-Skill 清单未含本 Skill，说明其在仓库叙事（README AI PM Workflow 7 阶段）中的位置还未深入人心——属于文档可见性问题而非设计问题。

#### 9. 改造建议

- 在 prd-architect 与本 Skill 双方文件中写明 mockup 职责分界（P3）。
- 未来 PRD Readiness Loop pattern 中将其列为 Ready 之后的可选下游节点，并定义"mockup 发现 PRD 缺口 → 回 prd-review"的回边（P3）。

---

## 总览矩阵

| Skill | 当前主角色 | 次角色 | 应调用场景 | 不应调用场景 | Loop 中角色 | 边界清晰度 1-5 | 主要问题 | 改造优先级 |
|---|---|---|---|---|---|---:|---|---|
| ai-collaboration-calibration | Framer | Critic(L3) / 隐性 Gate | 问题没定义清、方向可能跑偏、Loop 启动前模糊 | 简单执行任务；方案已成形要压测（→grill-me） | Framer Node + 入口 Gate / 回退节点 | 4 | 与 grill-me 零互引、触发词歧义 | P1 |
| research-topic-compiler | Researcher | Maker | 长期主题研究、系统学习、概念源流、Radar 跟踪 | 单次决策调研（→decision-research）；即时搜索 | Loop 主体（Radar Loop） | 3 | 模式过多；Product Candidate mode 与 decision-research 重叠 | P1 |
| decision-research | Researcher | Critic(内置反证) / Framer(R00) | 具体决策需要证据与有立场推荐 | 问题没定义清（→calibration）；长期沉淀（→compiler） | Loop 主体（Decision Loop） | 5 | 仅缺 grill-me 介入点约定 | P2 |
| prd-architect | Maker | 轻度 Gate | 想法/草稿 → PRD；评审后回填修订 | 评审已有 PRD（→prd-review）；方向未定 | Maker Node | 4 | 缺上游前提声明；回填义务未成文 | P2 |
| prd-review | Reviewer | 轻度 Maker(补丁) / Gate(判决) | 已有 PRD 找阻断项、判断能否进开发 | 从零写 PRD（→architect）；挑战方案思路（→grill-me） | Reviewer/Gate Node + PRD Loop 主体 | 4 | Loop 内无独立 Critic；无发散保护 | P1 |
| grill-me | Critic | — | 已有方案要压测盲点与失败模式 | 问题没定义清（→calibration）；要标准化评审（→prd-review） | Critic Node（三个 Loop 通用插件）；不适合 Loop 主体 | 4 | 零跨 Skill 引用；无 loop 输出契约 | P1 |
| ui-mockup-desktop-workbench | Maker | — | PRD+UI 规范已明确，要真实桌面页面 mockup | PRD 未成型；移动端/营销页；生产代码 | Maker Node（PRD Loop 下游） | 4 | 与 architect 的 mockup 分界未成文 | P3 |

---

## 5. Boundary Conflicts

### 冲突 1：ai-collaboration-calibration vs grill-me

**应有边界**：calibration = 问题还没定义清楚时，挑战问题本身；grill-me = 已有方案后，挑战方案为什么会失败。

**当前体现情况：内部已体现，互联未体现。**

支持边界成立的证据：

- calibration frontmatter 锚定"模糊感受说不清问题"；L4-fuzzy 有"延迟方案硬约束"——Done Signal 满足前用户要谈方案会被拦截（brainstorm-mode.md："我们可以讨论方案，但我想先确认问题定义够不够清晰"）。
- grill-me frontmatter 锚定"有一个产品方案、架构设计、计划或决策"；非触发示例明确拒绝"直接帮我写最终方案"。

边界失效的证据：

- 两边 SKILL.md **互不引用**，无任何 handoff 协议。calibration 完成后只说"进入执行"，没说"产物是方案方向时 → grill-me"。
- 触发词冲突：calibration 的"挑战我的假设""这个方案是不是想错了" vs grill-me 的"拷问我的方案"——以下场景路由器无法稳定判别：
  1. "帮我想想这个方案"（半成品想法还是真方案？）
  2. "压力测试一下这个设计，我感觉哪里不对劲"（设计有漏洞还是问题框错了？）
  3. "挑战我这个方案的假设"（问题层假设还是方案可行性假设？）
  4. 用户自称"我有个方案"但实为模糊想法的包装。

**建议（本轮不改）**：双向 cross-reference + 一条共享判别规则（"这个方案针对的问题是否已被确认？否 → calibration；是 → grill-me"）写入两边 SKILL.md 和 SKILL_ROUTING.md。优先级 P1。

### 冲突 2：decision-research vs research-topic-compiler

**应有边界**：decision-research = 为具体决策收敛结论；research-topic-compiler = 为长期主题建立认知地图。

**当前体现情况：宏观边界是全仓库最佳实践，但存在一处具体模式重叠。**

宏观边界证据（应作为范本推广）：

- decision-research SKILL.md L11-12 显式声明："调研完不需要沉淀成文档、不需要持续更新、不需要建立系统认知——只要得出一个决策结论就用这个；否则用 research-topic-compiler"。
- 一句话判别："调研是为了做一个决定 vs 调研是为了建立对某个领域的认知"。
- 双向升级路径：compiler L98"研究信号变成具体选择 → 升级到 decision-research"；decision-research Loop 合约"目标变成长期知识沉淀 → 转交 research-topic-compiler"。Radar Loop 合约还有显式 escalate 规则（出现实际决策/竞争选项时转 decision-research）。
- decision-research 内嵌四技能对比表（前提/时间尺度/输出/终止条件）。

具体重叠（需要收敛）：

- research-topic-compiler 的 **Product Candidate Research mode**（多源竞品研究 → 候选池评分 → cross-session handoff）与 decision-research 的 **Top-Down Product Research Mode**（行业叙事 → 用户角色 → 场景 → 能力 → 实现 → 商业包装六层递进）功能区间高度重合。当前唯一区分是持久化诉求，这对路由器来说信号太弱。

**建议（本轮不改）**：二选一——(a) 把 compiler 的 Product Candidate mode 重定义为"为 decision-research 准备候选池输入的预研模式"，终选职责显式让渡；(b) 删除该模式，需求直接路由到 decision-research，长期沉淀需求由 handoff 机制回流 compiler。倾向 (a)，因为 cross-session-handoff 机制已存在。优先级 P1。

### 冲突 3：prd-architect vs prd-review

**应有边界**：prd-architect = 生成/修订 PRD；prd-review = 审查 PRD 是否可交付。

**当前体现情况：清晰，仅需小修。两个担忧均不成立。**

- **architect 是否承担了过多评审职责？否。** 它的 readiness 判断（待确认项 ≥3 → 继续深化而非进 ui-mockup）是对自己产物下一站的流程把控，没有 findings/严重度/三视角等评审要素；且显式声明"已有完整 PRD 要评审 → prd-review"。
- **review 是否承担了过多生成职责？否（受控）。** 修订草案被三重约束：最小可替换块原则、"未经要求不重写整份 PRD 成终稿"禁令、"不凭空生成完整方案"禁令。Reviewer 输出可回填补丁属于"给出怎么改"，不越界。

残留小问题：双方的修订循环（review 出补丁 → architect 回填 → review 复查）只存在于 Loop 合约的隐含逻辑中，architect 侧没有声明"消费 revision_draft.md 回填"的义务。优先级 P2。

### 冲突 4：grill-me vs prd-review

**应有边界**：grill-me = 方案层压力测试；prd-review = 交付物层标准化评审。

**当前体现情况：机制差异客观成立，文件互联为零。**

差异成立的证据：grill-me 是开放式一问一答、输出决策记录、无固定清单；prd-review 是封闭式三视角清单、输出 findings + 三态判决。二者从输入（方案 vs 文档）、过程（对话 vs 清单）、输出（共识快照 vs 判决）三个维度都不同。

失效风险：

- 两边文件零互引。用户说"帮我挑挑这个 PRD 的毛病"时，路由可能落到 grill-me（它接受 PRD 作为 Context Intake 输入源），但正确答案是 prd-review。
- prd-review 在评审中发现"问题不在文档而在方案思路"时，唯一出口是"Pause and ask the user"，没有"建议走一轮 grill-me"的协议。
- PRD Readiness Loop 合约完全没把 grill-me 列为节点——意味着 PRD 工作流里方案层压测只能靠用户自发调用。

**建议（本轮不改）**：grill-me 增加"要标准化评审 → prd-review"转出；prd-review 增加"根本问题在方案 → grill-me"转出；PRD Readiness Loop pattern 中注册 grill-me 为可选前置/插入 Critic 节点。优先级 P1。

### 冲突 5：是否缺少 Router / Gate

**结论：缺，但缺的是"资产化分层判断"，不是"Skill 间路由"。**

已有的 Gate 能力（分散且未整合）：

- SKILL_ROUTING.md：静态按阶段路由表 + Loop 启用条件 + 反过度 Loop 化回退规则——审计时覆盖了"7 个 Skill 选哪个"；实施后已扩展为 8 个 Skill。
- calibration 的 L1-L4 层级判断：覆盖了"协作多深"。
- prd-review 的三态判决：覆盖了"PRD 工作流出口"。
- decision-research 的 R00 Framing Gate：覆盖了"调研入口框定"。

缺失的能力：没有任何机制回答——

```text
这个任务 / 这次成功的协作，应该沉淀到哪一层？
Prompt / Context Pack / Workflow / Skill / Loop / System？
值不值得资产化？现在做还是观察重复率？
```

calibration 的 references/ 里有 asset-capture 模式线索，但只是脑暴的附属动作，不是独立判断流程。

**建议（本轮不新增）**：新增 `ai-work-assetization-diagnoser` Skill，定位为纯 Router/Gate：输入是"一段工作/一个重复出现的任务"，输出是分层判定（沉淀到哪层）+ 理由 + 不沉淀的成本。它同时可以承担 Loop 启动前的 Gate（替代散落在 SKILL_ROUTING.md 中的 Loop 启用条件判断）。优先级 P2——P1 的边界互引完成后再做，否则路由器建在不稳的边界上。

---

## 6. Loop Pattern Readiness

总前提：本仓库的 Loop 定义为"围绕一个明确目标，把多个 Skill 组织成 *定义问题 → 生成/研究 → 挑战 → 修正 → 评审 → 再修正 → 停止/交还人* 的有状态闭环"，而非单个 Skill 长时间运行。按此定义，**当前三个 Loop Extension 合约都只是"单 Skill 有状态运行"，多 Skill 闭环层（loop-patterns/）整体缺失。**

### 6.1 PRD Readiness Loop

目标闭环：calibration → grill-me → [decision-research] → prd-architect → grill-me → architect 修订 → prd-review → architect 回归修复 → prd-review 复查 → Ready / Not ready / Human decision。

| 检查项 | 现状 |
|---|---|
| 是否应先挑战方案思路再输出 PRD | **应该**。当前链条（superpowers-comparison.md 的 7 步链）把 grill-me 放在 prd-review 之后压测"最终方案"——太晚了。方案层错误在 PRD 写成之后修复成本陡增。建议双 grill-me 点位：PRD 起草前挑战方案方向（重）、PRD 重大修订后挑战新方向（轻、可选） |
| calibration 与 grill-me 在前置阶段如何分工 | calibration 负责"问题是否真实、框定是否正确"（产出问题共识），grill-me 负责"基于该问题的方案方向能不能成"（产出决策记录）。顺序固定：calibration 先、grill-me 后；calibration 的 Done Signal 是 grill-me 的进入条件 |
| prd-review 停止条件是否足够明确 | **基本明确**：7 条停止条件 + 三态判决 + 升级人工的 5 种情形，且三态判决对齐 Superpowers implementation-plan-readiness。缺口：无最大轮数、无"连续 N 轮 blocker 不下降 → 强制 Human decision"的发散保护 |
| 是否需要维护 PRD Loop State | **已有 80%**：prd-readiness-loop-contract.md 定义了 8 个状态文件。缺的 20%：grill-me 决策记录的引用槽位、回边计数（第几次回归修复）、跨 Skill 状态目录约定（当前状态文件只服务 prd-review 单方） |
| 是否需要新增 loop-patterns/prd-readiness-loop.md | **需要（P1，三个 pattern 中最优先）**。它是用户工作流的主干，且所需材料最齐：Reviewer 主体 + 状态文件 + 三态出口都已存在，只缺把 calibration / grill-me / architect 编排进来的 pattern 文件 |

**就绪度：中高。** 单 Skill 闭环（review → 修订 → 复查 → 判决）今天就能跑；多 Skill 闭环缺前置链编排和 Critic 节点。

### 6.2 Decision Research Loop

目标闭环：calibration → decision-research 建 Research Map → grill-me 挑战研究设计 → decision-research 搜证/反证 → grill-me 挑战阶段结论 → decision-research 修正 → 有立场推荐 / PoC / 停止 / 交还。

| 检查项 | 现状 |
|---|---|
| decision-research 是否已具备 Framing、假设、反证、漂移检查、收敛条件 | **全部具备**：R00 Framing Gate、假设矩阵（含 5 态状态机）、R06 反证搜索、Scope Drift Checkpoint + scope_drift_log、三类收敛条件（三角收敛/信息饱和/暗知识缺口）+ ROI fuse + Human Gate。是全仓库 loop-readiness 最高的 Skill |
| grill-me 应在调研前还是调研后 | **两个可选点位都要，但默认只开第一个**：(1) Research Map 建立后、搜证前——挑战研究设计（决策问题对不对、假设枚举全不全），成本低收益高；(2) 阶段结论形成后——挑战收敛质量。注意第二点与内置反证机制部分重复，应定位为"高风险决策才开启"的可选节点，避免双重 Critic 拖慢收敛 |
| 是否需要维护 Decision Research State | **已有**：6 个状态文件齐备，无需新增；只需在 pattern 文件中给 grill-me 决策记录留引用槽位 |
| 是否需要新增 loop-patterns/decision-research-loop.md | **需要（P2）**。增量最小——本质是给现有合约加 2 个可选 Critic 检查点和 calibration 入口约定 |

**就绪度：高（单 Skill 维度全仓库第一）。** 缺的只是薄薄一层 pattern 文件。

### 6.3 Research Radar Loop

目标闭环：compiler 建研究项目 → grill-me 挑战研究地图 → compiler 扫描新资料 → 更新 Evidence Matrix / Update Log → grill-me 挑战阶段结论 → 需要决策时转 decision-research → 继续 / 暂停 / 停止。

| 检查项 | 现状 |
|---|---|
| research-topic-compiler 是否适合长期主题跟踪 | **适合**：Radar Mode (L5) + 00-09 文件结构 + watchlist + 更新日志 + 跨会话恢复，正是为此设计 |
| Radar Mode 是否已足够清晰 | **机制清晰，入口偏挤**：信号 8 分类、弱信号防漂移（只进更新日志、矛盾证据标 needs-human-review、no-op 也记录）、6 条暂停条件、5 类升级人工规则都已成文。问题在于 Radar Mode 埋在一个含 5 种模式的大 SKILL.md 里，模式判别成本高 |
| 是否需要新增 Research Radar State | **不需要新增**：00-09 + 09_更新日志 就是 Radar State。escalate 到 decision-research 的边也已成文（出现实际决策/竞争选项/方向选择时） |
| 是否需要新增 loop-patterns/research-radar-loop.md | **需要但不急（P2-P3）**。grill-me 在此 loop 中价值密度最低——长周期低频扫描场景下，"挑战研究地图"做一次（建项时）即可，不需要每轮；建议 pattern 中只设一个一次性 Critic 点位 + 按需触发条件（如连续 3 轮结论无变化时挑战 watchlist 是否失效） |

**就绪度：中高。** 主要欠缺是 Critic 约定和模式入口简化，机制本身完整。

### 6.4 AI Work Assetization Loop（缺口分析）

目标闭环（仓库当前完全没有）：识别重复工作 → 判断沉淀层级（Prompt / Workflow / Skill / Loop / System）→ 生成资产草稿 → 试用 → 复盘 → 升级或废弃。

现状：calibration 有 asset-capture 模式线索（脑暴产物的资产化提示），SKILL_REGISTRY 有 core/active/review 状态字段（资产生命周期的雏形），但没有判断流程、没有 Router Skill、没有 loop。

结论：这个 loop 依赖先有 `ai-work-assetization-diagnoser`（Gate 节点），属于 P2 序列；本轮只确认缺口，不展开设计。

---

## 7. Recommended Repository Structure

建议的目标结构（**本轮不实施**）：

```text
ai-product-manager-skills/
├── README.md
├── SKILL_REGISTRY.md
├── SKILL_ROUTING.md            # 增补：跨 Skill 判别规则（冲突 1/4 的判别问句）、四技能对比表上提
├── AGENTS.md                   # 新增（P2）：编排入口——角色模型、loop-patterns 索引、
│                               #   状态目录约定、停止/交还人总则、反过度 Loop 化规则
├── loop-patterns/              # 新增（P1 起步）：多 Skill 编排层
│   ├── prd-readiness-loop.md          # P1：主干工作流，材料最齐
│   ├── decision-research-loop.md      # P2：增量最小
│   └── research-radar-loop.md         # P2-P3
├── ai-work-assetization-diagnoser/    # 新增（P2）：Router/Gate Skill
│   └── SKILL.md
├── ai-collaboration-calibration/      # 保留；P1 小修（互引 grill-me）
├── grill-me/                          # 保留；P1 小修（互引 + 最小输出契约）
├── decision-research/                 # 保留；references/decision-loop-contract.md 不动
├── research-topic-compiler/           # 保留；P1 收敛 Product Candidate mode
├── prd-architect/                     # 保留；P2 小修（上游前提声明）
├── prd-review/                        # 保留；references/prd-readiness-loop-contract.md 不动
└── ui-mockup-desktop-workbench/       # 保留；P3
```

关键设计决定：

1. **现有 3 个 references/ 内的 loop contract 保留原位、不迁移**。它们是"单 Skill 如何有状态运行"的实现细节，归属各 Skill；loop-patterns/ 是"多 Skill 如何组成闭环"的编排约定，引用而不取代它们。两层分离符合现有"Loop Extension 不是新 Skill 入口"的定位声明。
2. **AGENTS.md 定位为薄索引而非厚规范**：角色模型一页、loop-patterns 索引、共享状态目录约定（建议 `.loop-state/<loop-name>/`）、全局停止总则。厚内容留在各 pattern 文件。
3. **loop-patterns 文件的最小结构**：目标 → 节点表（Skill × 角色 × 进入/退出条件）→ 回边定义 → 状态文件清单（引用各 contract）→ 停止/交还人条件 → 轮数上限与发散保护。

---

## 8. Recommended Changes

### P0（必须先改，否则影响整体路由）

**无。** 审查未发现影响运行时路由正确性的阻断级问题。README / REGISTRY / ROUTING 一致，审计快照中的 7 个 Skill 边界整体可用。

### P1（建议尽快改）

| # | 改动 | 涉及文件 |
|---|---|---|
| 1 | 修复旧研究 Skill 名残留，统一到 `decision-research` | `.github/ISSUE_TEMPLATE/skill_request.md`（不影响运行时路由，但属对外可见的命名不一致） |
| 2 | calibration ↔ grill-me 双向互引 + 共享判别规则（"方案针对的问题是否已确认？"），grill-me 同时增加 → prd-review 转出 | `ai-collaboration-calibration/SKILL.md`、`grill-me/SKILL.md`、`SKILL_ROUTING.md` |
| 3 | 收敛 research-topic-compiler 的 Product Candidate Research mode 与 decision-research 的 Top-Down Product Research Mode 重叠（推荐方案 (a)：compiler 降级为预研/候选池模式，终选让渡） | `research-topic-compiler/SKILL.md`、`decision-research/SKILL.md` |
| 4 | prd-review ↔ grill-me 互引（"根本问题在方案 → grill-me"） | `prd-review/SKILL.md`、`grill-me/SKILL.md` |
| 5 | 新增 `loop-patterns/prd-readiness-loop.md`：编排 calibration → grill-me →（可选 decision-research）→ prd-architect → grill-me（轻）→ prd-review ⇄ architect → 三态出口；补轮数上限/blocker 不收敛升级规则；为 grill-me 定义最小输出契约 | 新文件 + `grill-me/SKILL.md` |

### P2（可以后续优化）

| # | 改动 | 涉及文件 |
|---|---|---|
| 6 | 新增 `AGENTS.md`（薄索引：角色模型、loop 索引、状态目录约定、停止总则） | 新文件 |
| 7 | 新增 `ai-work-assetization-diagnoser/`（Router/Gate Skill：Prompt/Workflow/Skill/Loop/System 分层判定） | 新目录 |
| 8 | 新增 `loop-patterns/decision-research-loop.md`（2 个可选 grill-me 检查点 + calibration 入口） | 新文件 |
| 9 | prd-architect 增加上游前提声明（方向未定 → calibration/grill-me/decision-research）+ 回填 revision_draft 义务 | `prd-architect/SKILL.md` |
| 10 | decision-research 的四技能对比表上提/复制到 SKILL_ROUTING.md | `SKILL_ROUTING.md` |
| 11 | research-topic-compiler 模式拆分（Concept Lens / Learning Pack 移入 references/，主文件只留模式路由表） | `research-topic-compiler/` |

### P3（暂不需要改）

| # | 改动 |
|---|---|
| 12 | `loop-patterns/research-radar-loop.md`（一次性 Critic 点位 + 按需触发） |
| 13 | prd-architect ↔ ui-mockup-desktop-workbench 的 mockup 职责分界成文 |
| 14 | ui-mockup 接入 PRD Loop 的"mockup 发现缺口 → 回 prd-review"回边 |

---

## 9. Do Not Change Yet

本轮明确**不建议**做的事（防止过度设计）：

1. **不重写任何 SKILL.md**。P1 的互引改动都是"加几行边界规则"，不是重写；审计快照中的 7 个 Skill 的主体设计都应保留。
2. **不动现有 3 个 loop contract**（decision-loop / research-radar-loop / prd-readiness-loop）。它们质量较高，未来 loop-patterns/ 引用它们即可。
3. **不删除、不合并任何 Skill**。包括看似重叠的 Product Candidate mode——先收敛边界声明，观察实际使用后再决定是否删模式。
4. **本轮不新建 loop-patterns/、AGENTS.md、ai-work-assetization-diagnoser/**（任务约束；且 P1 边界互引应先于编排层落地，否则 pattern 建在模糊边界上）。
5. **不给 grill-me 增加状态机制**。它的价值在于无状态纯 Critic；loop 状态由 loop pattern 和主体 Skill 持有，不下放给 Critic 节点。
6. **不把 SKILL_ROUTING.md 改造成自动路由器**。静态路由表 + 判别问句已够用；自动化路由等 ai-work-assetization-diagnoser 设计成熟后再考虑。
7. **不为 ui-mockup-desktop-workbench 做任何改动**（P3 全部可等）。

---

## 10. Next Step Proposal

建议按以下顺序执行（每步可独立交付、独立验证）：

**Step 1 — 边界修补包（P1 #1-#4，约一次提交）**
修旧研究 Skill 名残留；calibration ↔ grill-me、prd-review ↔ grill-me 互引；SKILL_ROUTING.md 加两条判别问句；收敛 Product Candidate mode 声明。
验证：用第 5 章冲突 1 的 4 个歧义场景做路由演练，确认每个场景有唯一确定路由。

**Step 2 — 第一个 Loop Pattern（P1 #5）**
新增 `loop-patterns/prd-readiness-loop.md`，同时给 grill-me 定义最小输出契约。
验证：拿一个真实需求从 calibration 走到 Ready for writing-plans，检查每个节点的进入/退出条件是否可判定、状态文件是否完整、回边是否可执行。

**Step 3 — 编排层骨架（P2 #6、#8）**
新增 AGENTS.md（薄索引）+ decision-research-loop.md。
验证：AGENTS.md 能在一屏内回答"我现在该用哪个 Skill / 哪个 Loop"。

**Step 4 — Router 角色（P2 #7、#10）**
设计并新增 ai-work-assetization-diagnoser；四技能对比表上提。
验证：用 5 个历史任务（含不该资产化的反例）测试分层判定的一致性。

**Step 5 — 长尾优化（P2 #9、#11，P3 全部）**
按需推进，无截止压力。

---

*附注：本报告基于审计快照中的全部 7 个 SKILL.md、全部 references/（含 3 个 loop contract）、README / SKILL_REGISTRY / SKILL_ROUTING、docs/、examples/ 的完整阅读。引用的行号以审查日（2026-06-11）的仓库状态为准；实施后的当前发布口径见 README / Registry / Routing。*
