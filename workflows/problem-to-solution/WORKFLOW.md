# 问题到方案 / Problem To Solution

把一个模糊的产品问题推进成已确认方案。它是阶段级 Workflow，只负责编排原子 Skill 和局部 Loop，不复制研究、决策、方案设计或评审的专业逻辑。

```text
问题或机会
  -> ai-collaboration-calibration? (问题/目标/判断标准不稳定时)
  -> research-topic-compiler? / decision-loop?
  -> brainstorming
  -> solution-loop?
  -> 已确认方案
```

## Entry Gate

- 输入可以是模糊感受、产品机会、待定义问题或尚未成形的需求。
- 如果问题、目标和判断标准已经稳定且只需要生成方案，直接使用 `brainstorming`。
- 如果已有候选方案且只需要反复挑战和修订，直接使用 `solution-loop`。

## Routing

| 情况 | 路径 |
| --- | --- |
| 问题已稳定、没有候选方案 | Brainstorming -> 用户确认 |
| 需要外部事实或最佳实践 | 必要的 Calibration -> Research -> Brainstorming -> 必要时 Solution Loop |
| 存在明确选择且证据不足 | 必要的 Calibration -> Decision Loop -> Brainstorming -> 必要时 Solution Loop |
| 已有候选方案、只需挑战 | Solution Loop -> 用户确认或 Human Gate |
| 高风险或影响范围大 | 必要的 Calibration -> Research/Decision Loop -> Brainstorming -> Solution Loop -> Human Gate |

每次只进入当前状态需要的下一个节点，不为了“流程完整”运行全部 Skill。

## Confirmed Solution Gate

只有同时满足以下条件，Workflow 才能以 `solution_confirmed` 结束：

- 问题、目标和成功判断已稳定；
- 推荐方案、选择理由和被排除方向明确；
- 范围内、范围外、关键约束和依赖明确；
- 核心流程或行为规则足以进入 PRD；
- 关键风险已关闭，或作为已知非阻断项记录；
- 需要业务取舍时，用户或责任人已经确认。

否则输出唯一的 `next_gap`、责任节点和恢复点。Workflow 停在确认方案，不写完整 PRD、不生成研发事项，也不发布到外部系统。

## Output

```yaml
status: solution_confirmed | human_gate | blocked
problem_definition: <稳定的问题与目标>
decision_summary: <关键证据、取舍与结论>
confirmed_solution: <方案、范围、流程和约束>
preserved_items: []
remaining_gaps: []
next_owner: solution-to-delivery | human
resume_point: <可恢复节点>
```
