# AI Product Manager Skills 全量诊断报告

日期：2026-07-02
仓库：`PANGKAIFENG/ai-product-manager-skills`
审计基准：`origin/main` = `e7de560f553b0cf34dcc2c7865351ff7c313ca73`
评审模式：full / optimization-oriented audit

## 1. 这一轮 `prd-architect` 改动总结

本轮已经推到 GitHub 的提交是：

```text
bf4f92d refactor prd architect assets and shape checks
14 files changed, 1009 insertions(+), 346 deletions(-)
```

核心变化不是“加更多规则”，而是把原本混在 `SKILL.md` 里的骨架、模板、图示、mockup 和 handoff 规则资产化：

| 改动 | 文件 | 作用 |
| --- | --- | --- |
| `SKILL.md` 从大文档降为路由 / gate / workflow | `prd-architect/SKILL.md` | 保留触发、上游边界、模板选择、可选资产启用、自检和下游交接。 |
| PRD 类型选择独立成资产 | `prd-architect/references/template-selection.md` | 先判断 `PRD-lite / standard / ai-native`，再只加载一个模板。 |
| 三类 PRD 骨架拆成模板 | `prd-architect/references/templates/*.md` | 解决“既然能判断模板类型，为什么不按模板骨架写”的问题。 |
| mockup / handoff / shape gate 独立 | `references/mockup-handoff.md`、`handoff-appendix.md`、`prd-shape-gates.md` | 让 UI 承接、开发附录、PRD 形状检查按触发条件加载。 |
| Draw.io 能力显式纳入 PRD | `references/drawio-templates.md`、`scripts/validate_drawio.py` | PRD 起草阶段可生成可编辑流程图 / 架构图，并验证 `.drawio`。 |
| 产品初版过技术化加入确定性检查 | `scripts/check_prd_shape.py` | 检查 TypeScript / JSON schema / adapter / metadata 误入主文档等问题。 |
| `prd-review` 复用 PRD 形状检查 | `prd-review/references/prd-shape-gates.md`、`scripts/check_prd_shape.py`、`evals/evals.json` | 不把 `prd-review` 合并进 `prd-architect`，而是共享检查思路。 |

这轮形成的标准可以概括为：

1. `SKILL.md` 是触发契约、路由器和执行 gate，不是所有规则的收纳箱。
2. 模板 / 骨架 / 长规则进入 `references/`，并且只有被选中时读取。
3. 格式、结构、可编辑性、阶段混淆这类稳定问题进入 `scripts/` 做确定性检查。
4. 已知失败样例进入 `evals/`，用于之后回归。
5. 相邻 Skill 不随便合并；能共享的是检查资产、引用规范和 handoff contract。

## 2. 审计证据

本次检查了仓库中 13 个公开 Skill：

```text
ai-collaboration-calibration
ai-work-assetization-diagnoser
brainstorming
competitive-analysis
complex-exploration
decision-research
grill-me
prd-architect
prd-review
prd-to-issues
research-topic-compiler
ui-mockup-desktop-workbench
ui-wireframe-to-html
```

运行过的命令：

```bash
git -C /tmp/ai-product-manager-skills-read fetch --prune origin
git -C /tmp/ai-product-manager-skills-read status --short --branch
git -C /tmp/ai-product-manager-skills-read show --stat --oneline --decorate HEAD
python3 /Users/linctex/.config/skillshare/skills/skill-reviewer/scripts/check_skill.py <each-skill-dir>
wc -l */SKILL.md
find <skill-dir> -maxdepth 3 -type f
rg -n '~|/Users|\.honeycomb|TODO|FIXME|PLACEHOLDER|honeycomb|skillshare sync|Multica|\.claude|\.codex' .
```

确定性结果：

- 13 个 Skill 的 `SKILL.md` frontmatter / 基础结构均通过 `skill-reviewer/scripts/check_skill.py`。
- 这说明没有明显 YAML / 目录入口错误，但不代表触发边界、context budget、eval、脚本化检查已经达标。

