---
name: research-topic-compiler
description: >
  专题研究编译器 / 系统学习研究助手：当用户要围绕一个主题做系统学习、专题研究、行业调研、最佳实践提炼，
  并希望基于 Obsidian、本地资料、官方文档、GitHub、论文、产品渠道、Web、社区或 X 等渠道形成证据矩阵、
  Research Project 和研究报告时使用。适合“系统研究一个主题”“整理到 Obsidian”“做深度专题”
  “研究行业最佳实践”“把资料编译成研究报告”。不适合创建 Skill、评审 SKILL.md、普通即时搜索或一次性摘要。
---

# 专题研究编译器（research-topic-compiler）

## 中文速查

- 中文名：专题研究编译器 / 系统学习研究助手
- 英文稳定名：`research-topic-compiler`
- 分类：研究学习 / Obsidian 知识编译
- 你可以这样叫我：`系统研究这个主题`、`帮我整理到 Obsidian`、`做一个深度专题`、`研究行业最佳实践`、`把这些资料编译成研究报告`
- 适合：围绕研究主题做多渠道证据收集、筛选、证据矩阵、阶段结论和学习型研究报告
- 不适合：创建新 Skill，改用 `team-skill-creator`；评审 Skill，改用 `skill-reviewer`；普通新闻搜索或一次性摘要

## Overview

使用这个 Skill 把一个研究主题编译成可学习、可追溯、可继续扩展的 Obsidian Research Project。

核心原则：

- 先判断研究深度，再决定渠道和样本量。
- Obsidian 是内部基线和默认沉淀位置，不是唯一研究渠道。
- 外部渠道动态选择，不默认全开；根据主题类型、证据缺口、时效性和可信度要求启用。
- 结论必须能回到证据矩阵；报告负责系统学习，证据页负责按需深挖。
- 用户补充的新渠道可以进入渠道库，但要先判断适用主题、访问条件、证据强度和风险。

## Input / Context Intake

启动研究前先收集或推断这些上下文；不要问本地文件能发现的信息，只在答案会改变研究范围、访问权限或写回位置时追问：

- 研究主题：主题名称、用户要解决的决策或学习目标、是否已有种子资料。
- 预期产物：聊天内报告、Obsidian Research Project、更新已有专题、还是长期雷达。
- 深度约束：用户期望的速度、深度、样本量、是否需要 `L4/L5` 级外部扩展。
- 内部基线：是否扫描 Obsidian、哪些 Vault/目录可用、是否只读 `笔记同步助手`。
- 渠道偏好：必须看的渠道、明确排除的渠道、是否需要产品研究、GitHub、官方文档、论文、社区或 X。
- 访问边界：登录、API token、付费报告、私密社区、公司内部资料和引用限制。
- 写回边界：目标目录、命名规则、是否允许新增渠道到 `channel-registry.md`。

默认假设：Obsidian 是内部基线，公开外部渠道可用于补证；封闭、付费、登录或私密渠道必须先取得用户授权。用户补充渠道时，先判断是本次临时使用还是值得进入渠道库；只有用户明确希望复用时才写入 `references/channel-registry.md`。

## Catalog / Distribution Notes

- Catalog source：GitHub Skill 仓库 `git@github.com:PANGKAIFENG/skill.git` 的默认分支是标准源；本地 checkout 路径通常是 `/Users/linctex/.config/skillshare/skills`。
- Category/status：`categories/08-research-learning/`，中文分类“研究学习”，状态 `active`。
- Public/private decision：当前版本包含本机 Obsidian 路径和个人知识库约定，适合本地/团队 catalog；若要公开发布到 ClawHub 或其他市场，先参数化 Vault 路径并移除个人化约定。
- Distribution targets：保持 GitHub checkout、Multica 确认的 `multica-skill` 目录、`/Users/linctex/.codex/skills` 和 `/Users/linctex/.claude/skills` 一致；当前 Codex/Claude 可通过 Skillshare 管理的 symlink 使用。
- Sync rule：`skillshare sync` 是可选分发方式，不是本 Skill 的事实来源；使用前先确认目标路径确实由 Skillshare 管理。

