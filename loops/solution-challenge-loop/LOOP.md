# Solution Challenge Loop

这是 `brainstorming` Maker 与 `grill-me` Critic 之间的可恢复状态合同，不是 mega Skill。

## Contract

1. Maker 先输出 2-3 个方案、推荐、范围、流程、风险和 `Design Spec`。
2. Critic 只输出带证据的 `Challenge Record`，定位最早因果缺口。
3. Maker 只返回针对该缺口的 `Design Delta`，不得借机重写整套方案。
4. 每轮携带 `owner`、`closure_criterion`、`preserved_items` 和 `resume_point`。
5. 缺口关闭后交给 PRD/UI；连续两轮无有效差量，或取舍不能从事实推断时进入 Human Gate。