## 3. 全局诊断

### P0

未发现 P0。当前公开仓库没有“Skill 无法加载 / 明显误触发到危险动作 / 结构损坏”的问题。

### P1. 大型 Skill 还没有完全进入“router + assets”形态

受影响 Skill：

- `decision-research`：`SKILL.md` 370 行。
- `research-topic-compiler`：`SKILL.md` 417 行，`references/` 25 个文件。
- `prd-review`：`SKILL.md` 440 行。

证据：

- `decision-research/SKILL.md:60-96` 放 R00 framing gate，`152-265` 放 R04-R10 执行和终止细则，`268-303` 放结论输出规则。
- `research-topic-compiler/SKILL.md:96-125` 放研究模式，`127-158` 放 Pre-Research Source Expansion，`178-206` 放普通和 Product Candidate workflow，`227-251` 放 Research Run Plan。
- `prd-review/SKILL.md:117-194` 放角色 lenses 和 severity rules，`195-249` 放 PRD-specific / diagram review，`250-315` 放输出要求和 readiness 判定。

影响：

- 每次触发都要加载大量不一定相关的规则。
- 维护时容易继续往主文档加规则，回到 `prd-architect` 改造前的问题。
- 模板和检查规则不容易单独 eval。

建议：

- 把这些 Skill 的 `SKILL.md` 控制在 180-260 行左右，只保留触发、边界、模式选择、关键 gate、资源索引和 Definition of Done。
- 对每个模式建立一层 references，例如：
  - `decision-research/references/modes/technical-selection.md`
  - `decision-research/references/modes/product-strategy.md`
  - `research-topic-compiler/references/modes/product-candidate.md`
  - `prd-review/references/review-lenses.md`
  - `prd-review/references/output-skeleton.md`
- 让 `SKILL.md` 写清“什么时候加载哪一个 reference”，不要同时加载所有深规则。

### P1. eval 资产不一致，很多 Skill 只有内联 smoke prompt

证据：

- 有独立 `evals/` 的 Skill：`ai-collaboration-calibration`、`prd-architect`、`prd-review`、`ui-mockup-desktop-workbench`、`ui-wireframe-to-html`。
- 没有独立 `evals/` 的 Skill：`ai-work-assetization-diagnoser`、`brainstorming`、`competitive-analysis`、`complex-exploration`、`decision-research`、`grill-me`、`prd-to-issues`、`research-topic-compiler`。
- 多数 Skill 只有 `SKILL.md` 内的 `Smoke prompts / Non-trigger prompts / Regression checks`，没有结构化 eval 文件。

影响：

- 后续优化无法判断行为是否退化。
- 相邻 Skill 的 routing 冲突只能靠人工记忆，不能形成回归集。
- 很难把“这次 prd-architect 的失败样例”扩展成仓库级质量门禁。

建议：

- 为每个 Skill 建立 `evals/evals.json`，最小字段：
  - `id`
  - `prompt`
  - `should_trigger`
  - `expected_route`
  - `expected_output`
  - `assertions`
  - `known_regression`
- 对高风险 Skill 增加 fixture / checker：
  - `decision-research`：检查 Research Map、竞争假设、反证、结论。
  - `prd-to-issues`：检查 coverage matrix、AFK/HITL、发布确认。
  - `research-topic-compiler`：检查 Research Run Plan、evidence matrix、Obsidian 写回边界。

### P1. 公开 Skill 内仍有本地路径和 Honeycomb 遗留引用

证据：

- `research-topic-compiler/SKILL.md` 写了本地分发路径：`/Users/linctex/.codex/skills`、`/Users/linctex/.claude/skills`、`Multica`、`skillshare sync`。
- `research-topic-compiler/SKILL.md:170-176` 明确写了本地 distribution targets 和 sync rule。
- `ui-wireframe-to-html/SKILL.md:141-147` 引用 `~/.honeycomb-agent/templates/UI-spec-template.md` 和 example。
- `prd-review/SKILL.md:211`、`326`、`379-392` 引用 `honeycomb diagram-guard`、`/propose-honeycomb-change`、`~/.honeycomb-agent/templates/PRD-*.md`、`.claude/hooks/diagram-guard.sh`。
- `research-topic-compiler/references/obsidian-output-contract.md` 包含个人 Obsidian 路径 `/Users/linctex/Documents/ClawVault/...`。

