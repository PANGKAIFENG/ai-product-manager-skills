# Skill Registry

这个文件用于解释每个已纳入 GitHub 管理的 Skill 是什么、中文怎么叫、什么时候用、什么时候不用、当前维护状态和公开风险。

真实 Skill 目录保持在仓库根目录，确保 GitHub 历史、运行时分发和 Skill 触发名称稳定。`categories/` 只提供 GitHub 阅读时的分类入口，并通过 `.skillignore` 从 skillshare 发现结果中排除。

## 状态含义

- `core`: 个人 Skill 体系的核心能力，优先维护。
- `active`: 常用能力，适合加入目标工具白名单。
- `keep`: 低频但有明确价值，保留版本管理。
- `review`: 需要进一步确认质量、来源、触发边界或是否仍然需要。
- `private-only`: 含内部业务、流程或数据语义，不应公开发布。

## 分类体系

| 分类目录 | 中文分类 | 适用边界 |
| --- | --- | --- |
| `categories/01-product-prd/` | 产品与 PRD | 复杂概念解构、需求结构化、PRD 起草、PRD 评审和交付准备。 |
| `categories/02-collaboration-thinking/` | 认知与协作 | 复杂问题校准、假设挑战、方案压力测试和协作模式选择。 |
| `categories/03-engineering-practice/` | 工程实践 | 通用编码规范、问题诊断、实现约束和研发质量基线。 |
| `categories/04-architecture-visualization/` | 架构图与可视化 | 架构图、流程图、系统关系图和可编辑图示资产。 |
| `categories/05-project-governance/` | 项目治理 | 项目级规范、共享模板、目录治理和上游 proposal。 |
| `categories/06-skill-governance/` | Skill 治理 | Skill 创建、审查、版本维护、触发边界和质量评估。 |
| `categories/08-research-learning/` | 研究学习 | 专题研究、系统学习、多渠道证据、Obsidian Research Project 和研究报告。 |

## 中文检索表

