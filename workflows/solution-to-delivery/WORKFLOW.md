# 方案到交付 / Solution To Delivery

把已确认方案转成可供研发接手或对外发布的 Product Delivery Package。它拥有交付主路径，但不替代各原子 Skill 的专业判断。

```text
已确认方案
  -> prd-architect
  -> ui-mockup-desktop-workbench (有用户可见界面时)
  -> prd-review -> pre_split_review (pre-split readiness)
  -> prd-to-issues? (需要版本或研发拆分时)
  -> Manifest/hash/fingerprint
  -> delivery-loop (完整 Package 的最终 Review)
  -> product-delivery validator
  -> 可交付产品包
  -> Package publisher dry-run
  -> authorization_required (真实写入等待可信宿主能力)
```

## Entry Gate

- 必须有已确认方案，至少包含目标、范围、关键流程、约束和已知风险。
- 如果问题或方案仍不稳定，返回 `problem-to-solution`。
- 如果已有完整交付包且只需要 Review/修订，直接使用 `delivery-loop`。

## Delivery Rules

| 需求类型 | 必需交付物 |
| --- | --- |
| 有用户可见界面 | PRD、目标态 UI/HTML、关键状态截图、Review 证据、Manifest |
| 无用户可见界面 | PRD、`ui_required: false` 的可解释原因、Review 证据、Manifest |
| 需要版本拆分 | 上述交付物加 V1/V2/V3 或适用版本切片、研发事项草稿和 PRD 覆盖矩阵，并在 Review 前纳入 Manifest |

PRD 和 UI artifacts 必须先记录各自的 `producer_identity`。`prd-review` 将当前 fingerprint、覆盖的 Maker identities 和结论持久化到 `pre_split_review`；`prd-to-issues` 只能消费 validator 证明为 current/ready 的这条记录。如果 Review 仍有 P0/P1，先回到对应 Maker 修订，不生成规划产物。规划产物完成后必须进入 Manifest，并通过 actor-scoped validator 将 Backlog Splitter identity 绑定到每项规划产物，再由 `delivery-loop` 对完整 Package 和全部 artifact producers 进行最终独立 Review。

需求规模影响方案挑战、版本拆分和证据深度，不取消适用的 UI/截图责任。HTML 和截图是交付证据与 handoff，不等于生产代码。

## Delivery Ready Gate

只有同时满足以下条件，Workflow 才能以 `package_ready` 结束：

- PRD 内容与已确认方案一致；
- 页面型需求具有当前 HTML/预览和关键状态截图，或 UI 不适用理由成立；
- `pre_split_review` 在任何版本或事项拆分前已持久化，且 validator 判定为 current/ready；
- 独立 `prd-review` 没有 P0/P1 阻断项；
- Manifest 与文件 hash、全部生产者身份、最终 Review 结论和依赖状态一致；最终 Reviewer 已覆盖全部 artifact producers 且与其身份独立；版本拆分产物或生产者身份如有变化，旧 Review 必须失效；
- 需要研发拆分时，版本与事项覆盖 PRD 且仍处于用户要求的 draft/publish 状态。

Workflow 可以调用 Package Publisher 完成无副作用 dry-run，但当前 Agent Runtime 不能执行 Package 真实写入。Workflow 串联、当前 run 的自然语言确认、Manifest approval、CLI/env 或普通 receipt 都不构成可信 host approval capability；Package 保持 `status: package_ready`，并单独返回 `publish_status: authorization_required`。不得回退到 Legacy direct mode 绕过 Package 边界。

## Output

```yaml
status: package_ready | review_pending | human_gate | blocked
package_root: <path>
prd: <path>
ui_html: <path | not_applicable>
screenshots: []
review_verdict: <ready | needs_revision>
version_plan: <path | not_requested>
manifest: <path>
publish_status: not_requested | authorization_required | delegated
remaining_gaps: []
resume_point: <可恢复节点>
```
