# Skill Overlap Audit v0.2.1

日期：2026-08-04
仓库：`PANGKAIFENG/ai-product-manager-skills`
分支：`v0.2.1-skill-dedup`
审计基线：`v0.2.0` / `011e57f`
评审模式：full overlap and routing audit

## 1. 结论

当前 13 个 Skill 中，没有发现可以仅凭现有证据直接合并、删除或进入废弃流程的 Skill。

本轮看到的主要问题不是“存在大量重复 Skill”，而是三类治理风险：

1. `description` 中的宽触发词会让相邻 Skill 在 clean-context 下竞争，最高风险集中在 `competitive-analysis` / `decision-research` 和 `complex-exploration` / `decision-research`。
2. `prd-architect`、`ui-wireframe-to-html`、`ui-mockup-desktop-workbench` 的 `evals.json` 仍是旧格式，没有机器可读的 `should_trigger` 和 `expected_route`；部分相邻 Skill 也只有 1 条 non-trigger case，低于仓库文档建议的最低覆盖。
3. `prd-architect` 与 `prd-review` 有 3 份 byte-identical 资源，但它们是 self-contained 单 Skill 分发策略下的有意副本，仓库审计已经提供 parity gate。当前不应抽成仓库级共享依赖。

目录层面应继续保持 `skills/<skill-id>/` 的平级安装结构。不要为了视觉上减少目录数量，把拥有独立用户目标、输入输出和完成条件的 Skill 强行折叠成父子目录。

**Verdict：Needs revision。** Catalog 的能力边界总体成立，当前不需要删除 Skill；下一阶段应优先补路由回归和收窄少数 trigger contract，再用真实误触发证据决定是否需要合并。

## 2. 审计边界

本轮只审计：

- trigger / non-trigger 边界
- 输入、工作流、输出和完成条件重叠
- 资源文件的精确重复与同名异义
- `evals/evals.json` 对相邻 Skill 路由的覆盖
- registry / routing 文档是否能解释相邻能力

本轮不做：

- 不修改 `skills/*`
- 不合并、不删除、不重命名 Skill
- 不改变现有运行行为
- 不执行本地 `skillshare sync`
- 不覆盖本地安装目录

## 3. Evidence Summary

- Files inspected：13 个 `skills/*/SKILL.md`、13 个 `skills/*/evals/evals.json`、`SKILL_REGISTRY.md`、`SKILL_ROUTING.md`、`docs/eval-schema.md` 和 `scripts/audit_skills.py`。
- Deterministic checks：全仓 SHA-256 重复扫描、同名文件差异检查、eval 正反例/路由字段统计、Skill 行数和资源数量统计、PRD 副本 parity gate 检查。
- Review mode：full overlap and routing audit。
- Evidence limits：本轮没有调用真实模型对所有 prompt 做 clean-context 路由执行，因此 routing risk 分数属于基于 metadata、body boundary 和 eval coverage 的设计判断；没有读取 60 个 research fixture 的全部正文，因为它们不影响本轮 Skill 去重结论。
- Assumptions：当前仍支持单 Skill 独立安装与 symlink 分发；如果未来改成只能整仓安装，共享资源策略需要重新评估。

## 4. Catalog Scorecard

| Dimension | Score | Notes |
| --- | ---: | --- |
| Necessity and boundary | 4/5 | 13 个 Skill 均有独立用户目标；少数相邻 trigger 仍需收窄。 |
| Trigger contract | 3/5 | body 路由较清楚，但 `decision-research` 等 metadata 仍偏宽。 |
| Input/output contract | 4/5 | 大多数 Skill 有明确输入、输出和 Definition of Done。 |
| Workflow gates and degrees of freedom | 4/5 | PRD、UI、研究链路均有阶段门和转交条件。 |
| Progressive disclosure and assets | 4/5 | 资源组织成熟；个别主 `SKILL.md` 仍超过 290 行。 |
| Context budget | 3/5 | `research-topic-compiler`、`prd-architect`、UI mockup 主入口较重。 |
| Tool and safety boundary | 4/5 | 浏览器、GitHub 发布、UI 项目写入均有权限/副作用限制。 |
| Evaluation readiness | 3/5 | 13 个 Skill 都有 eval 文件，但 3 个仍是旧路由格式，多组 paired eval 不足。 |
| Maintainability and governance | 4/5 | catalog、routing、审计门和 PRD parity gate 已形成；最低路由覆盖尚未进入 CI。 |

