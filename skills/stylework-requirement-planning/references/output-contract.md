# Output Contract

Use progressive delivery. The first response should make the batch understandable; the scheduling table follows in the same response only when requested, or after the user clarifies the batch priorities.

## A. Batch theme map

| 主题 | 这一批在解决什么 | 代表需求 | 数量 | 当前迭代分布 | 性质 | 置信度 |
| --- | --- | --- | ---: | --- | --- | --- |
| ... | ... | ... | ... | ... | 用户体验/业务能力/平台基建/可靠性治理/探索验证 | 高/中/低 |

Then list:

- `重复/重叠候选`：需求 A <-> 需求 B，判断、差异待确认、误合并风险。
- `依赖/前置能力`：A -> B，依赖理由与错误判断风险。
- `模糊项`：标题、当前可推断范围、最小缺失事实、是否影响本轮排期。
- `批次观察`：当前重点、迭代负载信号、负责人集中、能力链是否断裂。

End with at most 1-3 batch-level questions when answers would materially improve the draft.

## B. Iteration direction

| 建议迭代 | 本迭代重点 | 优先进入的主题/需求 | 前置条件 | 负载与风险 |
| --- | --- | --- | --- | --- |
| `26.8.1` | ... | ... | ... | ... |

If capacity or estimates are unavailable, write `相对顺序建议，非容量承诺`.

## C. Per-requirement draft

Use these exact columns:

| 标题 | 主题 | 当前迭代 | 建议迭代 | 当前优先级 | 建议优先级 | 排期理由 | 依赖 | 风险 | 缺失信息 | 置信度 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | 高/中/低 |

Rules:

- Show unchanged items as well as moved items when the user asks for a complete draft.
- Use `暂不调整` when evidence does not justify a change.
- If a large item should be split, write the suggested validation and delivery sequence in `建议迭代` and explain it.
- Never hide missing information behind a confident narrative.

## D. Co-planning focus

Finish with the 1-3 decisions that would most improve the plan, for example:

1. Which theme is the month's primary outcome?
2. Which items have verified customer or leadership commitments?
3. Which shared foundation must land before downstream work?

Do not produce a long per-item questionnaire.

## E. Revision delta

After user clarification, show changes before the refreshed table:

| 需求/主题 | 原建议 | 新建议 | 变化原因 | 置信度变化 |
| --- | --- | --- | --- | --- |

This lets the user see how their priorities changed the plan without comparing two full tables manually.
