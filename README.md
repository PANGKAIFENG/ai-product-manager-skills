# AI Product Manager Skills Library

面向 AI 产品经理日常工作的、中文优先的 Skill、Loop、Workflow 和 Tool 集合。v0.3 把两个历史仓库合并为一个公开可读的权威目录：原子判断能力放在 `skills/`，需要状态收敛的串联放在 `loops/`，按工作阶段组合的流程放在 `workflows/`，会产生外部副作用的操作放在 `tools/`。

## 从哪里开始

默认 PM 面（`packs/pm-core.yaml`）只包含高频的 9 个原子 Skill：

| Skill | 用途 | 入口 |
| --- | --- | --- |
| `ai-collaboration-calibration` | 把模糊表达校准成可处理的问题 | [Skill](skills/ai-collaboration-calibration/) · [示例](docs/examples/ai-collaboration-calibration.md) |
| `research-topic-compiler` | 做产品研究并沉淀证据、判断和决策输入 | [Skill](skills/research-topic-compiler/) · [示例](docs/examples/research-topic-compiler.md) |
| `decision-research` | 针对一个具体选择做有界调研和推荐 | [Skill](skills/decision-research/) · [示例](docs/examples/decision-research.md) |
| `brainstorming` | 在 PRD 前比较方案、范围和交互路径 | [Skill](skills/brainstorming/) · [示例](docs/examples/brainstorming.md) |
| `grill-me` | 对已有方案做反方压力测试 | [Skill](skills/grill-me/) · [示例](docs/examples/grill-me.md) |
| `prd-architect` | 生成包含 UI、HTML、截图证据约定的 PRD | [Skill](skills/prd-architect/) · [示例](docs/examples/prd-architect.md) |
| `ui-mockup-desktop-workbench` | 结构到高保真 UI handoff，支持 `structure-only` | [Skill](skills/ui-mockup-desktop-workbench/) · [示例](docs/examples/ui-mockup-desktop-workbench.md) |
| `prd-review` | 从产品、研发、测试角度检查是否可交付 | [Skill](skills/prd-review/) · [示例](docs/examples/prd-review.md) |
| `prd-to-issues` | 把 ready PRD 按 vertical slice 和版本切片拆成研发事项 | [Skill](skills/prd-to-issues/) · [示例](docs/examples/prd-to-issues.md) |

按需面包含 StyleWork、Skill 维护和工程上下文能力：[完整 Registry](SKILL_REGISTRY.md)。`packs/` 是安装建议，不是新的发现入口。

按需 Skill：

| Skill | 用途 | 入口 |
| --- | --- | --- |
| `customer-requirement-discovery` | 售前需求澄清、可行性与 Demo 边界 | [Skill](skills/customer-requirement-discovery/) · [示例](docs/examples/customer-requirement-discovery.md) |
| `stylework-requirement-planning` | StyleWork 需求批次的只读主题与排期共创 | [Skill](skills/stylework-requirement-planning/) · [示例](docs/examples/stylework-requirement-planning.md) |
| `team-skill-creator` | Skill 查重、形态判断、生命周期与发布治理 | [Skill](skills/team-skill-creator/) · [示例](docs/examples/team-skill-creator.md) |
| `skill-reviewer` | Skill 触发、结构、安全和 eval 发布前审计 | [Skill](skills/skill-reviewer/) · [示例](docs/examples/skill-reviewer.md) |
| `agent-trace-diagnoser` | 基于 trace 的证据链和根因诊断 | [Skill](skills/agent-trace-diagnoser/) · [示例](docs/examples/agent-trace-diagnoser.md) |
| `project-context-steward` | 建立和维护可复用的 PROJECT_CONTEXT | [Skill](skills/project-context-steward/) · [示例](docs/examples/project-context-steward.md) |

## 工作方式

- 只有问题未定义清楚时才用 `ai-collaboration-calibration`；研究不是漫无边界地搜索，而是循环到证据足够支持决策。
- 研究、方案和 PRD 各自拥有自己的判断责任；Loop 只负责状态、回流和停止条件，不复制专业内容。
- 小需求可以直接走 `prd-architect -> ui-mockup-desktop-workbench -> prd-review`；中需求加一轮 `grill-me`；大需求先走 `workflows/product-discovery`，收敛后再走 `workflows/product-delivery`。
- PRD 交付包可以包含 HTML 和截图，但 HTML/截图是证据与 handoff，不等于生产代码。
- DingTalk、Yunxiao 和其他外部写入只由 `tools/` 的专用 publisher 在当前 run 取得明确授权后执行；Skill handoff 本身不构成授权。

## Loop

| Loop | 负责什么 | 终止条件 |
| --- | --- | --- |
| `research-decision-loop` | Research 与 Decision 之间往返，维护 evidence gap 和 decision record | 证据满足闭环、用户决策或两轮无有效收敛 |
| `solution-challenge-loop` | Maker 方案与 Critic 压测之间往返 | 方案差量关闭、用户确认或两轮无有效收敛 |
| `prd-delivery-readiness-loop` | PRD、UI、Review、Issue 拆解之间往返 | readiness 达标、用户确认或出现人工门 |

## Workflow

- [`product-discovery`](workflows/product-discovery/WORKFLOW.md)：问题校准、研究/决策、方案和压力测试的组合流程。
- [`product-delivery`](workflows/product-delivery/WORKFLOW.md)：PRD、HTML、截图、Review、版本拆分和发布器的组合流程。

Workflow 是可读的组合规则，不是一个需要被触发的 mega Skill。

## Tool / Publisher

- `tools/validators/product-delivery`：Product Delivery Manifest 确定性校验。
- `tools/publishers/dingtalk-prd-publisher`：把已确认的 PRD 交付包发布到钉钉。
- `tools/publishers/yunxiao-work-item-publisher`：创建并回读云效工作项。
- `tools/automations/yunxiao-requirement-sheet-sync`：把云效需求批次同步到钉钉 Sheet。

工具目录里的 `runtime-adapter/` 是为本地 Agent 分发保留的兼容入口，不计入 15 个原子 Skill。

## 目录

```text
skills/<skill-id>/                 # 15 个原子 Skill，唯一公开触发面
loops/<loop-id>/LOOP.md             # 3 个可恢复 Loop 合同
workflows/<workflow-id>/            # 2 个阶段组合流程
tools/{validators,publishers,automations}/
packs/*.yaml                        # 安装组合建议
catalog/skills.yaml                 # 15 个 Skill 机器目录
catalog/assets.yaml                 # Skill/Loop/Workflow/Tool/Pack 总目录
archive/                            # 历史入口和迁移墓碑，不参与发现
```

## 安装与验证

```bash
git clone https://github.com/PANGKAIFENG/ai-product-manager-skills.git
cd ai-product-manager-skills
python3 scripts/audit_skills.py .
```

本地多 Runtime 使用 Skillshare 时，从已合并的 `skills/<id>/` 或明确的 `tools/*/runtime-adapter/` 安装；不要把混合的 Skillshare 聚合目录当作 GitHub 仓库整体 push。详见 [迁移说明](docs/migration-v0.3.md) 和 [Registry](SKILL_REGISTRY.md)。

## 许可证

MIT，见 [LICENSE](LICENSE)。
