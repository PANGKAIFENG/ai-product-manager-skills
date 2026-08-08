# Product Discovery

面向问题尚未完全收敛、但需要形成产品判断的阶段组合。它只组织原子 Skill 和 Loop，不复制其专业逻辑。

```text
ai-collaboration-calibration
        -> research-decision-loop (当证据影响决策时)
        -> brainstorming
        -> solution-challenge-loop (当方案风险需要压测时)
        -> prd-architect 或回到 research-decision-loop
```

## Routing

- 小问题：校准后直接 `brainstorming`。
- 需要事实：先 `research-topic-compiler`；存在具体选择时进入 `decision-research`。
- 方案形成后再调用 `grill-me`；不要把 Critic 当作方案生成器。
- 两轮没有减少 gap，或用户必须做业务取舍时停止并交 Human Gate。

## Output

保留问题定义、决策记录、Design Spec、未决 gap、下一责任节点和恢复点。Loop 不自动调用外部写入工具。
