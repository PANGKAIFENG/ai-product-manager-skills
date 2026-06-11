# Example: prd-review

## Use When

You already have a PRD or handoff and need to find blockers before engineering starts.

## Prompt

```text
$prd-review

下面是一版 PRD。请从 PM、研发、测试视角评审，
重点找范围不清、状态缺失、验收不可测试、图示不足和研发无法开工的问题。

[paste PRD here]
```

## Expected Output Shape

- Findings first, ordered by severity.
- Each finding explains why it blocks delivery or testing.
- Separates blockers, risks, and polish suggestions.
- Gives concrete revision suggestions.
- States whether the PRD is ready for Superpowers `writing-plans`.

## Good Follow-Up

```text
把阻断项直接改成一版可回填到 PRD 的修订草案。
```
