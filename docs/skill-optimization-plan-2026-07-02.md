# Skill Optimization Plan

日期：2026-07-02
输入诊断：`docs/skill-audit-2026-07-02.md`
目标仓库：`PANGKAIFENG/ai-product-manager-skills`
执行模式：本地 issue backlog -> 逐项改造 -> 验证 -> commit -> push

## 目标标准

本轮以 `prd-architect` 的新结构作为仓库级标准：

1. `SKILL.md` 只承担触发契约、路由、关键 gate、资源索引和完成标准。
2. 模板、骨架、长规则和模式细则放到 `references/`。
3. 稳定结构问题放到 `scripts/` 做确定性检查。
4. 触发、非触发和历史失败样例放到 `evals/evals.json`。
5. 本地维护者路径、私有 runtime 说明和公开 Skill 执行规则分离。

## Issue Backlog

| Issue | Title | Priority | Status | Local file |
| --- | --- | --- | --- | --- |
| 001 | Add repo audit gate and eval schema | P1 | completed | `docs/issues/001-repo-audit-gate.md` |
| 002 | Refactor `prd-review` into router plus assets | P1 | completed | `docs/issues/002-prd-review-assets.md` |
| 003 | Refactor `decision-research` modes and checks | P1 | completed | `docs/issues/003-decision-research-modes.md` |
| 004 | Refactor `research-topic-compiler` router and cleanup local runtime notes | P1 | completed | `docs/issues/004-research-topic-router.md` |
| 005 | Harden UI wireframe and mockup Skills | P1 | completed | `docs/issues/005-ui-skills-hardening.md` |
| 006 | Add evals and checkers for product handoff Skills | P2 | completed | `docs/issues/006-product-handoff-evals.md` |
| 007 | Add evals and assets for collaboration/governance Skills | P2 | completed | `docs/issues/007-collaboration-governance-evals.md` |
| 008 | Sync registry, routing, metadata, and changelog | P2 | completed | `docs/issues/008-catalog-sync.md` |

## Execution Order

1. Land issue backlog and repo-level audit gate.
2. Fix high-blast-radius PRD review flow.
3. Fix research routing conflicts: `decision-research` then `research-topic-compiler`.
4. Harden UI outputs with templates and package checkers.
5. Add eval/checker coverage to the remaining product and collaboration Skills.
6. Sync catalog docs and run full verification.

## Verification Gate

Run before commit:

```bash
python3 scripts/audit_skills.py .
for d in */SKILL.md; do python3 /Users/linctex/.config/skillshare/skills/skill-reviewer/scripts/check_skill.py "${d%/SKILL.md}"; done
python3 prd-architect/scripts/check_prd_shape.py docs/fixtures/sample-prd-standard.md --type standard || true
python3 prd-review/scripts/check_prd_shape.py docs/fixtures/sample-prd-standard.md --type standard || true
git diff --check
```

If fixture files are not present, skip fixture-specific checks and rely on script help/audit execution.

## Execution Result

本轮已完成 8 个本地 issue：

- 仓库级 `scripts/audit_skills.py` 和 `docs/eval-schema.md` 已落地。
- 13 个公开 Skill 都已有 `evals/evals.json`。
- 高风险输出型 Skill 都已有最小 checker 或验证脚本。
- `decision-research`、`research-topic-compiler`、`prd-review` 已按 router-plus-assets 方向瘦身或拆出 references。
- `ui-wireframe-to-html` 不再依赖公开不可用的本地模板路径，改用随包模板。
- catalog、routing、changelog 和本地 issue backlog 已同步。

通过门禁：

```bash
python3 scripts/audit_skills.py .
```

## Push Policy

- Commit only intended files.
- Push to `origin main` after validation passes.
- Do not create remote GitHub Issues in this run; the stored Markdown issue backlog is the source of truth for this optimization pass.
