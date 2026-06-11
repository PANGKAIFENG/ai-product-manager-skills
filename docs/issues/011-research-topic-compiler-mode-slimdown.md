# Issue 011 - Slim research-topic-compiler mode surface

## Title

Reduce `research-topic-compiler/SKILL.md` mode complexity by moving heavy mode detail into references

## Type

HITL

## Priority / Labels

P2

Suggested labels: `refactor`, `research`, `context-budget`

## Source

- `docs/skill-boundary-and-loop-audit.md`
- `research-topic-compiler/SKILL.md`
- `research-topic-compiler/references/`

## Problem

`research-topic-compiler` is useful but mode-heavy. It currently covers Normal Research, Lightweight Concept Lens, Learning Pack, Application Mode, Radar Mode, and Product Candidate mode in one large entry file.

This increases routing and context-budget cost. The main `SKILL.md` should act as a mode router and keep detailed execution rules in references.

## What To Change

- Keep `research-topic-compiler/SKILL.md` as:
  - trigger contract
  - mode routing table
  - key boundaries
  - resource guide
  - evaluation checklist
- Move thick details for selected modes into references if not already there:
  - Lightweight Concept Lens
  - Learning Pack
  - Application Mode
  - Product Candidate / Product Candidate pre-research
- Ensure references are named clearly and loaded only when relevant.
- Do not change behavior while moving content.

## Acceptance Criteria

- [ ] Main `SKILL.md` remains readable as a routing surface.
- [ ] Mode-specific detail is available under `references/`.
- [ ] Product Candidate ownership remains aligned with Issue 004.
- [ ] Existing resources and scripts remain linked.
- [ ] No public trigger behavior is removed accidentally.

## Verification

Static:

```bash
wc -l research-topic-compiler/SKILL.md
rg -n "Lightweight Concept Lens|Learning Pack|Application Mode|Product Candidate|Radar Mode" research-topic-compiler/SKILL.md research-topic-compiler/references
```

Smoke prompts:

- [ ] `系统研究一下 AI Agent Memory，并整理到 Obsidian。`
- [ ] `轻量解构 MCP 的概念源流，输出 PM 决策看板。`
- [ ] `我对 Agent Harness 陌生，帮我系统学习。`
- [ ] `研究市面上的 AI 视频生成方案，先沉淀候选池。`
- [ ] `长期雷达跟踪 Claude Skills 生态变化。`

## Blocked By

- Issue 004

## Open Questions

- Which mode details should remain in `SKILL.md` because they are critical to safe routing?
