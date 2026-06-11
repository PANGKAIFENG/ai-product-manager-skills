# Example: prd-architect

## Use When

You have a product idea or rough notes and need a PRD structure.

## Prompt

```text
$prd-architect

帮我写一个 PRD-lite：
功能是让产品经理把一段会议纪要自动整理成需求草稿。
输入是会议文字，输出包括背景、用户问题、功能范围、验收标准和待确认问题。
先不要写实现计划。
```

## Expected Output Shape

- Chooses PRD-lite, PRD-standard, or PRD-ai-native.
- Defines target user, problem, scope, non-goals, and workflow.
- Lists states, inputs, outputs, exceptions, and acceptance criteria.
- Adds open questions and handoff notes.
- Uses Draw.io only when the workflow complexity justifies it.

## Good Follow-Up

```text
把这个 PRD 补成 PRD-standard，并增加异常流程和验收标准。
```
