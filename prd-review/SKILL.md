---
name: prd-review
description: >
  PRD 评审 / 需求评审：当用户已有 PRD 初稿、handoff、需求文档或产品方案，需要从 PM、研发、测试视角找缺口、
  冲突、不可实现点和不可测试点时使用。可用中文唤起：“帮我审 PRD”“从研发和测试视角挑问题”
  “这个需求文档能不能交付开发”“帮我给 PRD 出修改草案”。不用于凭空生成 PRD 初稿；从零起草优先用 prd-architect。
---

# PRD 评审（prd-review）

## 中文速查

- 中文名：PRD 评审 / 需求评审
- 英文稳定名：`prd-review`
- 你可以这样叫我：`帮我审 PRD`、`从研发测试视角挑问题`、`这个需求文档能不能交付开发`、`帮我补一版修订草案`
- 适合：已经有 PRD/handoff，需要发现阻断项、重要缺口、验收不可测、工程无法落地的地方
- 不适合：从零写 PRD，改用 `prd-architect`；只做语言润色时不需要触发

## Overview

站在不同角色视角审视已产出的第一版 PRD，输出：

1. 结构化评审报告
2. 可执行的修订建议
3. 可直接回填到 PRD 的修订草案

这个 skill 默认服务于“AI 先出第一版 PRD，人再做多轮 review 修正”的场景。

## Responsibilities

这个 skill 负责：

1. 先读取 handoff，建立功能背景、上下文、目标用户、约束和已确认事实
2. 再读取待评审的 PRD 初稿，识别事实、假设、缺口和冲突
3. 至少从 `产品经理`、`研发`、`测试` 三个视角做 review
4. 把重复问题合并，输出按严重程度排序的修改建议
5. 给出“怎么改”而不是只说“哪里有问题”
6. 在必要时补出可直接替换或新增到 PRD 的修订草案

它不负责：

1. 在没有 handoff / PRD 的情况下凭空生成完整方案
2. 把未确认业务事实伪装成已确认结论
3. 未经要求直接重写整份 PRD 成终稿
4. 为了显得完整而强行添加与当前阶段无关的大段章节

## Default Inputs

最好同时具备：

- `handoff` 文档
- 第一版 `PRD` 文档

可选补充输入：

- 本轮评审更关注的角色或维度
- 当前用户已经明确担心的问题
- 相关 UI / 架构图 / 历史评审意见

如果输入不完整：

1. 优先读取 handoff
2. 明确哪些结论来自 handoff，哪些只是 PRD 自己的写法
3. 对无法下结论的地方，输出“待确认问题”，不要强行补脑
4. 如果项目存在 `docs/templates-local/` 同名 override，应优先按 local override 的边界理解正文结构

## Review Order

默认按下面顺序工作：

1. 先读 handoff，提炼：
   - 功能背景
   - 当前用户与场景
   - 已确认目标
   - 范围边界
   - 风险与禁区
2. 再读 PRD，建立：
   - 当前结构
   - 已写明事实
   - 隐含假设
   - 明显缺口
3. 再按角色视角 review：
   - PM 视角
   - 研发视角
   - 测试视角
4. 合并重复问题，避免同一个问题在多个视角下重复堆砌
5. 输出“问题 + 影响 + 建议改法 + 修订草案”

## Review Lenses

### PM 视角

重点看：

1. 背景是否说清楚，为什么现在要做
2. 用户是谁，场景是什么，触发条件是什么
3. 要解决的问题是否清楚，不是泛泛而谈
4. 成功标准是否可判断，而不是口号
5. 范围边界、非目标、不做什么是否明确
6. 关键流程是否闭环
7. 是否存在“写了很多 HOW，但 WHY 仍不清楚”的问题
8. 是否把不同层次内容混在一起，导致后续评审难收敛

### 研发视角

重点看：

1. 模块边界和职责是否清楚
2. 输入、输出、状态、对象定义是否足够明确
3. 人工动作、AI 动作、系统动作是否分得开
4. 上下游依赖是否清楚
5. 失败、降级、人工接管、回退是否说明
6. 关键名词、字段、对象是否一致
7. 是否存在“开发无法落实现实决策”的模糊表述
8. 是否缺少必要的异常、权限、数据来源、确认点

### 测试视角

重点看：

1. 验收标准是否可测试
2. 正常流、异常流、边界条件是否覆盖
3. 失败回退、降级、人工确认点是否可验证
4. 输出结果是否有可检查的标准
5. 多模块衔接处是否有可观测状态
6. 是否写明哪些输入非法、哪些结果算失败
7. 是否存在“只能主观判断通过”的描述

### 可选补充视角

如果 handoff 明显提到以下角色，再补充：

- 业务 / 销售视角
- 设计 / 商品企划视角
- 运营 / 交付视角

但默认不为了凑数硬补视角。

## Severity Rules

### `❌ 阻断`

满足任一条件优先判定为阻断：

1. 开发无法开始拆解
2. 测试无法定义通过 / 失败
3. 关键目标、范围、输入输出严重缺失
4. handoff 与 PRD 关键事实冲突
5. AI-native 链路缺少人工确认、降级或失败回退等核心闭环

### `⚠️ 重要`

适用于：

1. 不会完全阻断，但会导致多轮返工
2. 多角色理解容易跑偏
3. 当前写法明显不利于研发 / 测试评审

