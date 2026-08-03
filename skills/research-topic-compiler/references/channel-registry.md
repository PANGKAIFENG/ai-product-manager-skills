# Channel Registry

This registry lists reusable research channels. Add new channels here when the user explicitly wants them available for future research runs.

## Evidence Levels

| Level | Meaning |
| --- | --- |
| Strong | Primary or implementation evidence; can support core conclusions |
| Medium | Credible secondary analysis or structured market signal |
| Weak | Community, social, anecdotal, or trend signal; needs verification |
| Context | Useful for discovery or interpretation, not enough for core claims |

## Internal and Local

| Channel | Best for | Access | Evidence level | Query method | Risks | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Obsidian Vault | Existing internal knowledge, prior articles, Resource pages, Research Projects, Theme cards | Local | Strong/Medium | `rg`, file reads, Obsidian links | Stale or duplicate notes | Default internal baseline |
| Local cloned repos | Existing source snapshots, prior industry references | Local | Strong | `rg`, `git log`, README/source inspection | May be stale | Prefer `git fetch` only when user wants freshness |
| User-provided files | Private docs, exported reports, screenshots | User-provided | Strong/Medium | File inspection | Sensitive content | Keep provenance and access notes |

## Official and Company Sources

| Channel | Best for | Access | Evidence level | Query method | Risks | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Official documentation | Definitions, API behavior, product capability, constraints | Public/login | Strong | Site search, docs pages | Docs may lag product | Use first for platform topics |
| Engineering blogs | Architecture, design rationale, best practices | Public | Strong/Medium | Web search by company/domain | Marketing bias | Prefer posts with implementation detail |
| Release notes / changelog | Recent product changes, timeline | Public/login | Strong | Site search, changelog pages | Incomplete context | Useful for time-sensitive topics |
| SDK examples / cookbooks | Practical usage and recommended patterns | Public | Strong | GitHub/docs search | Examples may be simplified | Good bridge from docs to implementation |
| Status pages | Reliability, incidents, operational maturity | Public | Medium | Vendor status page | Limited history | Useful for platform risk |

## GitHub and Developer Ecosystem

| Channel | Best for | Access | Evidence level | Query method | Risks | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| GitHub repositories | Implementations, architecture, examples, ecosystem maturity | Public/token | Strong | GitHub search, `gh`, clone/read | Stars can mislead | Default 5-10 candidates for engineering topics |
| GitHub issues | Real bugs, adoption friction, missing features | Public/token | Medium | issue search | Noisy, adversarial | Use as pain evidence |
| GitHub discussions | Usage patterns, maintainer intent | Public/token | Medium | discussion search | Mixed quality | Good for design rationale |
| GitHub releases | Version history and maintenance velocity | Public/token | Strong/Medium | releases/tags | Release notes vary | Use with commit recency |
| npm / PyPI / crates.io / Maven | Package adoption and ecosystem alternatives | Public | Medium | package search | Download counts can mislead | Good for implementation discovery |
| Docker Hub / GitHub Container Registry | Deployment patterns and image maturity | Public | Medium | registry search | Metadata thin | Use for infra/tooling topics |
| VS Code Marketplace / JetBrains Marketplace | Developer tool adoption and reviews | Public | Medium | marketplace search | Ratings can be sparse | Good for IDE/tool topics |

## Product and Market Research

