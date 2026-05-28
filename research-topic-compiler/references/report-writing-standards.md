# Report Writing Standards

Use these standards for `05_研究报告.md`.

## Purpose

The report is the learning layer. It should let the user understand the topic without reading every source first, while still making it easy to jump into evidence.

## Required Structure

```markdown
# 研究报告

## 研究主题概览

- 主题：
- 研究目标：
- 推荐深度：
- 渠道：
- 适用场景：
- 不适用场景：

## 学习顺序

- 先看：
- 再看：
- 需要深入时跳转：

## 问题 1：<from 01_问题清单>

### 标准答案

<systematic answer>

### 关键依据

- <1-3 strongest sources>

### 扩展阅读

- <optional sources>

## 行业最佳实践 / 可借鉴方法

## 适用边界与反例

## 给自己的默认模板或行动建议

## 仍需验证
```

## Writing Rules

- Answer by question, not by article order.
- Each question from `01_问题清单` must have a corresponding answer.
- Prefer synthesis over summaries. Do not paste long excerpts.
- Separate strong evidence from weak trend signals.
- Include `关键依据` for every major answer.
- Use `扩展阅读` only for sources worth reading after the report.
- If evidence is weak, say what would change the answer.

## Good Answer Shape

Each answer should include:

- The direct answer.
- Boundary conditions.
- Mechanism or reasoning.
- Practical implications.
- Evidence references.
- Open questions when evidence is incomplete.

## Evidence Labels

Use compact evidence notes:

```markdown
- [Anthropic Skills docs](...) - Evidence A; defines the platform mechanism.
- [Repo X](...) - Evidence B; shows implementation pattern.
- [HN discussion](...) - Evidence D; shows practitioner concern, not proof.
```

## Avoid

- Listing every source in the report body.
- Repeating `02_证据与卡片`.
- Treating X/community posts as definitive.
- Writing a conclusion without source path or evidence matrix support.
- Creating a report so long that the user still needs another summary.
