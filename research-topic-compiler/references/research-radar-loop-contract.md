---
name: research-radar-loop-contract
description: Research Radar Loop contract for maintaining a living knowledge base on evolving topics
---

# Research Radar Loop Contract

## Purpose

Research Radar Loop is used when a topic is changing over time and the user wants a living knowledge base instead of a one-time report.

The loop maintains signal quality, evidence changes, conclusion diffs, and practical implications. It is not a generic news monitor, and it does not create Codex automations unless the user explicitly asks to create or schedule one.

## When to Use

Use this contract for topics that meet most of these conditions:

1. The topic is evolving.
2. New sources can materially change the user's understanding.
3. The user has a recurring learning, product, strategy, or planning need.
4. Prior conclusions may need revision.
5. There is an existing or desired Research Project.
6. The output should be reusable across sessions.

Do not use this contract for:

1. A single article summary.
2. Stable foundational knowledge.
3. A one-time decision with clear options.
4. A simple factual lookup.
5. A topic with no user application or decision need.

## Required Inputs

- Research topic
- Why the topic matters
- User role and usage scenario
- Key questions
- Source scope
- Update frequency, if any
- Output format
- Existing Research Project path, if available
- Write boundary and authorization

If write boundary or authorization is unclear, default to chat-only output or a proposed patch plan. Do not write into broad knowledge bases without confirmation.

## State Files

Use these files for a Research Project. If the project has local naming overrides, map the same responsibilities onto the existing files.

| File | Purpose |
| --- | --- |
| `00_研究定义.md` | Topic definition, user goal, scope, source policy, and update cadence. |
| `01_研究地图.md` | Research questions, source map, watchlist, and open gaps. |
| `02_证据与卡片.md` | Evidence cards and source-backed findings. |
| `03_阶段结论.md` | Current synthesis and conclusion state. |
| `04_下一步.md` | Next research actions, application actions, or decision gates. |
| `09_更新日志.md` | Per-run signal log, no-op records, and pending review items. |

## Loop Steps

1. Read the existing research definition and last update log.
2. Check the watchlist and open gaps.
3. Scan selected high-quality sources.
4. Identify new signals and classify strength.
5. Update or propose updates to the evidence matrix.
6. Compare new evidence with current stage conclusions.
7. Record conclusion diffs, including no-op updates.
8. Identify practical implications for the user's work.
9. Decide whether to continue, pause, or escalate to `decision-research`.
10. Record the update log and next action.

## Signal Types

| Signal type | Meaning | Default action |
| --- | --- | --- |
| `strong-evidence` | Reliable source that changes or strengthens a conclusion. | Update evidence cards and propose conclusion diff. |
| `weak-signal` | Early sign, practitioner anecdote, or unverified trend. | Append to update log for later review. |
| `contradictory-evidence` | Evidence that conflicts with current conclusions. | Mark `needs-human-review`. |
| `repeated-consensus` | Multiple sources repeat the same pattern. | Consider updating stage conclusions. |
| `new-terminology` | New phrase or category appears. | Add to research map or glossary if useful. |
| `new-practice` | New workflow, pattern, or implementation method. | Add to evidence cards and application notes. |
| `hype-without-proof` | High attention but weak evidence. | Log as weak signal; do not upgrade. |
| `no-meaningful-update` | Sources add no new decision or learning value. | Record no-op update. |

## Update Rules

1. Weak signals go to `09_更新日志.md`.
2. Strong evidence updates `02_证据与卡片.md`.
3. Repeated consensus can update `03_阶段结论.md`.
4. Contradictory evidence is marked `needs-human-review`.
5. No meaningful update must still be logged as a no-op if the user expected a radar run.
6. Decision implications should trigger a recommendation to invoke `decision-research`.
7. Broad source, credential, private community, or automation changes require user confirmation.

## Pause Conditions

Pause the loop when:

1. No meaningful new signal appears for the agreed number of cycles.
2. Sources become repetitive.
3. The topic becomes stale for the user's work.
4. The user no longer has a learning, product, or decision need.
5. Continued tracking has low ROI.
6. Required sources need access the user has not authorized.

## Escalate to Decision Research

Recommend `decision-research` when:

1. A practical decision emerges.
2. Multiple competing options appear.
3. The user needs to choose a product, technical, business, or strategy direction.
4. Research findings affect product roadmap, packaging, investment, or implementation.

## Human Gate

Ask the user before:

1. Creating or updating an automation.
2. Updating stable conclusions based on weak signals.
3. Writing into broad Obsidian areas or non-project files.
4. Reading private, logged-in, paid, or customer-specific sources.
5. Changing the research scope or watchlist substantially.

## Output Template

Use this template after each radar run:

```markdown
# Research Radar Loop Update

## 1. Scan Scope

...

## 2. New Signals

| Signal | Source | Strength | Notes |
| --- | --- | --- | --- |

## 3. Impact on Current Conclusions

...

## 4. Files to Update

- `02_证据与卡片.md`
- `03_阶段结论.md`
- `09_更新日志.md`

## 5. Human Review Needed

Needed / Not needed

Reason: ...

## 6. Escalate to Decision Research

Yes / No

Reason: ...

## 7. Next Step

...
```

## Handoff

Every radar run should leave:

1. What changed
2. What did not change
3. Which signals are weak
4. Which conclusions need review
5. Whether the next step is scan, pause, decision research, PRD input, or assetization
