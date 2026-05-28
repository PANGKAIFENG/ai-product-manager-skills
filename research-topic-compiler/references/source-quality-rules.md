# Source Quality Rules

Use these rules when building the evidence matrix and writing conclusions.

## Evidence Strength

| Level | Source type | Can support |
| --- | --- | --- |
| A | Official docs, standards, regulator docs, source code, release notes, filings, reproducible benchmarks | Core definitions, mechanisms, constraints, timelines |
| B | Maintainer issues/discussions, engineering blogs, SDK examples, package metadata, credible technical reports | Implementation patterns, adoption friction, best practices |
| C | Reputable secondary analysis, high-quality tutorials, analyst reports, structured reviews | Market interpretation, learning path, product comparison |
| D | Community posts, X, Reddit, HN, forums, newsletters, videos | Trend signals, pain discovery, hypotheses |
| E | Unverified claims, reposts, SEO pages, anonymous screenshots | Discovery only; do not use for core conclusions |

Label each important claim with its strongest supporting evidence level.

## Source Metadata

Record at least:

- Title or repository name.
- Author, company, maintainer, or community.
- URL or local path.
- Access date.
- Publish or update date when available.
- Channel.
- Evidence level.
- Why it was included.
- What claim it supports.

## Screening Rules

- Prefer primary sources for definitions and platform behavior.
- Prefer implementation evidence for engineering claims.
- Prefer recent sources when product behavior, APIs, pricing, law, or market state can change.
- Cross-check social or community claims with official, implementation, or repeated independent evidence.
- Avoid using search snippets as evidence when the full source is accessible.
- Mark stale sources when the topic changes quickly.
- Do not let user persona or application needs upgrade weak evidence into stable conclusions.
- When applying a conclusion to the user's context, separate the evidence-backed claim from the inferred implication.

## Closed and Sensitive Sources

- Use only content the user is authorized to access.
- Do not bypass paywalls, login flows, API limits, or robots restrictions.
- Do not put private customer data, workspace content, or confidential excerpts into public-facing files.
- If a private source shaped the conclusion, summarize at the right abstraction level and mark it as private evidence.
- If exact citation is unsafe, cite the artifact class and access date, for example: `Private customer-support export, reviewed 2026-05-28`.

## GitHub Rules

- Default to reading docs, examples, issues, discussions, config, release notes, and source structure.
- Do not run third-party code unless the user explicitly asks and the risk is acceptable.
- Check recency with commits/releases when maintainability matters.
- Stars and forks are weak adoption signals; combine them with issue activity, release cadence, ecosystem usage, and documentation quality.

## X and Social Rules

- Treat X, Reddit, HN, Discord, Slack, and comments as weak evidence unless confirmed elsewhere.
- Use social sources to discover new projects, arguments, authors, launch timing, and user pain.
- Do not let viral claims drive the report unless stronger evidence supports them.
- If using X systematically, prefer official API access. Without API access, clearly mark the search as partial.

## WeChat and Semi-Closed Discovery Rules

- Treat WeChat Official Account articles as practitioner or market context unless the author is the primary source, the article contains original implementation detail, or claims are verified elsewhere.
- Use Sogou Weixin, Web search, OpenCLI adapters, and third-party APIs primarily for candidate discovery. Search result snippets are not enough for core conclusions.
- Prefer original `mp.weixin.qq.com` articles with account name, publish date, and full text available. Mark reposts, unattributed summaries, and AI-generated digest pages as weak or discovery-only.
- If a direct link triggers anti-spider, login, captcha, phone confirmation, or paywall, do not bypass it. Record the source as `verify later`.
- When forwarding or syncing an article to Obsidian through WeChat, record the action as ingestion provenance, not evidence strength. The synced article still needs normal source quality screening.
- Non-official API output must include provider, access date, returned fields, original URL availability, and known limitations.

## Persona and Application Claims

- Label persona-specific takeaways as interpretation when they are inferred from evidence rather than directly stated by sources.
- Application templates such as PRD snippets, workflows, evals, SOPs, roadmaps, and interface drafts can be generated from synthesis, but they must cite the evidence-backed principles they depend on.
- If a conclusion is useful for the user's context but supported only by trend or community evidence, mark it as a candidate judgment or experiment, not a stable recommendation.

## Citation in Reports

Use short citations inside `05_研究报告`:

```markdown
### 关键依据

- [Source title](path-or-url) - Evidence A/B/C; supports <claim>.
```

Use `02_证据与卡片` for fuller notes, source comparison, and source-by-source detail.
