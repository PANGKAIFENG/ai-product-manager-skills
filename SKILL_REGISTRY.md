# Skill Registry

这个文件用于解释每个已纳入 GitHub 管理的 Skill 是什么、适合什么时候用、当前维护状态和公开风险。

状态含义：

- `core`: 个人 Skill 体系的核心能力，优先维护。
- `active`: 常用能力，适合加入目标工具白名单。
- `keep`: 低频但有明确价值，保留版本管理。
- `review`: 需要进一步确认质量、来源、触发边界或是否仍然需要。
- `private-only`: 含内部业务、流程或数据语义，不应公开发布。

## 第一批

| Skill | 分类 | 状态 | 用途 | 备注 |
| --- | --- | --- | --- | --- |
| `prd-architect` | 产品与 PRD | active | 根据需求复杂度选择 `PRD-lite`、`PRD-standard` 或 `PRD-ai-native`，并决定草稿/讨论/确认阶段。 | 适合产品需求从想法进入文档结构时触发。 |
| `ai-collaboration-calibration` | 认知与协作 | active | 在复杂问题上先校准问题定义、挑战假设、识别反模式，避免直接进入执行模式。 | 适合方案变复杂、方向不确定、需要反驳或压力测试时使用。 |
| `coding-standards` | 工程实践 | keep | TypeScript、JavaScript、React、Node.js 的通用编码规范和最佳实践。 | 目前偏通用，后续可结合个人项目栈收敛。 |
| `generate-drawio-diagram` | 架构图与可视化 | active | 生成可在 Draw.io 中编辑的 `.drawio` 架构图或流程图。 | 适合架构、流程和 AI 协作链路图。 |
| `honeycomb-change-proposer` | 项目治理 | keep | 将 Honeycomb 共享模板、managed path 或安装包问题整理成上游 proposal。 | 低频但专业，适合保留。 |
| `prd-review` | 产品与 PRD | active | 从 PM、研发、测试视角评审第一版 PRD，输出修订建议和可回填草案。 | 通常与 handoff/PRD 文件一起使用。 |
| `project-guidelines-example` | 示例模板 | review | 项目专属 Skill 示例，展示架构、目录、测试、部署等项目指南结构。 | 当前不是标准 frontmatter 结构，建议后续决定是否重写为模板 Skill。 |
| `skill-reviewer` | Skill 治理 | core | 审查、评分和改进 Codex/Agent Skill，检查触发边界、输入输出、工具边界、资源和评估。 | 这是维护整个 Skill 库的核心工具。 |
| `team-skill-creator` | Skill 治理 | core | 在创建 Skill 前判断应做 Prompt/Workflow/Tool/Plugin/App/Skill，并按团队标准创建与验证。 | 这是新增 Skill 的入口工具。 |
| `web-artifacts-builder` | Web Artifact | keep | 用 React、Tailwind、shadcn/ui 等创建复杂 HTML Artifact 并打包为单文件。 | 带 Apache 2.0 license；公开前仍需单独审查用途和依赖。 |

## 推荐白名单

第一批里建议优先加入 Codex/Claude 常用白名单：

- `prd-architect`
- `prd-review`
- `ai-collaboration-calibration`
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
