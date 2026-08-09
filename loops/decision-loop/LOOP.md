# 决策闭环 / Decision Loop

当一个明确决策因为证据缺口无法成立时，在 `research-topic-compiler` 与 `decision-research` 之间做有界往返。目标是关闭决策，不是无限扩张研究。

## State Transition

```text
decision_blocked_by_evidence
  -> 定义唯一 material/researchable/closable gap
  -> Research 返回 Evidence Delta
  -> Decision 更新推荐、置信度和颠覆条件
  -> decision_ready | 下一 gap | Human Gate
```

## Cycle Contract

- `max_cycles: 3`。
- 每轮只处理一个会改变推荐或置信度的 gap。
- Research 只返回新增证据和来源变化，不复制完整研究正文。
- Decision 负责把证据转成推荐、排除理由、置信度和颠覆条件。
- 每轮保留 `preserved_items`，不得重开已经关闭且没有新证据影响的判断。
- 连续两轮没有有效 Evidence Delta、来源不可取得、达到三轮上限或需要业务取舍时进入 Human Gate。

## Recoverable State

```yaml
loop: decision-loop
cycle: 1
max_cycles: 3
decision_question: <明确选择>
current_recommendation: <当前结论>
confidence: <low | medium | high>
active_gap: <唯一 gap>
closure_criterion: <关闭条件>
evidence_delta: []
preserved_items: []
status: researching | deciding | decision_ready | human_gate | blocked
resume_point: <下一节点>
```

只有用户要求保存或恢复时才写 `.loop-state/decision-loop/`；聊天内执行保持同样字段即可。Loop 不授权 Runtime、Skillshare、DingTalk 或 Yunxiao 写入。