### `💡 优化`

适用于：

1. 不改也能推进，但表达不够稳
2. 结构或语言还可以进一步压缩和收束
3. 存在重复、冗余或阅读路径不顺

## PRD-Specific Checks

除了角色视角，默认还检查这些通用项：

1. 是否有一句话定位
2. 是否先讲 WHY，再讲 HOW
3. 是否存在章节重叠
4. 是否明确输出对象
5. 是否明确非目标
6. 是否给出验收口径
7. 如果是 `PRD-standard / PRD-ai-native`，是否具备正式图示要求
   - Markdown 正式引用是否指向根目录 `*.drawio.svg`
   - 是否误引用 `src/*.drawio` 或同名普通 `.svg`
   - `*.drawio.svg` 是否声明为文件本体内嵌 Draw.io 可编辑数据
   - 如果本地可运行 `honeycomb diagram-guard <path>`，应运行并把结果写入 review；如果不可运行，必须标记“图示可编辑性未验证”
8. 如果涉及 AI 协作，是否写清楚：
   - 澄清
   - 推理 / 生成
   - 人工确认
   - 记忆写入
   - 失败回退

## Output Requirements

输出必须是“发现问题 + 给出改法”的形式，而不是只有抽象评论。

默认输出结构：

### 1. Review Scope

- 评审对象
- handoff 来源
- 本轮重点视角
- 事实与假设边界

### 2. Executive Summary

- 当前 PRD 能否进入下一轮评审
- 主要阻断项有多少
- 最值得优先修的 3 个问题

### 3. Findings

按严重程度排序，逐条输出：

- `严重程度`
- `视角`
- `问题`
- `为什么是问题`
- `建议怎么改`
- `对应 PRD 位置`

### 4. Lens Summary

按 `PM / 研发 / 测试` 汇总各自最核心的问题，避免 reviewer 需要重新读长文。

### 5. Revision Draft

这是本 skill 的默认必选输出，不省略。

至少给出其中一种：

1. 建议新增 / 重写的章节结构
2. 建议替换的段落草案
3. 建议补充的验收 / 边界 / 异常列表

### 6. Open Questions

列出必须回到业务 / 产品确认的问题。

## Writing Rules

1. findings 必须先于总结
2. 不要按角色分三份几乎重复的报告
3. 同一个问题优先合并成一条，再标注受影响视角
4. 修订草案优先“最小可替换块”，不要默认重写整篇
5. 结论要明确指出来自：
   - handoff 已确认事实
   - PRD 当前写法
   - review 推断
6. 如果问题来自共享模板缺陷，而不是当前文档写法，应明确标记“疑似共享层问题”，必要时建议运行 `/propose-honeycomb-change`
7. 对图示相关结论必须区分“文本要求缺失”和“文件实际校验失败”；没有运行 `diagram-guard` 时不要声称图文件已合格

## Suggested Output Skeleton

可参考下面的输出骨架：

```md
PRD Review Report: <文件名>

## Review Scope
- Handoff: ...
- PRD: ...
- Required lenses: PM / 研发 / 测试
- Facts vs assumptions: ...

## Findings
### ❌ 1. <问题标题>
- 视角：PM / 研发
- 位置：第 X 章
- 问题：...
- 影响：...
- 建议：...

### ⚠️ 2. <问题标题>
- 视角：测试
- 位置：第 X 章
- 问题：...
- 影响：...
- 建议：...

## Lens Summary
- PM：...
- 研发：...
- 测试：...

## Revision Draft
### 建议重写章节结构
...

### 建议替换段落
...

## Open Questions
1. ...
2. ...
```

## Related References

优先参考：

- `~/.honeycomb-agent/templates/PRD-ai-native.md`
- `~/.honeycomb-agent/templates/PRD-standard.md`
- `~/.honeycomb-agent/templates/PRD-lite.md`
- `~/.honeycomb-agent/templates/examples/PRD-ai-native-example.md`
- `honeycomb diagram-guard <path>` 或 `.claude/hooks/diagram-guard.sh`

## Success Standard

一份合格的 `prd-review` 输出，应该满足：

1. reviewer 看完知道“最该先改哪几处”
2. 产品能直接把修订草案回填到 PRD
3. 研发能据此指出实现缺口，而不是继续帮忙翻译 PRD
4. 测试能开始提炼可验证场景，而不是只能说“先看看开发怎么做”

## Definition of Done

完成标准是：

- handoff 和 PRD 的边界已经分开
- findings 有严重程度排序
- 修订草案可直接回填
- 推断和事实没有混写

## Evaluation

Smoke prompts:

- handoff 充足时，能否指出 PRD 的主要缺口
- handoff 不足时，能否明确哪些结论只是推断
- AI-native PRD 时，能否检查协作闭环与回退
- PRD 引用了图示时，能否区分 `*.drawio.svg` 正式图、`src/*.drawio` 备份源和普通 `.svg`

Non-trigger prompts:

- 仅凭一句话生成完整 PRD
- 只做目录治理
- 只写 proposal，不评审 PRD

Resources:

- `handoff` 文档
- `PRD` 初稿
- `docs/templates-local/` 同名 override（如存在）
- `*.drawio.svg` 图示文件和对应 `src/*.drawio`（如存在）
