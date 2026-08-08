# v0.3.0 Release Gate

## Scope

本门禁覆盖 15 个原子 Skill、3 个 Loop、2 个 Workflow、4 个 Tool、4 个 Pack，以及三个可同步的 Tool adapter。目标是完成公开仓合并、目录收敛、重复路由治理和本地分发准备；不在本版本扩展新的业务 Skill，也不执行钉钉/云效真实写入。

## Fresh Evidence

| Gate | Result |
| --- | --- |
| Public authority merge | PASS；`PANGKAIFENG/ai-product-manager-skills` PR #12 merged as `21aeb9ab3eeb78f1119aba5f68be83cfd87de91b` |
| Legacy tombstone merge | PASS；`PANGKAIFENG/private-agent-skills` PR #21 merged as `9e4d40ee05aee01670c8c53b8ffbdd5cc15f63b3`；旧目录由 `.skillignore` 退出发现面 |
| `python3 scripts/audit_skills.py .` | PASS；15 个 Skill，无硬错误；`prd-architect` 323 行、`ui-mockup-desktop-workbench` 332 行为软警告 |
| `python3 scripts/check_v03_asset_catalog.py .` | PASS；skills=15, loops=3, workflows=2, tools=4, packs=4；Tool adapter 路径与稳定 ID 已校验 |
| Python regression suites | PASS，127/127；包含 repository/audit 26、PRD 28、research 30、governance 12、UI 3、DingTalk 23、Yunxiao 5 |
| `prd-architect` tests | PASS，28/28 |
| `research-topic-compiler` tests | PASS，30/30 |
| `team-skill-creator` tests | PASS，12/12 |
| `ui-mockup-desktop-workbench` tests | PASS，3/3 |
| DingTalk Publisher tests | PASS，23/23；注入 `PRODUCT_DELIVERY_VALIDATOR` 后无 skip |
| Yunxiao Publisher tests | PASS，5/5 |
| 15 个 `skill-reviewer/check_skill.py` | PASS；无确定性结构问题 |
| Skillshare default security gate | PASS；`prd-architect`、`team-skill-creator`、`dingtalk-prd-publisher` 的 CRITICAL 误报由 7 降为 0；普通安装不再被默认阈值阻断 |
| `git diff --check` | PASS |

## Local Distribution Evidence

- 在迁移前为 Claude、Codex、OpenCode、Qoder、WorkBuddy 五个目标分别建立备份：`2026-08-08_12-22-01`、`12-22-07`、`12-22-15`、`12-22-20`、`12-22-22`。
- 15 个原子 Skill 和 3 个 Tool runtime adapter 均已登记到公开仓路径；18/18 活跃入口的 source metadata 与预期路径一致。
- 旧来源替换产生的 21 个快照仍在 Skillshare 7 天回收站，可用于恢复；五个目标上 8 个退役入口均已不存在。
- 两个真实重复 discovery 入口 `prd-architect-workspace/iteration-2/skill-snapshot` 和 `skill-creator-workspace/skill-snapshot` 已加入 `.skillignore.local`，五个目标均已清理；`skillshare doctor --json` 报告 `duplicate_skills=PASS`、`sync_drift=PASS`。
- 可发现 Skill 从 67 收敛到 59；on-demand context 从约 119.5K 降到约 109.5K。最新 `skillshare sync --dry-run -g` 为 5 个目标、`updated=0`、`pruned=0`。
- 发布提交合并后，只重装本次安全误报修复影响的 `prd-architect`、`team-skill-creator`、`dingtalk-prd-publisher`，再执行五端同步和最终 parity 回读。

## Review Findings

- P0：无。
- P1：已修复入口 catalog 缺失、研究 Skill 触发词/上下文预算回归、Tool adapter 未登记、CI 漏测、新公开 Skill 的旧 private 状态、`archive/` 未从 Skillshare discovery 排除，以及三个包被 Skillshare 默认安全扫描误阻断的问题。
- P2：`prd-architect` 和 `ui-mockup-desktop-workbench` 入口略长；保持在 500 行上限内，本版本不做大拆分，记录到后续 context-budget backlog。

## Deferred / Explicit Limits

- 本机未安装 `pytest`，因此未运行 `pytest -q`；仓库声明的 CI 依赖是 `unittest + PyYAML`，所有可发现的 Python 回归已直接运行。
- 尚未执行真实 DingTalk/Yunxiao 外部写入；结构、模拟 MCP 和 read-back 合同已验证，真实写入仍需专用授权与测试项目。
- Skillshare `doctor` 的 3 个 warning 为聚合源本身的未提交文件、非 Skill 目录和本机 `skillshare` 包的既有 integrity 变化；当前没有 duplicate 或 sync drift，不属于本次 v0.3 发布阻断项。
- Skillshare 仍保留一个已忽略的 workspace snapshot metadata 记录；它不进入 discovery，当前不删除该用户工作区记录。
- `v0.3.0` tag 和 GitHub Release 只在本证据分支通过 CI、合并到 `main`，且三个受影响包从合并版本重新同步并回读后创建。