影响：

- 公开 GitHub Skill 对外使用时会出现不可访问路径。
- Runtime / distribution 规则和 Skill 执行规则混在一起，影响可迁移性。
- 用户或其他 agent 可能把本地路径当成强依赖。

建议：

- 主文档只保留通用默认：`if local templates exist, prefer project-local override`。
- 将个人路径移入 `docs/local-distribution.md` 或 `references/local-runtime-notes.md`，并明确“仅维护者环境适用”。
- `prd-review` 不应默认建议 Honeycomb 命令；应优先引用本仓库内的 `scripts/validate_drawio.py` 和 `scripts/check_prd_shape.py`。

### P1. PRD 检查脚本在 `prd-architect` / `prd-review` 中重复

证据：

- `prd-architect/scripts/check_prd_shape.py` 与 `prd-review/scripts/check_prd_shape.py` 内容相同。
- `validate_drawio.py` 也在两个 Skill 下重复。

影响：

- 后续修一份脚本容易漏另一份，导致 reviewer 与 architect 的判断漂移。
- 如果公开分发时单个 Skill 被单独安装，重复也有合理性；但需要同步策略。

建议：

- 如果 Skill 以整个仓库分发：抽成 `shared/prd/scripts/`，两个 Skill 引用共享脚本。
- 如果 Skill 可能单独分发：保留副本，但新增仓库级维护脚本或 CI 检查，确保两份脚本 byte-identical。
- 在两个 Skill 的 `Resource Guide` 里标注脚本同步关系。

## 4. Skill-by-Skill 诊断

### 4.1 `prd-architect`

Verdict：Ready。

做得好的地方：

- 已按模板选择资产化，`SKILL.md` 明确“选择且只选择一个模板”。
- mockup、Draw.io、handoff、shape gate 都是按需加载。
- 已有 `scripts/check_prd_shape.py` 和 `scripts/validate_drawio.py`。
- 已有 `evals/evals.json` 覆盖本轮真实失败样例。

剩余建议：

| 优先级 | 建议 | 理由 |
| --- | --- | --- |
| P2 | 增加 non-trigger eval：已有 PRD review、纯 UI mockup、直接编码。 | 当前 `evals/evals.json` 更偏能力正例，缺少误触发回归。 |
| P2 | 给 `check_prd_shape.py` 增加“可配置 section 别名”。 | 现在必需章节靠中文字符串匹配，模板标题稍微变体就可能误报。 |
| P2 | 和 `prd-review` 约定脚本同步策略。 | 防止两个 Skill 对 PRD shape 的判断漂移。 |

### 4.2 `prd-review`

Verdict：Needs revision。

主要问题：

| 优先级 | 证据等级 | 问题 | 影响 | 建议 |
| --- | --- | --- | --- | --- |
| P1 | observed | `SKILL.md` 440 行，角色 lenses、severity、图示审查、输出骨架、readiness、相关模板全部在主文档。 | 每次 review 都加载大量规则；维护时容易继续加长。 | 拆 `references/review-lenses.md`、`severity-rules.md`、`diagram-review.md`、`output-contract.md`、`implementation-readiness.md`。 |
| P1 | observed | `SKILL.md:379-392` 仍引用 `~/.honeycomb-agent/templates/PRD-*.md`、`honeycomb diagram-guard`、`/propose-honeycomb-change`。 | 公开仓库对外不可用，且会把本地工具假设带给其他用户。 | 改成本仓库 references/scripts；本地 Honeycomb 只放维护者 notes。 |
| P1 | deterministic | `check_prd_shape.py` / `validate_drawio.py` 与 `prd-architect` 重复。 | 后续漂移风险。 | 抽共享脚本或加同步检查。 |
| P2 | observed | `evals/evals.json` 只有 2 条。 | 覆盖不足，特别是 readiness verdict、handoff/PRD 冲突、图示缺失、无 PRD 输入。 | 扩到 8-12 条，覆盖 PM/研发/测试、图示、过技术化、非触发。 |