平均分：`3.7/5`。无 P0，但存在需要进入下一阶段的 P1 路由与 eval 治理项。

## 5. 判定标准

每对 Skill 使用 0-5 分评估六个维度。分数越高表示重叠或风险越高，不代表质量越差。

| 维度 | 0 分 | 5 分 |
| --- | --- | --- |
| Trigger overlap | 自然语言触发完全不同 | 同一用户表达很难稳定分流 |
| Input overlap | 输入对象不同 | 几乎消费同一类输入 |
| Workflow overlap | 执行路径不同 | 核心步骤基本相同 |
| Output overlap | 交付物不同 | 交付物和完成条件基本相同 |
| Resource duplication | 无共享内容 | 大量资源 byte-identical 或语义同构 |
| Routing risk | clean-context 下几乎不会竞争 | metadata 层很可能竞争 |

结论标签：

- `保留`：拥有独立用户目标、输入输出或完成条件。
- `保留但收窄 trigger`：能力独立，但 metadata 过宽。
- `合并资源`：Skill 保留，只治理共享资源。
- `并入父 Skill`：能力只是父流程 helper，不能形成独立用户目标。
- `进入废弃评估`：长期没有独立触发价值，且被另一个 Skill 完整覆盖。

## 6. 重叠矩阵

| 组 | Skill pair | Trigger | Input | Workflow | Output | Resource | Routing risk | 结论 |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 问题与方案 | `ai-collaboration-calibration` / `brainstorming` | 3 | 2 | 2 | 1 | 0 | 3 | 保留；以“问题是否已经成立”分流 |
| 问题与方案 | `ai-collaboration-calibration` / `complex-exploration` | 3 | 3 | 3 | 2 | 0 | 4 | 两者保留；收窄复杂背景相关 trigger |
| 问题与方案 | `brainstorming` / `complex-exploration` | 2 | 2 | 3 | 2 | 0 | 3 | 保留；以“比较方案”与“规划复杂探索”分流 |
| 探索与决策 | `complex-exploration` / `decision-research` | 4 | 3 | 3 | 2 | 0 | 4 | 保留；问题重构/探索规划 vs 最终推荐，需收窄 trigger |
| 探索与研究 | `complex-exploration` / `research-topic-compiler` | 3 | 3 | 3 | 2 | 0 | 3 | 保留；探索框架 vs 系统证据工程 |
| 研究与决策 | `research-topic-compiler` / `competitive-analysis` | 3 | 3 | 3 | 2 | 1 | 4 | 保留；候选池/系统认知 vs 竞品决策简报 |
| 研究与决策 | `research-topic-compiler` / `decision-research` | 4 | 3 | 4 | 3 | 1 | 4 | 保留；长期认知/候选池 vs 最终选择 |
| 研究与决策 | `competitive-analysis` / `decision-research` | 4 | 4 | 4 | 4 | 1 | 5 | 暂时保留；paired clean-context eval 后复核 |
| PRD 链路 | `prd-architect` / `prd-review` | 1 | 4 | 2 | 3 | 4 | 2 | 保留；三份资源副本继续做 parity gate |
| PRD 链路 | `prd-review` / `prd-to-issues` | 2 | 5 | 2 | 2 | 1 | 2 | 保留；readiness verdict vs issue backlog |
| PRD 链路 | `prd-review` / `grill-me` | 3 | 4 | 2 | 2 | 1 | 3 | 保留；artifact readiness vs 方案压力测试 |
| PRD 链路 | `prd-architect` / `prd-to-issues` | 1 | 3 | 1 | 1 | 0 | 1 | 保留 |
| PRD 链路 | `prd-architect` / `grill-me` | 2 | 3 | 1 | 1 | 0 | 2 | 保留 |
| PRD/UI 编排 | `prd-architect` / `ui-mockup-desktop-workbench` | 2 | 4 | 4 | 4 | 2 | 3 | 保留；这是页面型 PRD 的有意编排，不是重复 Skill |
| PRD/UI 编排 | `prd-architect` / `ui-wireframe-to-html` | 2 | 3 | 3 | 3 | 1 | 2 | 保留；PRD 起草 vs structure-only artifact |
| UI 链路 | `ui-wireframe-to-html` / `ui-mockup-desktop-workbench` | 4 | 5 | 5 | 3 | 2 | 4 | 保留；这是有意的阶段组合，不是重复 Skill |
| UI 链路 | `brainstorming` / `ui-wireframe-to-html` | 2 | 2 | 2 | 2 | 1 | 2 | 保留；design spec vs 低保真结构 artifact |
| UI 链路 | `brainstorming` / `ui-mockup-desktop-workbench` | 2 | 2 | 2 | 2 | 1 | 3 | 保留；方案确认 vs 高保真交付 |
| 资产化 | `complex-exploration` / `ai-work-assetization-diagnoser` | 3 | 4 | 2 | 3 | 0 | 4 | 两者保留；收窄“资产沉淀”用语并补 paired eval |

