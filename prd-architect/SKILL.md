---
name: prd-architect
description: >
  PRD 架构师 / 需求文档起草：当用户要把一个产品想法、需求草稿、脑暴结果或功能说明整理成 PRD 时使用。
  可用中文唤起：“帮我写 PRD”“帮我选 PRD 模板”“把这个需求整理成 PRD”“判断该用轻量 PRD 还是标准 PRD”
  “补一张可编辑 Draw.io 核心流程图”“PRD 里加架构图”。
  会在 PRD-lite、PRD-standard、PRD-ai-native 中选择一个模板资产按需加载，并在需要时加载 mockup handoff、
  Draw.io 图示或开发 handoff 附录；页面型 PRD 默认联动生成项目 UI 对齐的 HTML、关键截图和正文证据。
  不用于直接编码、单纯画 UI，或评审一份已经写好的 PRD。
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
3. 只加载本轮需要的附加资产；页面型 PRD 自动激活 mockup handoff 和 UI 证据链。
4. 写出与当前阶段一致的 PRD，并区分本地草稿内容和可发布正文。
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
7. 当 PRD 包含用户可见界面时，编排 `ui-mockup-desktop-workbench`，在同一交付中完成 HTML、关键截图和正文回填。

它不负责：

- 直接决定 UI 视觉细节。
- 把 standalone HTML 当成生产代码；正式视觉实现由 `ui-mockup-desktop-workbench` 负责，但本 Skill 负责触发、收口和验收这条交付链。
- 直接开始编码。
- 把核心规则外包给单独 guide 再让用户自己跳转理解。
- 在用户只要“初版 PRD”时展开接口字段、TypeScript、JSON schema、adapter 或 metadata 结构。

## Workflow

### 1. Intake

先从用户输入和可发现项目上下文提炼：

- 需求描述、目标用户、当前问题、成功标准。
- 已知边界、非目标、待确认点。
- 是否涉及既有界面、截图、HTML mockup 或正式 UI mockup。
- 已有页面资产属于现状参考、与本期目标一致的目标稿，还是已经过期/结构不匹配的旧原型。
- 是否涉及 AI 协作、模型生成、推荐、记忆、人工确认或人工接管。
- 是否明确要求开发 handoff、接口字段、协议 schema 或实现计划。
- 是否会发布到钉钉或其他在线文档；若会发布，默认按“发布版正文”组织，不把本地路径当成正文信息。

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
| `references/mockup-handoff.md` | PRD 涉及任何用户可见页面、弹窗、面板、按钮、表单或状态提示；即使用户没有单独要求 HTML 也要加载 |
| `references/drawio-templates.md` | 用户要求可编辑流程图 / 架构图，或 Standard / AI-native 存在多阶段链路、上下游依赖、状态流转 |
| `references/handoff-appendix.md` | 用户明确要求开发 handoff、字段定义、协议、接口、adapter、metadata 或实现计划前置材料 |
| `references/prd-shape-gates.md` | 需要自检 PRD 是否过重、过技术化、章节误激活或待确认项处理不当 |

### 3A. Detect UI-bearing PRDs

只要本期定义了用户可见的页面、弹窗、抽屉、表单、卡片、导航、按钮、空态、错误态、确认态或成功态，就把它判定为页面型 PRD。页面型 PRD 的默认交付不是单一 Markdown，而是：

`PRD + 项目 UI 对齐 HTML/preview + 关键状态截图 + PRD 对应章节内嵌截图`

执行规则：

1. 用户不需要再次说“生成 HTML”或“补截图”；页面型判断本身就是触发条件。
2. 先定位真实项目、app/路由、组件、样式 token、图标和相邻页面状态，再调用 `ui-mockup-desktop-workbench`。
3. 默认选择 `visual-handoff`，在 PRD 产物目录生成独立 HTML，不修改生产前端；只有用户明确要求项目内 preview 或真实实现承接时才选择 `project-native-preview`。
4. 讨论中 PRD 可以生成“目标态草稿” HTML，但必须把未决内容标成假设；只有阻断性的页面信息架构或状态决策未关闭时才跳过。
5. 至少截取每个实质变化页面的默认态；PRD 明确定义的关键拦截、失败、确认或成功态按验收需要补图。
6. 截图直接插入它解释的功能或状态章节，不在文末集中堆放。
7. standalone HTML 必须明确标记为视觉交付参考，不得声称它是生产代码。
8. 只有用户明确要求纯文本、需求完全无界面、阻断性页面决策未关闭、或真实项目不可访问且无法形成有证据的静态复刻时可以跳过。最终说明要写清原因、受影响页面和待补动作。

### 4. Write PRD

输出必须做到：

