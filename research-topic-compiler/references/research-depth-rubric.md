# Research Depth Rubric

Use this rubric to decide how deep a research run should go before selecting channels or writing to Obsidian.

## Levels

| Level | Name | Use when | Default output | Typical channels |
| --- | --- | --- | --- | --- |
| L1 | 快查 | User asks one narrow question or wants a quick orientation | Direct answer with sources and limitations | 1-3 sources, usually official/Web/Obsidian |
| L2 | 轻研 | User wants a compact topic map or first-pass learning path | Short report, optional project stub | Obsidian + 2-5 external sources |
| L3 | 标准研究 | User wants systematic learning or Obsidian organization | Research Project `00-05` | Obsidian + selected strong external channels |
| L4 | 深度专题 | Topic affects important decisions, team standards, product direction, architecture, or high-cost adoption | Research Project `00-08` with external study and best practices | Official/company docs, GitHub, Web, papers, product channels, community as needed |
| L5 | 长期雷达 | Topic is fast-moving and should be tracked repeatedly | Watchlist, update log, periodic review proposal | Dynamic sources + automation proposal |

## Automatic Upgrade Signals

- Upgrade to `L3` when the user says: systematize, study, research project, Obsidian, learning path, report, evidence matrix.
- Upgrade to `L4` when the theme will influence team standards, tooling choice, product strategy, architecture, Skill governance, security, compliance, or expensive adoption.
- Upgrade to `L5` when the user asks to monitor, track, keep watching, revisit periodically, or maintain a radar.

## Automatic Downgrade Signals

- Use `L1` when the request has one direct answer and no durable learning goal.
- Use `L2` when the user wants speed, a first-pass map, or a small number of references.
- Do not create a full Research Project for one-off news lookup, translation, summary, or a question that can be answered from one authoritative source.

## Sample Size Defaults

| Level | Obsidian | Official/company | GitHub | Web/articles | Papers | Community/X |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| L1 | 0-3 | 1-2 | 0-2 | 0-2 | 0-1 | 0 |
| L2 | 3-8 | 1-3 | 0-5 | 2-5 | 0-3 | 0-3 |
| L3 | 5-15 | 2-5 | 3-8 | 5-10 | 0-5 | 0-5 |
| L4 | 10+ | 3-8 | 5-10+ | 8-15 | 3-10 | 3-10 |
| L5 | Existing baseline + deltas | Watchlist | Watchlist | Watchlist | Watchlist | Watchlist |

These are defaults, not quotas. Stop when evidence converges, the marginal source adds no new insight, or channel quality is too low.

## Confirmation Gates

Ask for explicit confirmation before continuing when:

- Recommended depth is `L4` or `L5` and the user has not already requested deep research.
- The run needs paid, private, login-only, workspace, Slack/Discord, CRM, analytics, or customer-data channels.
- The run would create many files, update existing conclusions, or touch long-term Theme / Area pages.
- The run requires API credentials such as `GITHUB_TOKEN`, `GH_TOKEN`, `X_BEARER_TOKEN`, product analytics keys, or vendor tokens.

## Completion Bar by Level

- `L1`: answer, source links, confidence, missing evidence.
- `L2`: topic map, first conclusions, source list, next reading path.
- `L3`: `00_研究定义` to `05_研究报告`, with question-level answers.
- `L4`: `00-08`, cross-channel comparison, best practices, and reusable template or action model.
- `L5`: watchlist, refresh cadence, update log format, and automation proposal if requested.
