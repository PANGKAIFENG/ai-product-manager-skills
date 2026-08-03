# PRD Shape Gates for Review

按需加载本文件。用于 `prd-review` 识别 PRD 是否把产品讨论稿、设计对齐稿和开发 handoff 混在一起。

## Review Questions

1. 当前 PRD 是产品初版、设计对齐稿，还是开发 handoff？
2. 当前章节是否服务于这个阶段？
3. 是否写了很多 HOW，但 WHY、用户、触发、边界、验收仍不清楚？
4. 是否把实现字段、schema、metadata、adapter 写进了产品主链路？
5. 是否缺少必要图示或 mockup 承接，导致研发/设计只能猜？

## Common Findings

### 产品初版过早技术化

证据通常包括：

- 主文档包含 TypeScript interface。
- 主文档包含 JSON schema。
- `metadata`、`adapter`、`endpoint`、`capability registry` 成为核心章节。
- 大量代码路径代替产品对象和用户可见行为。

建议：

- 把技术内容移动到开发 handoff 附录。
- 主文档改写为核心对象、业务规则、入口触发、交互逻辑、异常和验收。

### 模板章节误激活

证据通常包括：

- 单点交互套用了完整系统 PRD。
- 不存在多阶段链路却强制要求一体化架构图。
- 用户只要初版 PRD，却直接进入开发计划建议。

建议：

- 降级模板类型。
- 删除不服务本轮决策的章节。
- 将未决问题保留为待确认项。

### Mockup / Diagram 承接缺失

证据通常包括：

- 需求发生在既有页面上，但没有页面入口、触发动作或状态说明。
- 复杂链路没有流程图或结构图。
- 图示不可编辑，或引用到普通 SVG / PNG 却声称可编辑。

建议：

- 既有页面改动补 screenshot / HTML mockup 承接。
- 多阶段链路补 Draw.io flow。
- 模块关系补 Draw.io architecture。

## Deterministic Check

如果本地文件可用，运行：

```bash
python3 scripts/check_prd_shape.py <prd.md> --type <lite|standard|ai-native>
```

如果 PRD 明确是开发 handoff，运行：

```bash
python3 scripts/check_prd_shape.py <prd.md> --type <lite|standard|ai-native> --allow-handoff
```

脚本 warning 是 review 证据，不自动等同于阻断；需要结合 PRD 阶段和用户要求判断。

