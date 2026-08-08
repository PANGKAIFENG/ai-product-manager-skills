# StyleWork 来源与版本清单

## Snapshot

更新日期：2026-07-24。

| 证据 | 位置/版本 | 证据等级 | 可用于 | 限制 |
| --- | --- | --- | --- | --- |
| StyleWork 审计仓库正式开发线 | 维护者本地审计 checkout，`origin/dev@b454d7896cd81206954bc350ff694b6735ad8d62`，2026-07-20 | 高 | 后端能力、Skill/Plugin、业务工作流、固定子模块版本 | 本地路径不属于公开合同，且仍需以实际部署版本校验 |
| 正式前端子模块指针 | `openwork@2549c939e42f9650265801a9a864ed3f2b3b6866` | 中 | 确认正式线固定了哪个前端提交 | GitLab 源码当前不可访问，不能验证该提交的菜单与组件细节 |
| 本地集成前端 | 同一审计仓库 `local/prd-backup@ede43a23001fc7b9b141da58cb56123bbe1475bd`，且工作区存在未提交改动 | 低/临时 | 理解候选 shell、会话、任务进度和 artifact UI | 不得视为正式发布或当前线上能力 |
| UI 原生预览资料 | `docs/PRD/styleclaw-agent-planning-policy/ui-runtime-visible-handoff/` | 低/设计证据 | Demo 布局、组件复用、状态模型 | 文档明确标注 `structure-assumed` 和 preview-only |
| 代表性预览截图 | `.../screenshots/preview-styleclaw-runtime-1440x900.png` | 低/视觉证据 | 理解三段式工作台与信息密度 | 不是线上截图 |

## 代码证据例

正式开发线中可核验的代表性来源：

- `dockerize/sandbox/opencode-template/plugins/stream-search/`：款式/面料检索管线与 `resource-picker`。
- `dockerize/sandbox/opencode-template/plugins/asset-library-search/skills/fabric-search/`：面料自然语言筛选与结果卡。
- `dockerize/sandbox/opencode-template/plugins/media-generation/skills/style-img-gen/`：款式图片生成。
- `dockerize/sandbox/opencode-template/plugins/media-generation/skills/image-to-video/`：图片转视频。
- `dockerize/sandbox/opencode-template/plugins/media-generation/skills/style-media-workflow/`：媒体工作流。
- `dockerize/sandbox/opencode-template/plugins/media-generation/skills/product-catalog-gen/`：结构化 artifact 输出示例。

## 使用规则

1. 产品能力判断优先使用正式开发线；本地集成分支只能补充产品结构和设计意图。
2. 无法读取正式前端源码时，必须写“UI 适配待正式版本验证”，不能凭截图确认菜单或组件已上线。
3. 客户需求不能反向成为“现有能力”的证据。
4. 代码、正式发布记录或产品负责人确认发生变化时，更新提交号、日期、能力变化和受影响判断。
5. 对外输出不暴露本地绝对路径；只说明“基于 2026-07-20 开发线快照”及必要限制。

## Refresh Checklist

- 拉取远端并记录最新正式分支提交；
- 核对前端子模块是否可访问以及实际提交；
- 检查代表性 Skill/Plugin 是否仍存在；
- 查看现有产品界面或正式截图；
- 更新现有、复用、配置、扩展、新建和技术验证判断；
- 对历史 Demo 与客户材料标记是否需要重评。
