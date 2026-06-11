# Example: brainstorming

## Use When

You have a problem or product direction that is clear enough to discuss, but you have not yet chosen the design path, PRD structure, UI flow, or implementation approach.

## Prompt

```text
$brainstorming

先不要写 PRD。我们想在 SaaS 里加一个下载桌面端的入口，
但不确定应该放在首页、头像菜单、Agent 工作台里，还是多个入口组合。
帮我先脑暴 2-3 个方案，说明取舍，然后推荐一个。
```

## Expected Output Shape

- Confirms the task is design brainstorming, not execution.
- Checks available context before asking questions.
- Asks at most one important clarifying question at a time.
- Presents 2-3 real options with trade-offs.
- Recommends one option and explains what it gives up.
- Gets user confirmation before moving to PRD, mockup, issues, or implementation planning.

## Good Follow-Up

```text
按你推荐的方案，转成 PRD-lite。
```

or:

```text
先用 grill-me 拷问一下这个推荐方案。
```
