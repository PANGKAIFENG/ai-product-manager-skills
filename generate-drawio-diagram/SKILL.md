---
name: generate-drawio-diagram
description: >
  Draw.io 图示生成器 / 架构图流程图：当用户要把模块架构、系统架构、AI 协作链路、业务流程或核心步骤
  生成可编辑 Draw.io 图时使用。可用中文唤起：“画一张架构图”“生成 Draw.io”“给我流程图”
  “输出 .drawio 文件”。主输出是标准 .drawio mxfile XML，不是静态截图或普通 SVG。
metadata:
  tags: drawio, diagram, architecture, flowchart, mxgraph
---

# Draw.io 图示生成器（generate-drawio-diagram）

## 目标

把用户描述的系统架构、业务流程或 AI 协作链路转换成可编辑的 Draw.io `.drawio` 文件。重点不是做一张静态好看的图，而是生成结构清晰、节点可继续编辑、关系可追踪的 mxGraph 图示资产。

## 中文速查

- 中文名：Draw.io 图示生成器 / 架构图流程图
- 英文稳定名：`generate-drawio-diagram`
- 你可以这样叫我：`画一张架构图`、`生成 Draw.io`、`给我流程图`、`输出 .drawio 文件`
- 适合：需要后续在 Draw.io、VSCode Draw.io 插件或 diagrams.net 中继续编辑的架构图和流程图
- 不适合：只要一张不可编辑 PNG、纯 Mermaid 图，或需要真实设计稿视觉表现的场景

## When to use

- 需要生成可编辑架构图（模块架构、系统架构、AI 协作链路等）
- 需要生成可编辑流程图（主流程、核心步骤、判断分支等）
- 输出文件需要在 Draw.io 桌面 / VSCode 扩展 / Web 中直接打开编辑

## How to trigger

- `/generate-drawio-diagram`
- 或直接描述："给我画一张 xxx 的架构图，drawio 格式"

---

## Input

用户至少提供：

| 字段 | 必选 | 说明 |
|------|------|------|
| 图的内容描述 | ✅ | 模块名称、主要节点、流转关系 |
| 图的类型 | ✅ | `architecture`（一体化架构总图）或 `flow`（核心流程图） |
| 输出路径 | 可选 | 默认 `资产/架构图/<模块名>/<图名>.drawio` |

信息不足时先问清楚再动手，不要凭假设直接生成。

---

## Output

**主输出**：`.drawio` 文件（mxfile XML，可直接在 Draw.io 中打开编辑）

