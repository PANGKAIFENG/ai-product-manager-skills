# Issue 004 - Clarify Product Candidate ownership

## Title

Clarify ownership between `research-topic-compiler` Product Candidate mode and `decision-research`

## Type

HITL

## Priority / Labels

P1

Suggested labels: `skill-boundary`, `research`, `routing`

## Source

- `docs/skill-boundary-and-loop-audit.md`
- `research-topic-compiler/SKILL.md`
- `decision-research/SKILL.md`
- `SKILL_ROUTING.md`

## Problem

The repo-level research boundary is good:

- `research-topic-compiler`: research for understanding, learning, long-term knowledge, and Research Projects.
- `decision-research`: research for a concrete decision and final recommendation.

But `research-topic-compiler` has a Product Candidate Research mode that currently handles candidate backlog, scoring, Top candidates, Candidate Summary, and cross-session handoff. This overlaps with `decision-research`, especially when users ask “选 A 还是 B” or “帮我选一个”.

## Recommended Decision

Use this ownership model:

- `decision-research` owns final concrete decision recommendations, exclusion reasons, confidence, and reversal conditions.
- `research-topic-compiler` may own candidate discovery, candidate backlog, long-cycle research state, and cross-session handoff.
- If `research-topic-compiler` produces ranked candidates, it should frame them as input to a decision, not as the final decision authority.

## What To Change

- In `research-topic-compiler/SKILL.md`:
  - Rename or clarify Product Candidate Research as candidate discovery / pre-research / long-cycle candidate pool mode.
  - Remove or soften language that claims final Top recommendation ownership for single-session concrete decisions.
  - Add transfer rule: final recommendation goes to `decision-research`.
- In `decision-research/SKILL.md`:
  - Clarify it can consume Candidate Backlog / Cross-Session Handoff from `research-topic-compiler`.
  - Clarify it owns final stance for concrete decisions.
- In `SKILL_ROUTING.md`:
  - Add explicit split:
    - candidate pool / long-term research -> `research-topic-compiler`
    - choose / decide / recommend one -> `decision-research`

## Acceptance Criteria

- [ ] `research-topic-compiler` no longer claims final single-decision ownership.
- [ ] `decision-research` explicitly accepts RTC candidate backlog as input.
- [ ] `SKILL_ROUTING.md` can route “候选池” vs “选一个” separately.
- [ ] Existing Research Radar Loop behavior is unchanged.

## Verification

Routing smoke tests:

- [ ] `帮我对比 Electron vs Tauri vs Flutter Desktop，选一个做桌面端。` -> `decision-research`
- [ ] `研究市面上的 AI 视频生成方案，先沉淀候选池，后续继续补。` -> `research-topic-compiler`
- [ ] `基于这个 Candidate Backlog 给我一个最终推荐。` -> `decision-research`
- [ ] `系统研究桌面端技术栈演进，整理到 Obsidian。` -> `research-topic-compiler`

Static check:

```bash
rg -n "Product Candidate|Top candidates|Candidate Backlog|decision-research" research-topic-compiler/SKILL.md decision-research/SKILL.md SKILL_ROUTING.md
```

## Blocked By

None.

## Open Questions

- Should the mode name remain `Product Candidate Research`, or be renamed to `Candidate Discovery Research` / `Product Candidate Research`?
