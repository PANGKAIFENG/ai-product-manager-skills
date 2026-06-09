---
name: prd-architect
description: >
  PRD 架构师 / 需求文档起草：当用户要把一个产品想法、需求草稿、脑暴结果或功能说明整理成 PRD 时使用。
  可用中文唤起：“帮我写 PRD”“帮我选 PRD 模板”“把这个需求整理成 PRD”“判断该用轻量 PRD 还是标准 PRD”。
  不用于直接编码、单纯画 UI，或评审一份已经写好的 PRD。
---

# PRD 架构师（prd-architect）

## 中文速查

- 中文名：PRD 架构师 / 需求文档起草
- 英文稳定名：`prd-architect`
- 你可以这样叫我：`帮我写 PRD`、`帮我选 PRD 模板`、`把这个需求整理成 PRD`、`这个需求该用哪种 PRD`
- 适合：需求还在成型，需要先判断文档深度、PRD 类型、当前成熟度和后续 handoff 接口
- 不适合：已经有完整 PRD 要评审，改用 `prd-review`；只要 UI 线框或直接编码也不应触发

## Overview

根据需求类型动态选择 PRD 模板，而不是固定套一套重型章节。

这个 skill 的职责是先定模板和阶段，再组织 PRD 的结构与承接关系。

## Responsibilities

这个 skill 负责：

1. 判断需求复杂度
2. 判断是否属于 AI-native 需求
3. 在 `PRD-lite / PRD-standard / PRD-ai-native` 中做选择
4. 判断当前应该输出 `草稿 / 讨论中 / 已确认` 哪一阶段的 PRD
5. 组织输出结构
6. 保留必要的待确认假设
7. 决定下一步是继续深化 PRD，还是可以进入 UI / handoff
8. 让 PRD 内部直接包含后续可执行的图示 / UI 承接接口

它不负责：

- 直接决定 UI 细节
- 直接开始编码
- 用重型模板压扁所有需求
- 把核心规则外包给单独 guide 再让用户自己跳转理解

## Decision Rules

### 选择 `PRD-lite`

当需求满足以下特征时优先：

- 单点改动
- 需求边界清晰
- 用户流程短
- 不涉及复杂状态与数据

### 选择 `PRD-standard`

当需求满足以下特征时优先：

- 常规产品功能
- 需要完整描述流程和边界
- 需要后续进入设计或开发

### 选择 `PRD-ai-native`

当需求满足以下特征时优先：

- 人和 AI 明显共同完成任务
- 需要写清人工动作与 AI 动作
- 需要定义状态反馈、人工接管、闭环

### 判断当前阶段

优先按下面规则判断：

- `草稿`
  - 仍在承接脑爆结果
  - 存在较多待确认项
  - 还不适合直接进入 UI
- `讨论中`
  - 主链路已经较清楚
  - 仍有少量关键问题待确认
  - 可以用来对齐，但还不是最终定稿
- `已确认`
  - 核心范围、主链路、关键输入输出与验收口径已基本确认
  - 不存在阻断性待确认项
  - 可以进入 UI / handoff / 开发承接

## Input Expectations

最好具备这些输入：

- 需求描述
- 目标用户
- 当前问题
- 成功标准
- 已知边界
- 是否涉及界面
- 是否涉及 AI 协作
- 如果项目里已有 `docs/PROJECT/` 总控上下文，优先把它当作输入约束之一

如果输入缺失：

- 先列出最少量澄清问题
- 或基于明确假设先出第一版

## Output Requirements

输出必须做到：

1. 结构与问题规模匹配
2. 明确事实与假设
3. 明确边界和不做项
4. 给后续 UI 或 handoff 留出承接接口
5. 如果是 `PRD-standard / PRD-ai-native`，把正式图示规则直接写进模板输出结构
6. 如果项目提供了 `docs/templates-local/` 下的同名 PRD 模板，优先使用 local override
7. 如果生成正式 `drawio.svg` 图示，必须避免“编辑视图”和“文档预览”指向不同内容：
   - Markdown 只引用根目录 `*.drawio.svg`
   - 不混用同名旧 `*.svg`
   - 不手工拼接 `mxfile`
8. 在文档顶部明确填写 `当前状态`，并让正文成熟度与该状态一致
9. 如果仍存在 `3` 个及以上待确认项，或存在任何阻断性待确认项，下一步默认应是“继续深化 / 对齐 PRD”，而不是 `/generate-ui-mockup`
10. 只有在 `当前状态=已确认`，且不存在阻断性待确认项时，才推荐 `/generate-ui-mockup`
11. 如果项目缺少真实 `project-context`，要把它作为 PRD 质量风险显式提醒出来，但不要因此拒绝输出第一版
12. 文档阶段判断只控制“下一步建议”和“待确认项处理”，不覆盖已有的正式图示要求