**可在以下工具打开：**
- VSCode 扩展：`hediet.vscode-drawio`（安装后直接双击 `.drawio` 打开）
- Draw.io 桌面 / Web：[app.diagrams.net](https://app.diagrams.net)，拖入即可

**关于 `.drawio.svg`（Markdown 嵌入）：**
生成 `.drawio` 文件后，如需 Markdown 可渲染的 `.drawio.svg`：
1. 在 Draw.io 中打开 `.drawio`，菜单 → Extras → Edit Diagram → File → Export as SVG（勾选 "Include a copy of my diagram"）
2. 或使用项目已有的 `sync-drawio-svg.sh` hook

## 验收标准

- 交付路径存在，文件扩展名为 `.drawio`，内容是完整 `<mxfile>` XML。
- Draw.io、diagrams.net 或 VSCode Draw.io 插件可以打开并继续编辑。
- 图中节点、泳道、判断和连线能覆盖用户给出的核心结构，不遗漏关键主流程。
- 所有边的 `source` / `target` 都指向存在的节点 ID，节点 ID 不重复。
- 布局符合所选图类型：架构总图用横向泳道，流程图用横向主线和外置分支。

## 评测与验证方式

生成后至少做文本级验证：检查 XML 闭合、ID 唯一、边引用有效、特殊字符已转义。若本地环境有 Draw.io CLI 或可视化预览工具，应再打开或导出一次确认文件可读。

---

## Diagram Types

### Type A: 一体化架构总图（`architecture`）

回答"系统是什么"——模块层次、输入输出、共享支撑。

**布局规则：**
- 4 列横向泳道，从左到右依次：外部输入层 → 核心处理层 A → 核心处理层 B → 输出回流层
- 每列 2–4 个核心卡片，不超过 4 个
- 底部加一条横跨各层的"共享支撑带"
- 禁止树状、放射状、脑图布局

**标准画布：** `pageWidth="1600" pageHeight="900"`

**泳道坐标模板：**

| 列 | x | width | 描述 |
|----|---|-------|------|
| 1 | 40 | 300 | 外部输入层 |
| 2 | 390 | 300 | 核心处理层 A |
| 3 | 740 | 300 | 核心处理层 B |
| 4 | 1090 | 300 | 输出回流层 |

泳道 y=80，height=520；卡片从 y=170 起，间距约 120。

---

### Type B: 核心流程图（`flow`）

回答"系统怎么跑"——主步骤、关键判断。

**布局规则：**
- 横向主线，主步骤 6–8 个，最多不超过 10 个
- 关键判断用菱形（rhombus）
- 深分支（澄清/回退/错误/人工确认）放主线上方或下方，不嵌入主线
- 如主流程超过 2 屏宽，必须拆子流程图

**标准画布：** `pageWidth="1600" pageHeight="900"`

**主线坐标模板：**

主步骤 y=190，height=100，步骤间距 240，从 x=40 开始。
上方分支 y=60，下方分支 y=340。

---

## Color Palette

| 角色 | fillColor | strokeColor |
|------|-----------|-------------|
| 外部输入层 / 泳道 A | `#eef4ff` | `#5b8def` |
| 核心处理 / 决策层 | `#fff7db` | `#d8a437` |
| 输出 / 完成节点 | `#dff4e6` | `#2e9c61` |
| 卡片默认底色 | `#ffffff` | 同层 strokeColor |
| 共享支撑带 | `#fff1b8` | `#d8a437` |
| 失败 / 回退节点 | `#ffe5e1` | `#c65d4d` |
| 菱形决策 | `#fff7db` | `#d8a437` |

**连线 strokeColor：**

| 场景 | 颜色 |
|------|------|
| 正向主流 | `#4e7fd1` |
| 决策 / 分支 | `#d8a437` |
| 输出 / 完成 | `#2e9c61` |
| 回退 / 失败 | `#c65d4d` |

---

## mxGraph XML Templates

### 文件骨架

```xml
<mxfile host="app.diagrams.net" modified="YYYY-MM-DDT00:00:00.000Z" agent="Claude/Codex" version="26.0.11">
  <diagram id="<diagram-id>" name="<图名>">
    <mxGraphModel dx="1600" dy="900" grid="1" gridSize="10" guides="1" tooltips="1"
      connect="1" arrows="1" fold="1" page="1" pageScale="1"
      pageWidth="1600" pageHeight="900" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- 节点和边 -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### 泳道容器

```xml
<mxCell id="lane-1" value="层标题&#xa;层说明"
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#eef4ff;strokeColor=#5b8def;strokeWidth=2;fontSize=20;fontStyle=1;"
  vertex="1" parent="1">
  <mxGeometry x="40" y="80" width="300" height="520" as="geometry"/>
</mxCell>
```

### 矩形卡片（普通节点）

```xml
<mxCell id="card-1" value="节点标题&#xa;补充说明（可省略）"
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#5b8def;strokeWidth=2;fontSize=17;"
  vertex="1" parent="1">
  <mxGeometry x="72" y="170" width="236" height="86" as="geometry"/>
</mxCell>
```

### 菱形（决策节点）

```xml
<mxCell id="decision-1" value="判断条件？"
  style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff7db;strokeColor=#d8a437;strokeWidth=2;fontSize=17;fontStyle=1;"
  vertex="1" parent="1">
  <mxGeometry x="520" y="182" width="160" height="100" as="geometry"/>
</mxCell>
```

### 边（连线）

```xml
<mxCell id="e1"
  style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor=#4e7fd1;strokeWidth=2.5;endArrow=block;"
  edge="1" parent="1" source="card-1" target="card-2">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

### 共享支撑带

```xml
<mxCell id="support" value="共享支撑带&#xa;记忆 / 规则 / 存储 / 治理等横向能力"
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff1b8;strokeColor=#d8a437;strokeWidth=2;fontSize=17;"
  vertex="1" parent="1">
  <mxGeometry x="390" y="640" width="650" height="90" as="geometry"/>
</mxCell>
```

---

## ID Naming Convention

| 类型 | 格式 |
|------|------|
| 泳道 / 层容器 | `lane-1`, `lane-2`, ... |
| 主步骤卡片 | `step-1`, `step-2`, ... 或 `card-1`, ... |
| 决策节点 | `decision-1`, `decision-2`, ... |
| 分支 / 深分支 | `branch-1`, `branch-2`, ... |
| 共享支撑 | `support`, `support-1`, ... |
| 边 | `e1`, `e2`, `e3`, ... |

---

## XML Encoding Rules

- 节点文字换行：用 `&#xa;`，不用 `\n`
- 文字中的特殊字符必须转义：`<` → `&lt;`，`>` → `&gt;`，`&` → `&amp;`，`"` → `&quot;`
- ID 不含空格、中文、特殊符号，只用字母数字和 `-`

---

## Quality Checklist

生成前自检：

- [ ] 架构总图：每列节点 ≤ 4，流程图主线 6–8 个
- [ ] 布局方向：横向，无树状 / 放射状
- [ ] ID 无重复，无空格
- [ ] 所有边的 source / target 均对应已存在的节点 ID
- [ ] 文字换行使用 `&#xa;`
- [ ] 特殊字符已转义
- [ ] `<mxfile>` 完整闭合，XML 合法

---

## Example

**输入：**
```
生成一张"推款智能体"核心流程图，drawio 格式
步骤：用户输入款式需求 → 款式理解与分解 → 知识库检索 → 结果排序与过滤 → 输出推款报告
关键判断：检索结果是否足够？不够则补充检索
输出路径：资产/架构图/推款智能体/推款主流程.drawio
```

**Claude/Codex 执行：**
1. 确认 5 个主步骤 + 1 个判断 → 符合 6–8 节点约定
2. 按模板骨架生成 mxfile XML
3. 写入 `资产/架构图/推款智能体/推款主流程.drawio`
4. 告知用户：用 Draw.io VSCode 扩展或 app.diagrams.net 打开编辑