## 7. 分组分析

### 7.1 `ai-collaboration-calibration` / `brainstorming` / `complex-exploration`

三个 Skill 都可能被“帮我想想”“脑暴”“先别直接做”触发，但负责的阶段不同：

| Skill | 前提 | 核心动作 | 完成信号 |
| --- | --- | --- | --- |
| `ai-collaboration-calibration` | 问题、目标、约束或判断标准还不稳定 | 显化假设、重定义问题、定位真正目标 | 真实问题与判断标准可被确认 |
| `brainstorming` | 问题基本成立，方案尚未确定 | 比较 2-3 个设计路径并收敛 design spec | 用户确认设计或留下显式待确认项 |
| `complex-exploration` | 已经是复杂、多轮、不能一次答完的探索任务 | 定题、规划探索、建立中间产物、复盘迭代 | 探索路径成立，或完成复盘/方法论沉淀 |

直接证据：

- `skills/ai-collaboration-calibration/SKILL.md:4-11` 同时包含“问题脑暴”和复杂背景主动触发，`93-98` 才给出退出与转交规则。
- `skills/brainstorming/SKILL.md:29-38` 明确按问题成熟度分流，`163-192` 给出完成条件和相邻 Skill 的 non-trigger。
- `skills/complex-exploration/SKILL.md:20-33` 已写明校准、方案比较、系统研究和资产诊断的转交，`144-155` 也定义了完整 handoff。

风险：`ai-collaboration-calibration` 的“背景复杂时主动识别”与 `complex-exploration` 的“复杂、不确定、多轮”在 metadata 层仍可能竞争；`complex-exploration` 当前只有 1 条 non-trigger eval，尚未直接覆盖 calibration、brainstorming 和 assetization 三个邻居。

结论：三个 Skill 都保留。后续只收窄触发描述并增加 paired routing eval，不合并。

### 7.2 `complex-exploration` / `research-topic-compiler` / `decision-research`

`complex-exploration` 的策略、Roadmap、定价和竞品定位触发词，会与研究和决策 Skill 竞争；三者的稳定边界应落在交付责任，而不是主题名：

| Skill | 交付责任 | 完成信号 |
| --- | --- | --- |
| `complex-exploration` | 重构问题、暴露假设、选择探索框架并规划中间产物 | 真正问题和探索路径成立，可转交研究或决策 |
| `research-topic-compiler` | 系统收集证据、建立证据矩阵、候选池或长期研究资产 | 研究达到证据门槛，并形成可复用 handoff |
| `decision-research` | 消费已有证据，对明确候选项给最终推荐和排除理由 | 推荐、置信度和颠覆条件可执行 |

直接证据：

- `skills/complex-exploration/SKILL.md:20-33` 把系统证据收集转给 `research-topic-compiler`，`144-155` 把最终方案推荐转给 `decision-research`。
- `skills/research-topic-compiler/SKILL.md:110-112` 只负责候选池和决策输入，明确把最终选择转给 `decision-research`。
- `skills/decision-research/SKILL.md:91-99` 要求问题已定义或可快速框定，并以最终选择为交付责任。

风险：`skills/complex-exploration/SKILL.md:3` 的 metadata 直接覆盖策略、定价、Roadmap 和竞品定位，却没有把“先重构问题与规划探索”和“已有明确决策问题”写成最短分流条件。短 prompt 仍可能与 `decision-research` 竞争；与 `research-topic-compiler` 的竞争次之。

结论：三个 Skill 都保留。先为两组 pair 增加只改变任务阶段的 clean-context routing eval，再收窄 `complex-exploration` trigger；没有持续误触发证据前不合并。

