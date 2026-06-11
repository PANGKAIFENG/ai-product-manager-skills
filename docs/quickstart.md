# Quickstart

This guide helps you try AI Product Manager Skills Library in a local Agent workflow.

The repository contains root-level Skill folders. Each Skill folder has a `SKILL.md` file with a stable `name` and `description`.

## 1. Clone The Repository

```bash
git clone https://github.com/PANGKAIFENG/ai-product-manager-skills.git
cd ai-product-manager-skills
```

## 2. Pick A First Skill

Start with one workflow:

| Goal | Skill | Prompt |
| --- | --- | --- |
| Clarify a fuzzy product problem | `ai-collaboration-calibration` | `$ai-collaboration-calibration 先别执行，帮我看清这个问题` |
| Research a topic for PM decisions | `research-topic-compiler` | `$research-topic-compiler 系统研究这个主题，并转成 PM 决策输入` |
| Choose between options | `decision-research` | `$decision-research 帮我比较这几个方案，给一个有立场推荐` |
| Draft a PRD | `prd-architect` | `$prd-architect 把这个想法整理成 PRD-lite` |
| Review a PRD | `prd-review` | `$prd-review 从研发和测试视角审一下这个 PRD` |
| Pressure-test a plan | `grill-me` | `$grill-me 拷问我的方案，找失败模式` |

## 3. Install Or Link The Skills

Recommended paths:

- Codex users: [install-codex.md](install-codex.md)
- Claude Code users: [install-claude-code.md](install-claude-code.md)
- skillshare users: use `skillshare install` and `skillshare sync`

If your tool supports manually loaded Agent Skills, copy or symlink the six root-level Skill directories into the tool's Skills directory.

## 4. Verify Skill Discovery

Ask your agent to list available Skills or explicitly invoke one by name:

```text
$prd-architect 把“AI 会议纪要自动生成任务清单”整理成 PRD-lite
```

Expected signs:

- The agent recognizes `prd-architect`.
- It asks only necessary clarification questions.
- It produces a structured PRD rather than a generic brainstorm.
- It keeps product requirements separate from implementation planning.

## 5. Use The Workflow

A common AI PM path:

```text
$ai-collaboration-calibration 先帮我校准这个需求是不是值得做
$research-topic-compiler 系统研究这个领域，输出 PM 决策输入
$decision-research 帮我比较候选方案，给一个有立场推荐
$prd-architect 基于上面的结论写 PRD-standard
$prd-review 从研发和测试视角审这个 PRD
$grill-me 拷问最终方案，找失败模式
```

When the PRD is clear enough, hand it to Superpowers `writing-plans` for implementation planning.

## Troubleshooting

Skill not showing up:

- Check that each Skill folder contains `SKILL.md`.
- Check that the Skill folder is in a directory your Agent tool scans.
- Restart the Agent tool if it caches available Skills.
- Try explicit invocation with `$skill-name`.

Wrong Skill triggers:

- Read [SKILL_ROUTING.md](../SKILL_ROUTING.md).
- Make the prompt state the workflow stage: brainstorm, research, PRD draft, PRD review, or pressure test.
- Open an issue if the Skill descriptions need clearer boundaries.