| Skill | 中文名 | 你可以这样说 | 适合什么时候用 | 不适合什么时候用 | 状态 |
| --- | --- | --- | --- | --- | --- |
| `concept-lens-dashboard` | 概念透镜看板 / 高阶概念解构 | “帮我解构一个概念”“做行业演进看板”“PM 技术评审提问脚本” | 冷启动或基于材料研究复杂概念、行业演进、技术/商业范式断代，输出带来源的 PM 决策矩阵和 Tailwind + Alpine.js HTML 看板。 | 一句话百科解释、无需来源引用的轻量回答、长期运行的 SaaS 管理后台或通用前端应用。 | active |
| `prd-architect` | PRD 架构师 / 需求文档起草 | “帮我写 PRD”“帮我选 PRD 模板”“把这个需求整理成 PRD” | 从想法、脑暴或需求草稿进入 PRD 结构；需要判断 `PRD-lite`、`PRD-standard`、`PRD-ai-native` 和文档成熟度。 | 已有完整 PRD 要评审；直接编码；单纯画 UI。 | active |
| `prd-review` | PRD 评审 / 需求评审 | “帮我审 PRD”“从研发测试视角挑问题”“这个需求文档能不能交付开发” | 已有 PRD/handoff，需要找阻断项、冲突、不可实现点、不可测试点，并给修订草案。 | 从零写 PRD；只做语言润色。 | active |
| `ai-collaboration-calibration` | 协作校准 / 认知校准 | “先别执行，帮我看清问题”“挑战我的假设”“这个方案是不是想错了” | 复杂问题进入执行前，先校准问题定义、领域定位、隐藏假设和方案裂缝。 | 翻译、摘要、格式转换、明确的小改动。 | active |
| `research-topic-compiler` | 专题研究编译器 / 系统学习研究助手 | “系统研究这个主题”“整理到 Obsidian”“做一个深度专题”“研究行业最佳实践” | 多渠道研究主题、动态选择渠道、生成证据矩阵、Research Project 和 `05_研究报告`。 | 创建 Skill、评审 Skill、普通即时搜索、一次性摘要。 | active |
| `grill-me` | 方案拷问 / 压力测试 | “拷问我的方案”“压力测试这个设计”“这个方案哪里会翻车” | 已有方案但担心盲点，需要一问一答澄清依赖、分支、取舍和失败模式。 | 直接写最终方案；泛泛总结；不希望互动追问。 | active |
| `agent-trace-diagnoser` | Agent trace 诊断器 / 日志根因定位 | “看下这个 trace”“根据日志定位根因”“只说明问题不要改文件” | 从 agent trace、日志 JSON、执行记录和工具调用序列中定位核心根因、证据链、可能文件/行和修复建议。 | 直接修复代码、普通代码解释、没有日志证据的新功能设计。 | active |
| `coding-standards` | 编码规范 / 工程规范 | “按编码规范实现”“帮我检查代码规范”“这个实现有没有工程坏味道” | TypeScript、JavaScript、React、Node.js 的实现约束、代码评审、重构建议和质量基线。 | 深度框架专用规则或业务专属规范；这类应沉淀为项目 Skill。 | keep |
| `generate-drawio-diagram` | Draw.io 图示生成器 / 架构图流程图 | “画一张架构图”“生成 Draw.io”“输出 .drawio 文件” | 需要可在 Draw.io、VSCode Draw.io 插件或 diagrams.net 中继续编辑的架构图/流程图。 | 只要不可编辑 PNG、纯 Mermaid 图或视觉设计稿。 | active |
| `honeycomb-change-proposer` | Honeycomb 变更提案 / 上游 proposal | “整理成 Honeycomb 上游提案”“这个模板问题该不该回上游” | 共享模板、managed path、安装包或本地 override 出现问题，需要证据化、归因并沉淀上游建议。 | 纯项目内 PRD、纯目录整理、未经确认直接修改上游仓库。 | keep |
| `project-guidelines-example` | 项目指南 Skill 示例 / 项目专属 Skill 模板 | “给我一个项目 Skill 模板”“项目指南型 Skill 怎么组织” | 参考项目级 Skill 如何表达架构、目录、代码模式、测试和部署约束。 | 直接作为真实项目规范套用；必须先替换示例事实。 | review |
| `skill-reviewer` | Skill 评审器 / Skill 审计 | “帮我 review 这个 Skill”“检查这个 SKILL.md”“优化 Skill 触发描述” | 评审 Skill 触发边界、输入输出、工具边界、资源组织、评估设计和复用风险。 | 创建新 Skill；创建或导入应使用 `team-skill-creator`。 | core |
| `team-skill-creator` | 团队 Skill 创建器 / 能力沉淀判断 | “帮我创建一个 Skill”“这个能力要不要沉淀成 Skill”“导入这个 GitHub Skill” | 新建、导入、合并、评估一个可复用能力是否应成为 Skill，并按团队标准验证。 | 已有 Skill 只需要评审；一次性任务。 | core |

## 推荐白名单

当前建议优先加入 Codex/Claude 常用白名单：

- `concept-lens-dashboard`
- `prd-architect`
- `prd-review`
- `ai-collaboration-calibration`
- `research-topic-compiler`
- `grill-me`
- `agent-trace-diagnoser`
- `generate-drawio-diagram`
- `skill-reviewer`
- `team-skill-creator`

暂时不建议作为常用白名单但应保留：

- `coding-standards`
- `honeycomb-change-proposer`

建议继续评审：

- `project-guidelines-example`

## 公开发布规则

发布到 ClawHub 或公开推广前，至少检查：

1. `SKILL.md` 是否有标准 frontmatter。
2. 是否包含公司、客户、个人或内部系统敏感信息。
3. 是否有许可证限制或第三方归属要求。
4. 触发边界是否足够清楚，避免误触发。
5. 是否有最小验证方式，例如脚本、示例 prompt 或检查清单。
