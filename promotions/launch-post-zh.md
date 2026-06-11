# 中文推广长文草稿

## 标题

我把 AI 产品经理的高频工作流做成了 Codex / Claude Code Skills

## 正文

过去一段时间我在用 Codex、Claude Code 和 Superpowers 做研发协作时，发现一个很明显的断层：

Superpowers 很适合研发侧，尤其是写计划、TDD、执行实现、验证和收尾。但产品经理在进入研发之前，还有大量工作没有被稳定沉淀下来。

比如：

- 一个想法还很模糊时，怎么先校准问题，而不是直接写 PRD？
- 一个主题需要研究时，怎么把资料转成 PM 判断，而不是百科摘要？
- 一个 PRD 初稿出来后，怎么从研发和测试视角找交付阻断项？
- 一个方案看起来合理时，怎么系统性拷问失败模式？
- 什么时候应该把 PRD 拆成 GitHub issues，什么时候应该直接交给 Superpowers `writing-plans`？

所以我整理了一个开源仓库：

https://github.com/PANGKAIFENG/ai-product-manager-skills

它是一个中文优先的 AI Product Manager Skills Library，目前包含 10 个公开 Skill：

- `ai-collaboration-calibration`：问题还没想清楚时，先挑战假设和目标。
- `research-topic-compiler`：系统研究主题、概念源流和行业演进，转成 PM 决策输入。
- `decision-research`：围绕具体决策、方案选型和可行性给出有立场推荐。
- `brainstorming`：在 PRD、mockup 或开发计划前，先比较设计方案并收敛成 spec。
- `prd-architect`：把想法、脑暴或草稿整理成 PRD。
- `prd-review`：从 PM、研发、测试视角审 PRD。
- `prd-to-issues`：把 ready PRD 拆成可领取、可验收的 GitHub implementation issues。
- `ui-mockup-desktop-workbench`：基于 PRD 和 UI 规范生成桌面端真实页面 mockup。
- `grill-me`：对已有方案做压力测试和失败模式追问。
- `ai-work-assetization-diagnoser`：判断重复 AI 工作该沉淀成 Prompt、Workflow、Skill 还是 Loop。

这个项目不是替代 Superpowers，而是补它前面的产品侧工作流：

产品问题校准 -> 主题研究 -> 决策调研 -> 方案脑暴 -> PRD 起草 -> PRD 评审 -> PRD 拆 issue -> UI mockup / 方案压测 -> 交给 Superpowers 做开发计划。

如果你是产品经理、产品负责人，或者正在用 Codex / Claude Code 做 AI 协作，可以先试这几个 prompt：

```text
$ai-collaboration-calibration 先别执行，帮我看清这个产品问题
$research-topic-compiler 系统研究这个主题，并转成 PM 决策输入
$decision-research 帮我比较这几个方案，给一个有立场推荐
$brainstorming 先不要写 PRD，帮我脑暴 2-3 个设计方案
$prd-architect 把这个想法整理成 PRD-lite
$prd-review 从研发和测试视角审一下这个 PRD
$prd-to-issues 把这个 PRD 拆成 GitHub implementation issues，先给我 draft
$ui-mockup-desktop-workbench 基于 PRD 和 UI 规范生成桌面端真实页面 mockup
$grill-me 拷问我的方案，找失败模式
$ai-work-assetization-diagnoser 判断这段 AI 工作该沉淀成 Prompt、Workflow、Skill 还是 Loop
```

我后续会继续补：

- 更完整的 examples
- 插件化分发
- 团队 PM 使用方式
- 更多真实 PRD / research / review 工作流样例

欢迎 star、提 issue，或者直接拿去改成你团队自己的 AI PM Skill 库。

GitHub:

https://github.com/PANGKAIFENG/ai-product-manager-skills
