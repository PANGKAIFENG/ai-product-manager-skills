# Mockup Handoff Reference

按需加载本文件。用于 PRD 涉及既有页面、弹窗、面板、按钮、表单、状态提示、HTML mockup 或截图承接时。

## Boundary

`prd-architect` 只负责 PRD 内的 UI 承接接口，不负责正式桌面端多状态高保真 mockup。

- PRD 内可交付：页面范围、关键状态、交互入口、验收口径、截图说明、轻量 HTML mockup notes。
- 正式 UI mockup：当 PRD 已确认且用户要求正式多状态页面稿，转 `ui-mockup-desktop-workbench`。

## Existing Project Rule

当需求发生在已有产品页面上，先定位：

1. 真实项目。
2. 真实 app / 路由。
3. 真实组件。
4. 用户触发动作。
5. 当前页面状态。

不要凭空画一个新页面代替真实项目页面。

## Static HTML / Screenshot Criteria

优先补静态 HTML mockup 或截图，当：

- 需求是一个现有页面上的新增状态、提示、弹窗、卡片、按钮区。
- 页面变化通过视觉位置更容易解释。
- 开发需要知道变更发生在哪个上下文。

PRD 中写清：

- 文件路径。
- 展示状态：默认态、拦截态、确认态、失败态、成功态。
- 是否基于真实组件结构复刻。
- 如果项目无法启动，明确标记“静态复刻，未运行真实应用”。

## Diagram vs Mockup

| 情况 | 优先产物 |
| --- | --- |
| 解释页面区域、按钮、状态提示 | screenshot / HTML mockup |
| 解释主链路、状态流转、上下游依赖 | Draw.io flow |
| 解释模块关系、输入输出、支撑层 | Draw.io architecture |
| 需要正式多状态高保真 UI | `ui-mockup-desktop-workbench` |

## Required PRD Text

PRD 中至少写：

- 页面入口。
- 触发动作。
- 新增或变化区域。
- 用户可见反馈。
- 关键状态。
- 验收方式。

## Correction Mode

如果用户指出“不是这个页面 / 不是这种 HTML / 要基于真实项目展示”，立即：

1. 回到用户指定项目和模块，重新确认 repo 边界。
2. 找到真实页面入口组件、触发按钮和状态来源。
3. 把 PRD 页面结构改成“真实页面 + 新增状态/弹窗”。
4. 删除错误页面相关术语、截图和流程。
5. 保留真实业务规则并映射到真实动作上。

