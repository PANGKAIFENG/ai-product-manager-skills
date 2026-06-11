# Example: tech-research

## Use When

You already know the decision question and need a grounded technical recommendation.

## Prompt

```text
$tech-research

我们要给 PM 团队分发一组 Agent Skills。
请调研应该用普通 Git 仓库 + 手动安装、skillshare 同步，还是做成 Codex/Claude 插件。
目标是 10 人团队低成本使用，后续能维护版本。
```

## Expected Output Shape

- States the decision question.
- Lists constraints and assumptions.
- Compares options with tradeoffs.
- Gives a recommended path.
- Explains what not to choose and why.
- Proposes a validation step before rollout.

## Good Follow-Up

```text
基于你的推荐，写一个两阶段落地计划。
```