## Workflow

1. 捕获主题和目标，用一句话复述研究对象、用户要解决的问题和预期产物。
2. 判断研究深度。非平凡主题先读 `references/research-depth-rubric.md`，推荐 `L1-L5`，并说明理由。
3. 选择渠道。读取 `references/channel-selection-rubric.md` 和 `references/channel-registry.md`，根据主题动态选择 Obsidian 之外的渠道。
4. 先输出 `Research Run Plan`。包含推荐深度、主题类型、核心问题、渠道选择、每个渠道启用或不启用的理由、样本量、写入位置、凭据或访问限制。
5. 做 Obsidian 内部基线扫描。查 `笔记同步助手`、`03_Resources`、已有 Research Project、主题卡片、规则和模板，确认已有沉淀、证据缺口和重复研究风险。
6. 做外部发现与筛选。只读取公开或用户授权内容；GitHub 仅读文档、源码、配置、issues 和 discussions，默认不执行第三方代码。
7. 建立证据矩阵。按“研究问题 × 来源 × 结论 × 证据强度 × 可借鉴点 × 扩展阅读”组织。
8. 写入或更新 Obsidian Research Project。默认输出 `00_研究定义` 到 `05_研究报告`；深度专题可增加 `06_外部渠道研究`、`07_行业案例对照`、`08_最佳实践与应用模板`。
9. 输出最终摘要。给出研究报告入口、核心结论、关键证据、仍需验证、下一步建议和新增渠道候选。

## Research Run Plan

开始研究前输出：

```markdown
**Research Run Plan**
- Topic: <研究主题>
- User goal: <用户要学会、判断或沉淀什么>
- Recommended depth: <L1 / L2 / L3 / L4 / L5, with reason>
- Topic type: <平台能力 / 开源工程 / 产品竞品 / 学术方法 / 政策合规 / 市场趋势 / 其他>
- Core questions: <3-8 个研究问题>
- Channels selected: <渠道 + 启用理由 + 样本量>
- Channels skipped: <未启用渠道 + 原因>
- Access needs: <GitHub token / X token / login / paywall / none>
- Obsidian output: <chat-only / new Research Project / update existing project>
- Expected files: <00-05, optional 06-08>
- Confirmation needed: <only if L4/L5, closed channels, credentials, or broad writes>
```

如果用户已经明确要求写入 Obsidian，`L1-L3` 可以在输出计划后继续执行。`L4/L5`、封闭渠道、付费资料、需要登录或凭据、自动化持续跟踪、跨多个项目的大范围写入，都要先取得明确确认。

## Channel Selection Rules

默认不是“所有渠道全开”，而是先判断主题，再选择渠道。

- 平台能力、API、机制、最佳实践：优先官方文档、公司工程博客、release notes、cookbook、SDK 示例。
- 开源实现、工程模式、工具链：启用 GitHub、包管理器、issues、discussions、示例项目。
- 产品研究、竞品、市场反馈：启用 Product Hunt、G2、Capterra、AlternativeTo、App Store、Chrome Web Store、VS Code Marketplace、定价页、changelog、用户评论。
- 学术方法、算法、评测、benchmark：启用论文、技术报告、Papers with Code、OpenReview、arXiv、Semantic Scholar。
- 趋势、近期发布、作者观点：启用 X、社区讨论、HN、Reddit、新闻稿和 newsletter；这些默认标为弱证据，除非能被官方或实现证据交叉验证。
- 政策、合规、安全：启用官方监管文件、标准组织、CVE/NVD、vendor advisories、security docs。
- 封闭或半封闭渠道：只在用户授权、提供访问方式且研究目标需要时使用；不要绕过登录、付费墙或访问限制。

## Obsidian Output Contract

