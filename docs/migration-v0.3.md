# v0.3 迁移说明

v0.3 将 `PANGKAIFENG/private-agent-skills` 的通用/运营内容迁入 `PANGKAIFENG/ai-product-manager-skills` 的统一公开目录。两个仓库当前都为 PUBLIC；旧仓不删除，改为迁移墓碑，避免破坏历史链接。

## 稳定 ID 变化

| 旧入口 | v0.3 入口 | 处理 |
| --- | --- | --- |
| `competitive-analysis` | `research-topic-compiler` 的 product-research/competitive-evidence mode | 合并，旧目录归档 |
| `ui-wireframe-to-html` | `ui-mockup-desktop-workbench` 的 `structure-only` mode | 合并，旧目录归档 |
| `stylework-solution-scoper` | `customer-requirement-discovery` 的下游 StyleWork 适配阶段 | 合并，旧目录归档 |
| `ai-work-assetization-diagnoser` | `team-skill-creator` 的 assetization gate | 合并，旧目录归档 |
| `prd-to-issues`（旧仓副本） | `skills/prd-to-issues` | 公开仓唯一权威实现 |
| `dingtalk-prd-publisher`、Yunxiao 入口 | `tools/*/runtime-adapter/` | Tool/Publisher，不计入 Skill 总数 |
| `product-discovery` | `problem-to-solution` | Workflow 改为结果导向命名，并增加显式 Runtime 入口 |
| `product-delivery` | `solution-to-delivery` | Workflow 明确为“已确认方案到可交付产品包” |
| `research-decision-loop` | `decision-loop` | Loop 按要闭合的对象命名 |
| `solution-challenge-loop` | `solution-loop` | Loop 按要闭合的对象命名 |
| `prd-delivery-readiness-loop` | `delivery-loop` | 覆盖 PRD、UI、截图、Manifest 和 Review，不再只强调 PRD |

## 本地同步

先从合并后的公开仓更新 15 个 `skills/<id>`；再按需安装 2 个 `workflows/<id>`、3 个 `loops/<id>` 和工具的 `runtime-adapter/`。五个组合入口都应显示为显式调用，旧名称不作为第二套 Runtime 入口保留。不要直接复制或删除 Runtime symlink，也不要从包含公私内容的 Skillshare 聚合目录运行 `skillshare push`。同步前先运行 `skillshare sync --dry-run`，逐个核对 Skill 名称，再正式同步。

## 回滚

原公开仓旧包保留在 `archive/`，`stylework-solution-scoper` 等旧运营内容保留在旧仓迁移墓碑中。回滚代码只恢复本地能力，不会自动撤销已经写入钉钉或云效的数据；外部数据需要 publisher 的独立回滚/人工处理。
