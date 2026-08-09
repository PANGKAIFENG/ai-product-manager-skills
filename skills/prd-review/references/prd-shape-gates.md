# PRD Shape Gates for Review

按需加载本文件。用于 `prd-review` 识别 PRD 是否把产品讨论稿、设计对齐稿和开发 handoff 混在一起。

## Review Questions

1. 当前 PRD 是产品初版、设计对齐稿，还是开发 handoff？
2. 当前章节是否服务于这个阶段？
3. 是否写了很多 HOW，但短背景、功能模块、触发、UI 反馈、边界和可验证结果仍不清楚？
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
- 主文档改写为短背景和功能模块；在对应模块内放目标态 UI、触发、系统行为、UI 反馈、边界和可验证结果。

### 模板章节误激活与重复

出现以下情况时应压缩，而不是要求补齐标题：

- 独立“用户场景、入口与触发、页面结构、核心对象、交互逻辑”重复同一规则。
- 独立“验收标准、模块验收、整体验收”与功能逻辑重复，或把本应就近说明的用户结果拆到文末。
- 背景超过 200 字并混入调研过程、长期愿景或实现说明。
- 简单页面改动生成了没有决策价值的流程图。
- 页面型功能只有文字说明，没有把目标态 UI 放在对应功能模块。

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
- 只有跨多角色/系统、关键判断或回流、异步恢复、6 个及以上依赖步骤，或用户明确要求时，才补 Draw.io flow / architecture。
- 不满足图示门槛时，用目标态截图和模块逻辑表完成说明，不把“多阶段”或“存在模块关系”单独当作画图理由。

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
