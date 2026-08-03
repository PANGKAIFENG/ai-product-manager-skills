# Gap-Driven Source Acquisition

Use this reference during `ACQUIRE` when the current Next Best Evidence (NBE) Action requires discovering or retrieving a source. Candidate discovery is not a one-time stage before research and is not a quota-filling exercise. It is a bounded response to the highest-value open Gap.

This reference refines evidence acquisition for Normal Research and Application. It does not change mode routing or require Learning Pack, Product Candidate, or Radar to adopt the iterative research loop.

## Entry and Skip Gate

Enter source acquisition only when all of the following are true:

- The current Framework has an open Gap whose closure would materially improve a Must or Should Claim.
- The Gap has a closure criterion and a ranked priority.
- One NBE Action has been selected for that Gap.
- Existing readable sources do not already meet the Claim's evidence contract.
- The action is within the run's scope, budget, and authorization.

Skip external discovery when the user supplied enough authoritative, direct, and current evidence for the present purpose. This is the normal L1/L2 path, not a degraded result. Also skip when the user forbids external discovery, the expected information gain is low, or a required access action is not authorized.

Do not enable acquisition merely because the topic is new, a channel exists, Obsidian has few files, or a depth level suggests a candidate count. Source count and channel coverage are budgets, never completion criteria.

## NBE Action Contract

Execute one NBE Action per loop. Record these fields before searching:

```markdown
- Target Gap: <gap ID and closure criterion>
- Action type: <trace origin / verify claim / compare peer / inspect implementation / seek independent validation / seek contrast or counterexample>
- Target: <specific source, owner, project class, or query>
- Expected information gain: <what uncertainty could decrease and what result would change the framework>
- Source role: <primary definition / implementation / independent validation / contrast / counterexample / context>
- Independence target: <required lineage or publisher separation>
- Cost/access risk: <time, paid/login/private, rate limit, anti-spider, or execution risk>
- Selection reason: <why this action outranks the next alternative>
```

If the top-ranked action is skipped, record the access, cost, scope, authorization, or low-yield reason and select the next feasible NBE. Do not silently substitute a convenient channel.

## Acquisition Strategies

Choose the smallest strategy that can close the target Gap:

1. **Trace the origin**: follow citations, document titles, repository references, release links, or quoted phrases from a secondary Seed Corpus to the actual primary source.
2. **Verify with the same owner**: find official docs, release notes, source code, talks, or examples that clarify what the owner actually claims or implements.
3. **Test generalization across peers**: only when the Claim applies beyond one platform, select comparable authoritative owners on an explicit comparison dimension.
4. **Inspect implementation**: examine canonical or independent repositories, examples, issues, configs, releases, and tests to check whether a stated practice is executable.
5. **Seek independent validation**: choose a different lineage root or publisher that can corroborate the mechanism or observed outcome.
6. **Seek contrast or counterexample**: look for a materially different design, a failed application, a limitation, or evidence that would challenge the current Claim.
7. **Acquire practitioner or market context**: use reviews, practitioner essays, communities, or local channels for pain, language, and hypotheses, then verify important Claims with stronger evidence.

Do not mechanically expand from one famous company to every other famous company. Peer expansion requires a cross-platform Gap and a named comparison dimension.

## Candidate Screening

Create a candidate table only when an NBE Action has multiple plausible targets. Keep it as small as needed to choose the next source; do not build a broad inventory by default.

```markdown
| Candidate | Channel | Source role | Target Gap | Expected information gain | Independence | Cost/access risk | Selection reason | Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| <title/repo> | <channel> | <role> | <gap ID> | <uncertainty reduced> | <lineage/publisher relation> | <risk> | <why now> | <acquire / verify later / skip> |
```

Screen candidates using these rules:

- Prefer sources that can satisfy the Gap's closure criterion, not sources that are merely relevant to the topic.
- Prefer the original source, direct implementation, or a genuinely independent lineage according to the NBE role.
- Treat snippets as discovery metadata. Do not cite them as Evidence when the underlying source is accessible.
- De-duplicate reposts, translations, summaries, SEO clones, forks, and articles that derive from the same lineage root.
- Put valuable but inaccessible candidates in the blocked action log with the affected Gap; do not count them as acquired Evidence.
- Stop candidate discovery as soon as one feasible target clearly dominates. Return to `EVALUATE` after acquisition rather than continuing to collect.

## WeChat Official Account Workflow

WeChat Official Account content is useful for Chinese practitioner essays, product framing, local market context, and terminology discovery. It is not a default authority source.

When the NBE Action calls for this channel:

1. Discover candidates through public/open paths first: Sogou Weixin, general Web search with title/account keywords, an available local adapter, or RSS for an already-known account.
2. Record title, account, date, snippet, access status, suspected origin, target Gap, and expected information gain.
3. Prefer the original `mp.weixin.qq.com` article with readable full text. Mark redirects, partial metadata, reposts, and unresolved origins as `verify later` or discovery-only.
4. Promote only the article selected for the NBE Action. If the user wants it in `笔记同步助手`, obtain current-run authorization before syncing.
5. Treat `笔记同步助手` as read-only source material after ingestion. Curated output belongs in the Research Project.

Sogou Weixin may expose titles, snippets, dates, and redirect links while blocking full article resolution. Treat it as discovery, not stable full-text retrieval. The official WeChat Open Platform APIs manage an owner's own content and are not a general public article search API. WeWe RSS/RSSHub are better for known-account monitoring than broad topic discovery.

## WeChat Client and Obsidian Sync Boundary

Opening the local WeChat client and forwarding an article is a side-effectful communication action.

- Do not silently send, forward, or sync content.
- Require explicit authorization in the current run and use a visible stop-before-send checkpoint.
- Stop on phone confirmation, captcha, re-authentication, paywall, anti-spider, or other access controls.
- Record what was synced, when, where it should appear, and which Gap motivated the action.
- Treat successful ingestion as provenance only; it does not increase evidence strength.

Safe default: write the selected link and screening note into `06_外部渠道研究.md`, ask the user whether to sync, and rescan `笔记同步助手` only after the user completes or authorizes the action.

## Third-Party API Evaluation

Before using a non-official API, record:

- access type, token/payment/login needs, quota, and authorization;
- whether it returns search results, metadata, full text, account archives, or RSS;
- whether original URL, owner, publish date, and content provenance are available;
- maintenance, freshness, anti-spider, dependency, and compliance risks;
- the target Gap, expected information gain, evidence role, independence, and why this provider is the next best action.

API output without a traceable original source is normally discovery or supporting material. Never upgrade it to primary evidence because the provider labels a result “official.”

## Product and Market Acquisition

Select product and market channels only when they match the current Gap:

- launch positioning or maker intent: Product Hunt and official launch posts;
- buyer pain and category language: G2, Capterra, GetApp, app stores, or marketplaces;
- packaging and direction: pricing pages, changelogs, release notes, and official demos;
- ecosystem surface: browser, IDE, Slack, Shopify, Atlassian, or Zapier marketplaces;
- organizational investment: job posts, filings, and investor materials;
- adjacent alternatives: AlternativeTo and comparable product directories.

Reviews, directories, and marketplace data usually provide supporting or hypothesis-generating evidence. Corroborate stable product Claims with official artifacts, implementation evidence, or repeated independent observations.

## Exit

After acquiring one source or recording why acquisition is blocked:

1. assign or confirm its source identity and lineage;
2. pass it to `EVALUATE` for Evidence extraction and Claim impact;
3. do not continue browsing until the Framework is updated and saturation is checked;
4. if acquisition failed, preserve the affected Gap and choose an authorized alternative only in the next NBE decision.
