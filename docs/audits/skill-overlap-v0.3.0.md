# Skill 重复与路由审计 v0.3.0

## 结论

v0.3 的公开发现面固定为 15 个原子 Skill。当前没有证据表明需要再删除一个活跃 Skill；主要风险已经从“重复实现”收敛为“相邻职责的路由边界”。五个历史高重叠入口已退役并建立替代路由：`competitive-analysis`、`ui-wireframe-to-html`、`complex-exploration`、`ai-work-assetization-diagnoser`、`stylework-solution-scoper`。前四个保留在公开仓 `archive/`，最后一个保留在旧仓迁移墓碑中。

## 审计范围与证据

- 范围：`skills/` 下 15 个活跃 Skill、`catalog/skills.yaml`、`catalog/assets.yaml`、`SKILL_ROUTING.md`、3 个 Loop、2 个 Workflow，以及 Tool adapter 入口。
- 机器校验：`python3 scripts/audit_skills.py .`、`python3 scripts/check_v03_asset_catalog.py .`、所有活跃 Skill 的 `skill-reviewer/scripts/check_skill.py`。
- Eval 覆盖：15 个 Skill 共 179 个 eval case，其中 125 个 trigger、54 个 non-trigger；每个 Skill 都有触发与非触发覆盖，核心相邻边界包含 routing/regression/return-edge case。
- 文件级 SHA-256：仅发现 3 组有意的 self-contained 副本，均为 `prd-architect` 与 `prd-review` 之间的 `check_prd_shape.py`、`validate_drawio.py` 和 `drawio-templates.md`；没有发现两个活跃 Skill 共享同一份 `SKILL.md`。

## 相邻职责判断

| 相邻面 | 当前职责分界 | 结论 |
| --- | --- | --- |
| `ai-collaboration-calibration` / `brainstorming` | 前者校准问题与假设；后者在问题成立后比较方案并形成 Design Spec | 保留，入口由问题成熟度区分 |
| `research-topic-compiler` / `decision-research` | 前者形成证据包、候选池和研究资产；后者围绕一个明确选择给推荐、排除理由和置信度 | 保留，研究完成后可通过 `research-decision-loop` 回流 |
| `brainstorming` / `grill-me` | 前者是 Maker；后者是独立 Critic，只返回可修复 Challenge Record | 保留，避免 Maker 自评放行 |
| `prd-architect` / `ui-mockup-desktop-workbench` | 前者负责 PRD 与页面型交付包编排；后者负责结构、状态、HTML、截图和 UI handoff | 保留，`prd-architect` 通过页面型规则调用后者 |
| `prd-architect` / `prd-review` | 前者起草；后者独立检查 readiness、可实现性和可测试性 | 保留，禁止自评通过 |
| `prd-review` / `prd-to-issues` | 前者判断是否 ready；后者仅把 ready PRD 拆成 vertical-slice issues | 保留，先 review 后拆分 |
| `customer-requirement-discovery` / `stylework-requirement-planning` | 前者澄清单一客户需求与可行性；后者只读分析一批需求的主题、依赖和排期 | 保留，避免再次拆出一次性报价 Skill |
| `team-skill-creator` / `skill-reviewer` | 前者决定是否资产化、权威源和生命周期；后者审计 Skill 质量与发布门禁 | 保留，治理决策与质量评审分离 |
| `agent-trace-diagnoser` / `project-context-steward` | 前者诊断具体 trace 的根因；后者维护跨需求可复用的上下文文档 | 保留，证据对象不同 |

## 归档与迁移

| 旧 ID | v0.3 替代 | 处理 |
| --- | --- | --- |
| `competitive-analysis` | `research-topic-compiler` 的 product-research mode | 合并，旧目录仅在 `archive/` |
| `ui-wireframe-to-html` | `ui-mockup-desktop-workbench` 的 `structure-only` mode | 合并，旧目录仅在 `archive/` |
| `complex-exploration` | `ai-collaboration-calibration` + `product-discovery` | 拆为问题校准与阶段 Workflow |
| `ai-work-assetization-diagnoser` | `team-skill-creator` 的 assetization gate | 合并为生命周期治理入口 |
| `stylework-solution-scoper` | `customer-requirement-discovery` 的 StyleWork 适配阶段 | 合并，旧实现仅在旧仓迁移墓碑中保留 |

## 发布判断

- 没有活跃目录级重复 Skill；不新增合并动作。
- 3 组精确重复文件继续保留为 self-contained 分发副本，后续修改必须保持 parity 或由 catalog 明确说明共享策略。
- 任何外部写入仍只能由 `tools/` publisher/automation 在当前 run 获得明确授权后执行；Loop/Workflow 不拥有写入权限。
- 下一版本只需根据真实使用频次、误触发和路由 eval 失败更新本审计，不应凭目录数量继续合并。
