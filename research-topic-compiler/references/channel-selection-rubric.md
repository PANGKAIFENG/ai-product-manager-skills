# Channel Selection Rubric

Use this rubric after depth selection. The goal is to pick channels that fit the topic instead of searching everywhere.

## Selection Questions

Answer these before collecting evidence:

- What kind of topic is this: platform, open-source implementation, product/market, academic method, policy/compliance, security, design/UX, trend, or internal knowledge?
- What claims must the report answer: definition, mechanism, adoption, best practice, evaluation, product fit, market signal, user pain, or risk?
- How current must the evidence be?
- Which evidence type is missing from Obsidian: official definition, implementation, user feedback, benchmark, pricing, adoption, or expert intent?
- Are any useful channels closed, paid, or login-only?

## Theme to Channel Mapping

| Topic type | Strong default channels | Optional channels | Usually skip |
| --- | --- | --- | --- |
| Platform/API capability | Official docs, release notes, SDK examples, company blogs | GitHub examples, changelog, community issues | Product Hunt unless adoption matters |
| Open-source engineering | GitHub repos, issues, discussions, package registries, docs | HN, Reddit, blogs, benchmarks | App stores unless end-user product |
| Product/competitor research | Product Hunt, G2, Capterra, AlternativeTo, app stores, browser/IDE marketplaces, pricing pages, changelogs | Reddit, X, YouTube demos, job posts | Academic papers unless core tech |
| Academic/method research | Papers, technical reports, benchmarks, Papers with Code, OpenReview | Official labs, GitHub implementations | Product review sites |
| AI agent/tooling practice | Official docs, GitHub, engineering blogs, examples, marketplace, eval reports | X, HN, Discord if authorized | General news unless launch context |
| Security/compliance | Vendor security docs, NVD/CVE, advisories, standards, regulator docs | GitHub issues, security blogs | Unverified social posts |
| Design/UX patterns | Product screenshots, Mobbin, Pageflows, app stores, Figma Community, product docs | YouTube walkthroughs, social launch posts | Academic unless UX research |
| Market/category sizing | Company filings, investor decks, analyst reports, Crunchbase/PitchBook if available, job posts | News, newsletters, Similarweb/BuiltWith | Random SEO articles |
| Trend/launch tracking | Official announcements, X, Product Hunt, HN, newsletters, GitHub releases | Reddit, Discord, YouTube | Old evergreen docs alone |

## Channel Decision Format

For each channel, record:

```markdown
| Channel | Decision | Reason | Sample target | Evidence role |
| --- | --- | --- | --- | --- |
| Official docs | Use | Need primary definition | 3-5 docs | Strong definition evidence |
| X | Skip | Topic is not time-sensitive | 0 | N/A |
```

## Scoring Channels

Score candidate channels from 0 to 3:

| Score | Meaning |
| --- | --- |
| 0 | Irrelevant or too noisy for this topic |
| 1 | Useful for discovery only |
| 2 | Useful supporting evidence |
| 3 | Core evidence channel |

Prefer channels with score `2-3`. Use score `1` only to discover leads that can be verified elsewhere.

## Closed Channel Handling

Closed or semi-closed channels include paid reports, private Slack/Discord, login-only communities, workspace docs, analytics dashboards, customer support tools, CRM, private repositories, and private Product Hunt/G2 vendor dashboards.

Rules:

- Use only when the user has authorization and explicitly asks to include that channel.
- Do not bypass paywalls, login, robots restrictions, or access controls.
- Do not quote sensitive private content into public-facing files unless the user confirms it belongs in the Vault.
- Mark access limitations in the evidence matrix.
- If the channel is valuable but unavailable, list it under `仍需验证` or `04_下一步`.

## When User Adds a Channel

If the user provides a new channel, decide whether it is:

- `run-only`: useful for this topic only.
- `registry-candidate`: likely useful for future topics, but needs confirmation.
- `registry-entry`: user explicitly wants it added to the Skill channel library.

For `registry-entry`, update `channel-registry.md` with best-fit topic, access type, evidence level, query method, risks, and notes.
