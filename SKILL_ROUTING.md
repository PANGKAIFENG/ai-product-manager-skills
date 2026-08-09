# Skill Routing

先按工作阶段分流，再决定是否进入 Loop。不要因为一条请求同时提到“研究、方案、PRD”就一次性调用所有 Skill。

| 阶段 | 首选 Skill | 何时停止或转交 |
| --- | --- | --- |
| 问题和目标含糊 | `ai-collaboration-calibration` | 问题可研究或可设计后再转下游 |
| 需要系统产品研究或竞品证据 | `research-topic-compiler` | 形成 evidence pack；具体取舍交 `decision-research` |
| 需要一个明确选择 | `decision-research` | 有推荐、排除理由、置信度和颠覆条件 |
| 方案尚未成形 | `brainstorming` | 用户确认 Design Spec 后交 PRD 或 UI |
| 方案已成形但担心失败 | `grill-me` | 返回最小 Challenge/Design Delta；不自行放行 |
| 需要正式 PRD | `prd-architect` | 产出 PRD 和可选 Product Delivery Manifest，停止在 `review_pending` |
| 需要 UI 结构或高保真 handoff | `ui-mockup-desktop-workbench` | `structure-only` 可在结构确认后停止，否则继续 HTML/截图/handoff |
| 已有 PRD 需要验收和评审 | `prd-review` | `ready` 才能拆 issues 或发布 |
| ready PRD 需要开发拆分 | `prd-to-issues` | 先 draft；版本切片或 GitHub/云效发布需单独确认 |

## 三个 Loop

| Loop | 入口 | 回流规则 | 人工门 |
| --- | --- | --- | --- |
| `$decision-loop` | 明确决策被证据 gap 阻塞 | 只回传一个 material/researchable/closable gap | 三轮上限、两轮无有效差量或需要业务选择 |
| `$solution-loop` | 已有候选方案需要多轮压测 | Maker 与 Critic 只交换 Challenge Record/Design Delta | 三轮上限、两轮无有效差量或取舍不可推断 |
| `$delivery-loop` | 已有 PRD/UI/交付包需要 Review 与修订 | 只回到最早不稳定的交付节点 | 三轮上限、两轮无有效差量或交付事实缺失；发布授权单独表达 |

## 两个 Workflow

- `$problem-to-solution`：`calibration -> research/decision-loop? -> brainstorming -> solution-loop? -> solution_confirmed`。
- `$solution-to-delivery`：`prd-architect -> UI/HTML/截图? -> prd-review ready -> prd-to-issues? -> Manifest/hash/fingerprint -> delivery-loop 最终 Review -> validator -> package_ready`。Pre-split Review 未通过时禁止生成规划产物。

两个 Workflow 和三个 Loop 只接受显式调用。小需求可直接使用原子 Skill；中大型需求才使用完整 Workflow，且只在有真实回流时进入 Loop。

## 外部写入边界

`tools/` 下的 publisher/automation 是副作用拥有者。任何 Skill handoff、Loop return edge 或 Workflow 串联都不能代替当前 run 的明确授权；Package 已就绪但没有发布授权时保持 `status: package_ready`，返回 `publish_status: authorization_required` 并停止。

## 迁移别名

`product-discovery` -> `problem-to-solution`；`product-delivery` -> `solution-to-delivery`；`research-decision-loop` -> `decision-loop`；`solution-challenge-loop` -> `solution-loop`；`prd-delivery-readiness-loop` -> `delivery-loop`。`competitive-analysis`、`ui-wireframe-to-html` 和 `stylework-solution-scoper` 的既有迁移关系保持不变。旧 ID 仅在 `archive/`、catalog 迁移记录或旧仓墓碑中供回读，不作为 Runtime 别名重复安装。
