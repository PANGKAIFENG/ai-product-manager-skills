# Skill Boundary And Loop Optimization Plan

审查日期：2026-06-11
输入来源：

- `docs/skill-boundary-and-loop-audit.md`
- `docs/skill-boundary-and-loop-audit.codex-draft.md`
- 当前仓库 README / Registry / Routing / Skill 文件抽查

## 1. 背景

当前仓库已经从单纯的 flat Skill Library 演进成 AI PM workflow library：

- 根目录保留 8 个 public Skill。
- `README.md` 是人类入口。
- `SKILL_REGISTRY.md` 是 catalog/status 边界。
- `SKILL_ROUTING.md` 是相邻 Skill 分流面。
- 3 个 Loop Extension contract 仍位于各 parent Skill 的 `references/` 下。

本轮不建议大规模重构。目标是修正几个真实路由歧义，并为后续多 Skill Loop 编排建立薄层，而不是重写所有 `SKILL.md`。

## 2. 总体判断

### 不存在 P0 阻断

README / Registry / Routing 已经基本一致，8 个 public Skill 可用。当前没有必须立刻阻断发布的结构性问题。

### P1 是边界修补

真正影响日常路由的是：

- `ai-collaboration-calibration` 与 `grill-me` 对“挑战假设 / 方案哪里错了”的触发重叠。
- `prd-review` 与 `grill-me` 对“挑毛病 / 找失败模式”的层次边界未成文。
- `research-topic-compiler` 的 Product Candidate Research mode 与 `decision-research` 的具体决策职责重叠。
- `.github/ISSUE_TEMPLATE/skill_request.md` 仍有旧研究 Skill 名残留。

### Loop Pattern 应先做一个

`loop-patterns/` 值得新增，但第一步只做 PRD Readiness Loop。它是材料最齐、用户路径最主干的多 Skill 闭环。Decision Research Loop 和 Research Radar Loop 后置。

### Router / Gate 后置

`ai-work-assetization-diagnoser` 有价值，但必须在 P1 边界稳定后再做。否则 Router 会把当前歧义固化为新的 public entry。

## 3. Scope

### In Scope

- 修复对外可见命名残留。
- 补充相邻 Skill 的双向边界和转出规则。
- 收敛研究类 Product Candidate ownership。
- 新增第一个多 Skill loop pattern 文档。
- 后续补薄编排入口和资产化 Router 草案。
- 将所有改动拆成可独立验收的 issue draft。

### Out Of Scope

- 不移动根目录 Skill。
- 不把根目录迁移到 `skills/` 子目录。
- 不删除或合并现有 Skill。
- 不重写所有 `SKILL.md`。
- 不把现有 3 个 loop contract 从 `references/` 迁走。
- 不让 `grill-me` 持有 loop state。
- 不把 `SKILL_ROUTING.md` 改造成自动路由器。

## 4. Delivery Phases

### Phase 1 - Boundary Patch Pack

目标：让相邻 Skill 的触发边界在文档层稳定。

Issues:

- [001 Fix skill request template old name](issues/001-fix-skill-request-template-old-name.md)
- [002 Add calibration and grill-me boundary handoff](issues/002-calibration-grill-routing-boundary.md)
- [003 Add prd-review and grill-me boundary handoff](issues/003-prd-review-grill-routing-boundary.md)
- [004 Clarify Product Candidate ownership](issues/004-research-product-decision-ownership.md)

Phase exit:

- 歧义触发词可以通过 `SKILL_ROUTING.md` 得到唯一优先路由。
- `research-topic-compiler` 不再输出单次最终决策 ownership。
- `decision-research` 明确拥有具体决策的最终推荐。

### Phase 2 - First Multi-Skill Loop

目标：新增薄版 PRD Readiness Loop Pattern，编排已有 Skill，而不是替代 parent Skill contract。

Issues:

- [005 Add PRD Readiness loop pattern](issues/005-prd-readiness-loop-pattern.md)
- [006 Add prd-architect upstream and revision contract](issues/006-prd-architect-upstream-and-revision-contract.md)

Phase exit:

- `loop-patterns/prd-readiness-loop.md` 存在。
- 它引用现有 `prd-review/references/prd-readiness-loop-contract.md`，但不迁移原 contract。
- 它定义 calibration / grill-me / decision-research / prd-architect / prd-review 的节点顺序、进入退出条件、回边和停止条件。

### Phase 3 - Orchestration Skeleton

目标：补仓库级薄编排入口和更清晰的 routing 判断。

Issues:

- [007 Promote cross-skill comparison into routing](issues/007-routing-cross-skill-comparison.md)
- [008 Add Decision Research loop pattern](issues/008-decision-research-loop-pattern.md)
- [009 Add AGENTS thin orchestration index](issues/009-agents-thin-orchestration-index.md)

Phase exit:

- `SKILL_ROUTING.md` 能回答“现在该用哪个 Skill / 哪个 Loop”。
- `AGENTS.md` 只是索引，不承载厚规范。
- Decision Research Loop 有可选 Critic 检查点，但不强制所有调研都走 grill-me。

