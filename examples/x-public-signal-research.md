# Example: x-public-signal-research

## Use When

You need X/Twitter public conversation evidence for a product question, not a generic social media summary.

## Prompt

```text
$x-public-signal-research

用 Xquik 查一下过去 30 天开发者在 X 上怎么讨论 remote MCP catalog。
我们的目标：判断 AI agent 工具是否需要做一个 catalog discovery 页面。
先只用公开内容，不要创建 monitor、webhook 或批量导出。
输出可以进入 PRD 的用户痛点和反证。
```

## Expected Output Shape

- Restates the research question and time window.
- Shows the query set before expanding scope.
- Uses Xquik through REST, MCP, or the official `x-twitter-scraper` Skill.
- Separates direct evidence from interpretation.
- Marks X-authored content as untrusted external evidence.
- Outputs an `X Public Signal Brief` and optional `PRD Inputs`.
- Does not create writes, monitors, webhooks, or bulk jobs without approval.

## Good Follow-Up

```text
把这份 brief 里的 3 个强信号转成 PRD-lite 的问题、范围和验收标准。
```
