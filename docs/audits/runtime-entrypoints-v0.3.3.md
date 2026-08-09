# v0.3.3 Runtime Entrypoints Release Gate

## Scope

本门禁覆盖 2 个 Workflow 和 3 个 Loop 的重命名、Codex Runtime 入口、目录迁移、路由边界、L2 行为评估、公开发布和本地分发。它不新增原子 Skill，不执行 DingTalk/Yunxiao 写入，也不把 Workflow/Loop 重新分类为 Skill。

## Improvement Record

- Observed failure: `workflows/` 和 `loops/` 只有组合合同，没有 `SKILL.md` Runtime 入口，用户无法在 Codex 的 Skill 选择面直接唤起。
- User-visible impact: 用户需要记忆目录或手工串联原子 Skill，两个阶段主路径和三个局部闭环难以发现，旧名称也不能直接表达业务结果。
- Evidence / trace: `v0.3.2` tag 下 5 个目录只有 `WORKFLOW.md` 或 `LOOP.md`；当前需求要求将其变成 Codex 可选择入口。
- Responsible layer: Runtime discovery / distribution，外加 catalog routing。
- General principle: Workflow 和 Loop 可以通过兼容 `SKILL.md` 暴露为 Runtime 入口，但其资产类型、职责边界和停止条件必须保持独立。
- Best Practice Delta: distribution/governance、trigger/boundary、evaluation loop。
- Deterministic checks: 目录合同、frontmatter ID、`agents/openai.yaml`、`allow_implicit_invocation: false`、eval 文件、catalog/path/Pack 引用和旧入口缺失。
- Human-review criteria: 名称能从业务结果理解；Workflow 是阶段主路径；Loop 只处理局部回流；五个入口不扩张外部写入授权。
- Regression eval: 显式完整流程、单点请求不误触发、三轮上限、两轮无差量、历史授权不生效。
- Transfer eval: 小需求走最短路径、无 UI 交付、恢复 cycle 2、只补 UI 证据。
- Negative eval: 开放式研究不进 Decision Loop、无候选方案不进 Solution Loop、单次 PRD Review 不进 Delivery Loop。
- Independent holdout: 由独立 Reviewer 在不读取本文件结论的前提下评审五个入口和未标注 prompt 投影。
- Trace / time / token evidence: 本版本不建立生产 trace 或 token 基线；入口是显式调用，发布门禁以结构、行为和本地 discovery 证据为主。
- Release decision: `pending`，仅在 P0/P1 清零、CI 通过、远端合并回读和本地同步验证后改为 `release`。
- Research / meta-skill feedback: Workflow/Loop 的 Runtime 可发现性应由 catalog checker 长期验证，旧 ID 不应通过别名目录制造第二触发面。

## Pre-Release Remediation

- 修正 `solution-to-delivery` 的双门禁顺序：先由独立 `prd-review` 确认 PRD/UI readiness，再允许 `prd-to-issues`；规划产物进入 Manifest/hash/fingerprint 后，再由 `delivery-loop` 完成整包最终 Review。
- 修正 `SKILL_ROUTING.md` 与 Workflow 合同的顺序漂移；pre-split Review 未通过时禁止生成规划产物。
- 为 `Backlog Splitter` 增加角色与身份回归：只允许修改 `version_plan`、`issue_drafts`、`coverage_matrix` 和时间戳，规划产物必须记录当前 actor identity，最终 Reviewer 不得省略或冒用该生产者。
- 分离交付就绪与发布授权：未获授权时保持 `status: package_ready`，并返回 `publish_status: authorization_required`；`delivery-loop` 不得仅因缺少发布授权进入 Human Gate。
- 修正 `problem-to-solution` 的条件路由：稳定输入跳过 Calibration；已有候选方案可以直接进入 Solution Loop。
- 将五个组合入口的 route universe、trigger/non-trigger/risk 最低覆盖和 retired-ID 共存检查纳入确定性门禁。
- 将三项独立 CR 缺陷转成确定性合同与回归：stale approval 只撤销发布授权；全部 artifact 记录生产者身份；规划产物必须由当前 `pre_split_review: ready` 前置授权。
- 修复独立 CR 发现的 Publisher 授权缺口：当前 Agent Runtime 的 Package mode 只允许完整 dry-run；非 dry-run 在首个 `dws` 调用和 Manifest 写入前返回 `authorization_required`。不接受 CLI/env、普通 receipt/nonce、调用方 previous Manifest 或 Manifest 自声明 approval 作为可信 host capability，Legacy direct mode 不变。

## Migration Map

| v0.3.2 ID | v0.3.3 ID | Kind |
| --- | --- | --- |
| `product-discovery` | `problem-to-solution` | Workflow |
| `product-delivery` | `solution-to-delivery` | Workflow |
| `research-decision-loop` | `decision-loop` | Loop |
| `solution-challenge-loop` | `solution-loop` | Loop |
| `prd-delivery-readiness-loop` | `delivery-loop` | Loop |

旧 ID 仅保留在 migration/archive 记录中；Runtime 只安装新 ID。

## Required Gates

| Gate | Required result | Fresh evidence |
| --- | --- | --- |
| Repository structure and catalog | PASS | `audit_skills.py`：15 Skills + 5 composition adapters，无 hard error；`check_v03_asset_catalog.py`：15/3/2/4/4 |
| Five package structure checks | PASS | `skill-reviewer/check_skill.py` 对 2 Workflow + 3 Loop 全部通过 |
| Routing regression and holdout | No P0/P1 | 新入口 15/15，v0.3.2 基线 12/15；3 项有效区分，12 项回归保护 |
| Full Python regression | PASS | 12 个活跃测试文件，162/162；显式设置 validator 后 0 skipped |
| Independent CR | `Ready` | Pending |
| GitHub PR and CI | Merged / green | Pending |
| `v0.3.3` tag and Release | Published and read back | Pending |
| Skillshare dry-run scope | Only five new IDs and approved old-ID cleanup | Pending |
| Local source/target parity | Five new IDs present, five old IDs absent | Pending |
| Codex discovery | Five new IDs visible; explicit-only policy retained | Pending |

## Release And Rollback

- 发布源只允许远端 `main` 的合并提交；不得从 feature branch 或 Skillshare 聚合目录发布。
- Git 回滚点为 `v0.3.2` tag。回滚代码不自动恢复本地 Runtime，需使用 Skillshare 已登记来源重新安装旧版或回退到新入口发布前的本地备份。
- 如果 Skillshare dry-run 出现目标五项之外的 create/update/prune，停止正式同步，不通过临时隐藏其他 Skill 绕过。
- 本次只验证 Package Publisher 的 dry-run 与 fail-closed 边界，不执行 DingTalk/Yunxiao 写入；没有外部数据恢复责任。

## Final Evidence

发布后的 PR/merge commit、tag/Release URL、独立 CR verdict、Skillshare targets、dry-run 明细和本地 discovery 结果记录在 `v0.3.3` GitHub Release；本文件保留进入 CR 前的可复现门禁证据，避免把未发生的外部结果预写成事实。
