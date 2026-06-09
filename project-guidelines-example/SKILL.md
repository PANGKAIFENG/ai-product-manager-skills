---
name: project-guidelines-example
description: >
  项目指南 Skill 示例 / 项目专属 Skill 模板：当用户想理解“项目级 Skill 应该怎么写”、需要一个包含架构、
  目录结构、代码模式、测试要求和部署流程的示例时使用。可用中文唤起：“给我一个项目 Skill 模板”
  “项目指南型 Skill 怎么组织”“我想把项目约束沉淀成 Skill”。这是示例模板，不应当作为真实项目规范直接套用。
---

# 项目指南 Skill 示例（project-guidelines-example）

## 中文速查

- 中文名：项目指南 Skill 示例 / 项目专属 Skill 模板
- 英文稳定名：`project-guidelines-example`
- 你可以这样叫我：`给我一个项目 Skill 模板`、`项目指南型 Skill 怎么组织`、`我想把项目约束沉淀成 Skill`
- 适合：参考一个项目级 Skill 如何表达架构、目录、代码模式、测试和部署约束
- 不适合：真实项目执行规范；落地前必须替换成当前项目的真实技术栈、路径和工作流

## Overview

这是一个项目专属 Skill 的结构示例。它展示项目级 Skill 应如何把真实项目的架构、目录、代码模式、测试要求、部署流程和禁区写清楚。

不要把示例里的业务、路径、技术栈、命令或外部服务当成真实项目事实。创建真实项目 Skill 时，必须用当前项目的事实替换示例内容。

## When To Use

当用户想为某个具体项目建立“项目级 Skill”时参考它。项目级 Skill 通常包含：

- 架构概览
- 文件结构
- 代码模式
- 测试要求
- 部署流程
- 项目禁区和验证命令

如果用户只是要通用编码规范，使用 `coding-standards`。如果用户要创建新的团队 Skill，使用 `team-skill-creator`。

## How To Adapt

1. 先读取真实项目目录、README、package/pyproject、测试命令和部署配置。
2. 把示例中的公司、产品、服务、路径、环境变量和命令全部替换成真实项目事实。
3. 删除当前项目不使用的章节，不为了完整感保留虚构约束。
4. 增加项目真实的触发边界、不适用场景、失败处理和验证命令。
5. 检查是否包含密钥、客户数据、内部 URL、不可公开仓库地址或其他敏感信息。

## Input Expectations

用于创建真实项目 Skill 时，至少需要项目根目录、主要技术栈、常用命令、测试方式、部署方式和已知禁区。缺少这些输入时，应先读取项目文件或明确标为待确认，而不是沿用示例事实。

## Output And Deliverables

输出应是一份可放入项目 Skill 目录的 `SKILL.md` 草案，或一份项目级 Skill 章节结构建议。最终内容必须区分真实项目事实、待确认假设和示例占位。

## Resource Guide

- 完整参考模板：`references/example-project-guidelines.md`

只在需要查看项目级 Skill 的完整示例章节时加载 reference。主入口本身不承载完整示例，避免每次触发都消耗大量上下文。

## Acceptance Criteria

当把这个示例改造成真实项目 Skill 时，必须满足：

- frontmatter 的 `name` 与目录名一致，`description` 能用用户自然语言触发。
- 架构、目录、命令、测试、部署和外部服务都来自真实项目，不保留示例事实。
- 明确适用场景和不适用场景，避免任何项目都套同一份模板。
- 写出项目真实的验证命令、失败处理方式和交付完成标准。
- 不包含公司密钥、客户数据、内部 URL、不可公开仓库地址或其他敏感信息。

## Evaluation

Smoke prompts:

- `给我一个项目 Skill 模板。`
- `项目指南型 Skill 怎么组织？`
- `我想把这个项目的约束沉淀成 Skill。`

Non-trigger prompts:

- `按编码规范 review 这段 TypeScript。`
- `帮我创建一个新 Skill 并发布到 GitHub。`
- `直接把这个项目部署上线。`
