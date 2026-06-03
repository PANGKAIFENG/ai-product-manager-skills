---
name: agent-trace-diagnoser
description: "Agent trace 诊断器：当用户提供 trace、日志 JSON、agent 执行记录或说“看下这个日志/trace，定位根因”时使用；输出核心根因、trace 证据链、可能对应的文件/行和修复建议，默认只读分析，不修改文件。"
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

Use this Skill to diagnose agent execution traces without jumping straight to code edits. The goal is to explain the core root cause, distinguish primary failures from fallback noise, map the likely bug to concrete files and line ranges when a repository is available, and recommend fixes.

Default mode is read-only. Do not modify files unless the user explicitly asks for implementation after the diagnosis.

## Workflow

1. Confirm the input artifact and user constraint.
   - Accept trace JSON files, copied logs, terminal excerpts, tool-call transcripts, network traces, or screenshots converted to text.
   - If the user says "不要修改文件", "只说明问题", or similar, do not edit or generate repo changes.
   - If a trace file path is provided, inspect only enough of the file to reconstruct the event sequence.
2. Reconstruct the execution timeline.
   - Identify user intent, selected capability or skill, first failing step, retries, fallback tools, terminal errors, and final user-visible failure.
   - Separate direct causes from downstream symptoms.
   - Treat the earliest failed intended path as the primary root-cause candidate unless later evidence disproves it.
3. Classify failure layers.
   - Planning or routing: wrong skill/tool chosen, wrong capability boundary, missing policy guardrail.
   - Skill/tool implementation: bad input handling, parser failure, dependency issue, path bug, unsupported media, fragile fallback.
   - Environment: permissions, missing binaries, read-only directories, network limits, temp path ownership, credentials.
   - Output policy: misleading summary, hidden failure, unsafe next action, omitted limitation.
4. Build an evidence chain.
   - Quote or paraphrase exact trace facts: command, status code, exception code, file URL, content type, size, fallback transition, missing dependency.
   - Avoid over-weighting the final error if it happened after a fallback.
   - Mark facts as `confirmed`, `inferred`, or `needs verification`.
5. Map to possible code locations.
   - Search the active repo for unique strings from the trace: skill name, CLI path, error code, fallback command, function names, config keys, and output messages.
   - Report exact file and line only when read in the current turn.
   - If the runtime path differs from the local repo, label the mapping as "likely source location" and state the path mismatch.
6. Give repair guidance without editing.
   - Recommend the smallest conceptual fix first.
   - Include test or eval coverage that would prevent regression.
   - Mention operational guardrails when needed, such as avoiding `webfetch` for binary PDFs or avoiding runtime builds in read-only skill installs.

## Required Checks

Read `references/investigation-checklist.md` when the trace is long, involves multiple fallbacks, or the root cause is not obvious.

Use `references/output-template.md` for the final structure unless the user requests a different format.

Before finalizing, verify that the answer includes:

- The core root cause in one or two sentences.
- Why later errors are symptoms or contributing factors.
- Trace evidence in chronological order.
- Possible file and line locations, with confidence.
- Concrete fix suggestions and regression checks.

## Safety And Side Effects

- Do not edit files by default.
- Do not run destructive commands.
- Do not download large external artifacts unless necessary for diagnosis and safe to do.
- Do not present inferred file/line mappings as confirmed.
- Do not claim the issue is "fixed" unless the user explicitly asked for a fix and verification was run.

## Output Contract

Final answers should be in Chinese by default when the user is writing Chinese.

Use this order:

1. 核心结论
2. 证据链
3. 不是主因但会放大的问题
4. 可能对应的代码位置
5. 修复建议
6. 建议补的回归验证

Keep the answer concise, but do not omit file/line candidates when the repo is available.

## Definition Of Done

- The primary root cause is separated from fallback symptoms.
- The trace timeline is clear enough for another engineer to reproduce the reasoning.
- File/line candidates are either confirmed from local code or explicitly marked as inferred.
- Fix recommendations are specific and testable.
- No file edits were made unless explicitly requested.

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
