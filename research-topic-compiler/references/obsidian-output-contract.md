# Obsidian Output Contract

This contract keeps research runs aligned with the Vault structure while supporting persona-adaptive learning and application outputs.

## Default Location

Create or update research projects under:

```text
/Users/linctex/Documents/ClawVault/02_Projects/Research_Projects/
```

Default folder name:

```text
研究-<主题名>
```

Use the existing folder if one already matches the topic.

## Default Research Project Files

Default L3+ and deep research projects use `00-09` when the depth and evidence justify them. L3 may stop at `00-05` if optional files would add no structure.

| File | Purpose |
| --- | --- |
| `00_研究定义.md` | Research goal, user context, scope, audience, output mode, depth, channels |
| `01_问题清单.md` | Questions grouped by cognitive path: understanding, judgment, design, practice, review |
| `02_证据与卡片.md` | Evidence matrix, source cards, source links, source quality, drill-down notes |
| `03_阶段结论.md` | Stable/candidate conclusions, evidence level, persona meaning, application impact, actions, boundaries |
| `04_下一步.md` | Follow-up reading, validation, actions, channel candidates, profile gaps |
| `05_研究报告.md` | First reading entry: systematic explanation, topic map, concept translation, mechanism, cases, learning route, practice tasks |
| `06_外部渠道研究.md` | GitHub, Web, product, paper, community, X, or other channel study |
| `07_行业案例对照.md` | Case comparison with lessons, non-transferable parts, and current-user implications |
| `08_最佳实践与应用模板.md` | Reusable practices and persona-adaptive templates for applying the research |
| `09_更新日志.md` | L5 radar updates and changes over time |

## Optional Independent Learning Files

Do not create these by default. Suggest them only when one condition is true:

1. The user explicitly asks for an independent learning package.
2. The topic is L4/L5 and content would make `05_研究报告.md` too long.
3. The project needs to be reused by other learners.
4. `05_研究报告.md` is already too long to remain the first reading entry.

| File | Purpose |
| --- | --- |
| `10_学习路线.md` | Staged learning path, required reading, skipped-for-now topics, outputs |
| `11_概念地图.md` | Concept map, dependency map, glossary, boundaries |
| `12_实践任务.md` | Practice tasks, deliverables, acceptance criteria, self-check questions |

## Source Layer Rules

- `笔记同步助手` is a source layer. Read it, link to it, but do not move, delete, or overwrite it.
- Do not copy full source articles into a project folder.
- When a source deserves long-term handling, create or update a Resource only if it fits existing Vault rules.
- Prefer links and concise notes over duplicate content.

## File Responsibilities

### `01_问题清单.md`

Group questions by cognitive path:

- A. 理解型问题：这是什么？解决什么问题？和相邻概念有什么区别？
- B. 判断型问题：什么时候重要？什么时候不重要？哪些结论可信，哪些只是趋势？
- C. 设计型问题：如果要做产品、系统或流程，应该怎么拆？关键模块、输入、输出、权限、评测是什么？
- D. 实践型问题：可以做什么最小练习？产物是什么？验收标准是什么？
- E. 复盘型问题：哪些判断后续可能变化？需要持续跟踪什么？

### `02_证据与卡片.md`

This is the drill-down layer, not the first reading entry. It should be source-oriented and matrix-oriented.

Include:

| Question | Source | Claim | Evidence level | User implication | Reusable lesson |
| --- | --- | --- | --- | --- | --- |

### `03_阶段结论.md`

Each stable conclusion must include:

- 一句话结论
- 为什么成立
- 证据等级
- 对当前用户画像的解释
- 对当前用户业务/目标的影响
- 可执行动作
- 适用边界
- 反例或误区

Do not output only abstract conclusions.

### `05_研究报告.md`

This is the first reading entry. It should not force the user to read `02_证据与卡片.md` first.

For Learning Pack Mode, follow `report-writing-standards.md` and include first-principles explanation, topic map, concept translation, mechanism breakdown, learning route, and practice tasks.

### `07_行业案例对照.md`

Use this matrix:

| Case | 核心做法 | 解决什么问题 | 值得学什么 | 不该照搬什么 | 对当前用户的启发 |
| --- | --- | --- | --- | --- | --- |

Do not only compare industries; convert cases into user-relevant judgments.

### `08_最佳实践与应用模板.md`

Best practices must include persona-adaptive application templates:

- Product manager: PRD snippets, capability-boundary table, workflow design table, eval metrics.
- Engineer: interface draft, module split, test checklist, log/trace fields.
- Designer: user journey, information architecture, decision path, diagram checklist.
- Operator: SOP template, metric review table, content production flow.
- Manager/founder: roadmap, investment table, risk matrix, org responsibilities.

## Link Rules

- Use Obsidian-compatible relative or absolute markdown links already common in the Vault.
- For local paths in final user messages, prefer clickable absolute markdown links.
- Keep each conclusion traceable to `02_证据与卡片` or a cited source.

## Write Safety

Before writing:

- Check whether a matching project already exists.
- Check whether existing files contain user edits.
- Preserve unrelated content and append or integrate carefully.
- If replacing a prior conclusion, mark it as an update with date and reason.
- For L4/L5 or broad edits, get explicit confirmation unless the user already requested implementation.
- Do not create automation from L5 unless the user explicitly asks to create or schedule it.
