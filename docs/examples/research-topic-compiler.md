# Example: research-topic-compiler

## Use When

You need structured research that becomes product judgment, not a generic summary.
It is also useful when your first prompt is still plain business language and needs to be turned into a clear research goal, research questions, and output requirements.

## Prompt

```text
$research-topic-compiler

系统研究“AI 产品经理工作流”这个主题。
我想知道它和传统 PM 工作流有什么变化，哪些环节最适合沉淀成 Agent Skills，
最后请输出 PM 决策输入，而不是百科介绍。
```

## Expected Output Shape

- Converts broad user language into an explicit research goal when needed.
- Defines primary research question, sub-questions, output requirements, and out-of-scope.
- Stops at the framing brief when the user asks not to start research yet.
- Clarifies research depth and decision goal.
- Builds a research frame before collecting facts.
- Separates concept lineage, current usage, workflow stages, and open questions.
- Produces a PM decision matrix or research report.
- Calls out source quality and uncertainty when live research is used.

## Good Follow-Up

```text
把研究结论转成 3 个可以优先沉淀的 Skill 候选。
```

## Goal-Framing Example

```text
$research-topic-compiler

我建议接下来先产出两份前置材料，再做 Roadmap：

1. Agent 产品演进叙事调研
回答：行业上 Agent 到底在怎么讲“从聊天到做事”？有哪些主流方向？
哪些是噱头，哪些会变成产品基本能力？

2. StyleClaw 垂直转译框架
回答：这些通用 Agent 方向落到服装行业后，分别对应什么用户、什么任务、
什么交付物、什么能力壁垒？

先不要开始搜资料。请先把我的大白话转成研究目标、研究问题、输出要求、
out-of-scope 和推荐研究模式。
```
