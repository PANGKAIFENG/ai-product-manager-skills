---
name: agent-trace-diagnoser
description: "Agent trace 诊断器：当用户提供 trace、日志 JSON、agent 执行记录、工具调用序列，或说“看下这个日志/trace，定位根因”“只说明问题不要改文件”时使用。不用于没有日志证据的新功能设计、普通代码解释或直接修复代码。"
---

# Agent Trace Diagnoser

## 中文速查

- 中文名：Agent trace 诊断器 / 日志根因定位
- 英文稳定名：`agent-trace-diagnoser`
- 分类：工程实践
- 你可以这样叫我：`看下这个 trace`、`根据日志定位根因`、`只说明问题不要改文件`、`具体到哪个文件哪行可能导致`
- 适合：从 agent trace、日志 JSON、执行记录、工具调用序列中定位主链路失败点，给出证据链、可能代码位置和修复建议。
- 不适合：直接修复代码、普通代码解释、没有日志证据的新功能设计。

## Overview

使用这个 Skill 诊断 agent 执行 trace，而不是直接进入代码修改。目标是说明核心根因，区分主链路失败和 fallback 噪声，在仓库可用时映射到具体文件/行，并给出修复建议。

默认模式是只读分析。除非用户在诊断后明确要求实现修复，否则不要修改文件。

最终诊断内容必须使用中文输出；只有用户明确要求英文或其它语言时，才切换输出语言。

## Workflow

1. 确认输入材料和用户约束。
   - 接收 trace JSON、复制的日志、终端片段、工具调用记录、网络 trace，或从截图转换出的文本。
   - 如果用户说“不要修改文件”“只说明问题”等，只做只读分析，不生成代码改动。
   - 如果用户提供 trace 文件路径，只读取足够重建事件顺序的内容。
2. 重建执行时间线。
   - 识别用户意图、被选中的 capability/skill、第一个失败步骤、重试、fallback 工具、终端错误和最终用户可见失败。
   - 分离直接原因和下游症状。
   - 除非后续证据推翻，否则把“预期主链路里最早失败的步骤”作为第一根因候选。
3. 分类失败层级。
   - 规划或路由：选错 skill/tool、能力边界错误、缺少 policy guardrail。
   - Skill/tool 实现：输入处理错误、解析失败、依赖问题、路径问题、不支持的媒体、脆弱 fallback。
   - 环境：权限、缺少二进制、只读目录、网络限制、临时目录归属、凭证。
   - 输出策略：误导性总结、隐藏失败、不安全下一步、遗漏限制说明。
4. 建立证据链。
   - 引用或转述 trace 中的精确事实：命令、状态码、异常码、文件 URL、content type、大小、fallback 转换、缺少依赖。
   - 如果最终错误发生在 fallback 之后，不要把最终错误过度放大成主因。
   - 每条证据标记为`已确认`、`推断`或`待验证`。
5. 映射可能的代码位置。
   - 在当前仓库中搜索 trace 里的唯一字符串：skill 名、CLI 入口、错误码、fallback 命令、函数名、配置键、输出消息。
   - 只有当前轮实际读过代码，才报告精确文件和行号。
   - 如果 runtime 路径和本地仓库路径不同，标记为“可能源码位置”，并说明路径不一致。
6. 给出不改文件的修复建议。
   - 先推荐最小概念修复。
   - 包含能防止回归的测试或 eval。
   - 必要时补充运行 guardrail，例如不要用 `webfetch` 读取二进制 PDF，或不要在只读 skill 安装目录里运行构建。

## Required Checks

Read `references/investigation-checklist.md` when the trace is long, involves multiple fallbacks, or the root cause is not obvious.

Use `references/output-template.md` for the final structure unless the user requests a different format.

Before finalizing, verify that the answer includes:

- 用中文写出一到两句话的核心根因。
- 说明为什么后续错误只是症状或放大因素。
- 按时间顺序列出 trace 证据。
- 给出可能的文件和行号，并标注置信度。
- 给出具体修复建议和回归验证。

## Safety And Side Effects

- Do not edit files by default.
- Do not run destructive commands.
- Do not download large external artifacts unless necessary for diagnosis and safe to do.
- Do not present inferred file/line mappings as confirmed.
- Do not claim the issue is "fixed" unless the user explicitly asked for a fix and verification was run.

## Output Contract

最终诊断回答必须使用中文，除非用户明确要求英文或其它语言。trace 原文、命令、错误码、文件路径、函数名和代码标识可以保留原文，不需要翻译。

Use this order:

1. 核心结论
2. 证据链
3. 不是主因但会放大的问题
4. 可能对应的代码位置
5. 修复建议
6. 建议补的回归验证

保持简洁，但仓库可用时不要省略文件/行候选。

## Definition Of Done

- 主因和 fallback 症状被明确分开。
- trace 时间线足够清楚，其他工程师能复核推理。
- 文件/行候选要么来自当前读取的本地代码，要么明确标注为推断。
- 修复建议具体、可测试。
- 除非用户明确要求，否则没有修改文件。

## Evaluation

Smoke prompts:

- `看下这个 trace，定位根因，只说明问题。`
- `这个 agent 为什么 fallback 到 webfetch？具体哪个文件哪行可能导致？`
- `根据这个日志给我核心根因、证据链、修复建议。`

Non-trigger prompts:

- `直接帮我修这个 bug。`
- `解释这个模块的调用链，不需要日志分析。`
- `帮我写一个新 Skill。`

Regression prompts:

- A PDF trace where the intended PDF skill fails first, then `webfetch` hits a 5MB limit. The correct answer must identify the skill URL/PDF parsing path failure as primary and `webfetch` as fallback symptom.
- A trace where a runtime build fails due to read-only install path. The correct answer must recommend using prebuilt artifacts or writable build/cache paths, not chmod as the only fix.

## Catalog Notes

- Category: `categories/03-engineering-practice/`
- Status: `active`
- Public risk: low; the Skill should not contain private trace content, only the diagnostic workflow.
