# DingTalk PRD Publisher

将本地 PRD 先做版本记录校验，再通过 Legacy direct mode 发布到钉钉文档并回读完整最新版本行；同时为已通过 Review 的 PRD Delivery Package 提供 fail-closed dry-run。Package 只允许 allowlisted 的 PRD、HTML 和截图 artifact；当前 Agent Runtime 没有可信 host approval capability，因此 Package 非 dry-run 返回 `authorization_required`，不调用 `dws`。`runtime-adapter/` 保留本地 Skillshare 兼容入口。
