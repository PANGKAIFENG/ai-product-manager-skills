# PRD Diagram Review

当 PRD 包含或应当包含流程图、架构图、系统关系图、AI 协作链路图时，图示是一等 review 对象。

## Need Check

- `PRD-lite`：简单局部改动不强制 Draw.io，优先文字步骤、表格、Mermaid 草稿、真实页面截图或 HTML mockup。
- `PRD-standard`：多阶段链路、模块依赖、上下游输入输出时，应考虑核心流程图或结构图。
- `PRD-ai-native`：人工动作、AI 动作、状态反馈、记忆写入、失败回退形成闭环时，应考虑一体化总图或核心流程图。

## Reference Check

正式 Markdown 引用应指向：

- 根目录 `*.drawio.svg`。
- 或明确的可编辑 Draw.io 产物。

注意：

- `src/*.drawio` 可以作为源文件，但不应成为 PRD 阅读主引用。
- 不要把普通 `.svg`、截图、PNG 或 Mermaid 当作可编辑 Draw.io 图示。
- 如果只有截图，应标记为“视觉参考”，不要说它可编辑。

## Support Check

图示必须回答“系统是什么”或“链路怎么跑”，不能只是装饰性大图。

检查：

- 节点、边、输入输出、关键分支和异常回退能否对应 PRD 正文。
- 图和正文是否冲突。
- 图是否过重、过散，是否应该拆成一体化总图、核心流程图或子流程图。

## Editability Check

有 `.drawio` 源文件时运行：

```bash
python3 scripts/validate_drawio.py <path>
```

需要判断布局、节点数、颜色或 XML 模板时读取 `references/drawio-templates.md`。

如果有 `*.drawio.svg` 但无法验证内嵌数据，标记“图示可编辑性未验证”，不要默认通过。

## Repair Suggestions

- 缺图：给出应补图类型、图要覆盖的核心节点和建议文件名。
- 图不可编辑：建议迁移到 `.drawio` / `*.drawio.svg`。
- 图与正文冲突：指出冲突章节，按阻断或重要问题处理。
- 图过重：建议拆分或收敛到评审真正需要的主链路。