### 7.3 `research-topic-compiler` / `competitive-analysis` / `decision-research`

这组是当前最高路由风险，但仍不是三个重复 Skill：

| Skill | 决策责任 | 典型输出 |
| --- | --- | --- |
| `research-topic-compiler` | 建立认知、证据体系、候选池或长期研究资产 | Research Project、Evidence Matrix、Candidate Backlog、Dashboard |
| `competitive-analysis` | 把竞品/替代方案证据转成我方产品动作 | Product Decision Brief、Copy/Adapt/Avoid、验证建议 |
| `decision-research` | 对明确决策给最终推荐并排除其他选项 | Recommendation、排除理由、置信度、颠覆条件 |

直接证据：

- `skills/research-topic-compiler/SKILL.md:4-12` 覆盖系统研究、Roadmap 输入和决策看板，但明确把最终选择交给 `decision-research`；`182-196` 只产出候选池与 handoff。
- `skills/competitive-analysis/SKILL.md:34-43` 区分取证层、产品层、决策层和研究层；`110-119` 明确竞品池、竞品简报和最终选型的三段路由。
- `skills/decision-research/SKILL.md:4-13` 仍包含“帮我调研”“行业怎么做”“竞品定位等所有需要做决定的调研”等宽触发；`91-99` 的 body 边界比 metadata 更清楚。

风险：`competitive-analysis` 默认输出本身含 `Recommendation`，而 `decision-research` 又包含 `competitive-decision` mode。clean-context 只看到 description 时，“分析三个竞品并告诉我们要不要做”很容易竞争。

结论：`research-topic-compiler` 保留；`competitive-analysis` 与 `decision-research` 暂时保留，待 paired clean-context eval 复核。先用仅改变“证据是否已齐”的对抗样例验证边界，再决定是否收窄 `decision-research` trigger 或进入合并评估。

### 7.4 `prd-architect` / `prd-review` / `prd-to-issues` / `grill-me`

这组共享 PRD 输入，但交付责任按状态机分离：

`方案压力测试 -> PRD 起草 -> PRD readiness 评审 -> issue backlog`

- `prd-architect` 负责选择 PRD 类型并起草或修订内容，不给 readiness verdict。
- `prd-review` 负责 findings、revision draft 和 `Implementation-Plan Readiness`。
- `prd-to-issues` 负责 vertical-slice issue backlog、coverage matrix 和发布确认。
- `grill-me` 评审的是 PRD 背后的方案，不评审 artifact readiness。

四个 Skill 在 `SKILL_ROUTING.md:108-154` 和各自 SKILL body 中已经形成双向边界。`prd-review` 与 `grill-me` 也有互相指向的 non-trigger eval。

结论：全部保留。唯一真实文件重复是三份 PRD 资源副本，按 self-contained 分发策略治理，不把 Skill 合并。

### 7.5 `prd-architect` / `ui-wireframe-to-html` / `ui-mockup-desktop-workbench` / `brainstorming`

`prd-architect` 会为页面型 PRD 自动编排 UI 证据交付，`ui-mockup-desktop-workbench` 又明确吸收了 wireframe discipline，因此输入、工作流和输出有意重叠。但它们的完成责任不同：`prd-architect` 收口 PRD 与证据链，mockup Skill 负责正式视觉交付，wireframe Skill 则允许用户只完成结构阶段并停止。

直接证据：

- `skills/prd-architect/SKILL.md:28-59` 对页面型 PRD 自动激活 mockup handoff，并由 PRD Skill 负责触发、收口和验收，不把 mockup 责任重新实现一遍。
- `skills/ui-wireframe-to-html/SKILL.md:20-40` 明确它是 structure-only entrypoint，并规定高保真 Skill 已激活时不要单独调用。
- `skills/ui-mockup-desktop-workbench/SKILL.md:35-45` 明确完整链路内部包含结构阶段，但只做低保真时转回 wireframe Skill。
- `skills/brainstorming/SKILL.md:29-38` 的输出是 design spec 和方案确认，不是页面 artifact。

结论：四个 Skill 都保留。PRD/UI 是 intentional orchestration；线框 Skill 也不是应并入父 Skill 的 helper，因为“只做结构并在这里停止”本身是独立、可验证的用户目标。UI pair 没有 byte-identical 资源，Resource 分仅反映少量结构纪律和模板语义复用。

