# Obsidian Output Contract

This contract keeps research runs aligned with the Vault structure.

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

## Required Files for L3+

| File | Purpose |
| --- | --- |
| `00_研究定义.md` | Research goal, scope, audience, expected output, depth, channels |
| `01_问题清单.md` | The questions the report must answer |
| `02_证据与卡片.md` | Evidence matrix and source links |
| `03_阶段结论.md` | High-level synthesis, current judgment, unresolved gaps |
| `04_下一步.md` | Follow-up reading, actions, validation, channel candidates |
| `05_研究报告.md` | Systematic learning report: question -> answer -> evidence -> further reading |

## Optional Files for L4/L5

| File | Purpose |
| --- | --- |
| `06_外部渠道研究.md` | GitHub, Web, product, paper, community, X, or other channel study |
| `07_行业案例对照.md` | Company/project/product comparison |
| `08_最佳实践与应用模板.md` | Reusable practices, checklist, template, operating model |
| `09_更新日志.md` | L5 radar updates and changes over time |

## Source Layer Rules

- `笔记同步助手` is a source layer. Read it, link to it, but do not move, delete, or overwrite it.
- Do not copy full source articles into a project folder.
- When a source deserves long-term handling, create or update a Resource only if it fits existing Vault rules.
- Prefer links and concise notes over duplicate content.

## Project File Responsibilities

- `01_问题清单` should contain the exact questions that `05_研究报告` answers.
- `02_证据与卡片` should be source-oriented and matrix-oriented.
- `03_阶段结论` should be decision-oriented and short enough to revisit.
- `05_研究报告` should be reader-oriented and should not force the user to read every source first.
- Optional `06-08` files should exist only when they add real structure.

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