写入 Obsidian 前读 `references/obsidian-output-contract.md`。

默认 Research Project 结构：

- `00_研究定义.md`
- `01_问题清单.md`
- `02_证据与卡片.md`
- `03_阶段结论.md`
- `04_下一步.md`
- `05_研究报告.md`

深度专题可补：

- `06_外部渠道研究.md`
- `07_行业案例对照.md`
- `08_最佳实践与应用模板.md`

`笔记同步助手` 是来源层，只读。不要移动、删除、覆盖原始同步文章。新 Resource、Theme 更新或长期 Area 结论只在规则允许时写回。

## Channel Registry Update

当用户补充新的研究渠道时，先判断它是否值得进入渠道库。

记录字段：

```markdown
| Channel | Best for | Access | Evidence level | Query method | Risks | Notes |
| --- | --- | --- | --- | --- | --- | --- |
```

处理规则：

- 如果用户明确说“以后也用这个渠道”或“补录进 Skill”，将它加入 `references/channel-registry.md` 的合适分区。
- 如果只是本次研究临时提供，把它记录到当前 Research Project 的 `02_证据与卡片` 或 `04_下一步`。
- 新渠道涉及登录、付费、私密社区、客户数据或内部资料时，必须标明访问条件和引用限制。
- 渠道库更新后，最终结果里说明新增了什么、适合什么主题、证据强度是什么。

## Output Format

完成后输出：

```markdown
**Research Result**
- Project/report: <Obsidian path or chat-only>
- Depth used: <L1-L5>
- Channels used: <channels and sample counts>
- Core conclusions: <3-7 bullets>
- Strongest evidence: <top sources>
- Weak or trend evidence: <sources that need caution>
- Added channel candidates: <new registry entries or none>
- Still uncertain: <evidence gaps>
- Next actions: <what to read or do next>
```

## Definition of Done

任务完成必须满足至少一种情况：

- `L1` 快查：给出直接答案、来源和证据局限。
- `L2-L3`：Research Project 或聊天报告已覆盖问题清单、证据矩阵、阶段结论和学习型报告。
- `L4`：额外形成外部渠道研究、行业案例对照或最佳实践模板。
- `L5`：形成 watchlist、更新日志和后续自动化建议；真正创建 automation 需用户单独确认。
- 如果渠道受限，必须说明未使用的渠道、限制原因和对结论可信度的影响。

## Resource Guide

- `references/research-depth-rubric.md`：判断 `L1-L5` 深度、样本量和确认门禁。
- `references/channel-selection-rubric.md`：按主题选择渠道。
- `references/channel-registry.md`：预置渠道库和后续补录位置。
- `references/source-quality-rules.md`：证据强度、来源筛选、引用和封闭渠道处理规则。
- `references/obsidian-output-contract.md`：Obsidian 写回结构和 Vault 规范。
- `references/report-writing-standards.md`：`05_研究报告` 写作标准。

## Evaluation Checklist

- Smoke：`帮我系统研究一下 AI Agent Memory，并整理到 Obsidian。`
- Smoke：`研究一下 MCP 安全最佳实践，需要看官方文档、GitHub 和行业案例。`
- Smoke：`快速了解 Claude Skills 的设计机制，不需要写入 Vault。`
- Channel selection：学术型主题应启用论文/技术报告。
- Channel selection：开源工具型主题应启用 GitHub。
- Channel selection：产品竞品型主题应考虑 Product Hunt、G2、marketplace、定价页、changelog 和用户评论。
- Channel selection：趋势型主题可启用 X/社区，但必须标注弱证据。
- Non-trigger：`帮我创建一个 Skill。` 应交给 `team-skill-creator`。
- Non-trigger：`帮我 review 这个 SKILL.md。` 应交给 `skill-reviewer`。
- Non-trigger：`搜一下今天某条新闻。` 不应触发本 Skill，除非用户要求沉淀成专题研究。
