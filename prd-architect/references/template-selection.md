# PRD Template Selection

按需加载本文件，用来选择一个 PRD 模板资产。选择后只读取对应模板，不要同时混用多个模板骨架。

## Selection Order

1. 先判断是否需要 PRD：如果问题、用户、目标或成功标准还不清楚，先转上游校准。
2. 再判断改动规模：单点规则、常规跨状态功能，还是 AI-native 协作链路。
3. 再判断当前状态：`草稿`、`讨论中`、`已确认`。
4. 最后决定是否加载 mockup、diagram 或 handoff 附加资产。

## PRD-lite

选择条件：

- 单点改动。
- 边界清楚，用户流程短。
- 不涉及复杂状态和多模块依赖。
- 只需要让研发理解触发条件、页面反馈、边界和验收。

典型例子：

- 一个现有按钮点击后的限制规则。
- 一个弹窗、提示、空态、错误态。
- 一项局部权限、配额或确认逻辑。

读取：`references/templates/prd-lite.md`

## PRD-standard

选择条件：

- 常规产品功能。
- 需要完整描述流程和边界。
- 涉及多个状态、异常分支或多个页面区域。
- 需要后续进入设计、研发或测试对齐。

注意：

- Standard 不等于开发 handoff。
- 默认写产品对象、业务规则、页面状态和验收。
- 只有用户明确要求开发 handoff 时，才加载 `references/handoff-appendix.md`。

读取：`references/templates/prd-standard.md`

## PRD-ai-native

选择条件：

- 人和 AI 明显共同完成任务。
- AI 会理解、生成、推荐、排序、记忆、改写或回写上下文。
- 需要写清人工确认、人工接管、失败回退、状态反馈或闭环。

不要因为需求里出现 Agent、AI、Sandbox、Workflow 就自动升级。若本期只是 AI 产品里的普通 UI 限制、提示、权限或配额，优先用 `PRD-lite` 或 `PRD-standard`。

读取：`references/templates/prd-ai-native.md`

## Maturity State

### 草稿

- 仍在承接脑暴结果。
- 存在多个待确认项。
- 不适合直接进入 UI 或开发计划。
- 输出要压缩，重点帮助用户对齐问题和范围。

### 讨论中

- 主链路较清楚。
- 仍有少量关键问题待确认。
- 可以用于评审和对齐，但不是最终定稿。

### 已确认

- 核心范围、主链路、关键输入输出与验收口径基本确认。
- 不存在阻断性待确认项。
- 可以进入 UI / handoff / 开发计划。

## Optional Asset Triggers

| 条件 | 加载资产 |
| --- | --- |
| 涉及既有页面、弹窗、按钮、表单、状态提示 | `references/mockup-handoff.md` |
| 用户要求可编辑流程图 / 架构图 | `references/drawio-templates.md` |
| 多阶段链路、上下游依赖、对象流转、状态切换 | `references/drawio-templates.md` |
| 用户明确要求字段、协议、接口、schema、metadata、adapter | `references/handoff-appendix.md` |
| 需要避免初版 PRD 过重或过技术 | `references/prd-shape-gates.md` |

