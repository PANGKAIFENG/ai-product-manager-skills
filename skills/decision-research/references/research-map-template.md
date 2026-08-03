---
name: research-map-template
description: Research Map 模板——搜索前必须输出的研究地图结构，支持迭代更新
---

# Research Map Template

## 目的

Research Map 是搜索前的强制产物。它让用户在 AI 开始搜索之前就能看到研究范围，及时修正。

它也是 Scope Drift Checkpoint 的基准——后续每次自检都对照 Research Map 判断是否偏移。

## 模板

```markdown
**Research Map**

- research_type: [技术选型 / 可行性 / 平台接入 / 产品策略 / 竞品判断 / 商业模型 / 行业格局]
- current_level: [行业 / 产品 / 场景 / 能力 / 实现 / 商业]
- decision_question: [一句话核心决策问题]
- sub_questions:
  - [子问题 1：理解型]
  - [子问题 2：判断型]
  - [子问题 3：设计/实践型]
- known_context: [已确认的事实、用户提供的参考、已排除方向]
- assumptions: [当前预设 + 反转信号]
  - [假设 A] — 如果错了应看到 [信号 X]
  - [假设 B] — 如果错了应看到 [信号 Y]
- competing_hypotheses: [H1 / H2 / H3]
- evidence_needed: [需要什么类型、来源层级的证据]
- channels: [计划使用的渠道 + 不使用的渠道]
- out_of_scope: [明确不研究什么]
- stop_conditions: [满足什么条件停止]
- mode: [标准决策流 / Top-Down Product Research]
```

## 更新规则

Research Map 不是一次性文档。以下情况必须更新：

1. 用户纠正了决策问题的理解
2. 新证据改变了竞争假设的结构
3. 研究层级上升或下降
4. out_of_scope 的内容变成了 in_scope（或反过来）
5. Scope Drift Checkpoint 判断需要更新

更新时标注变化原因：

```markdown
**Research Map (Updated)**
- [变化字段]: [新值] ← 原因：[用户纠偏 / 新证据 / 层级调整]
```

## Top-Down Mode 时的 Research Map

产品策略型研究的 Research Map 增加层级下钻计划：

```markdown
- drill_down_plan:
  - L1 行业叙事: [要回答什么] — status: [待调研 / 已完成 / 跳过]
  - L2 产品定位: [要回答什么] — status: [待调研]
  - L3 业务场景: [要回答什么] — status: [待调研]
  - L4 能力体系: [要回答什么] — status: [待调研]
  - L5 技术实现: [要回答什么] — status: [待调研]
  - L6 商业包装: [要回答什么] — status: [待调研]
```