## Visual Rules

### `PRD-standard`

- 如果存在多阶段链路、模块依赖、上下游输入输出，正式稿应直接要求正式 `*.drawio.svg` 阅读终态
- 正式图示必须是文件本体内嵌 Draw.io 数据、可直接打开编辑的 `*.drawio.svg`
- Markdown 正式引用只指向根目录 `*.drawio.svg`，不要回退去引用同名普通 `*.svg`
- 同目录 `src/*.drawio` 只作为可选备份或迁移图源
- 默认优先从 `资产/架构图/_模板/src/` 复制骨架，不从空白画布起手
- 系统级 PRD 优先一张一体化架构总图 + 一张核心流程图
- 架构总图默认使用横向分层 / 泳道式 board，禁止脑图、放射状、树状发散布局
- 核心流程图默认横向主线，只保留主步骤和关键分支
- 总图只承载主链路、输出对象、共享支撑层，不承载所有分支细节
- 主链路节点优先控制在 `6-8` 个，最多不超过 `10` 个
- 如果图经过文案压缩和结构压缩后仍超过 `2` 屏高度，必须拆图，不继续硬压
- 同时为后续 `UI-spec-template` 预留接口

### `PRD-ai-native`

- 默认要求一体化总图 + 核心流程图
- 正式图示必须是文件本体内嵌 Draw.io 数据、可直接打开编辑的 `*.drawio.svg`
- Markdown 正式引用只指向根目录 `*.drawio.svg`，不要回退去引用同名普通 `*.svg`
- 同目录 `src/*.drawio` 只作为可选备份或迁移图源
- 默认优先从 `资产/架构图/_模板/src/` 复制骨架，不从空白画布起手
- 默认要求模块拆解与输入输出
- 默认要求人工动作 / AI 动作 / 状态反馈 / 闭环一起成套表达
- 架构总图默认使用横向分层 / 泳道式 board，禁止脑图、放射状、树状发散布局
- 核心流程图默认横向主线，只保留 `6-8` 个核心节点
- 总图只承载主链路、输出对象、共享支撑层，不承载所有分支细节
- 主流程优先保留 `6-8` 个核心节点
- 澄清 / 降级 / 记忆写入 / 人工确认等深分支默认拆成子流程图
- 如果图经过文案压缩和结构压缩后仍超过 `2` 屏高度，必须拆图，不继续硬压
- 如果鼠标悬浮缩略图还是旧图，优先按编辑器缓存处理，不要直接判定文件失效

## Template References

优先参考：

- `~/.honeycomb-agent/templates/PRD-lite.md`
- `~/.honeycomb-agent/templates/PRD-standard.md`
- `~/.honeycomb-agent/templates/PRD-ai-native.md`
- `~/.honeycomb-agent/templates/examples/PRD-ai-native-example.md`
- `资产/架构图/_模板/src/模块一体化架构总图.drawio`
- `资产/架构图/_模板/src/模块核心流程图.drawio`

## Superpowers Writing-Plans Handoff

这个 Skill 与 superpowers 的关系是“产品需求输入 -> implementation plan”的上游衔接，不替代开发流。

只有 PRD 满足以下条件，才建议进入 superpowers `writing-plans`：

- 目标用户、问题、范围边界和非目标已经明确。
- 主流程、关键状态、输入输出、异常或人工接管点已经写清。
- 验收标准能被测试、人工检查或通过具体 artifact 验证。
- 阻断性待确认项已经关闭；若仍有假设，必须明确写成 implementation plan 的前置假设。

如果不满足这些条件，下一步应继续深化 PRD、补 handoff 或做 `prd-review`，不要把模糊需求交给开发计划 Skill。

## Definition of Done

完成标准是：

- 已选定合适的 PRD 类型
- 当前状态明确
- 待确认项和假设没有混在一起
- 图示与 UI 承接规则已写进正文
- 下一步建议不会把草稿误推成定稿

## Evaluation

Smoke prompts:

- 单点改动，是否会选 `PRD-lite`
- AI 协作需求，是否会选 `PRD-ai-native`
- 复杂流程需求，是否会保留 `当前状态` 和待确认项

Non-trigger prompts:

- 直接让它改代码
- 只让它画 UI
- 只让它做目录治理

Resources:

- `~/.honeycomb-agent/templates/PRD-lite.md`
- `~/.honeycomb-agent/templates/PRD-standard.md`
- `~/.honeycomb-agent/templates/PRD-ai-native.md`
- `~/.honeycomb-agent/diagram-templates/`
