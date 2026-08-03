# Example: ai-work-assetization-diagnoser

## Use When

You have a repeated AI collaboration pattern and need to decide the smallest reusable asset layer.

## Prompt

```text
$ai-work-assetization-diagnoser

我们连续三次用 AI 做类似工作：
先贴一段产品想法，再让 AI 帮忙澄清问题、列出风险、整理 PRD 草稿，
最后人工再改成团队能看的文档。

请判断这段工作应该沉淀成 Prompt、Context Pack、Workflow、Skill、Loop、System，
还是先不值得沉淀。不要直接创建 Skill，先给资产化诊断。
```

## Expected Output Shape

- Identifies the current shape of the repeated work.
- Recommends one primary asset layer.
- Explains why lower and higher adjacent layers are not the right fit.
- Names the smallest next artifact to create.
- Defines reuse signals and failure signals.
- Lists what not to do yet.

## Good Follow-Up

```text
按你的诊断，先把最小下一步 artifact 写出来。
```
