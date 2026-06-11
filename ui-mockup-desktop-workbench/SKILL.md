---
name: ui-mockup-desktop-workbench
description: >
  桌面工作台 UI mockup：当用户已有 PRD、桌面端 Agent 工作台需求、UI 规范、参考竞品或页面状态清单，
  需要基于这些约束输出可落地的真实桌面页面 HTML/CSS/React mockup、截图和状态说明时使用。适合左侧菜单、
  任务列表、中间执行区、右侧产物/工作区面板、设置页、产物页、Agent 运行态和桌面应用级布局。
---

# ui-mockup-desktop-workbench

## 中文速查

- 中文名：桌面工作台 UI Mockup 生成器
- 英文稳定名：`ui-mockup-desktop-workbench`
- 分类：产品与 PRD
- 你可以这样叫我：`基于 PRD 和 UI 规范出桌面端 mockup`、`生成桌面工作台真实页面`、`把这个 Agent Client PRD 做成 HTML mockup`
- 适合：把 PRD、UI 规范、参考竞品和状态清单转成可运行、可截图、可交给研发讨论的桌面端真实页面 mockup。
- 不适合：问题还没定义清楚；只需要 PRD 文案；只做移动端或营销页；要直接进入生产代码实现。

## Overview

Use this Skill when the goal is not a loose wireframe, but a realistic desktop workbench mockup that product, design, and engineering can inspect together.

The workflow combines:

1. `ui-wireframe-to-html` discipline: structure and state before polish.
2. Desktop Agent workbench patterns: navigation, task list, execution canvas, artifact/workspace panel, settings, and result surfaces.
3. User-provided UI specifications: tokens, layout rules, component style, copy tone, and interaction constraints override generic design instincts.
4. Frontend design quality: dense but readable desktop UI, realistic data, stable dimensions, no decorative one-note visual filler.

## PRD Boundary

This Skill is downstream of PRD maturity:

- If the user still needs to define the product goal, scope, workflow, states, or acceptance criteria, hand off to `prd-architect`.
- If a PRD exists but has conflicts, missing acceptance criteria, unclear states, or untestable flows, hand off to `prd-review` before producing the formal mockup.
- If the PRD and UI spec are clear enough, use this Skill to create the desktop mockup artifact.
- If the mockup process exposes PRD gaps, stop and record a PRD feedback note instead of silently inventing requirements.

`prd-architect` may include lightweight UI references, screenshots, or mockup notes inside a PRD. Formal multi-state desktop HTML mockups belong here.

## Context Intake

Before generating UI, collect or discover:

- PRD path or pasted PRD content.
- UI specification path or pasted style rules.
- Target page set: workbench, task list, execution session, artifact page, settings page, empty state, error state, or all of them.
- Runtime/product context: desktop app, browser shell, Electron/Tauri/native wrapper, logged-in assumptions, target viewport.
- Existing app conventions, component library, screenshots, or competitor references if provided.
- Output destination and expected format: standalone HTML, React route, static artifact folder, screenshot, or design handoff markdown.

Minimum input maturity:

- product goal and target user are known
- page or screen set is known
- primary workflow and key states are known
- non-goals or out-of-scope states are known
- acceptance or review criteria are known enough to judge the mockup

If these are missing, route back to `prd-architect` or `prd-review` depending on whether the PRD must be created or reviewed.

Ask at most three questions only when missing information changes the page set, design constraints, or output format. If the user supplied PRD and UI spec paths, read them and proceed with explicit assumptions.

## Workflow

1. **Read authoritative inputs**
   - Read the PRD before designing screens.
   - Read the UI specification before choosing colors, typography, spacing, density, or component styling.
   - If both conflict, preserve product requirements from the PRD and visual constraints from the UI spec; call out unresolved conflicts.
   - If conflicts block screen/state decisions, create a PRD feedback note and recommend `prd-review`.

2. **Extract a screen contract**
   - Identify primary user roles, core jobs, navigation model, data objects, and page hierarchy.
   - List required screens and states, including empty, loading, streaming/running, success, partial failure, error, permission/login, and recovery.
   - Map each screen to PRD sections and UI spec constraints.

3. **Draft structure before visual styling**
   - Produce a compact layout plan or ASCII map for the desktop viewport.
   - For Agent workbenches, default to a four-zone shell when suitable:
     - left navigation and account/workspace switcher
     - task/session list or recent work rail
     - central execution/conversation/work canvas
     - right artifact, resource, preview, inspector, or settings panel
   - Do not invent large marketing heroes, decorative cards, or mobile-first stacks for dense desktop tools.

