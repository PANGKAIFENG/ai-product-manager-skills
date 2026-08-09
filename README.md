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
- 小需求可以直接调用原子 Skill；需要完整推进时，显式使用 `$problem-to-solution` 或 `$solution-to-delivery`。Loop 只在存在真实回流时使用。
- PRD 交付包可以包含 HTML 和截图，但 HTML/截图是证据与 handoff，不等于生产代码。
- DingTalk、Yunxiao 和其他外部写入只由 `tools/` 的专用 publisher 执行；Skill handoff 本身不构成授权。当前 Agent Runtime 的 Product Delivery Package 只支持完整 dry-run，真实写入需要未来的可信宿主能力；Legacy 明确直发不等于 Package 发布。

## Loop

| Loop | 负责什么 | 终止条件 |
| --- | --- | --- |
| [`decision-loop`](loops/decision-loop/) | Research 与 Decision 之间往返，关闭一个影响决策的 evidence gap | 决策成立、三轮上限、两轮无有效差量或 Human Gate |
| [`solution-loop`](loops/solution-loop/) | Maker 与 Critic 之间往返，关闭一个方案 challenge | 方案确认、三轮上限、两轮无有效差量或 Human Gate |
| [`delivery-loop`](loops/delivery-loop/) | PRD/UI Maker 与独立 Reviewer 之间往返，关闭交付 finding | package ready、三轮上限、两轮无有效差量或 Human Gate |

## Workflow

- [`problem-to-solution`](workflows/problem-to-solution/)（问题到方案）：把模糊问题推进为可进入 PRD 的已确认方案。
- [`solution-to-delivery`](workflows/solution-to-delivery/)（方案到交付）：把已确认方案转成经过 Review 的完整产品交付包。

Workflow 和 Loop 在语义上仍是组合资产，不是原子 Skill；目录中的 `SKILL.md` 只是 Runtime 适配入口。五个入口均关闭隐式调用，只有显式选择 `$<id>` 才运行完整编排。

## Tool / Publisher

- `tools/validators/product-delivery`：Product Delivery Manifest 确定性校验。
- `tools/publishers/dingtalk-prd-publisher`：把已确认的 PRD 交付包发布到钉钉。
- `tools/publishers/yunxiao-work-item-publisher`：创建并回读云效工作项。
- `tools/automations/yunxiao-requirement-sheet-sync`：把云效需求批次同步到钉钉 Sheet。

Workflow、Loop 和工具目录里的 Runtime adapter 不计入 15 个原子 Skill。

## 目录

```text
skills/<skill-id>/                       # 15 个原子 Skill
loops/<loop-id>/{SKILL,LOOP}.md           # 3 个显式 Runtime 入口 + 可恢复合同
workflows/<workflow-id>/{SKILL,WORKFLOW}.md # 2 个显式 Runtime 入口 + 阶段组合
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

本地多 Runtime 使用 Skillshare 时，从已合并的 `skills/<id>/`、`loops/<id>/`、`workflows/<id>/` 或明确的 `tools/*/runtime-adapter/` 安装；不要把混合的 Skillshare 聚合目录当作 GitHub 仓库整体 push。详见 [迁移说明](docs/migration-v0.3.md) 和 [Registry](SKILL_REGISTRY.md)。

## 许可证

MIT，见 [LICENSE](LICENSE)。
