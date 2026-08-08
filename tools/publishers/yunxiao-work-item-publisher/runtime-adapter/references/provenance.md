# Provenance

## 来源

- Source repository: `PANGKAIFENG/ai-product-manager-skills`
- Source visibility: `PUBLIC`
- Published source branch: `main`
- Published source commit: `6dd7a6e2de81717f8eb4f0a4455249f124e1ff24`
- Source pull request: `PANGKAIFENG/ai-product-manager-skills#8`
- Original feature commit: `0230d7f4d82c79df8d6bb32c97de15c3077616fc`
- Original path: `skills/stylework-yunxiao-workitem-submitter/`
- License: MIT，见包根目录 `LICENSE`
- Migration date: `2026-08-05`

## 迁移决定

该适配器面向 StyleWork 云效工作项创建、云效 MCP、字段合同、附件确认和外部写入回读。v0.3 将其归入统一公开仓的 `tools/publishers/yunxiao-work-item-publisher/runtime-adapter/`，不计入原子 Skill catalog。

公开发布不降低数据治理要求；任何 secret、内部 URL、真实项目或组织 ID、客户数据和本机绝对路径仍禁止进入仓库。

## 内容处理

- 保留原稳定运行时 ID `stylework-yunxiao-workitem-submitter`，避免本地调用方断裂。
- Tool 目录负责副作用边界，`runtime-adapter/` 仅用于兼容本地 Agent 分发。
- v0.3 不修改创建、字段、附件或 read-back 行为。

## 后续维护

- Authoritative repository: `PANGKAIFENG/ai-product-manager-skills`
- Stable path: `tools/publishers/yunxiao-work-item-publisher/runtime-adapter/`
- Asset kind: `tool-runtime-adapter`
- GitHub visibility: `PUBLIC`
- Future behavior changes require Tool-level eval, CR, explicit side-effect review, and read-back evidence.