| Channel | Best for | Access | Evidence level | Query method | Risks | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Product Hunt | New product discovery, launch positioning, maker comments | Public/login | Medium/Weak | Product/category search | Launch hype | Prioritize maker comments and launch date |
| G2 | B2B product reviews, buyer pain, category alternatives | Public/login/paid | Medium | Category and product pages | Review bias, limited free access | Useful for competitor research |
| Capterra / GetApp / Software Advice | SMB SaaS reviews and categories | Public | Medium | Category search | SEO-heavy | Cross-check with G2 |
| AlternativeTo | Substitute products and user-tagged alternatives | Public | Weak/Medium | Product/category search | Community taxonomy is loose | Good discovery channel |
| App Store / Google Play | Mobile app reviews, update history, ratings | Public | Medium | Store search/reviews | Review sampling bias | Good for consumer/mobile topics |
| Chrome Web Store | Browser extension products and reviews | Public | Medium | Store search | Review spam | Good for extension/tooling topics |
| Shopify / Slack / Atlassian / Zapier marketplaces | Integration ecosystem and product surface | Public | Medium | Marketplace search | Vendor metadata shallow | Good for SaaS ecosystem topics |
| Pricing pages | Packaging, monetization, target segment | Public | Strong/Medium | Vendor pages | Prices change | Capture access date |
| Product changelogs | Product evolution and roadmap signals | Public/login | Strong/Medium | Vendor pages | Selective disclosure | Pair with release notes |
| Demo videos / webinars | Product workflows and positioning | Public/login | Context | YouTube/vendor site | Time-consuming, promotional | Use when UI workflow matters |
| User forums / community boards | Pain points and workflows | Public/login | Weak/Medium | Forum search | Anecdotal | Good for adoption barriers |

## Academic and Technical Reports

| Channel | Best for | Access | Evidence level | Query method | Risks | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| arXiv | Recent papers and preprints | Public | Medium/Strong | arXiv/Web search | Not peer reviewed | Good for emerging AI topics |
| Semantic Scholar | Citation graph and paper discovery | Public/API | Medium | Search by topic/author | Metadata gaps | Use to expand from seed papers |
| Google Scholar | Broad academic discovery | Public | Medium | Web search | Access friction | Good for citation trails |
| Papers with Code | Benchmarks, tasks, implementations | Public | Strong/Medium | Task/model search | Benchmark gaming | Good for eval topics |
| OpenReview | Peer review discussion and conference submissions | Public | Medium | Venue/topic search | Reviews vary | Useful for ML methods |
| ACL Anthology / ACM / IEEE | Domain literature | Public/paid | Strong/Medium | Search portals | Paywalls | Use abstracts if full text unavailable |
| Industry whitepapers | Methods and enterprise case studies | Public/form/paid | Medium | Company/analyst search | Marketing bias | Mark sponsor and access limits |

## Community and Trend Signals

| Channel | Best for | Access | Evidence level | Query method | Risks | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Hacker News | Developer reception, launch discussion, critiques | Public | Weak/Medium | HN search | Strong opinions | Good for early signal |
| Reddit | User pain, workflows, adoption barriers | Public/API | Weak/Medium | Subreddit/search | Anecdotal, noisy | Use quotes sparingly and cite |
| Stack Overflow | Developer problems and recurring errors | Public | Medium | Tag/search | Declining coverage for some topics | Good for API/tool pain |
| Discord / Slack communities | Practitioner workflows and closed community norms | Private/login | Weak/Medium | User-authorized search/export | Sensitive/private | Only with explicit authorization |
| X / Twitter | Launches, author intent, real-time trend signals | Public/API/login | Weak | X API or public Web search | API limits, virality bias | Mark as trend unless cross-verified |
| LinkedIn posts | Company/product narrative and hiring signals | Public/login | Weak/Context | Search | Promotional | Useful for enterprise go-to-market |
| Newsletters | Curated trend discovery and expert commentary | Public/subscription | Weak/Medium | Web/newsletter archive | Personal bias | Use as discovery, not final proof |
| YouTube / podcasts / interviews | Founder or researcher intent, demos | Public | Context/Weak | Search/transcripts | Hard to verify | Use for design intent only |

## Market, Company, and Organization Signals