### 7.6 `complex-exploration` / `ai-work-assetization-diagnoser`

两者都使用“资产”一词，但资产对象不同：

- `complex-exploration` 的 Asset Mode 沉淀本次复杂探索里的认知、结构、方法论、工具和影响力资产。
- `ai-work-assetization-diagnoser` 判断一段重复 AI 工作应该落到 Prompt、Context Pack、Workflow、Skill、Loop、System，或不应资产化。

风险来自用户只说“把这次过程沉淀成资产”时，metadata 不能判断用户要内容复盘还是资产层级诊断。`skills/complex-exploration/SKILL.md:31` 和 `144-155` 已经给出转交规则，但双方 eval 都缺少这一对相邻场景。

结论：两者保留。后续在 trigger 里增加“探索内容/方法论沉淀”与“AI 工作资产层级判断”的最短区分，并新增 paired eval。

## 8. 文件级重复审计

SHA-256 扫描只发现 3 组 byte-identical 文件，全部位于 `prd-architect` 与 `prd-review`：

| 文件 | 单份大小 | 结论 |
| --- | ---: | --- |
| `skills/prd-architect/scripts/check_prd_shape.py` + `skills/prd-review/scripts/check_prd_shape.py` | 14,928 bytes | 有意副本，审计脚本检查 parity |
| `skills/prd-architect/scripts/validate_drawio.py` + `skills/prd-review/scripts/validate_drawio.py` | 2,411 bytes | 有意副本，审计脚本检查 parity |
| `skills/prd-architect/references/drawio-templates.md` + `skills/prd-review/references/drawio-templates.md` | 5,391 bytes | 有意副本，审计脚本检查 parity |

第二份副本合计增加 22,730 bytes。这个成本小于拆出共享目录后对单 Skill 安装、自包含 symlink 和跨 runtime 分发造成的复杂度。

`scripts/audit_skills.py:45-49` 显式登记三份副本，`190-199` 在缺失或 byte drift 时失败。因此当前治理方式是“保留副本 + CI 防漂移”，不是未治理的复制粘贴。

同名但内容不同的文件不属于重复：

- `skills/*/references/prd-shape-gates.md`
- `skills/*/references/mode-selection.md`
- `skills/*/references/provenance.md`
- `skills/*/agents/openai.yaml`
- 各 Skill 的 `skills/*/evals/evals.json`

这些文件的 SHA-256 均不同，职责也属于各自 Skill。不能只按 basename 合并。

## 9. Eval 路由覆盖

仓库级 `docs/eval-schema.md` 建议每个 active Skill 至少有 2 条 trigger、2 条 non-trigger/handoff 和 1 条 known-risk case。当前统计：

| Skill | Cases | Machine-readable trigger | Machine-readable non-trigger | Unclassified | 结论 |
| --- | ---: | ---: | ---: | ---: | --- |
| `ai-collaboration-calibration` | 3 | 2 | 1 | 0 | 缺 brainstorming / complex handoff |
| `ai-work-assetization-diagnoser` | 3 | 2 | 1 | 0 | 缺 complex-exploration handoff |
| `brainstorming` | 4 | 2 | 2 | 0 | 基础边界可用 |
| `competitive-analysis` | 4 | 2 | 2 | 0 | 基础边界可用，仍需 ambiguous competitor-decision case |
| `complex-exploration` | 3 | 2 | 1 | 0 | 缺 calibration / brainstorming / assetization paired cases |
| `decision-research` | 6 | 4 | 2 | 0 | 基础边界可用，需和 competitive-analysis 做对抗样例 |
| `grill-me` | 3 | 2 | 1 | 0 | 与 PRD review 边界已有覆盖，数量仍低于建议 |
| `prd-architect` | 10 | 0 | 0 | 10 | 旧格式，缺机器可读路由字段 |
| `prd-review` | 6 | 4 | 2 | 0 | 基础边界可用 |
| `prd-to-issues` | 4 | 2 | 2 | 0 | 基础边界可用 |
| `research-topic-compiler` | 23 | 5 | 2 | 16 | 行为回归丰富，但多数 case 尚未分类；需补 competitive case |
| `ui-mockup-desktop-workbench` | 10 | 0 | 0 | 10 | 旧格式，缺机器可读路由字段 |
| `ui-wireframe-to-html` | 5 | 0 | 0 | 5 | 旧格式，缺机器可读路由字段 |

