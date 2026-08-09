# 交付闭环 / Delivery Loop

当已有 PRD 或 Product Delivery Package 但尚未达到可交付状态时，在 Maker、UI 和独立 Reviewer 之间做有界修订。目标是关闭交付缺口，不是重新定义产品方案。

## State Transition

```text
delivery_package_incomplete
  -> prd-review 定位最早不稳定节点
  -> prd-architect 或 UI Maker 返回 Artifact Delta
  -> validator + prd-review 复核
  -> package_ready | 下一 finding | Human Gate
```

## Cycle Contract

- `max_cycles: 3`。
- Reviewer 每轮只选择最早且会阻断交付的 finding。
- 修订只回到该 finding 的责任节点：PRD、UI/HTML/截图、Manifest 或版本切片。
- `prd-review` 负责 readiness；Maker 和 validator 都不能自评通过。
- Manifest 中每个 artifact 的 `producer_identity` 都是最终 Review 的权威 Maker 输入；`maker_identities` 不得省略生产者，Reviewer 不得与任一生产者同身份。
- 连续两轮没有有效 Artifact Delta、达到三轮上限或交付事实缺失时进入 Human Gate。
- 发布授权独立于 Package readiness；当前 Agent Runtime 只允许 Package dry-run，内容 ready 后保持 `status: package_ready` 并返回 `publish_status: authorization_required`，不得仅因缺少可信宿主能力进入 Human Gate。

## Recoverable State

```yaml
loop: delivery-loop
cycle: 1
max_cycles: 3
package_root: <path>
active_finding: <唯一阻断 finding>
return_owner: prd-architect | ui-mockup-desktop-workbench | prd-to-issues
closure_criterion: <关闭条件>
artifact_delta: []
preserved_items: []
review_verdict: needs_revision | ready
status: reviewing | revising | package_ready | human_gate | blocked
publish_status: not_requested | authorization_required
resume_point: <下一节点>
```

只有用户要求保存或恢复时才写 `.loop-state/delivery-loop/`。Package Publisher dry-run 可以作为本地验证；真实钉钉/云效写入和 Runtime 同步不属于 Loop，且不能用 Manifest 或 Loop 状态替代可信宿主授权。
