# v0.3.0 Release Gate

## Scope

本门禁覆盖 15 个原子 Skill、3 个 Loop、2 个 Workflow、4 个 Tool、4 个 Pack，以及三个可同步的 Tool adapter。目标是完成公开仓合并、目录收敛、重复路由治理和本地分发准备；不在本版本扩展新的业务 Skill，也不执行钉钉/云效真实写入。

## Fresh Evidence

| Gate | Result |
| --- | --- |
| `python3 scripts/audit_skills.py .` | PASS；15 个 Skill，无硬错误；`prd-architect` 323 行、`ui-mockup-desktop-workbench` 332 行为软警告 |
| `python3 scripts/check_v03_asset_catalog.py .` | PASS；skills=15, loops=3, workflows=2, tools=4, packs=4；Tool adapter 路径与稳定 ID 已校验 |
| Repository/audit unittest | PASS，26/26 |
| `prd-architect` tests | PASS，28/28 |
| `research-topic-compiler` tests | PASS，30/30 |
| `team-skill-creator` tests | PASS，12/12 |
| `ui-mockup-desktop-workbench` tests | PASS，3/3 |
| DingTalk Publisher tests | PASS，23/23；注入 `PRODUCT_DELIVERY_VALIDATOR` 后无 skip |
| Yunxiao Publisher tests | PASS，5/5 |
| 15 个 `skill-reviewer/check_skill.py` | PASS；无确定性结构问题 |
| `git diff --check` | PASS |

## Review Findings

- P0：无。
- P1：已修复入口 catalog 缺失、研究 Skill 触发词/上下文预算回归、Tool adapter 未登记、CI 漏测、新公开 Skill 的旧 private 状态，以及 `archive/` 未从 Skillshare discovery 排除的问题。
- P2：`prd-architect` 和 `ui-mockup-desktop-workbench` 入口略长；保持在 500 行上限内，本版本不做大拆分，记录到后续 context-budget backlog。

## Deferred / Explicit Limits

- 本机未安装 `pytest`，因此未运行 `pytest -q`；仓库声明的 CI 依赖是 `unittest + PyYAML`，所有可发现的 Python 回归已直接运行。
- 尚未执行真实 DingTalk/Yunxiao 外部写入；结构、模拟 MCP 和 read-back 合同已验证，真实写入仍需专用授权与测试项目。
- Skillshare 与五个 Runtime 的同步必须在 GitHub `main` 合并并发布 tag 后进行；本文件在发布后补录远端 merge/tag 和各目标 parity 证据。