当前 `scripts/audit_skills.py:180-186` 只强制 `id`、`prompt`、`expected_output`，不会因缺少 `should_trigger`、`expected_route` 或最低正反例数量而失败。因此“仓库审计通过”不能证明路由回归覆盖已经达标。

## 10. 优先级发现

### P0 - 0

没有发现会让 Skill 在正常使用中不可用、不安全或必然误触发的阻断项。

### P1 - `competitive-analysis` 与 `decision-research` 的 metadata 责任重叠

- Evidence level：observed
- Impact：同一竞品决策 prompt 可能因“竞品分析”“最终推荐”“Go/No-Go”同时命中两个 Skill。
- Repair：先增加两条只改一个变量的 paired clean-context eval，分别覆盖“还要收集竞品证据”和“证据已齐只做最终选择”；再依据误触发结果决定是否收窄 `decision-research` description。

### P1 - `complex-exploration` 与研究/决策 Skill 的阶段边界未进入 eval

- Evidence level：observed
- Impact：策略、定价、Roadmap 或竞品定位短 prompt 可能同时命中问题重构、系统研究和最终决策三类入口。
- Repair：分别为 `complex-exploration` / `research-topic-compiler` 和 `complex-exploration` / `decision-research` 增加 paired clean-context eval；以“问题与探索路径是否已稳定”和“是否已有明确决策问题”为单变量。

### P1 - 三个高价值输出 Skill 的 eval 仍是旧格式

- Evidence level：deterministic
- Affected：`prd-architect`、`ui-wireframe-to-html`、`ui-mockup-desktop-workbench`。
- Impact：现有 prompts 能人工阅读，但不能自动统计 trigger/non-trigger，也不能证明 UI 两阶段路由稳定。
- Repair：不改 prompt 行为，先补 `type`、`should_trigger`、`expected_route`、`expected_output` 和 assertions。

### P2 - “脑暴/复杂/沉淀资产”宽词存在语义竞争

- Evidence level：observed
- Affected：calibration / brainstorming / complex-exploration / assetization diagnoser。
- Impact：自然语言短请求可能依赖 body 才能完成分流，而 body 在 Skill 被选中后才加载。
- Repair：把最短判定条件写进 description，并补 paired non-trigger eval。

### P2 - 精确重复资源必须继续被当作发布不变量

- Evidence level：deterministic
- Impact：任何一份 PRD 副本单独修改都会让 architect/reviewer 判断漂移。
- Repair：保留现有 byte parity gate；未来只有在分发模型改成整仓强依赖时，才重新评估共享目录。

## 11. 建议执行顺序

下一阶段建议按低风险顺序推进：

1. `v0.2.2-routing-evals`：只统一旧格式 eval，补相邻 Skill paired routing cases，并让 audit 检查最低 trigger/non-trigger 覆盖。
2. `v0.2.3-trigger-contracts`：基于新增 eval 收窄 `decision-research`、`ai-collaboration-calibration`、`complex-exploration` 的 description，不改 workflow 和输出。
3. 采集真实 clean-context 路由结果。只有同一 pair 在多轮 eval 中仍持续误触发，才进入“合并或废弃”评估。
4. 保持 PRD 三份资源副本和 byte parity gate；不新增 `shared/` runtime dependency。

## 12. 本轮决策清单

| 决策类型 | 数量 | 对象 |
| --- | ---: | --- |
| 保留 | 11 | 除下述待复核 pair 外的现有 Skill |
| 暂时保留，待 paired clean-context eval 复核 | 2 | `competitive-analysis`、`decision-research` |
| 保留但建议收窄 trigger | 2 | `ai-collaboration-calibration`、`complex-exploration` |
| 合并资源 | 0 | 暂无；PRD 副本保留 parity gate |
| 并入父 Skill | 0 | 暂无新的 helper-only Skill |
| 进入废弃评估 | 0 | 暂无 |

历史上已完成的两次正确归并继续作为治理标准：`concept-lens-dashboard` 已并入 `research-topic-compiler`，`generate-drawio-diagram` 已并入 PRD 主流程。它们共同说明：高度依赖父流程、不能形成独立用户目标的 helper capability 应并入 canonical parent；本轮审计的 13 个 Skill 暂不满足这一删除条件。
