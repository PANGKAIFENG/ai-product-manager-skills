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
| `product-prd` | 产品与 PRD | 需求结构化、PRD 起草、PRD 图示、PRD 评审、issue backlog、UI 线框、UI mockup 和交付准备。 |

## 中文检索表

| Skill | 中文名 | 你可以这样说 | 适合什么时候用 | 不适合什么时候用 | 状态 |
| --- | --- | --- | --- | --- | --- |
| `ai-collaboration-calibration` | 协作校准 / 认知校准 | “先别执行，帮我看清问题”“挑战我的假设”“这个方案是不是想错了” | 复杂问题进入执行前，先校准问题定义、领域定位、隐藏假设和方案裂缝。 | 翻译、摘要、格式转换、明确的小改动。 | core |
| `research-topic-compiler` | 专题研究编译器 / 概念源流研究助手 | “系统研究这个主题”“整理到 Obsidian”“概念解读”“概念源流”“PM 技术评审提问脚本”“行业演进看板”“把我的大白话拆成研究目标” | 多渠道主题研究、系统学习、轻量概念解构、概念源流、语义演化、PM 决策看板和研究报告；也能把模糊主题、业务愿望或 Roadmap 前置想法转成研究目标、研究问题和输出要求；需要长期更新时可启用 Research Radar Loop。 | 创建或评审 Skill；普通即时搜索；一次性摘要。 | core |
| `decision-research` | 决策调研 / 决策驱动调研 | “有没有现成方案”“这个怎么接”“这个选择可行吗”“帮我选一个” | 问题已定义清楚，需要围绕平台接入、可行性、方案选型或决策路线做单次调研，并给出有立场推荐和排除理由；需要多轮收敛时可启用 Decision Research Loop。 | 问题还没定义清楚；需要长期知识沉淀；创建或评审 Skill。 | active |
| `brainstorming` | 设计脑暴 / 实现前方案校准 | “先脑暴一下方案”“先不要写 PRD，帮我设计几种路径”“参考 brainstorming 把这个需求变成设计 spec” | 问题基本成立，但在写 PRD、画 mockup 或进入开发计划前，还需要一问一答澄清关键缺口、比较 2-3 个方案、确认设计取舍；涉及 UI/mockup 时先发现并对齐项目视觉规范，再输出设计 spec。 | 问题还没定义清楚；已有方案要压力测试；直接写 PRD；直接实现代码。 | core |
| `prd-architect` | PRD 架构师 / 需求文档起草 | “帮我写 PRD”“帮我选 PRD 模板”“把这个需求整理成 PRD”“PRD 里补 Draw.io 流程图” | 从想法、脑暴或需求草稿进入 PRD 结构；需要判断 `PRD-lite`、`PRD-standard`、`PRD-ai-native`、文档成熟度和正式图示。 | 已有完整 PRD 要评审；直接编码；单纯画 UI。 | core |
| `prd-review` | PRD 评审 / 需求评审 | “帮我审 PRD”“从研发测试视角挑问题”“这个需求文档能不能交付开发”“检查 PRD 图示是否可编辑” | 已有 PRD/handoff，需要找阻断项、冲突、不可实现点、不可测试点、图示缺口，并给修订草案；需要多轮关闭阻断项时可启用 PRD Readiness Loop。 | 从零写 PRD；只做语言润色。 | core |
| `prd-to-issues` | PRD 到研发 Issue 拆解 | “把 PRD 拆成 issue”“需求文档拆任务”“生成 GitHub issues”“按 vertical slice 拆开发票” | PRD 已经 ready，需要拆成可独立领取、可验收、适合 GitHub Issues 承接的 vertical-slice implementation issues，并输出 coverage matrix。 | 从零写 PRD；评审 PRD 缺口；写文件级 implementation plan、测试策略或提交节奏。 | active |
| `ui-wireframe-to-html` | PRD 到 UI 线框 / 结构阶段 | “先出 UI 结构”“把 PRD 变成线框”“先做 ASCII 布局”“只确认状态和布局” | PRD 已可用，但只需要先输出 screen inventory、状态模型、ASCII layout 和可选低保真 HTML，确认结构/状态而不是视觉 polish。 | 高保真视觉；开发复刻；真实项目组件映射；project-native preview；implementation notes。 | active |
| `ui-mockup-desktop-workbench` | 高保真 UI 交付对齐器 / 桌面工作台 UI Mockup 生成器 | “基于 PRD 出高保真 mockup”“从 PRD 先结构再高保真”“开发要完全复刻这个 UI”“做项目原生 preview”“输出 component map” | PRD/UI 方向已确认，需要先承接结构阶段，再把桌面工作台 UI 转成可截图确认、可映射真实组件、可交给前端实现的 `project-native-preview`、`visual-handoff` 或 `concept-html`。 | 问题还没定义清楚；只要 PRD 文案；只做低保真结构且不进入高保真；直接写生产功能不需要视觉确认。 | active |
| `grill-me` | 方案拷问 / 压力测试 | “拷问我的方案”“压力测试这个设计”“这个方案哪里会翻车” | 已有方案但担心盲点，需要一问一答澄清依赖、分支、取舍和失败模式。 | 直接写最终方案；泛泛总结；不希望互动追问。 | active |
| `ai-work-assetization-diagnoser` | AI 工作资产化诊断器 / 资产化路由器 | “这段工作是不是值得做成 Skill”“这个 prompt 应该沉淀成 workflow 还是 Skill”“判断该资产化到哪层” | 重复 AI 工作、prompt、协作会话或团队场景需要判断应沉淀为 Prompt、Context Pack、Workflow、Skill、Loop、System，或不值得沉淀。 | 直接创建 Skill；普通 trace 根因定位；一次性事实查询；高责任专业判断。 | active |

