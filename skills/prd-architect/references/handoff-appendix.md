# Development Handoff Appendix

按需加载本文件。只有用户明确要求开发 handoff、字段定义、接口协议、schema、metadata、adapter、实现计划前置材料，或 PRD 已进入 `已确认` 阶段并需要交给研发拆解时使用。

## Boundary

开发 handoff 附录不替代 PRD 主文档。

- PRD 主文档回答：用户为什么需要、哪些场景触发、系统表现和可观察结果是什么。
- Handoff 附录回答：实现承接需要哪些对象、字段、状态、协议、事件和兼容约束。

## Activation Signals

加载本文件的信号：

- “补开发 handoff”。
- “字段怎么定义”。
- “协议怎么接”。
- “给研发接口 / schema / metadata”。
- “进入 implementation plan 前先补技术交接”。

不要因为读到了真实代码文件，就自动进入 handoff 模式。

## Appendix Skeleton

### A. 影响范围

- 涉及页面 / 模块。
- 涉及协议 / 数据对象。
- 不涉及的范围。

### B. 产品对象到实现对象映射

| 产品对象 | 用户可见含义 | 实现承接对象 | 备注 |
| --- | --- | --- | --- |

### C. 字段与协议建议

只有在必要时写 TypeScript / JSON。写前先说明这是建议，不是已确认实现。

```ts
// Optional handoff draft. Confirm with engineering before implementation.
```

### D. 状态与事件

| 状态 / 事件 | 触发 | 系统处理 | 用户可见反馈 |
| --- | --- | --- | --- |

### E. 兼容与迁移

- 历史数据如何处理。
- 刷新 / 恢复策略。
- 多端或多运行时差异。

### F. 风险与待确认

- 需要研发确认的技术约束。
- 需要产品确认的取舍。

## Main-body Guardrail

如果这份附录被启用，PRD 主文档仍不应被字段和 schema 淹没。主文档保留产品语义；技术字段留在附录。
