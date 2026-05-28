# Pre-Research Source Expansion

Use this reference when a research run needs more input than the user's existing Obsidian inbox or seed files provide.

The goal is not to search every channel. The goal is to widen the candidate pool, screen quickly, and only promote useful sources into the evidence matrix.

## When to Enable

Enable this stage when one or more conditions apply:

- The user says they do not want to rely on pre-collected Obsidian inputs.
- The topic is new, niche, fast-moving, China-local, product/market-driven, or practice-heavy.
- Obsidian baseline scan returns too few useful sources.
- The report needs examples, user pain, competitive products, launch signals, practitioner essays, or implementation references.
- The user asks to include a new channel such as WeChat Official Accounts, Sogou Weixin, Product Hunt, G2, X, Discord, or a third-party API.

Skip this stage when the user asks for a quick answer, provides enough authoritative sources, or forbids external discovery.

## Candidate Source Table

Before reading deeply, produce a candidate table:

```markdown
| Title | Channel | Author/account | Date | URL/access | Snippet | Relevance | Quality | Recommended action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| <title> | <Sogou Weixin / Product Hunt / GitHub / ...> | <author> | <date> | <url or access note> | <short snippet> | <why it matters> | <A-E or Strong/Medium/Weak/Context> | <read now / sync to Obsidian / verify later / skip> |
```

Screening rules:

- Keep 5-10 candidates for L3, 10-20 for L4, and a watchlist for L5.
- Prefer original sources, primary company pages, maintainers, official repos, and sources with implementation details.
- De-duplicate reposts, SEO clones, AI-generated summaries, and articles that only repeat the same seed.
- Use snippets only for screening. Do not cite snippets as evidence when the full source is accessible.
- Put blocked but valuable sources into `04_下一步.md` or `仍需验证`.

## WeChat Official Account Workflow

WeChat Official Account content is useful for Chinese practitioner essays, product framing, local market context, and early terminology discovery. It is not a default authority source.

Recommended path:

1. Search candidates through public/open discovery first:
   - Sogou Weixin result pages.
   - General Web search with title/account keywords.
   - OpenCLI Weixin adapter or similar local tools when available.
   - Third-party WeChat article APIs only with user authorization.
   - WeWe RSS/RSSHub when the target official account is already known.
2. Build the candidate table with title, account, date, snippet, access status, and suspected original/repost status.
3. Promote only selected articles:
   - `read now` if publicly readable and relevant.
   - `sync to Obsidian` if the user wants the article in `笔记同步助手` and confirms the sync action.
   - `verify later` if Sogou redirects to anti-spider, login is required, or only partial metadata is visible.
4. After articles enter `笔记同步助手`, treat that folder as read-only source material. Curated output belongs in the Research Project.

Important limitations:

- Sogou Weixin can often return titles, snippets, dates, and redirect links, but direct article resolution may trigger anti-spider pages. Treat it as discovery, not stable full-text retrieval.
- The official WeChat Open Platform APIs are mainly for account owners to manage their own published/material content; they are not a general public article search API.
- Non-official API sites can help with search/detail extraction, but they add dependency, compliance, quota, and freshness risk. Record the API provider, token requirement, access date, and extracted fields.
- WeWe RSS/RSSHub are better for known accounts and ongoing subscriptions than broad topic search.

## WeChat Client and Obsidian Sync Boundary

Opening the local WeChat client and forwarding articles to `Obsidian @笔记同步科技` or any sync account is a side-effectful communication action.

Rules:

- Do not silently send, forward, or sync content by default.
- Require explicit authorization in the current research run before operating WeChat or sending to the sync account.
- Prefer a visible stop-before-send checkpoint: prepare the selected article/link list, open the target chat if needed, then ask the user to confirm before the final send.
- If WeChat asks for phone login confirmation, captcha, or re-authentication, stop and mark the channel as blocked.
- Never bypass login, paywall, anti-spider, API limits, or access controls.
- Record what was synced, when, and where it is expected to appear in Obsidian.

Safe default:

- Write candidate links and screening notes into `06_外部渠道研究.md`.
- Ask the user to choose which items to sync.
- After sync completes, rescan `笔记同步助手` and incorporate the synced articles as read-only evidence.

## Third-Party API Evaluation

Before using a non-official API, check:

- Access: public, token, paid, login, rate limits.
- Scope: search only, metadata only, full article detail, account archive, or RSS.
- Provenance: whether it returns original `mp.weixin.qq.com` URLs, account names, publish dates, and content.
- Stability: whether the API is actively maintained and can handle anti-spider changes.
- Compliance: whether use is allowed for the user's research purpose.
- Evidence role: usually discovery/supporting evidence, not a core source unless the extracted content points back to an original article.

Record API-derived evidence as:

```markdown
- Channel: <provider/tool>
- Access: <public/token/paid/login>
- Fields used: <title/date/account/url/content/snippet>
- Original URL available: <yes/no>
- Evidence role: <discovery/supporting/full-text source>
- Limitations: <rate limit/blocked fields/anti-spider/staleness>
```

## Product and Market Expansion Channels

For product research, consider these before generic Web search:

- Product Hunt: launch positioning, maker comments, similar products.
- G2 / Capterra / GetApp: buyer reviews, pain points, category language.
- AlternativeTo: adjacent products and user-tagged alternatives.
- Chrome Web Store / VS Code Marketplace / Slack / Shopify / Atlassian / Zapier marketplaces: ecosystem surface and reviews.
- Pricing pages and changelogs: packaging, segment, maturity, and direction.
- App Store / Google Play: consumer reviews and update history.
- Job posts: indirect roadmap and team investment signals.

Use product/market channels as `Medium/Weak` evidence unless corroborated by official docs, implementation artifacts, or repeated independent evidence.
