# PRD Versioning

Use this contract whenever `prd-architect` creates or revises a PRD.

## Required Placement And Format

Place `版本记录` immediately after the PRD title and before `文档信息` or any other H2 section.

```markdown
# [PRD title]

## 版本记录

| 版本 | 日期 | 修改内容 |
| --- | --- | --- |
| V1.0 | YYYY-MM-DD | 首次创建 |
```

- Use `V<major>.<minor>`, such as `V1.0` or `V1.2`.
- Use `YYYY-MM-DD` in the document's working timezone.
- Keep the newest version in the first data row and preserve all older rows.
- Keep `V1.0` as the oldest row with a change summary that contains `首次创建`.
- Summarize actual product changes. Do not use empty descriptions such as `更新 PRD`, `优化 PRD`, `内容更新`, or `需求更新`.

## Initial Creation

For a new PRD:

1. Start at `V1.0` unless the user explicitly provides a different established version history.
2. Record today's date.
3. Use `首次创建` as the initial change summary. Add a short scope phrase only when it helps readers distinguish the first published scope.

## Later Iterations

Before revising an existing PRD, read its current version table first.

1. Compare the requested product changes with the latest recorded version.
2. Use the user's explicit target version when provided and valid.
3. Otherwise increment the minor version for ordinary feature additions, interaction changes, copy changes, rule clarifications, or acceptance-detail changes. Example: `V1.1 -> V1.2`.
4. Increment the major version and reset the minor version to `0` when the product goal, delivery scope, core information architecture, or core workflow changes materially. Example: `V1.4 -> V2.0`.
5. Prepend one new row with today's date and 1-3 concise, concrete modification points separated by `；`.
6. Never reuse or overwrite an existing version row.

Do not create a new version for a publish retry, DingTalk read-back, screenshot recapture, formatting-only cleanup, or typo-only correction when product meaning is unchanged. If product meaning changed while doing that work, record the product change normally.

## Examples

```markdown
| 版本 | 日期 | 修改内容 |
| --- | --- | --- |
| V1.2 | 2026-08-15 | 补充企业连接器上架规则；明确成员安装与取消逻辑 |
| V1.1 | 2026-08-10 | 新增自定义连接器创建与个人启用规则 |
| V1.0 | 2026-08-01 | 首次创建 |
```

Major revision example:

```markdown
| 版本 | 日期 | 修改内容 |
| --- | --- | --- |
| V2.0 | 2026-09-02 | 产品范围由个人连接扩展为企业连接器市场；重构发布与成员使用主流程 |
| V1.3 | 2026-08-28 | 补充连接异常提示 |
| V1.0 | 2026-08-01 | 首次创建 |
```

## DingTalk Contract

- The table is part of the PRD body and must remain visible near the top after publishing.
- `dingtalk-prd-publisher` validates the existing table before writing and verifies the latest row during read-back.
- The publisher never invents, increments, or rewrites a version. Missing or stale version history must return to `prd-architect` for correction before publishing.
