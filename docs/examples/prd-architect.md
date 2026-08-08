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
- Keeps the background within 200 Chinese characters, shorter when sufficient, and states the current scope in one sentence.
- Organizes the body by feature module instead of separate user-scenario, entry, page-structure, and interaction chapters.
- Places target-state UI evidence beside concise functional logic for every visible module.
- Lists only decision-relevant states, exceptions, and acceptance criteria.
- Adds open questions and handoff notes.
- Uses Draw.io only for explicit requests or genuinely complex cross-role/system flows.

## Good Follow-Up

```text
把这个 PRD 补成 PRD-standard，并增加异常流程和验收标准。
```
