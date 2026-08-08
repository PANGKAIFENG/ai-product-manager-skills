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
| `research-decision-loop` | Research 或 Decision | 只回传一个 material/researchable/closable gap | 两轮无有效差量或需要业务选择 |
| `solution-challenge-loop` | Brainstorming 或 Grill | Maker 与 Critic 只交换 Challenge Record/Design Delta | 两轮无有效差量或取舍不可推断 |
| `prd-delivery-readiness-loop` | PRD/UI/Review | 只回到最早不稳定的交付节点 | review、发布授权或事实缺失需要人工确认 |

## 两个 Workflow

- `workflows/product-discovery`：`calibration -> research-decision-loop? -> brainstorming -> solution-challenge-loop?`。
- `workflows/product-delivery`：`prd-architect -> ui-mockup-desktop-workbench -> prd-review -> prd-to-issues? -> tools?`。

小需求可跳过 Loop；中需求至少经历一轮 Review；大需求在 Discovery 收敛后再 Delivery，并可在 `prd-to-issues` 中输出 V1/V2/V3。

## 外部写入边界

`tools/` 下的 publisher/automation 是副作用拥有者。任何 Skill handoff、Loop return edge 或 Workflow 串联都不能代替当前 run 的明确授权；没有授权时返回 `authorization-required` 并停止。

## 迁移别名

`competitive-analysis` -> `research-topic-compiler` 的 `product-research/competitive-evidence` mode；`ui-wireframe-to-html` -> `ui-mockup-desktop-workbench` 的 `structure-only` mode；`stylework-solution-scoper` -> `customer-requirement-discovery` 的下游适配阶段。旧 ID 仅在 `archive/` 或旧仓迁移墓碑中供回读。
