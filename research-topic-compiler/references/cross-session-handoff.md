---
name: cross-session-handoff
description: 跨会话 handoff 规范——让多轮调研可合并、给汇总 AI 友好的交接格式
---

# Cross-Session Handoff

## 目的

用户的产品研究工作经常跨多个会话。最终会把多次调研内容汇总给另一个 AI 做决策。Handoff 让这个合并过程高效、无损。

## 触发时机

以下情况输出 Handoff：

- 用户明确说"后续要让另一个 AI 汇总"
- 用户说"今天先到这里""下次继续"
- 产品决策型研究完成时默认附带 Handoff
- 用户要求生成交接文档

## Handoff 模板

```markdown
# Cross-Session Handoff

## Metadata
- research_run_id: [唯一标识]
- date: [日期]
- decision_question_id: [关联的决策问题编号]
- taxonomy_version: [如果有内部 taxonomy，标注版本]
- supersedes: [如果更新了之前的研究，标注被更新的 run_id]
- needs_refresh_after: [预计过期时间，如"2 周后需要重新验证趋势数据"]

## 本轮回答了什么
- [核心问题 1]：[结论摘要]
- [核心问题 2]：[结论摘要]

## 新增的稳定判断
- [判断 1]（置信度：高/中）— 依据：[来源]
- [判断 2]（置信度：高/中）— 依据：[来源]

## 推翻或弱化的旧判断
- [旧判断]：被推翻/弱化，原因：[新证据/用户纠偏]

## 关键证据
- [来源 1]（L1/L2）— 支持 [结论]
- [来源 2]（L2）— 支持 [结论]

## 候选方案（如有）
- 候选总数：[N]
- 通过 Quality Gate：[M]
- Top 5：[列表]
- 候选池文件位置：[路径或内联]

## 仍需统一决策
- [决策 1]：[选项 A vs B，当前倾向，缺什么信息]
- [决策 2]：[同上]

## 可能过期的内容
- [内容]：原因 [趋势数据/产品 changelog 更新/行业变化]
- 建议重新验证时间：[日期/条件]

## Assumption Ledger（如有）
| # | 旧假设 | 用户纠正 | 新判断 |
|---|--------|---------|--------|

## 给汇总 AI 的建议
- 合并时注意：[具体注意事项]
- 建议下一轮聚焦：[方向]
- 不要重复：[已充分覆盖的方向]
```

## 合并规则

当多个 Handoff 需要合并时：

1. 以最新的 `decision_question_id` 为准
2. `supersedes` 字段指示哪些旧研究被更新
3. 相同决策问题的多轮 Handoff 按时间排序
4. 冲突判断：以最新轮为准，标注"更新了 [旧判断]"
5. 候选池合并时按 `candidate_id` 去重

## Research Run Metadata

为跨会话合并保留的稳定字段：

```yaml
research_run_id: "run-2026-06-10-skill-market"
decision_question_id: "dq-style3d-skill-market-differentiation"
taxonomy_version: "v2"
source_ledger:
  - { source: "Lovart官网", level: "L1", date: "2026-06-10" }
  - { source: "Claude Skills文档", level: "L1", date: "2026-06-10" }
candidate_ids: ["SC-001", "SC-002", "SC-003"]
assumptions:
  - "Style3D 技能市场面向三类客户"
  - "Capability ≠ Scenario Skill"
open_questions:
  - "starter scene 数量上限"
  - "Desktop 专属 Skill 的比例"
supersedes: null
needs_refresh_after: "2026-07-01"
```
