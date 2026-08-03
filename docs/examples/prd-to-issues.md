# Example: prd-to-issues

## Use When

You have a ready PRD or handoff and need a GitHub issue backlog that engineering agents or developers can pick up.

## Prompt

```text
$prd-to-issues

下面是一份已经 review 过的 PRD。请先用 draft-only 模式，把它拆成 GitHub implementation issues。
要求按 vertical slice 拆，不要按前端、后端、测试分层拆。
每个 issue 标注 AFK / HITL、依赖、验收标准和验证方式，并输出 coverage matrix。

[paste PRD here]
```

## Expected Output Shape

- Starts with readiness status: pass, needs clarification, or blocked.
- Produces draft issues before publishing anything.
- Each issue has a user-visible or system-visible outcome.
- Marks uncertain product, UX, architecture, release, or compliance decisions as HITL.
- Includes a coverage matrix mapping PRD items to issues or explicit exclusions.
- Asks for approval before creating GitHub issues.

## Good Follow-Up

```text
粒度可以，先不要发布。把 HITL 的 issue 合并成一个前置澄清 issue，再重新排序。
```

```text
确认发布到当前仓库，使用已有 labels，不要新建 label。
```
