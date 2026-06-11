# Skill Registry

这个文件用于解释公开 AI PM Skill catalog 中每个 Skill 是什么、中文怎么叫、什么时候用、什么时候不用、当前维护状态和公开边界。

真实 Skill 目录保持在仓库根目录，确保 GitHub 历史、运行时分发和 Skill 触发名称稳定。分类信息是 catalog metadata，不代表真实运行时目录；任何额外浏览索引都只是阅读辅助，不作为 skillshare 或 Agent runtime 的加载入口。

## 状态含义

- `core`: AI 产品经理主工作流的核心能力，优先维护。
- `active`: 常用能力，适合加入目标工具白名单。
- `review`: 需要进一步确认质量、触发边界或公开适用性。

## 分类体系

| 分类标签 | 中文分类 | 适用边界 |
| --- | --- | --- |
| `collaboration-thinking` | 认知与协作 | 复杂问题校准、假设挑战、方案压力测试和协作模式选择。 |
| `research-learning` | 研究学习 | 专题研究、系统学习、概念源流、行业演进、多渠道证据和 PM 决策看板。 |
| `decision-research` | 决策调研 | 明确具体决策、接入可行性、方案选型和一次性决策型调研。 |
| `product-prd` | 产品与 PRD | 需求结构化、PRD 起草、PRD 图示、PRD 评审和交付准备。 |

## 中文检索表

| Skill | 中文名 | 你可以这样说 | 适合什么时候用 | 不适合什么时候用 | 状态 |
| --- | --- | --- | --- | --- | --- |
| `ai-collaboration-calibration` | 协作校准 / 认知校准 | “先别执行，帮我看清问题”“挑战我的假设”“这个方案是不是想错了” | 复杂问题进入执行前，先校准问题定义、领域定位、隐藏假设和方案裂缝。 | 翻译、摘要、格式转换、明确的小改动。 | core |
| `research-topic-compiler` | 专题研究编译器 / 概念源流研究助手 | “系统研究这个主题”“整理到 Obsidian”“概念解读”“概念源流”“PM 技术评审提问脚本”“行业演进看板” | 多渠道主题研究、系统学习、轻量概念解构、概念源流、语义演化、PM 决策看板和研究报告。 | 创建或评审 Skill；普通即时搜索；一次性摘要。 | core |
| `decision-research` | 决策调研 / 决策驱动调研 | “有没有现成方案”“这个怎么接”“这个选择可行吗”“帮我选一个” | 问题已定义清楚，需要围绕平台接入、可行性、方案选型或决策路线做单次调研，并给出有立场推荐和排除理由。 | 问题还没定义清楚；需要长期知识沉淀；创建或评审 Skill。 | active |
| `prd-architect` | PRD 架构师 / 需求文档起草 | “帮我写 PRD”“帮我选 PRD 模板”“把这个需求整理成 PRD”“PRD 里补 Draw.io 流程图” | 从想法、脑暴或需求草稿进入 PRD 结构；需要判断 `PRD-lite`、`PRD-standard`、`PRD-ai-native`、文档成熟度和正式图示。 | 已有完整 PRD 要评审；直接编码；单纯画 UI。 | core |
| `prd-review` | PRD 评审 / 需求评审 | “帮我审 PRD”“从研发测试视角挑问题”“这个需求文档能不能交付开发”“检查 PRD 图示是否可编辑” | 已有 PRD/handoff，需要找阻断项、冲突、不可实现点、不可测试点、图示缺口，并给修订草案。 | 从零写 PRD；只做语言润色。 | core |
| `grill-me` | 方案拷问 / 压力测试 | “拷问我的方案”“压力测试这个设计”“这个方案哪里会翻车” | 已有方案但担心盲点，需要一问一答澄清依赖、分支、取舍和失败模式。 | 直接写最终方案；泛泛总结；不希望互动追问。 | active |

## 推荐白名单

当前建议加入 Codex/Claude 常用白名单的公开 Skill：

- `ai-collaboration-calibration`
- `research-topic-compiler`
- `decision-research`
- `prd-architect`
- `prd-review`
- `grill-me`

## 公开发布规则

发布到 ClawHub 或公开推广前，至少检查：

1. `SKILL.md` 是否有标准 frontmatter。
2. 是否包含公司、客户、个人或内部系统敏感信息。
3. 是否有许可证限制或第三方归属要求。
4. 触发边界是否足够清楚，避免误触发。
5. 是否有最小验证方式，例如脚本、示例 prompt 或检查清单。

## 相邻 Skill 路由

当多个 Skill 都可能被中文关键词触发时，先查 [SKILL_ROUTING.md](SKILL_ROUTING.md)。默认按用户当前阶段分流：问题未定义用 `ai-collaboration-calibration`，主题/概念学习用 `research-topic-compiler`，单次决策调研用 `decision-research`，PRD 起草用 `prd-architect`，PRD 评审用 `prd-review`，已有方案压测用 `grill-me`。
