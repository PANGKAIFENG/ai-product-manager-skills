# Quickstart

This repository has one installable root: `skills/`. It contains 15 atomic
Skills. `loops/`, `workflows/`, and `tools/` are composition and side-effect
contracts, not extra Skill discovery roots.

## Clone And Audit

```bash
git clone https://github.com/PANGKAIFENG/ai-product-manager-skills.git
cd ai-product-manager-skills
python3 scripts/audit_skills.py .
```

## Common Entries

| Goal | Skill | Example |
| --- | --- | --- |
| Clarify a fuzzy problem | `ai-collaboration-calibration` | `$ai-collaboration-calibration 先帮我把问题说清楚` |
| Research a product topic | `research-topic-compiler` | `$research-topic-compiler 研究这个方向并输出证据与决策输入` |
| Choose between options | `decision-research` | `$decision-research 比较方案并给出有立场推荐` |
| Compare product solutions | `brainstorming` | `$brainstorming 先不要写 PRD，比较 2-3 个方案` |
| Pressure-test a solution | `grill-me` | `$grill-me 拷问这个方案，找最早失败点` |
| Draft a PRD package | `prd-architect` | `$prd-architect 输出包含 UI、HTML、截图证据约定的 PRD` |
| Build UI handoff | `ui-mockup-desktop-workbench` | `$ui-mockup-desktop-workbench 先出结构再做高保真 handoff` |
| Review delivery readiness | `prd-review` | `$prd-review 检查 PRD 是否可实现、可测试、可交付` |
| Split versions and issues | `prd-to-issues` | `$prd-to-issues 拆 V1/V2/V3 和研发事项，先 draft` |

按需 Skill 和完整边界见 [`SKILL_REGISTRY.md`](../SKILL_REGISTRY.md)。

## Typical Product Path

小需求可以直接走 `prd-architect -> ui-mockup-desktop-workbench -> prd-review`。
中需求增加 `grill-me`。大需求先走 `workflows/product-discovery`，在研究/决策和方案
收敛后再走 `workflows/product-delivery`。需要外部写入时才显式调用对应
`tools/` publisher，并在当前 run 再次确认授权。

```text
$ai-collaboration-calibration 先校准问题
$research-topic-compiler 做证据研究
$decision-research 给出具体取舍
$brainstorming 形成方案
$grill-me 压测方案
$prd-architect 生成 PRD Delivery Package
$ui-mockup-desktop-workbench 输出结构、HTML、截图和 handoff
$prd-review 做独立评审
$prd-to-issues 拆版本与研发事项
```

## Install

- Codex：[`install-codex.md`](install-codex.md)
- Claude Code：[`install-claude-code.md`](install-claude-code.md)
- 本地 Skillshare：[`local-distribution.md`](local-distribution.md)
