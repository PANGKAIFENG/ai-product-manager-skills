# Example: ui-mockup-desktop-workbench

## Use When

You have a mature PRD, UI rules, or screen requirements and need a staged desktop workbench UI handoff: structure first, then high-fidelity visual handoff or project-native preview.

## Prompt

```text
$ui-mockup-desktop-workbench

基于下面这份 PRD、UI 规范和真实前端项目，生成一个桌面端 Agent 工作台高保真 UI handoff。

要求：
1. 先输出 screen inventory、state model 和 ASCII layout。
2. 结构确认后继续做高保真 visual handoff 或 project-native preview。
3. 页面需要包含左侧导航、任务列表、中间执行区、右侧产物面板。
4. 覆盖空状态、运行中、停止、完成和错误重试状态。
5. 输出 component map、implementation notes 和截图/验证说明。

PRD:
[paste PRD or path here]

UI 规范:
[paste UI spec or path here]

真实前端项目:
[paste frontend path here]
```

## Expected Output Shape

- Reads the PRD and UI specification before designing.
- Extracts wireframe-stage outputs before visual polish: screen inventory, state model, and ASCII layout.
- Uses a structure review gate before high fidelity, or explicitly carries assumptions forward.
- Extracts a screen contract with screens, states, and traceability.
- Creates a runnable/openable visual handoff or project-native preview.
- Includes component map and implementation notes for frontend implementation.
- Uses realistic operational data instead of decorative filler.
- Checks desktop layout at common workbench viewports.
- Calls out PRD gaps instead of silently inventing requirements.

## Good Follow-Up

```text
把 mockup 暴露出来的 PRD 缺口整理成一份给 prd-review 的修订清单。
```
