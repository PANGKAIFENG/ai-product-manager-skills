# Draw.io Templates Reference

按需加载本文件。主 Skill 只负责触发、输入输出和验证要求；这里保留布局、颜色、XML 模板、ID 和编码规则。

## Diagram Types

### Type A: Architecture

回答“系统是什么”：模块层次、输入输出、共享支撑。

布局规则：

- 4 列横向泳道，从左到右依次：外部输入层、核心处理层 A、核心处理层 B、输出回流层。
- 每列 2-4 个核心卡片，不超过 4 个。
- 底部加一条横跨各层的共享支撑带。
- 禁止树状、放射状、脑图布局。
- 标准画布：`pageWidth="1600" pageHeight="900"`。

泳道坐标：

| 列 | x | width | 描述 |
|----|---|-------|------|
| 1 | 40 | 300 | 外部输入层 |
| 2 | 390 | 300 | 核心处理层 A |
| 3 | 740 | 300 | 核心处理层 B |
| 4 | 1090 | 300 | 输出回流层 |

泳道 `y=80`，`height=520`；卡片从 `y=170` 起，间距约 120。

### Type B: Flow

回答“系统怎么跑”：主步骤、关键判断。

布局规则：

- 横向主线，主步骤 6-8 个，最多不超过 10 个。
- 关键判断用菱形。
- 深分支放主线上方或下方，不嵌入主线。
- 如主流程超过 2 屏宽，必须拆子流程图。
- 标准画布：`pageWidth="1600" pageHeight="900"`。

主线坐标：主步骤 `y=190`，`height=100`，步骤间距 240，从 `x=40` 开始。上方分支 `y=60`，下方分支 `y=340`。

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

连线颜色：

| 场景 | strokeColor |
|------|-------------|
| 正向主流 | `#4e7fd1` |
| 决策 / 分支 | `#d8a437` |
| 输出 / 完成 | `#2e9c61` |
| 回退 / 失败 | `#c65d4d` |

## XML Templates

### File Skeleton

```xml
<mxfile host="app.diagrams.net" modified="YYYY-MM-DDT00:00:00.000Z" agent="Claude/Codex" version="26.0.11">
  <diagram id="<diagram-id>" name="<图名>">
    <mxGraphModel dx="1600" dy="900" grid="1" gridSize="10" guides="1" tooltips="1"
      connect="1" arrows="1" fold="1" page="1" pageScale="1"
      pageWidth="1600" pageHeight="900" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        <!-- nodes and edges -->
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### Lane

```xml
<mxCell id="lane-1" value="层标题&#xa;层说明"
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#eef4ff;strokeColor=#5b8def;strokeWidth=2;fontSize=20;fontStyle=1;"
  vertex="1" parent="1">
  <mxGeometry x="40" y="80" width="300" height="520" as="geometry"/>
</mxCell>
```

### Card

```xml
<mxCell id="card-1" value="节点标题&#xa;补充说明"
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#5b8def;strokeWidth=2;fontSize=17;"
  vertex="1" parent="1">
  <mxGeometry x="72" y="170" width="236" height="86" as="geometry"/>
</mxCell>
```

### Decision

```xml
<mxCell id="decision-1" value="判断条件？"
  style="rhombus;whiteSpace=wrap;html=1;fillColor=#fff7db;strokeColor=#d8a437;strokeWidth=2;fontSize=17;fontStyle=1;"
  vertex="1" parent="1">
  <mxGeometry x="520" y="182" width="160" height="100" as="geometry"/>
</mxCell>
```

### Edge

```xml
<mxCell id="e1"
  style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor=#4e7fd1;strokeWidth=2.5;endArrow=block;"
  edge="1" parent="1" source="card-1" target="card-2">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

### Support Band

```xml
<mxCell id="support" value="共享支撑带&#xa;记忆 / 规则 / 存储 / 治理等横向能力"
  style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff1b8;strokeColor=#d8a437;strokeWidth=2;fontSize=17;"
  vertex="1" parent="1">
  <mxGeometry x="390" y="640" width="650" height="90" as="geometry"/>
</mxCell>
```

## ID Naming Convention

| 类型 | 格式 |
|------|------|
| 泳道 / 层容器 | `lane-1`, `lane-2` |
| 主步骤卡片 | `step-1`, `step-2` 或 `card-1` |
| 决策节点 | `decision-1`, `decision-2` |
| 分支 / 深分支 | `branch-1`, `branch-2` |
| 共享支撑 | `support`, `support-1` |
| 边 | `e1`, `e2`, `e3` |

## XML Encoding Rules

- 节点文字换行：用 `&#xa;`，不用 raw newline。
- 文字中的特殊字符必须转义：`<` -> `&lt;`，`>` -> `&gt;`，`&` -> `&amp;`，`"` -> `&quot;`。
- ID 不含空格、中文、特殊符号，只用字母数字和 `-`。

## Quality Checklist

- 架构总图：每列节点 <= 4；流程图主线 6-8 个。
- 布局方向：横向，无树状 / 放射状。
- ID 无重复，无空格。
- 所有边的 source / target 均对应已存在的节点 ID。
- 文字换行使用 `&#xa;`。
- 特殊字符已转义。
- `<mxfile>` 完整闭合，XML 合法。

## Example Prompt

```text
生成一张“推款智能体”核心流程图，drawio 格式
步骤：用户输入款式需求 -> 款式理解与分解 -> 知识库检索 -> 结果排序与过滤 -> 输出推款报告
关键判断：检索结果是否足够？不够则补充检索
输出路径：资产/架构图/推款智能体/推款主流程.drawio
```