1. 开头用一句话写清“本期只解决什么”。
2. 结构与问题规模匹配。
3. 明确事实、假设、待确认项和非目标。
4. 每个章节回答一个新问题；重复章节要合并或删除。
5. 如果涉及既有前端页面，先定位真实项目、真实路由和真实组件，再写页面稿。
6. 如果只是产品初版，不在正文写 TypeScript interface、JSON schema、endpoint、adapter、metadata 或 capability 字段。
7. 如果用户明确要求 handoff，把字段和协议放到“开发 handoff 附录”，不要污染产品主链路。
8. 页面型 PRD 无论是否已有 HTML/mock，都要在本轮完成目标态 HTML、关键状态截图和正文回填。已有旧原型与新 PRD 不一致时先更新原型，不把旧截图冒充目标稿。
9. 若用户准备把 PRD 发到钉钉，正文默认不输出“关联产物”聚合区和“待确认事项”章节；待确认项只保留在本地草稿、最终说明或明确标注的发布前检查清单中。

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
- 截图应该插入哪个 PRD 功能模块；同一 mock 可以复用，但不要在底部“关联产物”集中堆图。

页面型 PRD 执行页面证据门禁：

1. 先判断原型与本期 PRD 的页面、模块和状态是否一致。
2. 没有目标态原型时，调用 `ui-mockup-desktop-workbench` 新建；已有且一致时实际打开或渲染。至少截取每个实质变化页面的默认态，关键失败态、空态、确认态或成功态按需补图。
3. 将每张截图直接嵌入它解释的功能/页面/状态章节，图片下说明状态和验证重点。本地附录里的 HTML/PNG 路径不能替代正文截图。
4. 仅代表现状的截图要标注“现状参考”；与本期结构不一致的旧原型要先更新，或转 `ui-wireframe-to-html` / `ui-mockup-desktop-workbench`，不能作为目标态证据。
5. 只有 3A 节规定的跳过条件成立时可以跳过；原型不可运行时先尝试安全修复或重新生成，不把“当前没有 HTML”当作跳过理由。

### 7. Publish-ready PRD Mode

当用户明确提到“上传钉钉 / 发到钉钉文档 / 发布给开发看 / 线上 PRD”时，把 PRD 当作发布版写：

1. 文档信息表只放功能名、状态、模块、版本等可读信息，不放本地 mock URL、`.html`、`.png` 或 `dingtalk-assets` 路径。
2. 页面或 mock 截图应嵌入对应章节，例如输入框状态放在输入框章节、任务卡状态放在任务卡章节、取消逻辑放在取消章节。
3. “待确认事项”默认不进入发布版正文；确需保留时，改写成“发布前仍需确认”，并在最终说明中提示不要直接上传。
4. “关联产物”默认不作为发布版正文模块；本地草稿可以保留，但要标记为 `本地草稿，不上传钉钉正文`。
5. 如果 PRD 后续交给 `dingtalk-prd-publisher`，最终说明提醒它需要做钉钉回读和浏览器可见性验证。

### 8. Self-check

如果本轮把 PRD 写入 Markdown 文件，尽量运行：

```bash
python3 scripts/check_prd_shape.py <prd.md> --type <lite|standard|ai-native>
```

当用户明确要求开发 handoff 时增加：

```bash
python3 scripts/check_prd_shape.py <prd.md> --type <lite|standard|ai-native> --allow-handoff
```

当用户说明 PRD 要上传钉钉或发布到在线文档时增加：

```bash
python3 scripts/check_prd_shape.py <prd.md> --type <lite|standard|ai-native> --publish-ready
```

当已有与目标 PRD 一致的 HTML/mock，或用户明确要求“截图放入对应模块”时增加：

```bash
python3 scripts/check_prd_shape.py <prd.md> --type <lite|standard|ai-native> --require-mockup-evidence
```

页面型 PRD 还必须把本轮生成的 HTML 作为独立产物传给检查器：

```bash
python3 scripts/check_prd_shape.py <prd.md> --type <lite|standard|ai-native> \
  --require-mockup-evidence --require-mockup-artifact <mockup.html>
```

该门禁会检查功能正文中是否有图片证据，并验证本地图片引用是否真实存在；只放在“本地草稿附录/关联产物”中的图片不算完成。发布版应先完成本地证据检查，再由发布流程上传或重写图片引用。

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
- 页面型 PRD 已在同一交付中生成项目 UI 对齐的 HTML/preview，关键状态已实际截图并嵌入对应功能章节；旧原型不匹配时已更新或明确停止使用。
- 无截图只允许发生在明确的跳过条件下，且原因和待补状态已说明；HTML 路径或截图计划本身不算页面证据。
- 涉及发布到钉钉或在线文档时，本地 mock 链接、截图路径、关联产物和待确认项没有污染发布版正文。
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
- `这份 PRD 后面要上传钉钉，mock 截图直接放到对应模块里。`，应启用发布版正文规则，不输出本地 mock 链接、关联产物聚合区或待确认事项正文。
- `基于已有 HTML mockup 起草多页面 PRD，并把关键页面截图放到对应功能章节。`，应先校验原型与目标结构是否一致；一致则实际生成截图并内嵌，不一致则更新原型或明确停止把旧原型当目标稿。
- `基于真实项目写一个新增审批抽屉的 PRD。`，即使用户没有说 HTML，也应在同一交付中生成 UI 对齐 HTML、关键状态截图并回填对应章节。
- `写一个完全没有用户界面的 API 限流策略 PRD。`，不应生成 HTML 或截图。

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
