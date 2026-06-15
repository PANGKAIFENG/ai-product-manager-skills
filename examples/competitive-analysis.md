# Example: competitive-analysis

## Use When

You need competitor or alternative-product evidence to inform a product decision, not just a feature inventory.

## Prompt

```text
$competitive-analysis

打开 https://krowork.com 做一次竞品决策分析。
我们的背景：正在设计一个 AI PM / AI 工作台产品。
我不需要单纯走查，而是想知道这个产品对我们的定位、功能优先级和 onboarding 有什么决策启发。
先用公开信息；如果确实需要登录态走查，再说明你要看什么和为什么。
```

## Expected Output Shape

- Restates the product decision question.
- Selects evidence channels before browsing.
- Separates public evidence from walkthrough evidence.
- Outputs a Product Decision Brief.
- Explains what to copy, adapt, avoid, and validate.
- Does not present "clicked all features" as success.

## Good Follow-Up

```text
基于这个 brief，帮我把下个版本应该验证的 3 个 onboarding 假设转成 PRD 输入。
```