| Channel | Best for | Access | Evidence level | Query method | Risks | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| SEC EDGAR / annual reports | Public company strategy, risk, financials | Public | Strong | Filing search | Slow-moving | Best for company strategy |
| Investor decks | Market narrative and positioning | Public/private | Medium | Company/investor pages | Promotional | Mark sponsor bias |
| Crunchbase | Funding, category, company discovery | Public/paid | Medium | Search | Free data limited | Use as discovery |
| PitchBook / CB Insights | Market maps and private company data | Paid | Medium | Authorized access | Closed, expensive | Only with user access |
| Gartner / Forrester / IDC | Enterprise category definitions and vendor landscape | Paid | Medium | Authorized reports | Paywalled, analyst bias | Use as closed-channel evidence |
| Job posts | Roadmap hints, org priorities, tech stack | Public | Weak/Medium | LinkedIn/Greenhouse/Lever/Ashby search | Indirect evidence | Useful for capability investment |
| BuiltWith / Similarweb | Tech stack and traffic estimates | Public/paid | Weak/Medium | Domain lookup | Estimates can be wrong | Use as supporting signal |

## Policy, Standards, and Security

| Channel | Best for | Access | Evidence level | Query method | Risks | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Regulator websites | Law, guidance, enforcement | Public | Strong | Official search | Jurisdiction-specific | Use exact dates |
| Standards bodies | Protocols, interoperability, compliance | Public/paid | Strong | W3C/IETF/ISO/NIST search | Some specs paywalled | Prefer official specs |
| NIST / ENISA / CISA | Security and AI governance guidance | Public | Strong | Official search | Guidance may be broad | Good for governance topics |
| CVE / NVD | Vulnerabilities and identifiers | Public/API | Strong | CVE search | Detail may lag | Pair with vendor advisory |
| GitHub Security Advisories | Package security issues | Public | Strong | Advisory search | Ecosystem-specific | Good for dependency risk |
| Vendor security advisories | Product-specific risk and mitigations | Public | Strong | Vendor search | Selective disclosure | Use with dates and versions |

## China and Chinese-Language Sources

| Channel | Best for | Access | Evidence level | Query method | Risks | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| 微信公众号文章 | Chinese practitioner essays, product analysis, terminology discovery, local practice signals | Public/login | Weak/Medium | Sogou Weixin, Web search, OpenCLI Weixin adapter, authorized API, Obsidian sync | Hard to search, anti-spider, reposts, login friction | Prefer original author/source; use snippets for candidate screening only |
| 搜狗微信搜索 | Broad discovery of WeChat article candidates by topic | Public/anti-spider | Context/Weak | `weixin.sogou.com/weixin?type=2&query=<topic>` | Redirects may hit anti-spider; metadata can be incomplete | Good for candidate table; do not assume stable full-text retrieval |
| 第三方公众号 API | Programmatic WeChat article search/detail when user authorizes provider/token | API/paid/login | Context/Weak/Medium | Provider-specific search/detail endpoints | Compliance, freshness, quota, field quality, dependency risk | Record provider, access date, fields, and original URL availability |
| WeWe RSS / RSSHub 微信源 | Ongoing monitoring of known public accounts | Local/API/login | Context/Weak/Medium | RSS feed by known account | Not broad topic search; may require login/session | Use for L5 watchlists and known-account subscriptions |
| 微信客户端转发到 Obsidian 同步号 | User-approved ingestion into `笔记同步助手` | User-authorized login | Context | Manual/UI-assisted forwarding to `Obsidian @笔记同步科技` | Side effects, login/phone confirmation, wrong recipient risk | Never silent-send; stop before final send unless current run explicitly authorizes it |
| 知乎 | Chinese user discussion and expert commentary | Public/login | Weak | Web search | Opinion-heavy | Use as weak signal |
| 掘金 / CSDN / 博客园 | Chinese developer tutorials and issues | Public | Weak/Medium | Web search | Copy-paste content | Use for implementation pain, not authority |
| InfoQ / 机器之心 / 量子位 / 36氪 | Chinese tech news and analysis | Public | Medium/Weak | Site/Web search | Media framing | Use for discovery and local context |
| 阿里云 / 腾讯云 / 华为云 / 百度智能云 docs | China cloud/platform implementation details | Public/login | Strong | Official docs | Product-specific | Good for local platform topics |

## Registry Update Template

When adding a channel, use one row in the closest section:

```markdown
| <Channel> | <Best for> | <Public/login/paid/private/API> | <Strong/Medium/Weak/Context> | <How to search or inspect> | <Main risks> | <Usage notes> |
```
