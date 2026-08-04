# Routing Evals Audit v0.2.2

- 日期：2026-08-04
- 仓库：`PANGKAIFENG/ai-product-manager-skills`
- 分支：`v0.2.2-routing-evals`
- 审计基线：`v0.2.1-skill-dedup` / `92dd9e9`

## 1. 结论

本轮已把 13 个 active Skill 的 eval 统一为机器可读的 routing contract，并把最低覆盖要求加入仓库审计门禁。

- eval case 从 84 条增加到 129 条，原 84 条 case 的 `prompt` 和 `expected_output` 语义均保留。
- 基线中 41 条未分类 case 已全部补齐 `type`、`should_trigger`、`expected_route` 和 `assertions`。
- 新增或补齐 18 组同 prompt 的 paired routing case；每组只有一个 trigger owner，其余相邻 Skill 明确 handoff。
- 每个 Skill 都达到至少 `2 trigger / 2 non-trigger / 1 known-risk`。
- `scripts/audit_skills.py` 现在会拒绝缺失或无效的 routing 字段、非 JSON boolean、无效 assertions、单文件重复 ID 和最低覆盖回退。

本轮结论只证明 routing intent、schema 和最低覆盖可被确定性审计，不证明模型在 clean context 中一定选择预期 Skill。本轮没有运行真实模型 routing harness。

## 2. 范围边界

本轮只修改：

- 13 个 `skills/*/evals/evals.json`
- `scripts/audit_skills.py`
- `scripts/tests/test_audit_skills.py`
- `docs/eval-schema.md`
- 本实施计划和审计报告

本轮明确未修改：

- `skills/*/SKILL.md` 及其 trigger contract
- `catalog/skills.yaml`
- `SKILL_ROUTING.md` 和 `SKILL_REGISTRY.md`
- 本地已安装 Skill

本轮未执行 `skillshare sync`。

## 3. Before / After Coverage

`Unclassified before` 表示基线 case 缺少 `type`、`should_trigger`、`expected_route` 或 `assertions` 中至少一个字段。

| Skill | Before | Unclassified before | After | Trigger | Non-trigger | Known-risk |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `ai-collaboration-calibration` | 3 | 0 | 7 | 4 | 3 | 1 |
| `ai-work-assetization-diagnoser` | 3 | 0 | 5 | 3 | 2 | 1 |
| `brainstorming` | 4 | 0 | 7 | 3 | 4 | 1 |
| `competitive-analysis` | 4 | 0 | 6 | 3 | 3 | 1 |
| `complex-exploration` | 3 | 0 | 12 | 6 | 6 | 1 |
| `decision-research` | 6 | 0 | 10 | 6 | 4 | 1 |
| `grill-me` | 3 | 0 | 4 | 2 | 2 | 1 |
| `prd-architect` | 10 | 10 | 16 | 12 | 4 | 8 |
| `prd-review` | 6 | 0 | 9 | 5 | 4 | 2 |
| `prd-to-issues` | 4 | 0 | 7 | 3 | 4 | 1 |
| `research-topic-compiler` | 23 | 16 | 25 | 21 | 4 | 8 |
| `ui-mockup-desktop-workbench` | 10 | 10 | 13 | 7 | 6 | 3 |
| `ui-wireframe-to-html` | 5 | 5 | 8 | 3 | 5 | 1 |
| **Total** | **84** | **41** | **129** | **78** | **51** | **30** |

## 4. Paired Routing Inventory

下表只统计跨 Skill 使用相同 ID 和相同 prompt、同时包含 `true` 与 `false` owner 的 18 组 intentional pairs。不同 Skill 中历史遗留的字符串 ID `3`、`4`、`5` prompt 不同，不计入 paired case。

