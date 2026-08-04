---
name: assumption-ledger
description: 纠偏日志——记录用户纠正方向的结构化日志，防止已排除方向被重新引入
---

# Assumption Ledger

## 目的

记录调研过程中用户明确纠正的方向。防止：

1. 同一个已排除的方向被重新引入
2. 跨会话时接手 AI 不知道哪些已被否定
3. 复盘时找不到关键决策转折点

## 触发条件

用户明确说以下类似内容时记录：

- 「不是」「不对」「这个方向不对」
- 「这个不是重点」「这只是其中一个点」
- 「应该先看…」「更重要的是…」
- 「和 SaaS 没区别」「这个不够差异化」
- 给出了更高层级或更根本的判断

## Ledger 格式

```markdown
**Assumption Ledger**

| # | Timestamp | old_assumption | user_correction | new_framing | discarded_conclusions | impact_on_research_map |
|---|-----------|----------------|-----------------|-------------|----------------------|----------------------|
| 1 | [时间] | [之前的假设] | [用户怎么纠正的] | [新的理解] | [哪些结论被废弃] | [Research Map 怎么变] |
```

## 示例

```markdown
| # | old_assumption | user_correction | new_framing | discarded | impact |
|---|---|---|---|---|---|
| 1 | 桌面端差异在推款闭环 | 推款和SaaS没区别 | 差异在执行过程不在生成结果 | "推款闭环"不再作为桌面端差异论据 | 重新定义桌面端价值主张 |
| 2 | 本地款式资产治理是切入点 | 只是能力切片不是方向 | 它服务于更大的本地上下文理解 | "资产治理"从战略降级为能力 | L2 定位重新研究 |
| 3 | 应该从场景出发研究桌面端 | 先看行业 Agent 顶层叙事 | 需要先建立行业上下文再下钻 | 之前的场景列表暂搁置 | 启用 Top-Down Mode |
```

## 使用规则

- 每次记录后检查 Research Map 是否需要更新
- 被废弃的结论不要删除，标注为 `[discarded]` 保留审计
- 如果累计纠偏 ≥ 3 次，强烈建议暂停搜索，重新输出 Research Map
- Ledger 是输出的一部分，应包含在最终结论中供后续参考
- 跨会话 handoff 时，Assumption Ledger 必须完整传递
