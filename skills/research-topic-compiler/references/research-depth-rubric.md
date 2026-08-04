# Research Depth Rubric

Use this rubric to decide how deep a research run should go before selecting channels or writing to Obsidian.

Depth is not only source count. It is whether the output helps the user understand, judge, and act.

## Levels

| Level | Name | Use when | Completion bar | Typical output |
| --- | --- | --- | --- | --- |
| L1 | 快速摘要 | User asks one narrow question or wants quick orientation | Explain what the topic is, give a basic conclusion, cite sources and limits | Direct answer or compact chat report |
| L2 | 基础研究 | User wants a compact topic map or first-pass learning path | Explain the problem solved, core concepts, basic cases, and next reading path | Short report, optional project stub |
| L3 | 系统学习 | User wants systematic learning, Obsidian organization, or unfamiliar-domain onboarding | Build topic map, explain mechanisms, provide learning route and minimal practice task | Research Project `00-05` |
| L4 | 深度研究 | Topic affects product direction, technical selection, architecture, PRD, team standards, security, commercialization, workflow/platform packaging, enterprise adoption, or high-cost/irreversible investment | Compare cases, transfer reasoning, form judgment framework, identify boundaries and counterexamples, guide design/selection/commercialization/PRD input | Research Project `00-08` |
| L5 | 长期雷达 | Topic changes quickly and should be revisited | Track evidence changes; separate stable conclusions, candidate judgments, pending validation, and discarded conclusions | `00-09`, watchlist, update log, automation proposal only if requested |

## Automatic Upgrade Signals

- Upgrade to `L3` when the user says: systematize, study, research project, Obsidian, learning path, report, evidence matrix, unfamiliar domain, or wants to learn.
- Upgrade to `L4` when the theme will influence team standards, tooling choice, product strategy, commercialization, architecture, workflow/platform packaging, enterprise adoption, Skill governance, security, compliance, PRD, or expensive/irreversible adoption.
- Upgrade to `L5` when the user asks to monitor, track, keep watching, revisit periodically, maintain a radar, or maintain stable/candidate judgment states over time.

## Automatic Downgrade Signals

- Use `L1` when the request has one direct answer and no durable learning goal.
- Use `L2` when the user wants speed, a first-pass map, or a small number of references.
- Do not create a full Research Project for one-off news lookup, translation, summary, or a question that can be answered from one authoritative source.

## Learning and Application Requirements

| Level | Understand | Judge | Act |
| --- | --- | --- | --- |
| L1 | Topic definition | Basic confidence and limitations | One next step |
| L2 | Problem solved, concepts, examples | What seems important or not | Reading path or simple checklist |
| L3 | Topic map and mechanism | Stable vs candidate conclusions | Minimal practice task with deliverable |
| L4 | Case comparison, transfer reasoning, boundaries, anti-patterns | Applicability, risks, selection criteria, adoption constraints | PRD input, workflow, architecture, eval, SOP, roadmap, commercialization frame, or template |
| L5 | Change model and signal taxonomy | Stable/candidate/pending/discarded states | Watchlist, update log, review cadence; no automatic automation unless requested |

## Sample Size Defaults

| Level | Obsidian | Official/company | GitHub | Web/articles | Papers | Community/X |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| L1 | 0-3 | 1-2 | 0-2 | 0-2 | 0-1 | 0 |
| L2 | 3-8 | 1-3 | 0-5 | 2-5 | 0-3 | 0-3 |
| L3 | 5-15 | 2-5 | 3-8 | 5-10 | 0-5 | 0-5 |
| L4 | 10+ | 3-8 | 5-10+ | 8-15 | 3-10 | 3-10 |
| L5 | Existing baseline + deltas | Watchlist | Watchlist | Watchlist | Watchlist | Watchlist |

These are defaults, not quotas. Stop when evidence converges, the marginal source adds no new insight, or channel quality is too low.

## Iterative Loop Trimming

Normal Research 和 Application 都遵循 `FRAME -> GAP -> NBE -> ACQUIRE -> EVALUATE -> UPDATE -> SATURATION`，但深度决定状态规模和持久化，不允许为了展示流程把 L1/L2 升级成研究工程。

| Level | Loop scope | Acquisition cap | Persistence | Stop bar |
| --- | --- | --- | --- | --- |
| L1 | One core Claim/Gap, one ephemeral compressed cycle | Usually 0-1; no expansion when supplied authority is sufficient | None | Core question answered with source, confidence and limitation |
| L2 | 3-5 framework nodes | At most 2 NBE acquisition actions by default | Inline; no full Source Graph | Core map is fit-for-purpose; unresolved conflict triggers upgrade advice |
| L3 | All Must Claims carry status | Gap-driven, within agreed budget | `00-05`; compact Claim/Gap/Change state | Must Claims meet contract; secondary core Claims have origin-trace attempt |
| L4 | Full Claim/Evidence/Source Graph and Change Log | Gap-driven; include independent validation and counterexample search | `00-08` plus Checkpoint as needed | Formal completion gate; saturated only after two independent-lineage low-yield actions |
| L5 | First run establishes L4 baseline; later runs process deltas | Watchlist and open-Gap driven | `00-09`, including `No change` | Pause after agreed low-yield cycles; automation requires explicit authorization |

Sample counts above are planning budgets only. Do not continue acquiring merely to hit them, and do not stop merely because they were reached.

## Confirmation Gates

Ask for explicit confirmation before continuing when:

- Recommended depth is `L4` or `L5` and the user has not already requested deep research.
- The run needs paid, private, login-only, workspace, Slack/Discord, CRM, analytics, or customer-data channels.
- The run would create many files, update existing conclusions, or touch long-term Theme / Area pages.
- The run requires API credentials such as `GITHUB_TOKEN`, `GH_TOKEN`, `X_BEARER_TOKEN`, product analytics keys, or vendor tokens.
- The run would create or schedule automation.

## Completion Bar by Level

- `L1`: answer, source links, confidence, missing evidence.
- `L2`: problem solved, concepts, basic cases, source list, next reading path.
- `L3`: `00_研究定义` to `05_研究报告`, with topic map, mechanism explanation, learning route, and minimal practice task.
- `L4`: `00-08`, cross-channel comparison, case comparison, transfer reasoning, judgment framework, boundaries, counterexamples, staged path, and reusable application template.
- `L5`: `00-09`, watchlist, refresh cadence, stable/candidate/pending/discarded conclusion states, and automation proposal only if requested.

For Normal Research/Application, apply the unique terminal order from `iterative-research-loop.md`: `blocked-authorization`, `partial-access`, `partial-budget`, `escalated`, `complete-saturated`, then `complete-fit-for-purpose`. A `complete-*` result additionally requires all Must Claims to meet or be explicitly downgraded against the Evidence Contract, no untreated critical contradiction, and no residual Gap that blocks the user's next action.
