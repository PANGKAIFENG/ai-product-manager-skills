# PRD-lite Template

用于单点改动、局部体验、轻量规则。目标是让研发、设计或测试快速理解“触发条件、用户反馈、边界、验收”，不追求完整系统图。

## Output Skeleton

### 0. 文档信息

| 字段 | 内容 |
| --- | --- |
| 功能名 |  |
| 需求类型 | PRD-lite |
| 当前状态 | 草稿 / 讨论中 / 已确认 |
| 关联模块 |  |
| 更新时间 |  |

开头必须用一句话说明：本期只解决什么。

### 1. 功能目标

写：

- 当前问题。
- 本期目标。
- 成功标准。
- 非目标。

不要写泛泛的行业背景或长期愿景。

### 2. 用户场景

只保留 1-2 个真实场景。每个场景写：

- 用户是谁。
- 在什么上下文触发。
- 期望系统怎么反馈。

如果只有一个核心场景，不要硬写场景 B。

### 3. 关键交互

用表格表达：

| 触发 | 系统响应 | 用户可见反馈 | 备注 |
| --- | --- | --- | --- |

### 4. 主流程概览

写 3-5 步主链路。有必要时可用 Mermaid 草稿；不默认生成 Draw.io。

### 5. 验收标准

写可验证 checklist。每条都应该能通过人工检查、测试用例或具体 artifact 验证。

### 6. 待确认事项

只放真实未决问题。不要把假设写成已确认需求。

## Optional Sections

- 涉及既有页面时，加载 `references/mockup-handoff.md`，补真实页面截图或 HTML mockup 承接。
- 用户明确要求开发字段时，加载 `references/handoff-appendix.md`，把字段放在附录。

## Prohibited In Main Body

产品初版和讨论稿正文不要写：

- TypeScript interface。
- JSON schema。
- endpoint 或路由定义。
- adapter 字段。
- hidden metadata 结构。
- capability registry。

