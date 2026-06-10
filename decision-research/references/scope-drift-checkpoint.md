---
name: scope-drift-checkpoint
description: 范围漂移自检——每轮信息收集后检查研究是否偏离 Research Map
---

# Scope Drift Checkpoint

## 目的

研究过程中问题会不断演化。Scope Drift Checkpoint 防止 AI 在旧范围内继续搜索，而实际问题已经变了。

## 触发时机

以下情况必须执行一次 Scope Drift Check：

1. 完成一轮主要信息收集后
2. 用户给出明确纠偏后
3. 发现新的重要子问题后
4. 里程碑推进到下一阶段时（V1→V2→V3→V4）
5. 调研时间超过预期 50% 时（ROI 熔断）

## 检查项

```markdown
**Scope Drift Check**

1. 当前回答的问题还是 Research Map 里的 decision_question 吗？ [是/否]
2. 有新增的子问题吗？ [列出]
3. 有哪些结论因为用户纠偏被降级或废弃？ [列出]
4. competing_hypotheses 是否变化？ [列出变化]
5. out_of_scope 的内容是否变成了 in_scope？ [列出]
6. Research Map 是否需要更新？ [是/否 + 原因]
7. 当前调研进度：[V1/V2/V3/V4]，预期置信度：[高/中/低]
```

## 决策规则

| 情况 | 动作 |
|------|------|
| 无 drift，一切正常 | 继续当前计划 |
| 小 drift：新增子问题但主问题不变 | 更新 Research Map，继续 |
| 中 drift：研究层级发生变化 | 暂停搜索，向用户确认新方向 |
| 大 drift：决策问题本身改变了 | 停止当前调研，重新执行 R00 |
| ROI 熔断：50% 进度但置信度不足 | 缩小范围或定向补充，不全面扩展 |

## 连续 drift 处理

如果连续 2 次 Scope Drift Check 都发现问题改变了，强制执行：

> 「我注意到研究方向已经从 [原问题] 转向了 [新问题]。这是有意的转变，还是我应该回到原来的问题？」

## 与 Assumption Ledger 的关系

- Scope Drift Check 检测"范围是否偏了"
- Assumption Ledger 记录"为什么偏了"（用户纠偏）
- 两者配合使用：Scope Drift Check 发现问题，Assumption Ledger 记录原因
