# Skill Routing

这个文件用于解决相邻 Skill 的触发边界。原则是先判断用户当前处在哪个工作阶段，再选择 Skill；不要因为关键词相似就叠加多个 Skill。

## 核心路由表

| 用户当前状态 | 优先 Skill | 触发信号 | 不要用它做什么 |
| --- | --- | --- | --- |
| 问题还没定义清楚，需要先看清真正问题 | `ai-collaboration-calibration` | “先聊一下”“帮我想想”“挑战我的假设”“方向是不是错了” | 不直接产出最终 PRD、方案或调研结论 |
| 已有方案，需要压力测试和追问 | `grill-me` | “拷问我的方案”“压力测试”“问 hard questions”“哪里会翻车” | 不从零写方案，不替代 PRD 评审 |
| 有明确技术决策，需要单次调研和推荐 | `tech-research` | “有没有现成方案”“怎么接入”“技术上可行吗”“选 A 还是 B” | 不做长期知识库沉淀，不替代问题脑暴 |
| 要围绕主题做系统学习、专题研究或 Obsidian 沉淀 | `research-topic-compiler` | “系统研究”“做深度专题”“整理到 Obsidian”“我对这个领域陌生” | 不处理一次性即时搜索，不创建或评审 Skill |
| 要把想法、脑暴或需求草稿整理成 PRD | `prd-architect` | “帮我写 PRD”“选 PRD 模板”“把需求整理成 PRD” | 不评审已经成稿的 PRD，不直接写代码 |
| 已有 PRD/handoff，需要找缺口并修订 | `prd-review` | “帮我审 PRD”“从研发测试视角挑问题”“能不能交付开发” | 不从零生成 PRD，不做纯语言润色 |

## PRD 到开发计划的衔接

`prd-architect` 和 `prd-review` 的边界止于产品需求交付准备度。只有当 PRD 已经满足以下条件，才适合进入 superpowers `writing-plans`：

- 目标用户、问题、范围边界和非目标已明确。
- 主流程、关键状态、输入输出、异常或人工接管点已写清。
- 验收标准能被测试或人工检查。
- 阻断性待确认项已经关闭，或被显式列为 implementation plan 的前置假设。

进入 `writing-plans` 后，开发计划应负责文件边界、测试、实现步骤和提交节奏；PRD Skill 不替代开发计划 Skill。

## 研究类分流规则

- 如果用户问的是“我到底该解决什么问题”，先用 `ai-collaboration-calibration`。
- 如果用户问的是“这个技术路线应该选哪个”，用 `tech-research`。
- 如果用户问的是“我要系统理解一个领域并沉淀材料”，用 `research-topic-compiler`。
- 如果用户问的是“我已有一个方案，帮我找漏洞”，用 `grill-me`。
