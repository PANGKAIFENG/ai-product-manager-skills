# Example: ui-wireframe-to-html

## Use When

You have a PRD or page requirement and want to confirm UI structure, state coverage, and layout before high-fidelity design.

## Prompt

```text
$ui-wireframe-to-html

基于下面这份 PRD，先输出 UI 结构、状态模型和 ASCII 布局。
当前只确认结构和状态，不要做高保真，也不要输出 component map。

页面范围：
- 桌面端 Agent 工作台首页
- 会话执行页
- 设置弹窗
- 错误/重试状态

PRD:
[paste PRD or path here]
```

## Expected Output Shape

- Reads the PRD and identifies page boundaries.
- Produces `screen-inventory.md` or an equivalent section.
- Produces `state-model.md` or an equivalent section.
- Produces `ascii-layout.md` with desktop regions and state variants.
- Creates low-fidelity HTML only if requested.
- Lists structure assumptions and questions before high-fidelity design.
- Recommends `ui-mockup-desktop-workbench` when the structure is ready for high-fidelity handoff.

## Good Follow-Up

```text
结构确认了，继续用 ui-mockup-desktop-workbench 做高保真 visual handoff，并输出 component map。
```
