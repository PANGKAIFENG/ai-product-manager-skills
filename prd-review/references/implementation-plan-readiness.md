# Implementation Plan Readiness Reference

用于 `prd-review` 判断 PRD 是否可以交给 superpowers `writing-plans`。

## Verdicts

- `Ready for writing-plans`：PRD 可以进入开发计划。
- `Ready with assumptions`：可以进入开发计划，但假设必须写进 plan 前置条件。
- `Not ready`：仍有阻断性需求缺口，不能进入开发计划。

## Required Checks

- 目标用户、问题、范围边界和非目标已经明确。
- 主流程、关键状态、输入输出、异常或人工接管点已经写清。
- 验收标准能被测试、人工检查或通过具体 artifact 验证。
- 阻断性待确认项已经关闭，或已经显式转成 implementation plan 的前置假设。

## Boundary

这个检查只判断产品需求是否可交给开发计划，不负责拆文件边界、测试步骤、提交节奏或具体实现方案。那些内容由 superpowers `writing-plans` 承接。
