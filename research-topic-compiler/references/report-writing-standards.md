# Report Writing Standards

Use these standards for `05_研究报告.md`.

## Purpose

`05_研究报告.md` is the first reading entry for the user. It should let the user understand the topic, form judgments, and know what to do next without reading every evidence card first.

`02_证据与卡片.md` is the drill-down layer. The report should cite it and the strongest sources, but it must not force the user to read source cards before understanding the topic.

## Report Modes

Choose the report shape based on the research mode:

- Normal Research: synthesize questions, evidence, conclusions, limitations, and next steps.
- Learning Pack Mode: teach the topic from first principles, then provide concept translation, learning route, and practice tasks.
- Application Mode: convert research into the user's current work decisions, templates, tasks, or implementation path.
- Radar Mode: separate stable conclusions, candidate judgments, changing signals, and watchlist items.

Modes can be combined, but avoid producing a bloated course-like report.

## Learning-Oriented Structure

Use this structure for Learning Pack Mode or when the user is entering an unfamiliar domain:

```markdown
# 研究报告

## 0. 一句话结论

<Write for the resolved user context. Product managers get product judgment; engineers get implementation judgment; managers get strategic judgment; unknown roles get a generic conclusion.>

## 1. 第一性解释

- 这个主题本质上解决什么问题？
- 为什么旧方法不够用了？
- 为什么现在重要？
- 对当前用户有什么关系？

## 2. 主题地图

<Use a text tree or Mermaid diagram. Show modules, dependencies, and boundaries.>

## 3. 核心概念转译表

| 概念 | 技术解释 | 面向当前用户的解释 | 例子 | 常见误解 | 推荐来源 |
| --- | --- | --- | --- | --- | --- |

## 4. 关键机制拆解

| 机制 | 解决什么问题 | 工作中怎么体现 | 需要什么能力支撑 | 风险/边界 |
| --- | --- | --- | --- | --- |

## 5. 核心问题回答

### 理解型问题
### 判断型问题
### 设计型问题
### 实践型问题
### 复盘型问题

## 6. 案例对照

| 案例 | 值得学什么 | 不该照搬什么 | 对当前用户的启发 |
| --- | --- | --- | --- |

## 7. 学习路线

| 阶段 | 目标 | 必读 | 暂时跳过 | 产出 |
| --- | --- | --- | --- | --- |

## 8. 实践任务

| 任务 | 产物 | 验收标准 | 对当前用户的价值 |
| --- | --- | --- | --- |

## 9. 当前判断

- 现在应该相信什么？
- 哪些还只是候选判断？
- 哪些证据不足？
- 下一步应该做什么？
```

## Normal Research Structure

For ordinary research where the user does not need a learning route, use a compact version:

```markdown
# 研究报告

## 研究主题概览

- 主题：
- 用户画像：
- 研究目标：
- 推荐深度：
- 渠道：
- 适用场景：
- 不适用场景：

## 一句话结论

## 核心问题回答

## 关键证据

## 阶段结论与边界

## 对当前用户的应用

## 仍需验证
```

## Question Types

`01_问题清单.md` should group questions by cognitive path. The report should answer the same groups:

- 理解型问题：这是什么？解决什么问题？和相邻概念有什么区别？
- 判断型问题：什么时候重要？什么时候不重要？哪些结论可信，哪些只是趋势？
- 设计型问题：如果要做产品、系统或流程，应该怎么拆？关键模块、输入、输出、权限、评测是什么？
- 实践型问题：可以做什么最小练习？产物是什么？验收标准是什么？
- 复盘型问题：哪些判断后续可能变化？需要持续跟踪什么？

## Persona-Adaptive Rules

- Product manager: translate technical mechanisms into product decisions, capability boundaries, PRD inputs, workflow design, eval criteria, and launch risks.
- Engineer: expose architecture, interfaces, state, data structures, permissions, traceability, tests, and implementation risk.
- Designer: explain user scenarios, flows, information architecture, cognitive load, and visual representation.
- Operator: convert conclusions into SOP, execution flow, content production, metrics, and review cadence.
- Manager/founder: convert conclusions into strategy, ROI, cost, risk, roadmap, resource allocation, and staged investment.
- Unknown role: use a generic explanation and avoid assuming product or engineering identity.

Every major conclusion should state its implication for the resolved user context when that context is known.

## Writing Rules

- Start with synthesis, not source order.
- Prefer first-principles explanation before jargon.
- Answer by question and cognitive path, not by article order.
- Each major answer must have `关键依据` or cite the evidence matrix.
- Separate stable conclusions, candidate judgments, weak trend signals, and unknowns.
- Include boundaries, counterexamples, and common misunderstandings.
- Keep evidence cards out of the main flow unless the user needs to drill down.
- Use `扩展阅读` only for sources worth reading after the report.
- If evidence is weak, say what would change the answer.

## Evidence Labels

Use compact evidence notes:

```markdown
- [Source title](path-or-url) - Evidence A/B/C; supports <claim>.
```

Use `02_证据与卡片.md` for detailed source-by-source notes.

## Avoid

- Listing every source in the report body.
- Repeating `02_证据与卡片`.
- Treating X/community posts as definitive.
- Writing abstract conclusions with no action or user-context implication.
- Writing generic technical explanation unrelated to the user's role or application context.
- Creating a report so long that the user still needs another summary.