建议重构骨架：

```text
prd-review/
  SKILL.md                         # 触发、边界、review order、resource guide
  references/
    review-lenses.md               # PM/研发/测试/可选视角
    severity-rules.md              # 阻断/重要/优化
    diagram-review.md              # drawio/svg/png/mermaid 检查
    output-contract.md             # report skeleton + revision draft
    implementation-plan-readiness.md
    prd-shape-gates.md
  scripts/
    check_prd_shape.py
    validate_drawio.py
  evals/evals.json
```

### 4.3 `decision-research`

Verdict：Needs revision。

主要问题：

| 优先级 | 证据等级 | 问题 | 影响 | 建议 |
| --- | --- | --- | --- | --- |
| P1 | observed | `SKILL.md:60-303` 把 R00-R11 细则、渠道表、Top-Down 模式、输出模板都放在主文档。 | `SKILL.md` 作为 router 不够薄；产品策略和技术选型会互相污染上下文。 | 主文档保留 R00/R01/R04/R08/R11 的摘要，其余移入 `references/modes/`。 |
| P1 | observed | 没有 `evals/` 结构化回归。 | 最容易和 `research-topic-compiler`、`competitive-analysis` 发生路由冲突，但没有可复测样例。 | 新增 `evals/evals.json`：技术选型、平台接入、产品定位、商业分层、候选池最终推荐、非触发。 |
| P2 | inferred | 没有确定性输出检查。 | 容易跳过 Research Map、竞争假设、反证或颠覆条件。 | 新增 `scripts/check_decision_report.py`，检查必备小标题和证据标签。 |

建议拆分：

```text
decision-research/references/
  modes/technical-selection.md
  modes/platform-integration.md
  modes/product-strategy.md
  modes/business-model.md
  templates/research-map.md
  templates/conclusion.md
```

### 4.4 `research-topic-compiler`

Verdict：Needs revision。

主要问题：

| 优先级 | 证据等级 | 问题 | 影响 | 建议 |
| --- | --- | --- | --- | --- |
| P1 | deterministic | `SKILL.md` 417 行，`references/` 25 个文件。 | 能力很强，但主入口过重；新模式容易继续堆进去。 | 像 `prd-architect` 一样建立 `mode-selection.md`，主文档只做模式选择和资源加载。 |
| P1 | observed | `SKILL.md:170-176` 包含维护者分发路径和 `skillshare sync` 规则。 | 公开 Skill 与本地分发治理混在一起。 | 移到 `docs/local-distribution.md` 或 maintainer notes。 |
| P1 | observed | 没有 `evals/`，只有 `scripts/validate_html_artifact.py` 针对 Concept Lens HTML。 | 研究计划、证据矩阵、Obsidian 输出、候选池 handoff 这些关键行为无回归检查。 | 新增 evals 覆盖 Research Goal Framing、Normal Research、Product Candidate、Radar Loop、非触发。 |
| P2 | inferred | 25 个 references 缺少目录化分组。 | 维护者难判断哪些是 mode、template、policy、channel、output。 | 拆为 `references/modes/`、`templates/`、`checks/`、`channels/`。 |

建议重构后的资源索引：

```text
references/
  mode-selection.md
  modes/normal-research.md
  modes/concept-lens.md
  modes/product-candidate.md
  modes/learning-pack.md
  modes/radar-loop.md
  output/obsidian-contract.md
  output/report-standards.md
  channels/channel-registry.md
  channels/channel-selection-rubric.md
```

### 4.5 `ui-mockup-desktop-workbench`

Verdict：Needs revision, but close to Ready。

做得好的地方：

