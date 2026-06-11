# Issue 009 - Add AGENTS thin orchestration index

## Title

Add `AGENTS.md` as a thin orchestration index

## Type

HITL

## Priority / Labels

P2

Suggested labels: `documentation`, `agent-runtime`, `routing`

## Source

- `docs/skill-boundary-and-loop-audit.md`
- `README.md`
- `SKILL_ROUTING.md`
- `SKILL_REGISTRY.md`
- `loop-patterns/`

## Problem

The repo has several entry surfaces. README is for humans, Registry is catalog/status, Routing is adjacent Skill disambiguation. Agent-facing runtime orientation is still implicit.

An `AGENTS.md` can help agents start from the correct routing surface without bloating README or Registry.

## What To Build

Create `AGENTS.md` as a thin index, not a thick spec.

Minimum content:

- Start here: read `SKILL_ROUTING.md` before choosing adjacent Skills.
- Role model summary:
  - Framer
  - Researcher
  - Maker
  - Critic
  - Reviewer
  - Router / Gate
- Loop pattern index:
  - `loop-patterns/prd-readiness-loop.md`
  - future `loop-patterns/decision-research-loop.md`
  - future `loop-patterns/research-radar-loop.md`
- State directory convention.
- Stop / human handoff rules.
- Anti-over-looping rule.
- Catalog update rule: README / Registry / Routing must stay coordinated.

## Acceptance Criteria

- [ ] `AGENTS.md` exists at repo root.
- [ ] It is short enough to serve as a first-pass agent orientation file.
- [ ] It links to README, Registry, Routing, and existing loop-pattern files.
- [ ] It does not duplicate all Skill descriptions.
- [ ] It preserves current responsibility split between README / Registry / Routing.

## Verification

```bash
test -f AGENTS.md
rg -n "SKILL_ROUTING|SKILL_REGISTRY|README|loop-patterns|anti|human|catalog" AGENTS.md
```

Manual check:

- [ ] A new agent can answer “where do I route a fuzzy product problem?”
- [ ] A new agent can answer “when do I enable a loop?”
- [ ] A new agent can answer “what catalog files must change when adding a Skill?”

## Blocked By

- Issue 005
- Issue 007

## Open Questions

- Should `AGENTS.md` be added before or after `loop-patterns/decision-research-loop.md`?
