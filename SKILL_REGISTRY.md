# Skill Registry

v0.3 的公开触发面固定为 15 个原子 Skill。`core` 表示默认 PM 面，`active` 表示按需加载；Loop、Workflow 和 Tool 不在此表中冒充 Skill。

| Skill | 职责 | 状态 | 合并/边界说明 |
| --- | --- | --- | --- |
| `ai-collaboration-calibration` | 校准问题、目标、假设和讨论边界 | core | 不直接写 PRD 或替用户做最终决策 |
| `research-topic-compiler` | 产品研究、竞品证据、候选池、研究项目和决策输入 | core | 合入 `competitive-analysis` 的 evidence mode |
| `decision-research` | 围绕一个具体问题做有界取证并给推荐 | core | 不做开放式专题知识沉淀 |
| `brainstorming` | 生成并比较产品方案、范围、流程、交互和 Design Spec | core | 不自批 readiness；压力测试交给 `grill-me` |
| `grill-me` | 对方案和 PRD 前置判断做反方挑战 | core | 只返回最小可修复 gap |
| `prd-architect` | 将确认后的需求编成 PRD 与 Product Delivery Package | core | PRD 可带 HTML、截图清单和 Manifest，但不发布 |
| `ui-mockup-desktop-workbench` | 结构、状态、HTML、高保真 UI 与实现 handoff | core | 合入 `ui-wireframe-to-html` 的 `structure-only` mode |
| `prd-review` | 评审完整性、可实现性、可测试性和交付证据 | core | 不由 Maker 自评通过 |
| `prd-to-issues` | 按 vertical slice、依赖和 V1/V2/V3 拆研发事项 | core | 吸收版本切片规则，不直接写云效 |
| `customer-requirement-discovery` | 售前/客户需求澄清、可行性判断和轻量 Demo 边界 | active | 合入 StyleWork solution scoping 的前置发现职责 |
| `stylework-requirement-planning` | 只读分析需求批次、主题、依赖、优先级和迭代建议 | active | 不导出 Sheet、不修改云效或钉钉 |
| `team-skill-creator` | Skill 查重、权威源、生命周期、发布和分发治理 | active | 合入 assetization/improvement 的治理入口 |
| `skill-reviewer` | 审计 Skill 触发、结构、安全、资源和 eval | active | 不负责创建或发布决策 |
| `agent-trace-diagnoser` | 基于 trace 和日志做证据链根因诊断 | active | 只读，不直接修改代码 |
| `project-context-steward` | 建立和维护跨需求复用的 PROJECT_CONTEXT | active | 不替代 PRD、目录治理或一次性实现 |

## 默认安装面

默认安装 [`packs/pm-core.yaml`](packs/pm-core.yaml) 的 9 个 `core` Skill。StyleWork、维护者和工程 Skill 按需安装，减少触发竞争和运行时噪声。

## 生命周期

- `active -> compatibility -> deprecated -> archived` 是旧入口的迁移路径。
- `archive/` 只用于历史回读和回滚，不是可发现的安装源。
- 同一稳定 ID 只允许一个权威实现；仓库合并后旧仓只保留迁移墓碑。