### Phase 4 - Router / Gate

目标：新增 public-safe 的资产化分层诊断能力。

Issues:

- [010 Add ai-work-assetization-diagnoser](issues/010-ai-work-assetization-diagnoser.md)

Phase exit:

- 能判断一次工作应该沉淀为 Prompt / Context Pack / Workflow / Skill / Loop / System。
- 能判断“不值得沉淀”。
- 不替代任何具体 Skill 执行。

### Phase 5 - Long Tail Cleanup

目标：降低大 Skill 认知负担，并处理 UI mockup 长尾边界。

Issues:

- [011 Slim research-topic-compiler mode surface](issues/011-research-topic-compiler-mode-slimdown.md)
- [012 Clarify UI mockup PRD boundary and feedback loop](issues/012-ui-mockup-prd-boundary-and-loop-feedback.md)

Phase exit:

- `research-topic-compiler/SKILL.md` 主体保留模式路由，厚内容下沉 references。
- `prd-architect` 与 `ui-mockup-desktop-workbench` 的 mockup 职责分界成文。
- mockup 发现 PRD 缺口时有回到 `prd-review` 的建议路径。

## 5. Dependency Order

```text
001
  -> 002
  -> 003
  -> 004
  -> 005
       -> 006
  -> 007
       -> 008
       -> 009
  -> 010
  -> 011
  -> 012
```

Notes:

- `001` 可随时做，是低风险修复。
- `002` 和 `003` 应先于 `005`，否则 PRD loop pattern 会引用尚未稳定的 Critic 边界。
- `004` 应先于 `008`，否则 Decision Research Loop 的 ownership 会含糊。
- `010` 必须后置到 routing 边界稳定之后。

## 6. Verification Strategy

### Static Checks

- 旧研究 Skill 名不再出现在 public template、README、Registry 或 Routing 中。
- `find . -maxdepth 2 -name SKILL.md` 仍返回 8 个 public Skill。
- `find . -maxdepth 2 -type d -name loop-patterns` 仅在 Phase 2 后出现。
- Existing parent loop contracts 保留：
  - `decision-research/references/decision-loop-contract.md`
  - `research-topic-compiler/references/research-radar-loop-contract.md`
  - `prd-review/references/prd-readiness-loop-contract.md`

### Routing Smoke Tests

每轮边界改动后，用以下 prompt 做路由演练：

- `帮我想想这个方案。`
- `压力测试一下这个设计，我感觉哪里不对劲。`
- `挑战我这个方案的假设。`
- `帮我挑挑这个 PRD 的毛病。`
- `这个 PRD 背后的产品方案能不能成？`
- `帮我对比 Electron vs Tauri vs Flutter Desktop，选一个做桌面端。`
- `系统研究一下桌面端技术栈演进，沉淀成长期研究项目。`

### Definition Of Done

整个优化计划完成时应满足：

- 所有 P1 issue 已完成并通过 routing smoke tests。
- `loop-patterns/prd-readiness-loop.md` 存在且能引用现有 loop contract。
- README / Registry / Routing 的职责没有混淆。
- 新增 public Skill 时仍遵守 catalog 同步规则。
- 没有创建未经确认的 GitHub issue。

## 7. Issue Index

| # | Title | Priority | Type | File |
|---|---|---|---|---|
| 001 | Fix skill request template old name | P1 | AFK | `docs/issues/001-fix-skill-request-template-old-name.md` |
| 002 | Add calibration and grill-me boundary handoff | P1 | HITL | `docs/issues/002-calibration-grill-routing-boundary.md` |
| 003 | Add prd-review and grill-me boundary handoff | P1 | HITL | `docs/issues/003-prd-review-grill-routing-boundary.md` |
| 004 | Clarify Product Candidate ownership | P1 | HITL | `docs/issues/004-research-product-decision-ownership.md` |
| 005 | Add PRD Readiness loop pattern | P1 | HITL | `docs/issues/005-prd-readiness-loop-pattern.md` |
| 006 | Add prd-architect upstream and revision contract | P2 | AFK | `docs/issues/006-prd-architect-upstream-and-revision-contract.md` |
| 007 | Promote cross-skill comparison into routing | P2 | AFK | `docs/issues/007-routing-cross-skill-comparison.md` |
| 008 | Add Decision Research loop pattern | P2 | HITL | `docs/issues/008-decision-research-loop-pattern.md` |
| 009 | Add AGENTS thin orchestration index | P2 | HITL | `docs/issues/009-agents-thin-orchestration-index.md` |
| 010 | Add ai-work-assetization-diagnoser | P2 | HITL | `docs/issues/010-ai-work-assetization-diagnoser.md` |
| 011 | Slim research-topic-compiler mode surface | P2 | HITL | `docs/issues/011-research-topic-compiler-mode-slimdown.md` |
| 012 | Clarify UI mockup PRD boundary and feedback loop | P3 | AFK | `docs/issues/012-ui-mockup-prd-boundary-and-loop-feedback.md` |
