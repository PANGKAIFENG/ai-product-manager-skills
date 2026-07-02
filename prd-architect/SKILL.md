---
name: prd-architect
description: >
  PRD 架构师 / 需求文档起草：当用户要把一个产品想法、需求草稿、脑暴结果或功能说明整理成 PRD 时使用。
  可用中文唤起：“帮我写 PRD”“帮我选 PRD 模板”“把这个需求整理成 PRD”“判断该用轻量 PRD 还是标准 PRD”
  “补一张可编辑 Draw.io 核心流程图”“PRD 里加架构图”。
  会在 PRD-lite、PRD-standard、PRD-ai-native 中选择一个模板资产按需加载，并在需要时加载 mockup handoff、
  Draw.io 图示或开发 handoff 附录。不用于直接编码、单纯画 UI，或评审一份已经写好的 PRD。
---

# PRD 架构师（prd-architect）

## 中文速查

- 中文名：PRD 架构师 / 需求文档起草
- 英文稳定名：`prd-architect`
- 你可以这样叫我：`帮我写 PRD`、`帮我选 PRD 模板`、`把这个需求整理成 PRD`、`这个需求该用哪种 PRD`、`PRD 里补 Draw.io 流程图`
- 适合：需求还在成型，需要判断 PRD 类型、当前成熟度、模板资产和后续 UI / handoff 承接
- 不适合：已有完整 PRD 要评审时改用 `prd-review`；只要正式 UI mockup 时改用 `ui-mockup-desktop-workbench`；直接编码不触发

## Overview

这个 Skill 负责把产品想法组织成结构匹配的 PRD。它不是固定展开重型模板，而是：

1. 先判断上游输入是否足够成熟。
2. 再选择 `PRD-lite / PRD-standard / PRD-ai-native` 其中一个模板资产。
3. 只加载本轮需要的附加资产，例如 mockup handoff、Draw.io 图示或开发 handoff。
4. 写出与当前阶段一致的 PRD，并保留明确的待确认项。
5. 生成文件时尽量运行 PRD shape 自检，避免把初版 PRD 写成实现方案。

## Upstream Boundaries

不要把所有输入都直接写成 PRD。先判断上游是否已经成熟：

- 问题、用户、目标或判断标准还不清楚：先转 `ai-collaboration-calibration` 做问题校准。
- 问题已确认，但具体方案、架构、计划或产品决策需要压力测试：先转 `grill-me`。
- PRD 中存在重大产品、技术、商业或平台选择，且缺少证据：先转 `decision-research`。
- 已有 PRD/handoff 只是要判断能否交付开发：转 `prd-review`，由它给 readiness verdict。
- PRD 和 UI 规范都已确认，用户要正式桌面端多状态页面 mockup：转 `ui-mockup-desktop-workbench`。

`prd-architect` 可以根据上游输出起草或修订 PRD，但不自我批准 `Ready for writing-plans`。

## Responsibilities

这个 Skill 负责：

1. 判断需求复杂度和当前成熟度。
2. 判断是否属于 AI-native 需求。
3. 选择并加载一个 PRD 模板资产。
4. 按需加载 mockup、Draw.io 或 handoff 资产。
5. 组织 PRD 正文、待确认项和下一步建议。
6. 在生成到文件时运行可用的确定性检查。

它不负责：

- 直接决定 UI 视觉细节。
- 生成正式桌面端多状态页面 mockup；这由 `ui-mockup-desktop-workbench` 负责。
- 直接开始编码。
- 把核心规则外包给单独 guide 再让用户自己跳转理解。
- 在用户只要“初版 PRD”时展开接口字段、TypeScript、JSON schema、adapter 或 metadata 结构。

## Workflow

### 1. Intake

先从用户输入和可发现项目上下文提炼：

- 需求描述、目标用户、当前问题、成功标准。
- 已知边界、非目标、待确认点。
- 是否涉及既有界面、截图、HTML mockup 或正式 UI mockup。
- 是否涉及 AI 协作、模型生成、推荐、记忆、人工确认或人工接管。
- 是否明确要求开发 handoff、接口字段、协议 schema 或实现计划。

如果输入缺失，可以基于明确假设先出第一版；不要把缺失业务判断伪装成已确认事实。

### 2. Select Template Asset

读取 `references/template-selection.md`，选择且只选择一个模板：

- `references/templates/prd-lite.md`
- `references/templates/prd-standard.md`
- `references/templates/prd-ai-native.md`

不要同时加载三份模板来拼接章节。选中模板后，按模板内的“章节启用条件”和“禁止内容”写正文。

### 3. Activate Optional Assets

只在触发条件满足时加载附加资产：

| 资产 | 何时加载 |
| --- | --- |
| `references/mockup-handoff.md` | 涉及既有页面、弹窗、面板、按钮、表单、状态提示、HTML mockup 或截图承接 |
| `references/drawio-templates.md` | 用户要求可编辑流程图 / 架构图，或 Standard / AI-native 存在多阶段链路、上下游依赖、状态流转 |
| `references/handoff-appendix.md` | 用户明确要求开发 handoff、字段定义、协议、接口、adapter、metadata 或实现计划前置材料 |
| `references/prd-shape-gates.md` | 需要自检 PRD 是否过重、过技术化、章节误激活或待确认项处理不当 |

