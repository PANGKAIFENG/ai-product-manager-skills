# DingTalk PRD Publisher

将已通过 Review 的 PRD Delivery Package 发布到钉钉文档。只允许 allowlisted 的 PRD、HTML 和截图 artifact；发布前必须有当前 run 的明确确认、payload fingerprint 和目标节点，发布后必须 read-back。`runtime-adapter/` 保留本地 Skillshare 兼容入口。
