---
name: generate-drawio-diagram
description: >
  Draw.io 图示生成器 / 架构图流程图：当用户要把模块架构、系统架构、AI 协作链路、业务流程或核心步骤
  生成可编辑 Draw.io 图时使用。可用中文唤起：“画一张架构图”“生成 Draw.io”“给我流程图”
  “输出 .drawio 文件”。不用于只要不可编辑 PNG、普通 SVG、纯 Mermaid 或设计稿视觉表现的场景。
---

# Draw.io 图示生成器（generate-drawio-diagram）

## Overview

把用户描述的系统架构、业务流程或 AI 协作链路转换成可编辑的 Draw.io `.drawio` 文件。重点不是做静态截图，而是生成结构清晰、节点可继续编辑、关系可追踪的 mxGraph 图示资产。

## 中文速查

- 中文名：Draw.io 图示生成器 / 架构图流程图
- 英文稳定名：`generate-drawio-diagram`
- 你可以这样叫我：`画一张架构图`、`生成 Draw.io`、`给我流程图`、`输出 .drawio 文件`
- 适合：需要后续在 Draw.io、VSCode Draw.io 插件或 diagrams.net 中继续编辑的架构图和流程图
- 不适合：只要一张不可编辑 PNG、纯 Mermaid 图，或需要真实设计稿视觉表现的场景

## Input

用户至少提供：

| 字段 | 必选 | 说明 |
|------|------|------|
| 图的内容描述 | yes | 模块名称、主要节点、流转关系 |
| 图的类型 | yes | `architecture` 一体化架构总图，或 `flow` 核心流程图 |
| 输出路径 | no | 默认 `资产/架构图/<模块名>/<图名>.drawio` |

信息不足时先问清楚再动手，不要凭假设直接生成。

## Output

主输出是 `.drawio` 文件，内容为完整 `<mxfile>` XML，可在 Draw.io、diagrams.net 或 VSCode Draw.io 插件中打开编辑。

如需 Markdown 可渲染的 `.drawio.svg`，先生成 `.drawio`，再用 Draw.io 导出 SVG 并勾选包含图数据，或使用项目已有同步 hook。

## Workflow

1. 判断图类型：`architecture` 或 `flow`。
2. 按用户给出的节点和关系压缩主链路，避免把所有细节堆进一张图。
3. 从 `references/drawio-templates.md` 加载对应布局、颜色、XML 骨架和 ID 规则。
4. 写入 `.drawio` 文件。
5. 运行 `scripts/validate_drawio.py <path>`。
6. 如果校验失败，先修复 XML、重复 ID 或边引用，再交付。

## Acceptance Criteria

- 交付路径存在，文件扩展名为 `.drawio`，内容是完整 `<mxfile>` XML。
- 图中节点、泳道、判断和连线覆盖用户给出的核心结构，不遗漏关键主流程。
- 所有边的 `source` / `target` 都指向存在的节点 ID，节点 ID 不重复。
- 布局符合所选图类型：架构总图用横向泳道，流程图用横向主线和外置分支。
- `python3 scripts/validate_drawio.py <path>` 通过。

## Resource Guide

- 布局、颜色、XML 模板、ID 和编码规则：`references/drawio-templates.md`
- 确定性校验脚本：`scripts/validate_drawio.py`

## Evaluation

Smoke prompts:

- `生成一张推款智能体的一体化架构图，drawio 格式。`
- `给我画一张订单审核核心流程图，输出 .drawio 文件。`

Non-trigger prompts:

- `画一个 Mermaid 流程图就行。`
- `给我做一张不可编辑 PNG 海报。`
- `帮我写 PRD，不需要图。`