### 4. Write PRD

输出必须做到：

1. 开头用一句话写清“本期只解决什么”。
2. 结构与问题规模匹配。
3. 明确事实、假设、待确认项和非目标。
4. 每个章节回答一个新问题；重复章节要合并或删除。
5. 如果涉及既有前端页面，先定位真实项目、真实路由和真实组件，再写页面稿。
6. 如果只是产品初版，不在正文写 TypeScript interface、JSON schema、endpoint、adapter、metadata 或 capability 字段。
7. 如果用户明确要求 handoff，把字段和协议放到“开发 handoff 附录”，不要污染产品主链路。

### 5. Diagram Mode

当用户要求“写 PRD，并补流程图 / 架构图 / Draw.io 图示”时，本 Skill 直接负责 PRD 内正式图示能力。

执行规则：

1. 先判断图要回答的问题：系统是什么、链路怎么跑、还是人和 AI 如何协作。
2. 读取 `references/drawio-templates.md`，选择 `architecture` 或 `flow` 布局。
3. 生成可编辑 `.drawio` 源文件；如果 PRD 需要 Markdown 可预览，优先交付包含 Draw.io 数据的 `*.drawio.svg`。
4. 在 PRD 正文引用正式图示路径，并说明它支撑哪个章节。
5. 对 `.drawio` 源文件运行 `python3 scripts/validate_drawio.py <path>`。
6. 如果验证工具不可用，必须在 PRD 的关联产物或最终说明里标记“图示可编辑性未验证”。

### 6. Mockup Handoff

当需求发生在既有产品页面上，优先读取 `references/mockup-handoff.md`。PRD 中应写清：

- 页面范围、触发入口、关键状态、用户可见反馈。
- 需要截图、静态 HTML mockup、真实页面截图，还是转交正式 UI mockup。
- mockup 展示哪个状态：默认态、拦截态、确认态、失败态或成功态。

### 7. Self-check

如果本轮把 PRD 写入 Markdown 文件，尽量运行：

```bash
python3 scripts/check_prd_shape.py <prd.md> --type <lite|standard|ai-native>
```

当用户明确要求开发 handoff 时增加：

```bash
python3 scripts/check_prd_shape.py <prd.md> --type <lite|standard|ai-native> --allow-handoff
```

检查失败不等于不能交付，但最终说明必须解释哪些 warning 是故意保留的，哪些需要修订。

## Revision Input Contract

当用户提供 `prd-review` findings、revision draft、open blockers 或 readiness status 时，可以进入修订模式：

1. 先识别本轮 patch scope：只修 blocker、补验收、补异常、补图示，还是重组章节。
2. 把 review finding 分成事实缺口、表达缺口、验收缺口、图示缺口和待确认决策。
3. 只改能从输入中支撑的内容；缺失业务判断写成待确认项。
4. 输出最小可替换章节或段落，不默认重写整份 PRD。
5. 修订后建议回到 `prd-review` 做 readiness re-check；readiness verdict 不由本 Skill 给出。

## Downstream Handoff

只有 PRD 满足以下条件，才建议进入 superpowers `writing-plans`：

- 目标用户、问题、范围边界和非目标已经明确。
- 主流程、关键状态、输入输出、异常或人工接管点已经写清。
- 验收标准能被测试、人工检查或通过具体 artifact 验证。
- 阻断性待确认项已经关闭；若仍有假设，必须明确写成 implementation plan 的前置假设。

如果不满足这些条件，下一步应继续深化 PRD、补 handoff 或做 `prd-review`。

## Definition of Done

完成标准是：

- 已选定且只加载一个 PRD 类型模板。
- 当前状态明确，正文成熟度与状态一致。
- 待确认项和假设没有混在一起。
- mockup / 图示 / handoff 附加资产只在需要时启用。
- 如果本轮生成 Draw.io 图示，`.drawio` 已验证或验证限制已明确说明。
- 如果本轮写入 PRD 文件，已运行 `check_prd_shape.py` 或说明未运行原因。
- 下一步建议不会把草稿误推成定稿。

## Evaluation

Smoke prompts:

- 单点改动，是否只加载 `PRD-lite` 并保持 5 分钟可读。
- 常规跨状态功能，是否加载 `PRD-standard`，但不默认写 TS/JSON schema。
- AI 协作需求，是否加载 `PRD-ai-native` 并写清人工动作、AI 动作、状态反馈和闭环。
- `帮我写一个 PRD，并补一张可编辑 Draw.io 核心流程图。`
- `回答后下一步行动建议 PRD 初版`，应输出产品规则和 UX 行为，不输出实现 schema。

Non-trigger prompts:

- 直接让它改代码。
- 只让它画正式 UI mockup。
- 只做目录治理。
- 已有 PRD 要找问题，应转 `prd-review`。

Resources:

- `references/template-selection.md`
- `references/templates/prd-lite.md`
- `references/templates/prd-standard.md`
- `references/templates/prd-ai-native.md`
- `references/mockup-handoff.md`
- `references/drawio-templates.md`
- `references/handoff-appendix.md`
- `references/prd-shape-gates.md`
- `scripts/check_prd_shape.py`
- `scripts/validate_drawio.py`
