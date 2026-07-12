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
- Product Candidate Research 完成时默认附带 Handoff
- 用户要求生成交接文档

## Handoff 模板

```markdown
# Cross-Session Handoff

## Metadata
- research_run_id: [唯一标识]
- date: [日期]
- decision_question_id: [关联的决策问题编号]
- taxonomy_version: [如果有内部 taxonomy，标注版本]
- framework_version: [当前 Framework 版本]
- terminal_status: [唯一终态；仍在进行时写 active]
- last_completed_state: [最后完成的 loop state]
- supersedes: [仅在证据满足替换规则时填写被更新的 run_id/claim_id，否则为 null]
- supersedes_evidence: [支持替换的 evidence_id + 强度/直接性/新鲜度/独立性理由]
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
- [来源 1]（Evidence A-E + directness + independence group）— 支持/挑战 [Claim]
- [来源 2]（Evidence A-E + directness + independence group）— 支持/挑战 [Claim]

## 研究恢复点
- Current Gap: [当前最高优先 Gap]
- Ranked NBE Queue: [按优先级列出下一证据动作]
- Completed / blocked actions: [已完成与受阻动作]
- Next exact action: [下一会话可直接执行的单一动作]
- Artifact paths: [状态与产物路径]

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

1. 先按 `decision_question_id` / research goal 对齐同一问题；问题不同则并列，不能因时间更晚合并成一个结论。
2. 按 canonical URL/path/repository identity 与 `lineage_root` 去重来源；转载、镜像、摘要和 fork 不重复计作独立证据。
3. 逐 Claim 比较 Evidence 的强度、直接性、新鲜度、独立性和适用范围。时间顺序只用于建立历史，不决定真伪或覆盖权。
4. 只有新证据更强、更直接、更适用于当前范围，或旧结论已明确过期/被用户纠正时，才填写 `supersedes`；同时必须填写 `supersedes_evidence` 和对应 Change Event。
5. 冲突证据强弱不足以替换时，保留两侧 Claim，标记 `contested`，生成 contradiction Gap；不得采用“最新轮覆盖”。
6. `supersedes: null` 表示补充或并列，不表示默认继承覆盖权。
7. 候选池按 `candidate_id` 去重，但评分和状态变化同样保留证据与版本历史。

## Research Run Metadata

为跨会话合并保留的稳定字段：

```yaml
research_run_id: "run-2026-06-10-skill-market"
decision_question_id: "dq-style3d-skill-market-differentiation"
taxonomy_version: "v2"
framework_version: "v3"
terminal_status: "partial-access"
last_completed_state: "CHECK SATURATION"
source_ledger:
  - { source: "Lovart官网", evidence_level: "A", directness: "direct", independence_group: "lovart", date: "2026-06-10" }
  - { source: "Claude Skills文档", evidence_level: "A", directness: "direct", independence_group: "anthropic", date: "2026-06-10" }
candidate_ids: ["SC-001", "SC-002", "SC-003"]
assumptions:
  - "Style3D 技能市场面向三类客户"
  - "Capability ≠ Scenario Skill"
open_questions:
  - "starter scene 数量上限"
  - "Desktop 专属 Skill 的比例"
current_gap: "验证生产环境中的失败边界"
ranked_nbe_queue:
  - "读取独立生产案例的事故复盘"
next_exact_action: "在已授权来源中定位一份可引用的事故复盘"
artifact_paths: ["01_问题清单.md", "02_证据与卡片.md", "04_下一步.md"]
supersedes: null
supersedes_evidence: null
needs_refresh_after: "2026-07-01"
```
