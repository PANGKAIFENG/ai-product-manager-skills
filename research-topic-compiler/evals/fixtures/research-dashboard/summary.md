# AI 产品 tracing 健康看板研究摘要

- One-sentence conclusion: 首屏应优先暴露业务完成、技术失败和成本倒挂，再把 P50/P99 与具体 trace 放入下钻。
- Research goal: 验证通用 `research-dashboard-html` 能承载跨职能研究结果。
- Audience: 领导、产品负责人、研发负责人。
- Research mode: Application.
- Output artifact mode: research-dashboard-html.
- Terminal status: complete-fit-for-purpose.
- Confidence: Medium-high；当前 fixture 使用冻结的本地研究摘录验证信息结构，不代表真实线上指标。

## Key findings

1. 业务完成率比单独的技术成功率更接近用户价值。
2. 成本倒挂需要同时展示 AI 推理点数和核心工具点数。
3. 问题必须落到 Agent、业务 Skill、执行 Skill、Tool 或 Runtime 责任层。

## Framework change

- Before: 首屏以调用量、错误率和耗时为主。
- After: 首屏改为规模、健康红线、行动队列三层；技术分位数进入下钻。
- Evidence: 用户工作流要求是“发现异常 → 判断影响 → 定位责任 → 进入队列 → 验证复发”。

## Residual gaps and risks

- 缺少稳定 `root_request_id` 与 Skill 委托链时，责任层排名只能作为探索信号。
- 当前 fixture 不包含真实企业、用户或 trace 数据。

## Next actions

1. 补齐根任务、租户、Outcome、Skill 委托链和 Runtime 阶段字段。
2. 建立指标字典和问题簇闭环。
3. 对桌面与移动端执行视觉回归。

## Sources

- `references/iterative-research-loop.md`，研究终态与残余 Gap。
- `references/research-dashboard-output-contract.md`，Dashboard 产物合同。
- `evals/fixtures/research-dashboard/summary.md`，本地 fixture 内容来源。
