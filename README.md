# PANGKAIFENG Skill Library

这是我用于统一管理个人常用 Agent Skills 的仓库。目标不是收集越多越好，而是让常用 Skill 能被中文自然唤起、能看懂用途、能版本化维护。

当前仓库是 GitHub 管理的 Skill catalog，同时保持 `skillshare` 兼容结构：每个 Skill 保持为根目录下的独立文件夹，避免因为物理分组目录影响安装、同步和触发名称。分类、中文名、唤起语、状态和用途通过 [SKILL_REGISTRY.md](SKILL_REGISTRY.md) 和 [categories/](categories/) 维护。

## 为什么名称仍保留英文

`name` 和目录名是 Skill 的稳定 ID，会被 Codex、Claude、skillshare、GitHub 历史和分类入口引用。直接改成中文有同步断链、重复安装、历史追踪丢失的风险。

所以本仓库采用：

- 英文 slug 保持稳定，例如 `prd-architect`
- `description` 改成中文触发优先
- 每个 `SKILL.md` 顶部增加“中文速查”
- README/Registry 提供中文目录、中文别名和自然语言唤起语

## 快速找 Skill

| 我想做什么 | 可以这样说 | 对应 Skill | 状态 |
| --- | --- | --- | --- |
| 写 PRD、选 PRD 模板 | “帮我写 PRD”“这个需求该用哪种 PRD” | [`prd-architect`](prd-architect/) | active |
| 审 PRD、挑需求缺口 | “帮我审 PRD”“从研发测试视角挑问题” | [`prd-review`](prd-review/) | active |
| 复杂问题先别急着执行 | “先别执行，帮我看清问题”“挑战我的假设” | [`ai-collaboration-calibration`](ai-collaboration-calibration/) | active |
| 系统研究主题、整理学习报告 | “系统研究这个主题”“整理到 Obsidian”“做一个深度专题” | [`research-topic-compiler`](research-topic-compiler/) | active |
| 拷问方案、压力测试设计 | “拷问我的方案”“这个方案哪里会翻车” | [`grill-me`](grill-me/) | active |
| 按工程规范写或审代码 | “按编码规范实现”“检查代码有没有工程坏味道” | [`coding-standards`](coding-standards/) | keep |
| 生成可编辑架构图/流程图 | “画一张架构图”“生成 Draw.io” | [`generate-drawio-diagram`](generate-drawio-diagram/) | active |
| 把 Honeycomb 问题写成上游提案 | “整理成 Honeycomb 上游提案”“判断这是共享问题还是本地问题” | [`honeycomb-change-proposer`](honeycomb-change-proposer/) | keep |
| 参考项目级 Skill 怎么写 | “给我一个项目 Skill 模板”“项目指南型 Skill 怎么组织” | [`project-guidelines-example`](project-guidelines-example/) | review |
| 评审、优化一个 Skill | “帮我 review 这个 Skill”“检查这个 SKILL.md” | [`skill-reviewer`](skill-reviewer/) | core |
| 创建、导入、沉淀新 Skill | “帮我创建一个 Skill”“这个能力要不要沉淀成 Skill” | [`team-skill-creator`](team-skill-creator/) | core |
| 生成复杂交互式 Web Artifact | “做一个复杂交互页面”“生成 React Artifact” | [`web-artifacts-builder`](web-artifacts-builder/) | keep |

## 分类导航

| 分类目录 | 中文分类 | 包含 Skill |
| --- | --- | --- |
| [categories/01-product-prd/](categories/01-product-prd/) | 产品与 PRD | `prd-architect`, `prd-review` |
| [categories/02-collaboration-thinking/](categories/02-collaboration-thinking/) | 认知与协作 | `ai-collaboration-calibration`, `grill-me` |
| [categories/03-engineering-practice/](categories/03-engineering-practice/) | 工程实践 | `coding-standards` |
| [categories/04-architecture-visualization/](categories/04-architecture-visualization/) | 架构图与可视化 | `generate-drawio-diagram` |
| [categories/05-project-governance/](categories/05-project-governance/) | 项目治理 | `honeycomb-change-proposer`, `project-guidelines-example` |
| [categories/06-skill-governance/](categories/06-skill-governance/) | Skill 治理 | `skill-reviewer`, `team-skill-creator` |
| [categories/07-web-artifacts/](categories/07-web-artifacts/) | Web Artifact | `web-artifacts-builder` |
| [categories/08-research-learning/](categories/08-research-learning/) | 研究学习 | `research-topic-compiler` |

## 管理原则

- GitHub 线上仓库是精选 Skill 的标准源，不是本机所有 Skill 的原样倾倒。
- `skillshare` 可以作为把这些 Skill 分发到 Codex、Claude 等目标工具的实现方式，但不是唯一同步机制。
- 常用/收藏 Skill 应通过 `skillshare target include` 白名单控制，而不是删除低频 Skill。
- 含公司流程、业务数据、客户数据或内部系统语义的 Skill 默认标记为 `private-only`。
- 发布到 ClawHub 前必须单独检查许可证、敏感信息、适用边界和 README 说明。

## 状态说明

- `core`: 高频、稳定、应长期维护。
- `active`: 常用，可进入 Codex/Claude 白名单。
- `keep`: 低频但有明确价值，保留在仓库中。
- `review`: 来源、质量或用途还需要复核。
- `archive`: 历史能力或已被替代，不进入常用白名单。
- `private-only`: 不能公开发布。