| Paired case ID | Trigger owner | Explicit handoff from |
| --- | --- | --- |
| `paired-competitor-evidence-ready-final-selection` | `decision-research` | `competitive-analysis` |
| `paired-competitor-evidence-still-missing` | `competitive-analysis` | `decision-research` |
| `paired-complex-run-content-retrospective` | `complex-exploration` | `ai-work-assetization-diagnoser` |
| `paired-high-fidelity-after-structure-confirmed` | `ui-mockup-desktop-workbench` | `prd-architect`, `ui-wireframe-to-html` |
| `paired-multiround-complex-exploration` | `complex-exploration` | `ai-collaboration-calibration`, `brainstorming` |
| `paired-prd-drafting-stage` | `prd-architect` | `prd-review`, `prd-to-issues` |
| `paired-prd-only-before-ui-structure` | `prd-architect` | `ui-mockup-desktop-workbench`, `ui-wireframe-to-html` |
| `paired-prd-readiness-review-stage` | `prd-review` | `prd-architect`, `prd-to-issues` |
| `paired-prd-ready-issue-decomposition-stage` | `prd-to-issues` | `prd-architect`, `prd-review` |
| `paired-problem-stable-needs-design-options` | `brainstorming` | `ai-collaboration-calibration`, `complex-exploration` |
| `paired-problem-unstable-before-design-options` | `ai-collaboration-calibration` | `brainstorming` |
| `paired-repeated-ai-work-needs-layer-diagnosis` | `ai-work-assetization-diagnoser` | `complex-exploration` |
| `paired-research-path-still-unstable` | `complex-exploration` | `research-topic-compiler` |
| `paired-research-question-stable-systematic-evidence` | `research-topic-compiler` | `complex-exploration` |
| `paired-single-fuzzy-problem-before-complex-exploration` | `ai-collaboration-calibration` | `complex-exploration` |
| `paired-stable-decision-ready-for-recommendation` | `decision-research` | `complex-exploration` |
| `paired-structure-stage-before-high-fidelity` | `ui-wireframe-to-html` | `prd-architect`, `ui-mockup-desktop-workbench` |
| `paired-unstable-exploration-before-decision` | `complex-exploration` | `decision-research` |

所有 `should_trigger: false` case 的 `expected_route` 均指向本仓库 13 个 Skill 之一，或使用显式 `external:<skill-id>` handoff。仓库审计会校验本地 route allowlist 和 trigger owner 一致性；外部 Skill 继续使用命名 handoff，不成为本仓库安装依赖。

## 5. Deterministic Gate

新增仓库门禁要求：

1. `id`、`type`、`prompt`、`expected_route`、`expected_output` 必须是非空字符串。
2. `should_trigger` 必须是严格 JSON boolean；整数 `1` 不视为 `true`。
3. `assertions` 必须是非空 list，每项必须是 object 且包含非空字符串 `text`。
4. `expected_route` 必须指向仓库 Skill 或合法的 `external:<skill-id>`；trigger 必须指向自身，non-trigger 不得指回自身。
5. eval ID 在单个 eval 文件内不得重复；跨 Skill 的 intentional paired ID 允许重复。
6. 每个 active Skill 至少包含 2 个 trigger、2 个 non-trigger 和 1 个 known-risk case。
7. 非空 `known_regression`，或 `type` 中包含 `risk` / `regression`，计为 known-risk。

`scripts/tests/test_audit_skills.py` 共 22 个测试方法，覆盖必填字段的 missing、empty、whitespace、integer、list、boolean 等非法值，route target / owner 错配，以及 exact `2/2/1` 边界。

## 6. Release Evidence

| Gate | Result |
| --- | --- |
| `python3 scripts/audit_skills.py .` | PASS，13 个 Skill，无 hard error |
| `python3 -m unittest discover -s scripts/tests -p 'test_*.py' -v` | PASS，22/22 |
| `python3 -m unittest discover -s skills/prd-architect/tests -p 'test_*.py' -v` | PASS，13/13 |
| `python3 -m unittest discover -s skills/research-topic-compiler/tests -p 'test_*.py' -v` | PASS，28/28 |
| `python3 .../skill-reviewer/scripts/check_skill.py skills/*` | PASS，13/13，无 deterministic hard failure |
| `python3 -m json.tool` for all eval files | PASS，13/13 |
| `python3 -m py_compile scripts/audit_skills.py scripts/tests/test_audit_skills.py` | PASS |
| `git diff --check` | PASS |

非阻塞 warning：`research-topic-compiler` 的 5 个既有 Concept Lens reference 未被 `SKILL.md` 直接提及，checker 提示可能不易发现：

- `references/concept-lens-html-dashboard-template.md`
- `references/concept-lens-source-and-factuality.md`
- `references/concept-lens-paradigm-framework.md`
- `references/concept-lens-design-quality.md`
- `references/concept-lens-output-contract.md`

这些 warning 在本轮开始前已存在，且本轮禁止修改 `SKILL.md`，因此记录为非阻塞项，留给后续 trigger/context 治理阶段评估。

## 7. Evidence Limits and Next Gate

- 没有运行真实模型的 clean-context routing harness；paired eval 目前是可审计的预期行为资产，不是模型路由成功率报告。
- 没有验证 Codex、Claude Code 或其他运行时的实际选择结果。
- 没有修改或同步本地安装，因此本轮不会改变当前本地 Skill 使用行为。
- 发布后仍需等待 GitHub `Audit Skills` workflow 对已推送 commit 给出成功结果，才完成远端发布门禁。