4. **Design realistic page states**
   - Use real product nouns from the PRD.
   - Fill tables, task cards, logs, artifact panels, and settings with plausible domain data.
   - Include the state transitions a PM or engineer needs to judge: first-run empty, active execution, completed output, error/retry, and settings or artifact management.

5. **Implement the mockup**
   - Prefer the user's requested format. If not specified, create a standalone HTML/CSS mockup that opens locally without a build step.
   - Use existing project stack only when the user asks to integrate into a repo route.
   - Keep dimensions stable with explicit desktop layout constraints, fixed rails, responsive min/max widths, and scrollable panels.
   - Use icons from the existing project icon library when available. For standalone HTML, use text labels or simple CSS shapes rather than importing a new dependency.

6. **Verify visually**
   - Open or render the mockup when tools are available.
   - Check at least one desktop viewport around 1440x900 and one narrower desktop viewport around 1280x800.
   - Verify text does not overflow buttons, cards, rails, tabs, or panels.
   - Verify the UI is not blank, overlapped, or dominated by a single decorative color family.

7. **Package the result**
   - Provide file paths, local open/run instructions, screenshots if generated, and a short handoff note.
   - Include a traceability table from PRD requirement to screen/state.
   - Include known assumptions and any PRD/UI-spec conflicts.
   - Include any PRD feedback discovered while building the mockup, with recommended next route: `prd-review` for conflict/readiness issues, `prd-architect` for missing PRD sections.

## Desktop Workbench Rules

Read `references/desktop-workbench-ui-principles.md` before designing a desktop Agent workbench shell, multi-panel workspace, settings page, artifact page, or task execution UI.

Key defaults:

- Dense operational UI beats landing-page composition.
- User attention should flow from navigation/context to task list to execution canvas to artifact panel.
- Running, queued, failed, and completed task states must be visually distinct.
- Settings pages should feel like system controls, not content cards.
- Artifact pages should prioritize inspection, versioning, actions, and provenance.

## Output Contract

Read `references/mockup-output-contract.md` before finalizing deliverables.

Default deliverables:

- `README.md` or handoff note with purpose, assumptions, and open/run instructions.
- `screen-contract.md` or equivalent section describing screens, states, and PRD traceability.
- `mockup.html` or project-native page/component.
- Screenshot or browser verification notes when feasible.

## Side Effects And Safety

- Do not overwrite existing product routes or design files unless the user explicitly asks for repo integration.
- Do not push, publish, or commit unless explicitly requested.
- Do not fetch paid/private competitor assets unless credentials and permission are clear.
- Do not treat a mockup as production implementation; mark integration work separately.
- Do not invent missing product requirements to make a page look complete; surface them as PRD feedback.
- Keep generated data fictional unless the user supplied safe real examples.

## Definition Of Done

The Skill run is complete when:

- PRD and UI spec constraints have been read or explicitly marked unavailable.
- Screens and states are mapped before visual implementation.
- The mockup is runnable or openable from a local path.
- Desktop layout, state coverage, and visual quality have been checked.
- The final response includes changed/created files, verification result, assumptions, and remaining decisions for production implementation.

## Evaluation

Smoke prompts:

- `基于 /path/to/prd.md 和 /path/to/ui-spec.md 输出桌面端 Agent Client 真实页面 mockup。`
- `把这个桌面工作台 PRD 做成 HTML mockup，包含左侧菜单、任务列表、执行区和右侧产物面板。`
- `按这份 UI 规范做一个设置页和产物页 mockup，给我可打开的 HTML。`

Non-trigger prompts:

- `帮我写一份 PRD。`
- `只审一下这个 PRD 有没有问题。`
- `做一个手机端 landing page。`
- `直接实现生产功能并补测试。`

Capability checks:

- The output names the PRD and UI spec used.
- The mockup includes at least one active execution state and one non-happy-path state when relevant.
- The desktop layout remains coherent at 1440x900 and 1280x800.
- Catalog or project files outside the requested mockup scope are untouched.

## Catalog Notes

- Category: `product-prd`
- Chinese name: 桌面工作台 UI Mockup 生成器
- Status: `active`
- Provenance: new team Skill created locally for the AI Product Manager Skills Library; no upstream import source.
