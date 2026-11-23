# Agent Trace Diagnoser

默认快速诊断也先给案例事实：用户要求与附件、预期交付、实际回复和产物、记录覆盖范围；再区分失败点、根因候选、已确认机制和损失放大。

示例：`只读分析这个 trace，先说明用户想做什么、实际拿到什么，再定位问题。不要创建文件。`

最早错误不自动等于根因。第一次请求已恢复、后续交付失败时，应定位真正影响交付的环节；没有匹配历史部署的源码，不能用当前 checkout 确认过去的实现根因。

用户要求 HTML 时，读取 [数据契约](../../skills/agent-trace-diagnoser/references/replay-contract.md)，把脱敏投影交给固定渲染器，不逐案重写页面：

```bash
python3 skills/agent-trace-diagnoser/scripts/render_report.py \
  skills/agent-trace-diagnoser/tests/fixtures/case.json --validate-only
python3 skills/agent-trace-diagnoser/scripts/render_report.py \
  skills/agent-trace-diagnoser/tests/fixtures/case.json --output-dir /tmp/trace-example-new
```

`/tmp/trace-example-new/index.html` 是合成案例报告，默认呈现原始问答，处理过程、关键参数/JSON 和独立问题分析逐层展开。生成文件不等于公开发布，也不修改业务代码。
