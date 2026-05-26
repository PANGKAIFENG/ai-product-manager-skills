---
name: honeycomb-change-proposer
description: Use when Codex needs to turn Honeycomb shared-template, managed-path, or installation-packaging problems into a formal upstream proposal, including shared-vs-local classification, drift evidence, and MR-ready summary text.
---

# honeycomb-change-proposer

## Overview

把下游项目中发现的 Honeycomb 共享模板 / 安装包治理问题，整理成可提交到 Honeycomb 上游仓库的正式 proposal。

这个 skill 负责的是 proposal 归因、证据整理和上游建议，不负责直接改上游仓库。

## Workflow

1. 先读取当前问题描述和项目上下文。
2. 检查 `docs/PROJECT/`、相关 PRD、handoff、决策记录和 `.honeycomb/managed-files.json`。
3. 判断问题属于共享层、本地模板 override，还是本地 capability。
4. 如果存在 drift 或临时直改，记录为 `temporary downstream patch`。
5. 按 proposal 模板输出问题、证据、影响、建议修改文件、回收动作和周会摘要。
6. 默认只写入 `.honeycomb/proposals/YYYY-MM-DD-<slug>.md`；除非用户明确要求，不修改上游仓库、managed files 或当前项目模板。

## Responsibilities

这个 skill 负责：

1. 读取当前对话里的问题上下文
2. 读取 `docs/PROJECT/`、相关 PRD / handoff / 决策，补齐业务背景和真实使用链路
3. 判断问题是共享问题还是项目特有问题
4. 检查当前项目是否存在 managed path drift
5. 把问题、证据、影响范围、建议修改文件整理成标准 proposal
6. 补齐可用于周会 / 复盘 / 发版说明的业务摘要
7. 给出后续 GitLab MR 的建议动作

它不负责：

- 直接修改 Honeycomb 上游仓库
- 自动创建 GitLab MR
- 把项目特有问题伪装成共享标准问题
- 在没有证据时编造业务指标或影响规模
- 未经用户明确要求直接修改 managed path、共享模板或本地 override

## Decision Rules

### 判定为共享问题

优先满足以下特征：

- 多个项目都可能遇到
- 影响共享模板的默认输出质量
- 会影响 PM / UI / 开发等多个使用者的协作体验
- 应该回到 Honeycomb 上游仓库统一修复

### 判定为项目特有问题

优先满足以下特征：

- 只属于当前项目业务特殊性
- 只影响当前项目术语、字段、章节或交付物
- 更适合放进 `docs/templates-local/`

## Input Expectations

最好具备这些输入：

- 当前对话中与问题相关的关键片段
- `docs/PROJECT/` 中的项目背景或等价上下文文档
- 相关 PRD / handoff / 决策记录
- 当前项目里已修改的模板文件
- 当前用户对问题的描述
- 当前 Honeycomb 版本和 managed path 信息

## Output Requirements

输出 proposal 时必须做到：

1. 明确共享 / 本地的判定
2. 明确当前是否已经存在 `temporary downstream patch`
3. 如果有 drift，列出 drift 文件
4. 说明问题在哪个业务场景、哪个角色、哪个交付阶段暴露
5. 记录当前 workaround 和代价；没有量化数据时明确写出边界
6. 给出建议修改的上游文件
7. 给出下游回收动作
8. 输出一段可直接复用于周会 / 复盘的摘要
9. 明确本次执行的写入边界；默认只有 proposal 文件被创建或更新

## Template References

优先参考：

- `~/.honeycomb-agent/templates/honeycomb-change-proposal.md`

## Definition of Done

完成标准是：

- 问题是共享还是本地已经判定
- drift 和 temporary downstream patch 已说明
- 上游建议文件和回收动作已给出
- 周会 / 复盘摘要可直接复用
- 除 proposal 文件外没有产生未声明的文件写入

## Evaluation

Smoke prompts:

- 项目里出现临时直改，能否判断是否属于 drift
- 共享模板与本地 override 混用时，能否区分归属
- 只有定性证据时，能否避免编造量化数据

Non-trigger prompts:

- 纯项目内 PRD 生成
- 纯目录治理
- 纯 UI 结构设计

Resources:

- `~/.honeycomb-agent/templates/honeycomb-change-proposal.md`
- `.honeycomb/managed-files.json`
- `.honeycomb/proposals/`
