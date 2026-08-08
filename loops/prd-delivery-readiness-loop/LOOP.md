# PRD Delivery Readiness Loop

这是 `prd-architect`、`ui-mockup-desktop-workbench`、`prd-review` 和 `prd-to-issues` 之间的交付收敛合同。

## Contract

1. Maker 负责 PRD 与 Manifest，UI 负责结构/HTML/截图证据，Reviewer 负责 readiness 判断，Issue splitter 负责版本切片。
2. 每轮只回到最早仍不稳定的节点，并记录 `review_findings`、`closure_criterion`、`preserved_items` 和 `resume_point`。
3. `package_ready` 必须同时满足 PRD、UI、截图、Manifest 和 Review 证据；validator 只能证明结构，不替代 Review。
4. 小需求可以在 PRD + Review 后结束，中需求增加 Critic 或 UI 校验，大需求才输出 V1/V2/V3 和下游工单。
5. 发布器调用、钉钉/云效写入和 Runtime 同步永远是单独授权动作。