- 已清楚区分 `project-native-preview`、`visual-handoff`、`concept-html`。
- 已吸收 `ui-wireframe-to-html` 的结构阶段纪律。
- 有 `evals/evals.json`，覆盖高保真、项目原生、视觉 handoff、非触发。

主要问题：

| 优先级 | 证据等级 | 问题 | 影响 | 建议 |
| --- | --- | --- | --- | --- |
| P1 | inferred | 高风险输出是 UI 文件和截图，但没有脚本检查 mockup 包。 | 容易生成缺 `screen-contract`、缺 `component-map`、HTML 未标 visual-only、截图未验证的交付。 | 新增 `scripts/check_mockup_package.py`，检查必备文件、HTML 标记、截图/验证 notes。 |
| P2 | observed | `SKILL.md:47-65` 放 Output Modes，`104-143` 放 Design Discovery / Wireframe Gate，`205-210` 放视觉验证，主文档仍承担较多 workflow。 | 可维护性尚可，但可以继续瘦身。 | 把 Output Modes、Design Discovery Gate、Wireframe Stage、Verification Gate 拆到 references。 |
| P2 | observed | `references/` 只有 2 个文件。 | mode contracts 和 package contract 还不够资产化。 | 增加 `references/output-modes.md`、`references/design-discovery-gate.md`、`references/verification-gate.md`。 |

### 4.6 `ui-wireframe-to-html`

Verdict：Needs revision。

主要问题：

| 优先级 | 证据等级 | 问题 | 影响 | 建议 |
| --- | --- | --- | --- | --- |
| P1 | observed | `SKILL.md:141-147` 引用 `~/.honeycomb-agent/templates/UI-spec-template.md` 和 example。 | 对外不可用；运行时可能读不到。 | 将 UI structure 模板复制/改写到本 Skill 的 `references/templates/`。 |
| P1 | observed | 没有 `references/`，但输出要求包括 screen inventory、state model、ASCII layout、mockup。 | 骨架没有资产化，之后会继续堆在主文档。 | 新增 `references/templates/screen-inventory.md`、`state-model.md`、`ascii-layout.md`、`wireframe-handoff.md`。 |
| P2 | inferred | 没有低保真 HTML / package 检查脚本。 | 无法机械确认是否误做高保真、是否标记 non-production。 | 新增 `scripts/check_wireframe_package.py`。 |

### 4.7 `prd-to-issues`

Verdict：Ready with improvements。

做得好的地方：

- 默认 `draft-only`，发布 GitHub issue 前必须用户确认。
- `references/` 拆出了 readiness checklist、vertical slice rules、issue template、github publish。
- 对 AFK / HITL、coverage matrix、查重、发布副作用边界描述清楚。

建议：

| 优先级 | 建议 | 理由 |
| --- | --- | --- |
| P2 | 新增 `evals/evals.json`。 | 覆盖未确认 PRD、按前后端拆票、未确认直接发布、GitHub issue 输入等回归。 |
| P2 | 新增 `scripts/check_issue_plan.py`。 | 检查 issue plan 是否含 Type、Source、Acceptance、Verification、Blocked by、Open questions 和 Coverage Matrix。 |
| P2 | `agents/openai.yaml` 已有，建议补齐没有 agents metadata 的同级核心 Skill。 | 当前 agent metadata 不一致，影响产品化展示。 |

### 4.8 `competitive-analysis`

Verdict：Ready with improvements。

做得好的地方：

- 定位明确：竞品分析服务产品决策，不服务信息完整性。
- evidence-channel、browser-walkthrough、decision-brief 都已进入 references。
- 权限边界清楚，不默认登录、不绕过付费墙。

建议：

| 优先级 | 建议 | 理由 |
| --- | --- | --- |
| P2 | 新增 `evals/evals.json`。 | 竞品池 vs 决策简报、只剩最终选择 vs `decision-research`、登录态授权边界都需要回归。 |
| P2 | 新增 `scripts/check_decision_brief.py`。 | 检查是否包含 decision question、evidence base、copy/adapt/avoid、open risks、next validation。 |
| P2 | 与 `research-topic-compiler` 的 Product Candidate Research 建立 handoff 模板。 | 防止候选池研究与竞品决策简报之间重复产物。 |

