# Skill Registry

这个文件用于解释每个已纳入 GitHub 管理的 Skill 是什么、适合什么时候用、当前维护状态和公开风险。

真实 Skill 目录保持在仓库根目录，确保 `skillshare` 同步和 Skill 触发名称稳定。`categories/` 只提供 GitHub 阅读时的分类入口，并通过 `.skillignore` 从 skillshare 发现结果中排除。

状态含义：

- `core`: 个人 Skill 体系的核心能力，优先维护。
- `active`: 常用能力，适合加入目标工具白名单。
- `keep`: 低频但有明确价值，保留版本管理。
- `review`: 需要进一步确认质量、来源、触发边界或是否仍然需要。
- `private-only`: 含内部业务、流程或数据语义，不应公开发布。

## 分类体系

| 分类目录 | 中文分类 | 适用边界 |
| --- | --- | --- |
| `categories/01-product-prd/` | 产品与 PRD | 需求结构化、PRD 起草、PRD 评审和交付准备。 |
| `categories/02-collaboration-thinking/` | 认知与协作 | 复杂问题校准、假设挑战、方向收敛和协作模式选择。 |
| `categories/03-engineering-practice/` | 工程实践 | 通用编码规范、实现约束和研发质量基线。 |
| `categories/04-architecture-visualization/` | 架构图与可视化 | 架构图、流程图、系统关系图和可编辑图示资产。 |
| `categories/05-project-governance/` | 项目治理 | 项目级规范、共享模板、目录治理和上游 proposal。 |
| `categories/06-skill-governance/` | Skill 治理 | Skill 创建、审查、版本维护、触发边界和质量评估。 |
| `categories/07-web-artifacts/` | Web Artifact | 复杂交互式前端 Artifact 的生成与打包。 |

## 已纳入 Skill

| Skill | 分类 | 状态 | 用途 | 备注 |
| --- | --- | --- | --- | --- |
| `prd-architect` | 产品与 PRD | active | 根据需求复杂度选择 `PRD-lite`、`PRD-standard` 或 `PRD-ai-native`，并决定草稿/讨论/确认阶段。 | 适合产品需求从想法进入文档结构时触发。 |
| `ai-collaboration-calibration` | 认知与协作 | active | 在复杂问题上先校准问题定义、挑战假设、识别反模式，避免直接进入执行模式。 | 适合方案变复杂、方向不确定、需要反驳或压力测试时使用。 |
| `coding-standards` | 工程实践 | keep | TypeScript、JavaScript、React、Node.js 的通用编码规范和最佳实践。 | 目前偏通用，后续可结合个人项目栈收敛。 |
| `generate-drawio-diagram` | 架构图与可视化 | active | 生成可在 Draw.io 中编辑的 `.drawio` 架构图或流程图。 | 适合架构、流程和 AI 协作链路图。 |
| `grill-me` | 认知与协作 | active | 通过一问一答压力测试方案或设计，按决策树澄清分支、依赖、假设和失败模式。 | 适合发送方案前做反方追问，也适合架构、产品、流程设计的 hard questions。 |
| `honeycomb-change-proposer` | 项目治理 | keep | 将 Honeycomb 共享模板、managed path 或安装包问题整理成上游 proposal。 | 低频但专业，适合保留。 |
| `prd-review` | 产品与 PRD | active | 从 PM、研发、测试视角评审第一版 PRD，输出修订建议和可回填草案。 | 通常与 handoff/PRD 文件一起使用。 |
| `project-guidelines-example` | 示例模板 | review | 项目专属 Skill 示例，展示架构、目录、测试、部署等项目指南结构。 | 当前不是标准 frontmatter 结构，建议后续决定是否重写为模板 Skill。 |
| `skill-reviewer` | Skill 治理 | core | 审查、评分和改进 Codex/Agent Skill，检查触发边界、输入输出、工具边界、资源和评估。 | 这是维护整个 Skill 库的核心工具。 |
| `team-skill-creator` | Skill 治理 | core | 在创建 Skill 前判断应做 Prompt/Workflow/Tool/Plugin/App/Skill，并按团队标准创建与验证。 | 这是新增 Skill 的入口工具。 |
| `web-artifacts-builder` | Web Artifact | keep | 用 React、Tailwind、shadcn/ui 等创建复杂 HTML Artifact 并打包为单文件。 | 带 Apache 2.0 license；公开前仍需单独审查用途和依赖。 |

## 推荐白名单

当前建议优先加入 Codex/Claude 常用白名单：

- `prd-architect`
- `prd-review`
- `ai-collaboration-calibration`
- `grill-me`
- `generate-drawio-diagram`
- `skill-reviewer`
- `team-skill-creator`

暂时不建议作为常用白名单但应保留：

- `coding-standards`
- `honeycomb-change-proposer`
- `web-artifacts-builder`

建议继续评审：

- `project-guidelines-example`

## 公开发布规则

发布到 ClawHub 或公开推广前，至少检查：

1. `SKILL.md` 是否有标准 frontmatter。
2. 是否包含公司、客户、个人或内部系统敏感信息。
3. 是否有许可证限制或第三方归属要求。
4. 触发边界是否足够清楚，避免误触发。
5. 是否有最小验证方式，例如脚本、示例 prompt 或检查清单。
