# Product Delivery

面向已经形成方案、需要交付 PRD 和开发输入的阶段组合。

```text
prd-architect
        -> ui-mockup-desktop-workbench (structure-only 或高保真 HTML/preview)
        -> prd-review
        -> prd-to-issues (需要研发拆分时)
        -> tools/validators/product-delivery
        -> tools/publishers/* (当前 run 明确授权后)
```

## Delivery sizes

| 需求规模 | 最小路径 | 额外要求 |
| --- | --- | --- |
| 小 | PRD -> Review | 可省略 Loop，但 PRD 仍记录 UI/截图是否适用 |
| 中 | PRD -> UI/HTML/截图 -> Review | 至少一轮修订或压力测试 |
| 大 | Discovery -> PRD -> UI/HTML/截图 -> Review -> V1/V2/V3 | 每个版本独立目标、范围、依赖、验收和回滚点 |

Product Delivery Package 只能在 Review 通过后进入发布准备。DingTalk/Yunxiao publisher 的 `runtime-adapter` 不拥有产品判断，也不能因为 Workflow 串联而自动写外部系统。
