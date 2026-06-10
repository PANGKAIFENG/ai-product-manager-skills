---
name: product-decision-mode
description: 产品决策型研究模式——围绕产品策略选择的多源竞品研究+候选池+决策交接
---

# Product Decision Research Mode

## 触发信号

用户的研究目标包含以下任一：

- 产品策略选择（选哪个方向、怎么定位、做不做某个功能体系）
- 竞品研究后要落地（不只是了解竞品，而是转化为内部行动）
- 市场到 backlog（外部观察 → 内部候选池）
- 候选方案池生成（生成 N 个候选 Skill/场景/功能/方向）
- starter scene / demo beachhead 筛选
- 跨会话合并多次调研

## 与其他模式的区别

| | Normal Research | Learning Pack | Product Decision |
|---|---|---|---|
| 目标 | 建立对主题的认知 | 系统学习陌生领域 | 做出产品决策 |
| 核心产物 | 证据矩阵 + 阶段结论 | 学习框架 + 实践任务 | 候选池 + 评分 + 排除项 + handoff |
| 停止标准 | 问题覆盖充分 | 认知框架建立 | 决策可做出 / 候选池可评审 |

## 默认工作流

1. **决策问题锚定**：这次研究服务什么产品决策？
2. **项目上下文 intake**：读取本地项目事实（见 `project-context-intake.md`）
3. **竞品市场分层**：按类别组织外部观察
4. **Taxonomy 转译**：把外部模式转成内部分类（见 `taxonomy-translation.md`）
5. **候选池生成**：输出标准化候选 backlog（见 `candidate-backlog-schema.md`）
6. **质量门禁**：每个候选通过 Quality Gate
7. **评分排序**：按多维度评分
8. **排除项清单**：明确说不做什么、为什么
9. **下一步验证**：哪些候选进入 starter / PRD / demo / eval

## 默认产物

```markdown
**Product Decision Research Result**
- Decision question: [核心产品决策]
- Project context: [当前项目状态摘要]
- Market segments studied: [竞品分层]
- Internal taxonomy: [转译后的内部分类]
- Candidates generated: [N 个]
- Passed quality gate: [M 个]
- Top candidates: [排序后 Top 5-15]
- Excluded: [排除项 + 理由]
- Recommended beachhead: [Top 3 starter / demo]
- Open decisions: [仍需统一决策的问题]
- Next validation: [下一步验证动作]
- Handoff available: [是/否]
```

## 评分维度

候选方案默认评分（0-3 分）：

| 维度 | 含义 |
|------|------|
| 用户频次 | 这个场景用户多久做一次 |
| 差异化强度 | 竞品做不了或做不好 |
| 行业最佳实践含量 | 是否包含领域知识 |
| 输入资产可得性 | 用户是否容易提供输入 |
| 输出 artifact 清晰度 | 交付物是否明确可检查 |
| 实现复杂度 | 工程成本 |
| Surface/Channel fit | 适合 SaaS/Desktop/Mobile/IM |
| 风险等级 | 合规/安全/用户隐私风险 |
| Starter 适合度 | 是否适合作为首批展示 |
| Demo 适合度 | 是否适合作为演示重点 |

## 何时不用 Product Decision Mode

- 用户只是想了解一个主题（用 Normal Research）
- 用户要系统学习一个陌生领域（用 Learning Pack）
- 用户已经做完决策，只想监控后续变化（用 Radar）
- 研究不涉及候选池、评分或排除（用 Normal/Application）
