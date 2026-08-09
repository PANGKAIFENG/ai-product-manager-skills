# 方案闭环 / Solution Loop

当已有候选方案但仍存在关键风险时，在 `brainstorming` Maker 与 `grill-me` Critic 之间做有界往返。目标是关闭方案缺口，不是不断重写整套方案。

## State Transition

```text
solution_candidate
  -> Critic 定位最早因果缺口
  -> Maker 返回最小 Design Delta
  -> Critic 复核同一 closure criterion
  -> solution_confirmed | 下一 gap | Human Gate
```

## Cycle Contract

- `max_cycles: 3`。
- Critic 每轮只输出一个可修复、会阻断确认的 `Challenge Record`。
- Maker 只修改被挑战部分，返回 `Design Delta`，不得借机重写保留项。
- Critic 负责关闭 challenge；Maker 不得自评通过。
- 连续两轮没有有效 Design Delta、达到三轮上限或需要业务取舍时进入 Human Gate。

## Recoverable State

```yaml
loop: solution-loop
cycle: 1
max_cycles: 3
solution_version: <id/version>
active_challenge: <唯一 challenge>
closure_criterion: <关闭条件>
design_delta: <本轮差量>
preserved_items: []
status: challenging | revising | solution_confirmed | human_gate | blocked
resume_point: <下一节点>
```

只有用户要求保存或恢复时才写 `.loop-state/solution-loop/`。Loop 完成后交给 PRD/UI，不自动进入交付 Workflow，也不授权任何外部写入。
