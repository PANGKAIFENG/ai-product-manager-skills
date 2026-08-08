# StyleWork UI 基线

仅用于 StyleWork 相关 Demo 和方案讨论。当前正式前端源码不可访问，本文件的细节主要来自本地集成分支和项目原生预览，必须视为临时 UI 证据。

## 产品壳

优先沿用三段式工作台逻辑：

1. 左侧 workspace/session 导航；
2. 中间 conversation、任务进度、结果摘要与 composer；
3. 右侧按需出现的资源或 artifact 查看区域。

不要默认新增顶层菜单。新增功能的入口顺序：

1. 会话中的 Agent 任务；
2. 会话内结构化结果卡；
3. 右侧资源/artifact 面板；
4. 只有持续监控、跨任务管理或复杂配置确有必要时才新增独立页面。

## 交互模式

| 场景 | 优先模式 |
| --- | --- |
| 上传图、文件或已有资源 | composer attachment / resource selection |
| 展示候选款式或面料 | `resource-picker`，支持单选或多选 |
| 展示生成图片、视频、报告 | media result 或 artifact |
| 多步复杂任务 | 会话内 step progress，显示业务步骤 |
| 轻量任务 | brief progress，不展开冗长技术过程 |
| 失败或降级 | 说明业务影响、可重试/继续路径，不展示原始堆栈 |
| 后续动作 | 结果摘要后的 next actions 或继续对话 |

## 视觉规则

- 复用项目现有设计系统、DLS token、排版、按钮、Tabs、Resizable Panel 和 Lucide 图标。
- 保持安静、紧凑、工作导向；卡片只承载独立结果、选择项或状态块，不把页面章节层层卡片化。
- 状态使用现有语义色：中性、运行、成功、警告、错误；不要自创主色体系。
- 不把原始 tool payload、runId、callId、JSON 或 stack trace 暴露给普通用户。
- Demo 中所有交互控件要有完整状态；模拟结果必须清楚标注。

## Demo 结构选择

- 一次性生成/检索任务：在现有 session 中完成“输入 -> 进度 -> 结果 -> 下一步”。
- 候选选择任务：结果使用 resource-picker，不另做表格式后台。
- 需要长期趋势监控或对比：可以设计独立工作区视图，但必须说明为什么会话与 artifact 不足以承载。
- StyleWork 适配不明确时，先做低保真线框，不急于高保真视觉稿。

## 禁止误用

本地 `/preview/styleclaw-runtime`、runtime planning blocks 和 artifact panel 方案是项目原生预览/候选实现证据，不等于正式发布功能。对客户材料不得写成“当前已上线”，除非最新正式版本另有验证。