## Loop Extension Catalog

Loop Extension 是现有 Skill 内的状态化合约，不是新增公开 Skill，不改变根目录 Skill 数量。

| Loop Extension | Parent Skill | 触发信号 | 合约文件 |
| --- | --- | --- | --- |
| Decision Research Loop | `decision-research` | “持续跟踪这个决策”“多轮收敛”“保存状态”“下一轮继续更新结论” | `decision-research/references/decision-loop-contract.md` |
| Research Radar Loop | `research-topic-compiler` | “长期雷达”“持续更新这个主题”“定期复盘”“更新已有研究项目” | `research-topic-compiler/references/research-radar-loop-contract.md` |
| PRD Readiness Loop | `prd-review` | “继续上一轮 review”“关闭阻断项”“判断是否能进 writing-plans”“跟踪修订状态” | `prd-review/references/prd-readiness-loop-contract.md` |

## 推荐白名单

当前建议加入 Codex/Claude 常用白名单的公开 Skill：

- `ai-collaboration-calibration`
- `research-topic-compiler`
- `decision-research`
- `brainstorming`
- `prd-architect`
- `prd-review`
- `prd-to-issues`
- `ui-wireframe-to-html`
- `ui-mockup-desktop-workbench`
- `grill-me`
- `ai-work-assetization-diagnoser`

## 公开发布规则

发布到 ClawHub 或公开推广前，至少检查：

1. `SKILL.md` 是否有标准 frontmatter。
2. 是否包含公司、客户、个人或内部系统敏感信息。
3. 是否有许可证限制或第三方归属要求。
4. 触发边界是否足够清楚，避免误触发。
5. 是否有最小验证方式，例如脚本、示例 prompt 或检查清单。

## 相邻 Skill 路由

当多个 Skill 都可能被中文关键词触发时，先查 [SKILL_ROUTING.md](SKILL_ROUTING.md)。默认按用户当前阶段分流：问题未定义用 `ai-collaboration-calibration`，主题/概念学习用 `research-topic-compiler`，单次决策调研用 `decision-research`，方案还没定但要进入 PRD / mockup / 开发计划前用 `brainstorming`，PRD 起草用 `prd-architect`，PRD 评审用 `prd-review`，PRD 已 ready 要拆 GitHub implementation issues 用 `prd-to-issues`，只做 UI 结构/状态/ASCII 线框用 `ui-wireframe-to-html`，PRD 后高保真 UI handoff / project-native preview / 组件映射用 `ui-mockup-desktop-workbench`，已有方案压测用 `grill-me`，重复 AI 工作资产化判断用 `ai-work-assetization-diagnoser`。
