# PRD Review Output Contract

输出必须是“发现问题 + 给出改法”，不是抽象评论。

## Default Structure

```markdown
PRD Review Report: <文件名或对象>

## Review Scope
- Handoff: <path / provided / unavailable>
- PRD: <path / provided / unavailable>
- Required lenses: PM / 研发 / 测试 / optional
- Facts vs assumptions: <how evidence is separated>

## Findings
### 阻断 1. <问题标题>
- 视角：PM / 研发 / 测试
- 位置：<章节 / 文件 / 未定位>
- 证据来源：handoff fact / PRD text / reviewer inference / script warning
- 问题：...
- 影响：...
- 建议：...

### 重要 2. <问题标题>
- 视角：...
- 位置：...
- 证据来源：...
- 问题：...
- 影响：...
- 建议：...

## Lens Summary
- PM：...
- 研发：...
- 测试：...

## Revision Draft
### 建议重写章节结构
...

### 建议替换段落
...

### 建议补充可验证结果 / 边界 / 异常
...

## Open Questions
1. ...
2. ...

## Implementation-Plan Readiness
- Verdict: Ready for writing-plans / Ready with assumptions / Not ready
- Reason: ...
- Required assumptions before planning: ...
```

## Revision Draft Rules

至少给出一种可直接回填的修订材料：

1. 建议新增 / 重写的章节结构。
2. 建议替换的段落草案。
3. 建议补充的可验证结果 / 边界 / 异常列表。

优先输出最小可替换块。只有用户明确要求完整重写时，才输出完整 PRD 改写稿。

## Writing Rules

- Findings 必须先于总结。
- 不按角色输出三份重复报告。
- 同一个问题优先合并成一条，再标注受影响视角。
- 结论要明确指出来自 handoff 已确认事实、PRD 当前写法、脚本 warning 还是 review 推断。
- 图示相关结论必须区分“文本要求缺失”“文件实际校验失败”和“未能验证”。