### 4.9 `brainstorming`

Verdict：Ready with improvements。

做得好的地方：

- 边界清楚：问题未定义转 `ai-collaboration-calibration`，已有方案压测转 `grill-me`，正式 PRD 转 `prd-architect`。
- 已有 `references/design-spec-contract.md` 和 `references/visual-design-standards.md`。
- UI/mockup 前要求 Design Discovery Gate，符合本轮“不要通用化模板”的标准。

建议：

| 优先级 | 建议 | 理由 |
| --- | --- | --- |
| P2 | 新增 `evals/evals.json`。 | 覆盖轻量方案讨论、UI 视觉规范发现、转 PRD、转 mockup、非触发。 |
| P2 | 将 `Visual Companion` 的 gate 与 `visual-design-standards.md` 去重。 | 减少主文档和 reference 重复更新。 |
| P2 | 增加 `design-spec` 的最小 checker。 | 防止输出缺推荐方案、取舍、待确认、下游 handoff。 |

### 4.10 `complex-exploration`

Verdict：Needs revision, medium priority。

主要问题：

| 优先级 | 证据等级 | 问题 | 影响 | 建议 |
| --- | --- | --- | --- | --- |
| P1 | inferred | 边界覆盖复杂策略、Roadmap、定价、竞品定位、复杂 PRD 前置、复盘和资产沉淀，范围很宽。 | 容易和 `ai-collaboration-calibration`、`brainstorming`、`research-topic-compiler` 重叠。 | 增加 `references/mode-selection.md`，把 Quick / Deep / Review / Asset 的进入条件做成 gate。 |
| P2 | observed | 没有 `evals/`。 | 复杂探索最容易被误用为“更长回答”，需要回归。 | 新增 evals：Roadmap 不直接排期、定价不直接套餐、复盘不写流水账、简单任务不触发。 |
| P2 | observed | `agents/openai.yaml` 有，但 runtime 展示 metadata 不是所有核心 Skill 都有。 | 产品化入口不一致。 | 仓库级统一 agents metadata 策略。 |

### 4.11 `ai-collaboration-calibration`

Verdict：Ready with improvements。

做得好的地方：

- 已有 17 个 references 和 `evals/test-prompts.csv`。
- L1/L2/L3/L4-fuzzy/L4-framed 分层清楚。
- 对 `grill-me` 的边界写得清楚。

建议：

| 优先级 | 建议 | 理由 |
| --- | --- | --- |
| P2 | 把 CSV eval 转成仓库统一的 `evals/evals.json`。 | 方便和其他 Skill 使用同一格式回归。 |
| P2 | 增加一个 `scripts/check_calibration_response.py`。 | 现在 eval 规则是手工 Markdown，可检查“是否输出方案候选”“是否有假设/领域/层级”。 |
| P2 | `references/modes/` 12 个模式建议补 README/index。 | 防止维护者不知道哪些模式是常用、哪些是补充。 |

### 4.12 `ai-work-assetization-diagnoser`

Verdict：Needs revision, low-to-medium priority。

主要问题：

| 优先级 | 证据等级 | 问题 | 影响 | 建议 |
| --- | --- | --- | --- | --- |
| P1 | observed | 没有 `references/`、`scripts/`、`evals/`。 | 它本质是资产层级 gate，但层级判断、反例和输出样例都在主文档。 | 新增 `references/asset-layer-rubric.md`、`references/examples.md`、`evals/evals.json`。 |
| P2 | inferred | Output Contract 很好，但没有 checker。 | 容易输出多个推荐层级而不是一个 primary layer。 | 新增 `scripts/check_assetization_report.py`，检查 Recommended layer、Why not adjacent layers、Smallest next artifact、Reuse Signal。 |

### 4.13 `grill-me`

Verdict：Ready with minor improvements。

做得好的地方：

