# PRD Shape Gates

按需加载本文件。用于生成后自检 PRD 是否结构过重、章节误激活或过早技术化。

## Product Draft Gates

适用于 `草稿` 和 `讨论中` 阶段：

- 是否用一句话写清本期只解决什么。
- 是否只加载一个 PRD 模板。
- 是否没有把字段、schema、metadata 写进产品主链路。
- 是否保留真实待确认项。
- 是否没有把草稿误推成开发计划。

## Template-specific Gates

### PRD-lite

- 主场景不超过 2 个。
- 主流程 3-5 步。
- 不强制正式 Draw.io。
- 页面变更优先截图或 HTML mockup。

### PRD-standard

- 有入口、触发、核心对象、页面状态、交互逻辑、异常、验收。
- `核心对象与业务规则` 不应退化成 TypeScript / JSON schema。
- 多阶段链路才启用正式流程图。

### PRD-ai-native

- 人工动作、AI 动作、系统反馈、边界清楚。
- 状态反馈和人工确认闭环清楚。
- 记忆 / 上下文写入只写产品语义，技术 schema 放 handoff 附录。

## Over-technical Warnings

产品初版正文出现以下内容时通常需要降级或移到 handoff 附录：

- `interface Xxx`。
- ```ts / ```typescript 代码块。
- ```json 代码块。
- `metadata`、`adapter`、`endpoint`、`schema` 作为章节核心。
- `requiredCapabilities`、`capability registry`、`action_template_registry` 等实现治理细节。
- 大量真实代码路径列表。

## Readiness Gates

PRD 只有满足以下条件，才建议进入 `writing-plans`：

- 目标用户、问题、范围边界和非目标明确。
- 主流程、关键状态、输入输出、异常或人工接管点清楚。
- 验收标准可测试、可人工检查或可通过具体 artifact 验证。
- 阻断性待确认项已经关闭，或显式转成 implementation plan 前置假设。

