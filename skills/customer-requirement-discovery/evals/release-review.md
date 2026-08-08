# Release Review

评审日期：2026-07-24
评审模式：release-gate

## Evidence Summary

- 检查对象：`SKILL.md`、`agents/openai.yaml`、全部 `references/`、`assets/demo-brief-template.md`、`evals/`、仓库 Registry、Routing、README 和契约测试。
- 确定性检查：system `quick_validate.py`、`skill-reviewer/scripts/check_skill.py`、新 Skill 契约测试、权威仓库全量单元测试和 `git diff --check`。
- 行为证据：三组无 Skill 红灯基线和五组带 Skill 前向测试，覆盖通用模糊需求、StyleWork 条件上下文、过早 Demo、一次性客户清单和客户回复回收。
- 证据限制：行为测试为语义评审，不代表真实客户环境、外部平台 API、生产数据或模型效果验证；StyleWork 正式前端源码当前不可访问，UI 仅使用已标注为临时的本地证据。

## Verdict

Ready。没有 P0/P1 问题；Skill 的触发、访谈上限、阶段路由、StyleWork 条件上下文、Demo 边界和下游交接均有可检查契约及回归证据。

## Highest Priority Issues

- [P2][observed] StyleWork 产品与 UI 参考会随正式开发线变化而过期。影响：未来适配判断可能基于旧快照。处理：每次涉及正式方案或 Demo 前按 `stylework-source-manifest.md` 的 Refresh Checklist 刷新版本，不把临时前端证据升级为已上线能力。
- [P2][inferred] 语义行为仍依赖模型判断信息增益和问题质量。影响：不同运行时可能产生措辞和选题差异。处理：保留红灯基线、前向测试和数量契约；重大修改后重跑真实 prompt，并由产品或售前人工复核客户外发清单。

## Scorecard

| Dimension | Score | Notes |
| --- | ---: | --- |
| Necessity and boundary | 5 | 高频团队场景，和报价、PRD Skill 边界明确 |
| Trigger contract | 5 | 包含自然语言角色、使用情境和非触发边界 |
| Input/output contract | 5 | 内部轮次、客户清单、回复回收和 Demo 产物明确 |
| Workflow gates and degrees of freedom | 5 | 最多五轮、提前停止、条件加载和交接门槛明确 |
| Progressive disclosure and assets | 5 | 通用方法、StyleWork 上下文和模板按需拆分 |
| Context budget | 5 | `SKILL.md` 低于 500 行，参考链仅一层 |
| Tool, permission, and safety boundary | 4 | 明确非生产、无虚假接入和不承诺边界；具体 Demo 工具按运行时选择 |
| Evaluation readiness | 5 | 包含 smoke、regression、non-trigger、红灯基线、前向测试和契约测试 |
| Maintainability and governance | 5 | 稳定名、统一公开来源、Registry、Routing、README 和版本清单齐全 |

平均分：4.9 / 5。

## Eval Checklist

- 首轮内部问题保持 1-3 个，最多五轮，信息足够时提前结束。
- 客户清单必答不超过 8 个、选答不超过 5 个。
- 通用技术可行性与 StyleWork 适配分开输出。
- StyleWork 资料只在明确相关时加载，并保留证据版本与限制。
- 信息不足时不直接制作 Demo；强制先做时输出 Demo Brief、显式假设、模拟数据和非生产声明。
- 报价范围只在需求达到可交接成熟度后进入当前项目或人工商务流程，不再拆出独立 Skill；正式需求交给 PRD 工作流。

## Release Decision

发布。P2 作为持续维护项，不阻塞统一公开仓合并与本地多运行时同步。
