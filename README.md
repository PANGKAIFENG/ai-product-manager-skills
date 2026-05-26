# PANGKAIFENG Skill Library

这是我用于统一管理个人常用 Agent Skills 的仓库。

当前仓库采用 `skillshare` 兼容结构：每个 Skill 保持为根目录下的独立文件夹，避免因为物理分组目录影响安装、同步和触发名称。分类、状态和用途通过 `SKILL_REGISTRY.md` 和 `categories/` 维护。

`categories/` 是 GitHub 阅读用的分类导航层，里面的 Skill 入口是指向根目录真实 Skill 的相对 symlink。它已经写入 `.skillignore`，避免被 `skillshare` 当成重复 Skill 发现。

## 管理原则

- GitHub 仓库是精选 Skill 的版本库，不是本机所有 Skill 的原样倾倒。
- `skillshare` 负责把这些 Skill 同步到 Codex、Claude 等目标工具。
- 常用/收藏 Skill 应通过 `skillshare target include` 白名单控制，而不是删除低频 Skill。
- 含公司流程、业务数据、客户数据或内部系统语义的 Skill 默认标记为 `private-only`。
- 发布到 ClawHub 前必须单独检查许可证、敏感信息、适用边界和 README 说明。

## 第一批导入

当前已导入 11 个高价值 Skill，覆盖产品/PRD、协作校准、方案压力测试、工程规范、图示生成、Skill 管理和 Web Artifact 生产。

## 分类导航

| 分类目录 | 中文分类 | 包含 Skill |
| --- | --- | --- |
| `categories/01-product-prd/` | 产品与 PRD | `prd-architect`, `prd-review` |
| `categories/02-collaboration-thinking/` | 认知与协作 | `ai-collaboration-calibration`, `grill-me` |
| `categories/03-engineering-practice/` | 工程实践 | `coding-standards` |
| `categories/04-architecture-visualization/` | 架构图与可视化 | `generate-drawio-diagram` |
| `categories/05-project-governance/` | 项目治理 | `honeycomb-change-proposer`, `project-guidelines-example` |
| `categories/06-skill-governance/` | Skill 治理 | `skill-reviewer`, `team-skill-creator` |
| `categories/07-web-artifacts/` | Web Artifact | `web-artifacts-builder` |

| Skill | 分类 | 状态 |
| --- | --- | --- |
| `prd-architect` | 产品与 PRD | active |
| `ai-collaboration-calibration` | 认知与协作 | active |
| `coding-standards` | 工程实践 | keep |
| `generate-drawio-diagram` | 架构图与可视化 | active |
| `grill-me` | 认知与协作 | active |
| `honeycomb-change-proposer` | 项目治理 | keep |
| `prd-review` | 产品与 PRD | active |
| `project-guidelines-example` | 示例模板 | review |
| `skill-reviewer` | Skill 治理 | core |
| `team-skill-creator` | Skill 治理 | core |
| `web-artifacts-builder` | Web Artifact | keep |

## 后续维护

新增 Skill 时先判断状态：

- `core`: 高频、稳定、应长期维护。
- `active`: 常用，可进入 Codex/Claude 白名单。
- `keep`: 低频但有明确价值，保留在仓库中。
- `review`: 来源、质量或用途还需要复核。
- `archive`: 历史能力或已被替代，不进入常用白名单。
- `private-only`: 不能公开发布。

详细说明见 `SKILL_REGISTRY.md`。
