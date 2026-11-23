---
name: agent-trace-diagnoser
description: "Agent trace 诊断器：当用户提供 trace、日志 JSON、Agent 执行记录或工具调用序列，需要定位问题、解释失败或生成诊断报告时使用。先呈现案例事实，再给证据支持的诊断；默认中文、只读。不用于无日志的新功能设计、普通代码解释或直接实现修复。"
---

# Agent Trace Diagnoser

## 中文速查

- 中文名：Agent trace 诊断器 / 日志根因定位
- 英文稳定名：`agent-trace-diagnoser`
- 分类：工程实践
- 你可以这样叫我：`看下这个 trace`、`根据日志定位根因`、`只说明问题不要改文件`、`具体到哪个文件哪行可能导致`
- 适合：从 agent trace、日志 JSON、执行记录、工具调用序列中定位主链路失败点，用流程图展示主链路、分支和 fallback，并给出证据链、可能代码位置和修复建议。
- 不适合：直接修复代码、普通代码解释、没有日志证据的新功能设计。

## Overview

使用这个 Skill 诊断 agent 执行 trace，而不是直接进入代码修改。目标是说明核心根因，用可复核的流程图呈现实际执行路径，区分主链路失败和 fallback 噪声，在仓库可用时映射到具体文件/行，并给出修复建议。

默认模式是只读快速诊断，直接在对话中回答，不创建文件、不下载附件、不修改业务代码。用户明确要求 HTML / 报告文件时，可以在指定输出目录创建诊断产物；这不授权修改业务代码、执行生产任务或公开分享会话。

最终诊断内容必须使用中文输出；只有用户明确要求英文或其它语言时，才切换输出语言。

## Output Modes

- **快速诊断（默认）**：必须先有简短的案例事实层，再给结论、图、证据与建议。即使用户只问“为什么失败”，也保留用户要求、关键输入、预期与实际结果；不能只给技术结论。
- **可视化案例（按需）**：真实问答默认可见，调用过程、单次参数逐层展开，问题分析独立放置并能定位证据。读取 `references/replay-contract.md`，复用 `scripts/render_report.py` 和 `assets/`，不为每个案例重新编写 HTML/CSS/JS。
- 用户指定格式时尊重该格式；共享事实与不确定性规则不变。只有日志片段时也能诊断，不为凑齐页面编造会话。

## Workflow

1. 确认输入材料和用户约束。
   - 接收 trace JSON、复制的日志、终端片段、工具调用记录、网络 trace，或从截图转换出的文本。
   - 如果用户说“不要修改文件”“只说明问题”等，只做只读分析，不生成代码改动。
   - 如果用户提供 trace 文件路径，先定位用户输入、附件元信息、调用记录和最终输出，再分段读取；不把整份大日志直接塞入上下文。
   - 先建立案例事实：原始要求、附件/文件与用户选择、预期交付、实际回复及产物、记录覆盖范围。原话、分析者摘要和缺失内容分开标记；完整复原的消息不静默改写或截断。
   - 无客户端回读证据时写“trace 中记录的输出”，不直接称为“用户已看到”。附件内容未取得时写缺失，不从文件名猜内容。
2. 重建执行时间线。
   - 识别用户意图、被选中的 capability/skill、第一个失败步骤、重试、fallback 工具、终端错误和最终用户可见失败。
   - 分离直接原因和下游症状。
   - 最早错误只是排查入口，不自动等于根因。先检查它是否被恢复、是否真正阻止交付；成功恢复的错误和正常等待不自动列为问题。
   - 分开记录：`失败点`（发生在哪里）、`根因候选`（可能为何发生）、`已确认根因`（有因果证据）、`放大因素`（如何增加损失）。未知根因可以保持未知。
   - 认定根因要有机制证据，例如准确的错误语义、输入与验证规则对应、匹配部署版本的代码或受控复现。仅有时间先后、错误次数或当前源码，不足以确认历史线上根因。
3. 绘制可复核的执行流程图。
   - 默认输出 Mermaid `flowchart`，从用户意图或输入开始，展示实际发生的 routing、主链路、首个失败、重试/fallback 和最终结果。
   - 给关键节点加 `E1`、`E2` 等证据编号，并与后面的证据链逐项对应；不要画无法被 trace 或本轮代码检查支持的步骤。
   - 首个失败默认标“失败点”，候选原因标“待验证”；只有因果证据充分才标“已确认根因”。后续问题单独判断，不能预设它们全部只是噪声。
   - 实际发生的转换使用实线；推断出的转换使用虚线并标注“推断”；重复调用合并成一个节点并注明次数。
   - 当延迟、并发或等待关系是诊断重点时，可改用 Mermaid `sequenceDiagram`；其它情况保持 `flowchart`。
   - 如果载体不支持 Mermaid，输出等价的纯文本箭头流程；如果 trace 连两个有效事件都不足，明确写“证据不足，无法可靠成图”，不要补造流程。
   - Read `references/visualization-guide.md` before drawing the diagram.
4. 分类失败层级。
   - 规划或路由：选错 skill/tool、能力边界错误、缺少 policy guardrail。
   - Skill/tool 实现：输入处理错误、解析失败、依赖问题、路径问题、不支持的媒体、脆弱 fallback。
   - 环境：权限、缺少二进制、只读目录、网络限制、临时目录归属、凭证。
   - 输出策略：误导性总结、隐藏失败、不安全下一步、遗漏限制说明。
