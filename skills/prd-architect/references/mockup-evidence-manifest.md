# Mockup Evidence Manifest

页面型 PRD 使用本契约记录 UI 来源、HTML、截图和 PRD 之间的可追溯关系。它解决的是本地多产物工作流的 checkpoint、失效和恢复问题，不要求部署 Temporal 服务。

## State Model

```text
source_resolution_required
  -> source_resolved
  -> mockup_built
  -> screenshots_fresh
  -> prd_embedded
  -> verified
```

每次恢复都重新验证上游身份：

- UI 基线 commit/hash 改变：从 `source_resolved` 后重新执行。
- `mockup.html` hash 改变：从 `mockup_built` 后重新执行并重拍截图。
- 任一截图 hash、路径或文件状态改变：重新完成 `prd_embedded`。
- PRD hash 改变：重新检查正文图片引用。

## Source Resolution

| kind | 何时使用 | 必须记录 | 可声称的对齐程度 |
| --- | --- | --- | --- |
| `frontend-repo` | 已验证真实产品仓库和目标页面 | repo path、branch、commit、worktree status hash | 可以说明项目基线和组件证据 |
| `design-system` | 没有页面仓库，但有正式设计系统资产 | source path、SHA-256 | 只能说明设计系统对齐 |
| `reference-html` | 用户确认没有仓库，提供现有 HTML | source path、SHA-256 | 静态参考对齐，生产组件未验证 |
| `screenshot` | 用户确认没有仓库，只提供截图 | source path、SHA-256 | 截图推断，最低置信度 |

候选仓库不唯一或目标页面归属无法证明时，不要生成 manifest。先问用户一个简短问题，状态保持 `source_resolution_required`。

## Capture Command

在截图已从当前 HTML 重新生成、PRD 已嵌入对应图片后运行：

```bash
python3 scripts/capture_mockup_evidence.py \
  --manifest /path/to/output/mockup-evidence.json \
  --baseline-kind frontend-repo \
  --baseline-source /path/to/frontend \
  --baseline-note '订单页路由和审批抽屉组件' \
  --mockup /path/to/output/mockup.html \
  --prd /path/to/output/feature-prd.md \
  --screenshot 'default=/path/to/output/screenshots/default.png' \
  --screenshot 'permission-blocked=/path/to/output/screenshots/permission-blocked.png'
```

没有真实前端时，把 `--baseline-kind` 改为 `screenshot` 或 `reference-html`，`--baseline-source` 指向用户确认的证据文件。

Capture 会：

- 记录 frontend repo 的 branch、commit 和 worktree status hash，或记录文件型基线 SHA-256。
- 记录 HTML、PRD 和每张截图的 SHA-256。
- 把当前 HTML hash 写入每张截图的 `source_mockup_sha256`。
- 拒绝修改时间早于 HTML 的旧截图。
- 写入 `prd_embedded` checkpoint；最终 `verified` 由 `check_prd_shape.py` 的成功结果提供。

## Verification Command

```bash
python3 scripts/check_prd_shape.py /path/to/output/feature-prd.md \
  --type standard \
  --require-mockup-evidence \
  --require-mockup-artifact /path/to/output/mockup.html \
  --require-current-mockup-evidence \
  --mockup-manifest /path/to/output/mockup-evidence.json
```

验证失败时不要手工修改 hash、触碰 mtime 或把旧图另存为新文件。回到最早失效状态，重新生成对应下游产物。

## Manifest Shape

```json
{
  "schema_version": 1,
  "workflow": {
    "stage": "prd_embedded",
    "captured_at": "2026-07-30T12:00:00+00:00"
  },
  "baseline": {
    "kind": "frontend-repo",
    "source": "/path/to/frontend",
    "revision": "<git-sha>",
    "branch": "main",
    "dirty": false,
    "worktree_status_sha256": "<sha256>",
    "note": "target route and component evidence"
  },
  "mockup": {
    "path": "mockup.html",
    "sha256": "<sha256>",
    "mtime_ns": 0
  },
  "screenshots": [
    {
      "state": "default",
      "path": "screenshots/default.png",
      "sha256": "<sha256>",
      "source_mockup_sha256": "<sha256>",
      "mtime_ns": 0
    }
  ],
  "prd": {
    "path": "feature-prd.md",
    "sha256": "<sha256>",
    "mtime_ns": 0
  }
}
```
