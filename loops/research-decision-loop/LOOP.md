# Research Decision Loop

这是 `research-topic-compiler` 与 `decision-research` 之间的可恢复状态合同，不是新的 Skill。

## Contract

1. 先写清 `decision_question`、当前结论、证据覆盖和唯一剩余 gap。
2. Research 只接收 `material`、`researchable`、`closable` 的 gap，并返回 `Evidence Delta`。
3. Decision 负责把证据转成推荐、排除理由、置信度和颠覆条件；不把开放学习伪装成选择。
4. 每轮保留 `preserved_items` 和 `resume_point`；不复制完整专业产物正文。
5. 证据足够、用户做出选择、无法取得授权来源，或连续两轮没有有效差量时停止。

Loop handoff 不授权 Runtime、Skillshare、DingTalk 或 Yunxiao 写入；这些动作必须交给 `tools/` 的专用入口并重新确认。
