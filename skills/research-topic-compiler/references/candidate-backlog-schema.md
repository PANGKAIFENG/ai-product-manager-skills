---
name: candidate-backlog-schema
description: 候选池 schema + Quality Gate——标准化候选方案输出格式和质量检查
---

# Candidate Backlog Schema

## 目的

产品决策型研究的核心产物之一是"候选池"——一组经过筛选、评分、可进入后续 PRD/starter/demo 的方案候选。

## Schema

支持 Markdown 表格或 CSV 双格式输出：

```markdown
| candidate_id | name | customer_type | persona | business_stage | scenario | input_assets | output_artifact | workflow_steps | underlying_capabilities | source_inspiration | differentiation_reason | surface_fit | complexity | priority | quality_gate | next_validation |
```

### 字段说明

| 字段 | 含义 | 示例 |
|------|------|------|
| candidate_id | 唯一编号 | SC-001 |
| name | 候选名称 | 欧洲买手店推款看板 |
| customer_type | 客户类型 | ODM/OEM |
| persona | 使用角色 | 商品企划 |
| business_stage | 业务阶段 | 推款期 |
| scenario | 一句话场景描述 | 根据买手偏好生成推款方向看板 |
| input_assets | 输入资产 | 买手 brief、历史订单、趋势素材 |
| output_artifact | 输出交付物 | 推款方向看板 PDF |
| workflow_steps | 最佳实践步骤 | 1.解析brief 2.匹配趋势 3.筛选款式 4.排版输出 |
| underlying_capabilities | 底层能力 | brief理解、趋势检索、款式匹配、PDF生成 |
| source_inspiration | 灵感来源 | 参考 Lovart 多步骤流 + WGSN 趋势映射 |
| differentiation_reason | 差异化理由 | 绑定服装行业款式库和买手偏好模型 |
| surface_fit | SaaS/Desktop/Both | Both |
| complexity | 实现复杂度 L/M/H | M |
| priority | P0/P1/P2 | P1 |
| quality_gate | 通过/未通过/降级 | 通过 |
| next_validation | 下一步验证 | 需要真实买手 brief 测试 |

## Quality Gate

每个候选必须回答以下 5 个问题。不通过则降级。

### 检查项

1. **不是按钮换名**：它有没有超越单次 API 调用的判断链？
   - 如果只是"点击→生成图"→ 降级为 capability
   
2. **不是纯 prompt gallery**：它有没有特定角色、场景和输入资产？
   - 如果任何人用任何输入都能用 → 降级为 prompt template

3. **不是泛助手**：它有没有明确的输出 artifact 和验收标准？
   - 如果输出只是"一段文字回复" → 降级为 capability

4. **有最佳实践**：它包含的工作流是否包含领域判断？
   - 如果步骤可以被通用 Agent 无差别执行 → 不是场景 Skill

5. **有明确边界**：什么时候它不应该被使用？
   - 如果回答不出来 → 定义不清晰

### 降级处理

| Quality Gate 结果 | 处理 |
|-------------------|------|
| 通过 | 进入候选池 |
| 降级为 capability | 作为底层能力记录，不上架为独立 Skill |
| 降级为 prompt template | 作为 prompt 库候选 |
| 降级为 backlog 草稿 | 待补充完善后重新评审 |
| 排除 | 记录排除理由，不进入候选池 |

## 排除项清单

好的产品研究不仅要说做什么，还要说不做什么：

```markdown
**排除项**
| 排除内容 | 排除理由 | 是否可能在后续版本恢复 |
|---------|---------|---------------------|
```

## 评分规则

通过 Quality Gate 后评分（每项 0-3）：

- 0：不适用或无此优势
- 1：弱
- 2：中等
- 3：强

总分排序后取 Top N 进入下一步。