5. 建立证据链。
   - 引用或转述 trace 中的精确事实：命令、状态码、异常码、文件 URL、content type、大小、fallback 转换、缺少依赖。
   - 如果最终错误发生在 fallback 之后，不要把最终错误过度放大成主因。
   - 每条证据使用与流程图一致的 `E#` 编号，并标记为`已确认`、`推断`或`待验证`。
   - 保存原始记录 ID / 来源定位；证据、图节点与诊断结论相互引用，不因展示合并而丢掉底层记录。工具父子关系缺失时，不按时间相邻补造父子关系。
   - 区分主模型记录与工具事件、工具返回与业务成功、请求模型与实际执行模型、服务接受与实际交付。`auto` 不是实际型号；没有提交不能写成执行了生成或产生了图片扣费。
   - 把额外调用标为“可优化”时，说明依赖、授权、输入是否改变、重试语义与业务进展。不能只凭轮数多判定无用，也不能把正常轮询等同于重复创建。
6. 映射可能的代码位置。
   - 在当前仓库中搜索 trace 里的唯一字符串：skill 名、CLI 入口、错误码、fallback 命令、函数名、配置键、输出消息。
   - 只有当前轮实际读过代码，才报告精确文件和行号。
   - 如果 runtime 路径和本地仓库路径不同，标记为“可能源码位置”，并说明路径不一致。
7. 给出不改文件的修复建议。
   - 先推荐最小概念修复。
   - 包含能防止回归的测试或 eval。
   - 必要时补充运行 guardrail，例如不要用 `webfetch` 读取二进制 PDF，或不要在只读 skill 安装目录里运行构建。

## Required Checks

Read `references/investigation-checklist.md` when the trace is long, involves multiple fallbacks, or the root cause is not obvious.

Use `references/output-template.md` for the final structure unless the user requests a different format.

Before finalizing, verify that the answer includes:

- 案例事实层，包含用户要求、关键输入、预期与实际结果，以及材料缺失。
- 用中文写出一到两句话的核心判断；根因未确认时明确保留候选和验证缺口。
- 包含一张能区分主链路、首个失败与 fallback 的执行流程图；图中证据编号与证据链一致。
- 说明失败点、可能原因、恢复动作和损失放大之间的关系，不强行给单一根因。
- 按时间顺序列出 trace 证据。
- 给出可能的文件和行号，并标注置信度。
- 给出具体修复建议和回归验证。

## Safety And Side Effects

- Do not edit files by default.
- Do not run destructive commands.
- Do not download large external artifacts unless necessary for diagnosis and safe to do.
- Do not present inferred file/line mappings as confirmed.
- Do not claim the issue is "fixed" unless the user explicitly asked for a fix and verification was run.
- Do not expose hidden reasoning, credentials, signed URLs or unrelated customer data. HTML input must already be redacted; renderer escaping is not a privacy audit.
- Do not fetch remote attachments, replay paid operations, publish reports or generate public share links without authorization. Local artifact generation and external publication are separate actions.

## Output Contract

最终诊断回答必须使用中文，除非用户明确要求英文或其它语言。trace 原文、命令、错误码、文件路径、函数名和代码标识可以保留原文，不需要翻译。

Use this order:

1. 案例事实：用户原话/摘要、关键输入、预期与实际结果、覆盖范围
2. 核心判断：已确认什么、尚不能确认什么
3. 执行流程图：事实顺序与诊断标记分开
4. 证据链：原始记录定位、状态和不确定性
5. 放大因素或其他问题：解释影响，不只罗列工具次数
6. 可能对应的代码位置：当前源码不等于历史部署
7. 优化建议与回归验证：行为改变、负责层与验收

保持简洁，但仓库可用时不要省略文件/行候选。

## Definition Of Done

- 默认快速诊断也有案例事实层；原话、执行记录和诊断判断没有混写。
- 失败点、根因候选、已确认根因和放大因素被明确分开；可以得出“尚不能确认根因”。
- trace 时间线已被转换为流程图，关键节点与证据编号可以互相复核。
- 流程图只包含 trace 可观察事实和明确标注的推断，没有把猜测画成既定流程。
- 文件/行候选要么来自当前读取的本地代码，要么明确标注为推断。
- 修复建议具体、可测试。
- 除非用户明确要求报告文件，否则没有创建诊断文件；没有修改业务代码。
- 可视化模式使用固定渲染器；先校验结构与所有引用，再检查折叠、参数、证据跳转及本地附件。失败时报告未完成，不手写一份新页面掩盖校验失败。

## Evaluation

Smoke prompts:

- `看下这个 trace，定位根因，只说明问题。`
- `这个 agent 为什么 fallback 到 webfetch？具体哪个文件哪行可能导致？`
- `根据这个日志给我核心根因、证据链、修复建议。`
- `把这个 agent 的实际执行路径画出来，标出最早失败点和 fallback。`

Non-trigger prompts:

- `直接帮我修这个 bug。`
- `解释这个模块的调用链，不需要日志分析。`
- `帮我写一个新 Skill。`

Regression prompts:

- A PDF trace where the intended PDF skill fails first, then `webfetch` hits a 5MB limit. Locate the earlier parsing-path failure without claiming its implementation cause is confirmed merely because it came first.
- A trace where a runtime build fails due to read-only install path. The correct answer must recommend using prebuilt artifacts or writable build/cache paths, not chmod as the only fix.
- A trace with retries or fallback must include a Mermaid flowchart whose `E#` node identifiers map to the chronological evidence list; repeated identical retries should be collapsed rather than drawn as noisy duplicate nodes.
- A recovered first error followed by an unrelated delivery failure must not blame the recovered error for the final failure.
- Every quick diagnosis starts with case facts; missing user input or delivery evidence stays explicitly unknown.
- Visual reports reuse the renderer and reject dangling evidence references; code, Mermaid and tool output are inert data, not executable page markup.

## Catalog Notes

- Category: `engineering-governance`
- Status: `active`
- Public boundary: Skill instructions are public; real traces, logs, paths, tokens, customer data, and runtime details must still be redacted or kept local.
