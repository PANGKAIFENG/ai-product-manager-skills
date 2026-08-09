# Quickstart

This repository contains 15 atomic Skills plus five optional explicit Runtime
entry adapters: two Workflows under `workflows/` and three Loops under `loops/`.
Tools keep separate side-effect adapters. Runtime adapters do not change the
catalog kind of their owning asset.

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

小需求直接调用原子 Skill。需要从模糊问题完整推进到确认方案时使用
`$problem-to-solution`；方案确认后需要完整产品交付包时使用
`$solution-to-delivery`。只有局部节点需要多轮回流时，才显式使用三个 Loop。
外部写入仍需调用对应 `tools/` publisher，并在当前 run 确认授权。

```text
$problem-to-solution 从模糊问题推进到已确认方案
$decision-loop 为一个明确决策补齐关键证据
$solution-loop 对候选方案反复挑战和定点修订
$solution-to-delivery 从已确认方案生成完整产品交付包
$delivery-loop 对现有 PRD/UI/截图做 Review 和修订闭环
```

## Install

- Codex：[`install-codex.md`](install-codex.md)
- Claude Code：[`install-claude-code.md`](install-claude-code.md)
- 本地 Skillshare：[`local-distribution.md`](local-distribution.md)