- `SKILL.md` 91 行，context budget 最好。
- 一问一答、每个问题附推荐答案、先查本地资料再问用户，边界清晰。

建议：

| 优先级 | 建议 | 理由 |
| --- | --- | --- |
| P2 | 增加 `evals/evals.json`。 | 覆盖方案压测、PRD artifact review 非触发、问题未定义转校准。 |
| P2 | 增加 `references/question-patterns.md`。 | 让“依赖、假设、分支、失败模式”的追问模式可复用，而不是只靠模型发挥。 |
| P2 | 给结束决策记录加更明确 skeleton。 | 方便复盘和交给 `brainstorming` / `prd-architect`。 |

## 5. 建议执行顺序

### 第一批：必须先做

1. `prd-review` 资产化改造：减少主文档体积，清理 Honeycomb / 本地路径，强化图示和 readiness 资产。
2. `research-topic-compiler` router 化：主文档降为 mode selector，移除本地分发治理内容。
3. `decision-research` mode 化：把技术选型、产品策略、商业模型、平台接入拆成按需加载 references。
4. 建立统一 `evals/evals.json` schema，并给所有核心 Skill 至少补 5 条 eval。

### 第二批：质量门禁

1. 给 `prd-to-issues`、`decision-research`、`competitive-analysis`、`ui-wireframe-to-html`、`ui-mockup-desktop-workbench` 增加输出 checker。
2. 解决 `prd-architect` / `prd-review` 重复脚本同步。
3. 建立仓库级 `scripts/audit_skills.py` 或 `make audit`：
   - 跑 `skill-reviewer/scripts/check_skill.py`
   - 检查 `SKILL.md` 行数
   - 检查本地路径 / Honeycomb 遗留引用
   - 检查每个 Skill 是否有 evals
   - 检查高风险 Skill 是否有 scripts

### 第三批：产品化一致性

1. 统一 `agents/openai.yaml` 策略。目前只有 `brainstorming`、`competitive-analysis`、`complex-exploration`、`prd-to-issues` 有。
2. 更新 `SKILL_REGISTRY.md` 和 `SKILL_ROUTING.md`，把新增 references/evals/scripts 的边界同步进去。
3. 对公开 README / quickstart 增加“如何选择 Skill + 如何验证 Skill”的短说明。

## 6. 推荐的最小改动计划

如果下一轮要直接动手，建议按小提交拆：

1. `docs: add unified skill audit and eval schema`
   - 新增本报告。
   - 新增 `docs/eval-schema.md`。

2. `refactor prd-review assets`
   - 拆 `prd-review` references。
   - 清理 Honeycomb / local path。
   - 扩充 evals。
   - 保持现有行为不变。

3. `refactor decision research modes`
   - 拆 mode references。
   - 补 evals 和 report checker。

4. `refactor research topic compiler router`
   - 建 `mode-selection.md`。
   - 分组 references。
   - 把本地分发说明移出 `SKILL.md`。

5. `add evals and output checkers for remaining skills`
   - `prd-to-issues`
   - `competitive-analysis`
   - `brainstorming`
   - `complex-exploration`
   - `ai-work-assetization-diagnoser`
   - `grill-me`
   - UI 两个 Skill

## 7. 总结判断

当前仓库已经不是“散乱 prompt 集合”，而是一个有清晰 AI PM 工作流的 Skill catalog。最大问题不在结构能不能加载，而在高价值 Skill 的治理成熟度还不均匀：

- `prd-architect` 已经完成了本轮标准化改造，可作为样板。
- `competitive-analysis`、`brainstorming`、`prd-to-issues`、`grill-me` 已经接近 Ready，主要补 eval / checker。
- `prd-review`、`decision-research`、`research-topic-compiler` 是下一轮重点，因为它们最容易继续膨胀，也最影响主工作流质量。
- `ui-wireframe-to-html` 需要优先清理本地模板路径，并补齐自己的结构模板资产。
- 仓库级必须补统一 eval/checker 规范，否则每个 Skill 会继续各写各的 smoke prompt，无法形成长期质量门禁。
