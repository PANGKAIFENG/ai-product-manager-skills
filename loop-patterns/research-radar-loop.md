# Research Radar Loop Pattern

This is a thin research orchestration pattern. It does not replace `research-topic-compiler/references/research-radar-loop-contract.md`; that file remains the state contract owned by `research-topic-compiler`.

## Purpose

Use this loop when an evolving topic needs a living research base, recurring evidence review, and conclusion diffs that can inform product, strategy, roadmap, or learning work.

`research-topic-compiler` remains the loop owner. `decision-research` is an escalation path when the research produces a concrete choice that needs final recommendation or exclusion logic.

## When To Use

- The topic is changing over time and new signals may alter the current understanding.
- The user wants a reusable Research Project instead of a one-pass report.
- Prior conclusions need to be compared against new evidence.
- The user wants to maintain a watchlist, evidence updates, stage conclusion diffs, and an update log.
- The research should support later roadmap, PRD, candidate backlog, or decision work.

## When Not To Use

- The user only needs a single article summary or a one-time report.
- The topic is stable foundational knowledge with no recurring product or learning need.
- The user already has a concrete A/B/C decision to close; use `decision-research`.
- The user wants generic news monitoring without a user goal, application context, or decision implication.
- The user asks to create a scheduled automation; first follow the contract's Human Gate and automation boundary.

## Node Roles

| Node | Skill | Role | Enter When | Exit With |
| --- | --- | --- | --- | --- |
| Loop Owner | `research-topic-compiler` | Maintain research definition, research map, evidence cards, stage conclusions, update log, and practical implications. | A changing topic needs reusable, cross-session research state. | Research Radar update, conclusion diff, next scan or pause decision. |
| Optional Framer | `ai-collaboration-calibration` | Clarify user goal, scope, application context, or why the topic matters. | Topic is broad, goal is fuzzy, or no application/decision need is visible. | Research goal, scope boundaries, usage scenario, open questions. |
| Optional Decision Escalation | `decision-research` | Convert research findings into a concrete recommendation when choices emerge. | Multiple product, technical, business, or strategy options must be selected or excluded. | Recommendation, confidence, reversal condition, next gate. |
| Optional Critic | `grill-me` | Challenge a stable conclusion or roadmap implication before it is acted on. | Weak signals are influencing important product, market, or investment judgment. | Critic Handoff: challenged assumptions, hype risks, missing counter-evidence. |

## State Reference

Use `research-topic-compiler/references/research-radar-loop-contract.md` for state files:

- `00_研究定义.md`
- `01_研究地图.md`
- `02_证据与卡片.md`
- `03_阶段结论.md`
- `04_下一步.md`
- `09_更新日志.md`

If a shared folder is needed, use `.loop-state/research-radar/` for local loop state, or a user-approved Research Project path for durable research artifacts.

## Output Shape

Each radar run should produce:

- scan scope and source boundary
- new signals with strength labels
- impact on current conclusions
- files to update or proposed update patch
- human review needed or not
- whether to escalate to `decision-research`
- next action: scan again, pause, update conclusions, create PRD input, or enter decision research

## Signal Handling

| Signal Type | Default Action |
| --- | --- |
| `strong-evidence` | Update evidence cards and propose a conclusion diff. |
| `weak-signal` | Append to update log; do not upgrade stable conclusions. |
| `contradictory-evidence` | Mark for human review before changing conclusions. |
| `repeated-consensus` | Consider updating stage conclusions when sources are independent. |
| `new-terminology` | Add to research map or glossary if it changes framing. |
| `new-practice` | Add to evidence cards and application notes. |
| `hype-without-proof` | Log as weak signal and track for later validation. |
| `no-meaningful-update` | Record a no-op update if the user expected a radar run. |

## Escalation Points

Escalate to `decision-research` when:

- the research creates a concrete product, technical, business, or strategy choice
- multiple options need a final recommendation and exclusion reasons
- roadmap, packaging, investment, integration, or implementation depends on the conclusion
- a Candidate Backlog needs a final decision owner

Escalate to `prd-architect` only after the research has enough stable conclusions to become product requirements.

Escalate to `prd-to-issues` only after a PRD or issue-ready backlog exists.

## Human Gates

Ask the user before:

- creating or changing a scheduled automation
- reading private, logged-in, paid, customer-specific, or company-internal sources
- updating stable conclusions based on weak signals
- writing into broad Obsidian areas or non-project files
- changing the research scope or watchlist substantially
- moving from research implications into roadmap commitment or implementation

## Stop Or Pause Conditions

Pause with one of:

- `no-meaningful-update`: recent sources add no new learning or decision value.
- `source-access-blocked`: required sources need authorization.
- `low-roi-pause`: continued scanning will not change current work.
- `decision-emerged`: a concrete choice now belongs to `decision-research`.
- `prd-input-ready`: conclusions are stable enough to become PRD or roadmap input.

## Guardrails

- Do not treat Research Radar as generic news monitoring.
- Do not create automation unless the user explicitly asks for scheduling.
- Do not rewrite stable conclusions from weak or single-source evidence.
- Do not let `research-topic-compiler` own final recommendation for a concrete decision.
- Do not keep scanning only because more sources exist.
