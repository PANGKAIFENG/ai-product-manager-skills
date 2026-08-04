# Dynamic Channel Selection Rubric

Use this rubric when planning a Next Best Evidence (NBE) Action. Select a channel for the current highest-value Gap, not for the topic in the abstract and not once for the entire run.

This rubric refines Normal Research and Application. It does not change routing for Learning Pack, Product Candidate, Radar, or other mode-specific flows.

## Selection Gate

Before selecting a channel, answer:

- Which ranked Gap is the action targeting, and what is its closure criterion?
- What result would materially change the Claim or Framework?
- Does the action need an original definition, implementation, independent validation, market signal, contrast, counterexample, or context?
- Which lineage or publisher must be independent from evidence already held?
- How current and direct must the Evidence be?
- What are the time, tool, payment, login, privacy, and authorization risks?
- Is there already enough authoritative Evidence for the current purpose?

If the last answer is yes, skip channel expansion and proceed to evaluation or synthesis. Do not search merely to satisfy channel diversity.

## Rank Actions, Then Channels

Rank candidate actions by their expected reduction of decision-relevant uncertainty. Default priorities are:

1. Must Gap before Should before Could.
2. Trace a secondary Claim to its origin before collecting more summaries of it.
3. Prefer high decision impact and high uncertainty.
4. Prefer direct Evidence that can meet the closure criterion.
5. Prefer a genuinely independent lineage when corroboration or generalization is required.
6. Prefer the lowest reasonable cost and access risk among actions with similar information gain.
7. Seek contrast or counterexamples before stabilizing a high-impact generalized Claim.

Channel familiarity, brand visibility, search ranking, Stars, and available snippets are weak convenience signals. They do not outrank information gain, directness, independence, or access feasibility.

## Channel Decision Format

Record each considered action, including the selected one:

```markdown
| Target Gap | Candidate action/channel | Source role | Expected information gain | Independence target | Cost/access risk | Decision | Selection reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| <gap ID> | <specific target via channel> | <role> | <what uncertainty may change> | <lineage/publisher requirement> | <risk> | <select/defer/skip> | <why it ranks here> |
```

Every selected action must have all seven explanatory fields. “Popular,” “high-star,” “industry leader,” “many results,” or “recommended channel for this topic” is insufficient by itself.

## Gap to Channel Lookup

Use this table as a candidate generator after the Gap and evidence role are known. It is not a fixed itinerary.

| Needed Evidence | Strong candidate channels | Supporting channels |
| --- | --- | --- |
| Platform definition or current capability | Official docs, source code, standards, release notes, SDK examples | Maintainer issues, engineering blogs, changelog |
| Open-source mechanism or implementation | Canonical repo docs/source/tests/releases, package registry | Independent implementations, issues, discussions, benchmarks |
| Product positioning or packaging | Official product pages, pricing, changelog, launch posts | Product Hunt, marketplaces, demos, reviews |
| User pain or adoption friction | Structured reviews, support/issue evidence, independent user reports | Reddit, HN, X, videos, authorized communities |
| Academic method or benchmark | Papers, technical reports, OpenReview, reproducible benchmarks | Lab pages, implementation repos, critique papers |
| Security or compliance | Standards, regulator docs, NVD/CVE, vendor advisories | Security research, issue trackers, credible technical reports |
| Design or UX behavior | Current product, product docs, screenshots, Pageflows/Mobbin | App stores, demos, user reports, Figma Community |
| Market size or organizational investment | Filings, investor materials, regulator statistics | Analyst reports, job posts, Similarweb/BuiltWith |
| Recent launch or trend | Official announcements, release feeds, changelogs | Product Hunt, HN, X, newsletters, communities |
| China-local practice | Original WeChat articles, local platform/cloud docs, direct implementations | Sogou discovery, Zhihu, Juejin/CSDN, Chinese tech media |

Use generic Web search to locate candidates across these channels, not as an Evidence class of its own.

## Open-Source Project Sampling

Select repositories by the evidence role required to close the Gap. A project may hold more than one role, but each selected project needs one primary reason for inclusion.

| Role | What it tests | Typical candidate |
| --- | --- | --- |
| `Canonical` | What the originating owner officially specifies or implements | Owner-maintained repo or official example |
| `Independent` | Whether the mechanism transfers outside the original lineage | Separate maintainers with no fork/derivation relation |
| `Production` | How the practice survives real operations, maintenance, and constraints | Deployed project with releases, issues, tests, and active use evidence |
| `Contrast` | How a materially different design solves the same problem | Alternative architecture chosen on an explicit comparison dimension |
| `Counterexample` | Where the Claim fails, causes harm, or does not generalize | Failed implementation, limitation report, rejected design, or conflicting result |

For every selected project, record:

- target Gap and closure criterion;
- project role and observable artifacts to inspect;
- expected information gain and framework-changing result;
- lineage root, fork/derivation relationship, and independence group;
- cost/access/execution risk and selection reason;
- limitations such as toy status, stale releases, narrow domain, or missing production evidence.

Do not run third-party code unless the user explicitly asks and the risk is acceptable. Stars and forks may help discover candidates but are weak popularity signals. Never use them as the primary selection reason or as proof of quality, production readiness, correctness, or independent validation. Prefer the evidence-bearing artifacts relevant to the Gap: source, tests, configs, releases, issue history, deployment evidence, maintainer explanations, and reproducible behavior.

## Dynamic Re-selection

Re-run channel selection after each `EVALUATE → UPDATE FRAMEWORK → CHECK SATURATION` cycle. The next Gap may require a different evidence role and channel.

- A recovered original source may eliminate the need for more same-publisher material.
- A disputed Claim may shift the next action from official docs to independent validation.
- A generalized Claim may require a peer comparison or counterexample.
- A low-yield action may lower the rank of that channel for the current Gap without banning the channel globally.
- A new Must Gap may replace the prior queue leader.

Do not continue collecting from a selected channel after the target Gap closes or its marginal information gain falls below the next feasible action.

## Closed Channel Handling

Closed or semi-closed channels include paid reports, private Slack/Discord, login-only communities, workspace docs, analytics dashboards, customer support tools, CRM, private repositories, and private vendor dashboards.

- Use them only when the user is authorized and explicitly includes the channel in the current run.
- Do not bypass paywalls, login, robots restrictions, API limits, captcha, or access controls.
- Record the target Gap, expected value, access risk, and affected Claim when access is blocked.
- Do not quote sensitive private content into public-facing artifacts without confirmation.
- A sending or syncing action requires current-run authorization and a visible confirmation point.
- For unavailable high-value sources, preserve the action as blocked and consider a public alternative in the next NBE decision.

## When the User Adds a Channel

Classify a user-provided channel without changing other mode routes:

- `run-only`: useful for the current Gap.
- `registry-candidate`: potentially reusable but not yet validated across topics.
- `registry-entry`: the user explicitly requests addition to the channel library.

For `registry-entry`, update `channel-registry.md` with best-fit evidence roles, access type, query method, source-quality ceiling, independence considerations, risks, and notes. Registry presence only makes a channel discoverable; it never makes the channel mandatory.
