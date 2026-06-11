---
name: taxonomy-translation
description: 外部模式→内部分类的转译规范——把竞品观察转成内部可用的产品 taxonomy
---

# External-to-Internal Taxonomy Translation

## 目的

研究结论不能停在"竞品有这些功能"。必须转译成内部产品分类，服务实际产品决策。

## 触发时机

Product Candidate Research Mode 的第 4 步：竞品/外部观察收集完后，写入证据矩阵之前。

## 竞品市场分层模板

外部观察先按类别组织：

| 分层 | 含义 | 示例 |
|------|------|------|
| 通用 Agent / Skill 市场 | 不限行业的 Agent 平台 | Claude Skills, GPT Store, Kuse |
| 垂直行业 Agent | 特定行业的 Agent 产品 | Lovart, WGSN AI, Accio Work |
| 开放 Registry / Mirror | 开源/社区 Skill 仓库 | ClawHub, GitHub skill repos |
| 行业相邻 Workflow | 相邻行业的自动化工具 | Canva, Figma Make, Runway |
| 安全与治理案例 | 权限、审计、合规实践 | Azure AI governance, AWS Bedrock guardrails |

每类输出：
- 代表产品
- 组织逻辑（按什么维度分类）
- 分发/上新/审核机制
- 可借鉴模式
- 不适合照搬的原因

## 转译字段

把外部观察转成内部产品分类时，使用以下通用字段：

```markdown
| 外部模式 | 内部用户类型 | 业务阶段 | 输入资产 | 输出 artifact | 底层 capability | 场景 Skill | Surface fit | 风险等级 | 权限边界 |
|---------|------------|---------|---------|-------------|---------------|-----------|------------|---------|---------|
```

## Surface / Channel Fit 取值

不同产品 surface 适合不同类型的 Skill/功能：

| 取值 | 含义 |
|------|------|
| SaaS-first | 在线轻量操作为主 |
| Desktop-heavy | 需要本地文件/浏览器/工具执行 |
| Both | SaaS 和 Desktop 都适合 |
| Mobile | 移动端适合 |
| IM | 即时通讯渠道适合 |
| Protocol artifact | 通过 API/协议输出 |

## 转译规则

1. 不要只列外部功能名 → 必须映射到内部用户角色+业务阶段
2. 不要照搬外部分类 → 用内部已有的 taxonomy 去匹配
3. 如果外部产品的分类暴露了内部 taxonomy 的盲区 → 建议扩展内部分类
4. 标注"可借鉴模式"和"不适合照搬的原因"

## 示例

```markdown
外部观察：Lovart 把创意设计任务拆成"品牌研究→风格定义→概念生成→多变体→导出"

转译为内部：
- 内部用户类型：品牌设计师 / 商品企划
- 业务阶段：品牌企划期
- 输入资产：品牌指南、参考图、关键词
- 输出 artifact：风格板、多方案对比图、设计稿
- 底层 capability：理解品牌、图像生成、多变体、格式导出
- 场景 Skill：品牌视觉企划助手
- Surface fit：SaaS-first
- 可借鉴：多步骤拆解 + 中间产物可检查
- 不适合照搬：Lovart 面向通用设计，我们面向服装行业有垂直知识
```
