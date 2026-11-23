# 可视化案例数据契约 v1

## 分工与使用

LLM 负责理解用户要求、定位证据与诊断；确定性脚本负责校验引用、统计投影记录、附件打包、折叠、跳转和渲染。不要让 LLM 为每条日志生成页面代码。不同日志格式通过一次性或可复用 adapter 转成同一契约；不承诺能自动解析任意供应商 trace。

用户要求 HTML 时：

1. 先脱敏，再把所需消息、事件、证据与分析整理成 `case.json`。已有投影则复用；不要让模型重写整份原始日志。
2. `python3 <skill>/scripts/render_report.py case.json --validate-only`
3. `python3 <skill>/scripts/render_report.py case.json --output-dir <new-report-dir>`
4. 打开 `<new-report-dir>/index.html`。报告目录含脱敏数据包、引用到的本地附件；离线可读，无 CDN、远程字体或运行服务依赖。
5. 验证默认对话、过程/参数/JSON逐层折叠、分析定位与返回、缺失数据说明、手机布局和附件可读。静态脚本成功不等于浏览器验收。

运行 `--help` 查看用法。输出目录必须不存在；脚本不覆盖报告，不下载附件，不访问生产，不自动生成分享链接。结构校验失败时补齐投影或说明限制，不绕过校验手写 HTML。

## 顶层结构

可执行最小样例见 `tests/fixtures/case.json`，全部为合成数据，不能当生产事实。

| 字段 | 内容 |
| --- | --- |
| `schema_version` | 固定 `1`，未知版本拒绝 |
| `case` | `id`、`title`、`request`、`inputs`、`expected`、`actual`、`coverage`，均为非空字符串。后六项是明确标示的案例事实摘要，缺失写“未取得/未核验”，不假装原话 |
| `sources[]` | `id`、`label`、`locator`；来源定位显示为文本，不自动打开生产页面 |
| `messages[]` | 按原会话顺序的 `id`、`role`、`text`、`origin`、`source_ids`，可有 `attachments[]` |
| `events[]` | 按投影顺序的 `id`、`kind`、`name`、`status`、`after_message_id`、`source_ids`；可有时间、真实 `parent_id`、`input`、`output`、`fields[]` |
| `evidence[]` | `id`、`status`、`text`、`source_ids`、`message_ids`、`event_ids`。所有引用须存在；未知证据可以没有来源 |
| `analysis` | `conclusion`、`findings[]`、`flow`；独立于消息、事件，不伪装成助手输出 |

无消息时 `messages: []`；`events[].after_message_id` 为 `null`，页面明确“原始对话未取得”，仍能检查事件。末尾缺失答复不能补造最终消息。数组未覆盖全部日志时必须在 `case.coverage` 说明范围；页面统计只称“本页投影”。

## 消息与事件

- `role`：`user` / `assistant`。`origin`：`trace` / `client` / `tool-interaction` / `summary`。摘要在页面明确标记，不能冒充原话。系统提示词和隐性思考不放入消息。
- `kind`：`model` / `tool`。模型名和工具名分别记录，不把标题生成/辅助模型混作主模型。
- `status`：`recorded` / `returned` / `error` / `rejected` / `unknown`。`returned` 只表示工具返回，不代表生成成功。
- `after_message_id` 只决定事件展示在何条消息之后，不证明发起调用的原生父子关系。它在事件数组中必须保持会话顺序，不能来回穿插重排。
- `parent_id` 可省略；只有原始日志明确记录时才填，并要求父项已经存在于事件序列，不能基于相邻时间推断。
- 可选 `time` 为原样显示的带时区文本；不转换成“思考用时”。
- `input` / `output` 保留脱敏投影。大块正文在上游投影中明确省略原因，不在 renderer 静默截断。不要把未记录输出设为业务成功。
- `fields[]` 为 `{ "label": "请求模型", "pointer": "/input/arguments/modelVersion" }`。使用 JSON Pointer 直接从事件输入/输出取值，不接受模型另填一份可能不一致的值。指针缺失即校验失败。
- 例如 requested model 来自输入，actual model 来自服务返回；无实际型号就不创建假字段，在事实/诊断说明未知。`auto` 原样显示，不映射成供应商型号。

## 证据与诊断

- 证据 `status`：`confirmed` / `inferred` / `unknown`，页面显示“已确认/推断/待验证”。`confirmed` 只证明证据条目的具体内容，不自动证明诊断机制。
- 每条 finding：`id`、`title`、`role`、`certainty`、`fact`、`impact`、`recommendation`、`verification`、`evidence_ids`。可选 `mechanism`。
- finding `role`：`failure-point`、`root-cause-candidate`、`root-cause`、`amplifier`、`opportunity`、`unknown`。
- `root-cause-candidate` 的 certainty 只能是 `inferred` / `unknown`。只有 `root-cause` 要求 `certainty: confirmed`、非空 `mechanism` 和至少一条已确认的证据。这是必要条件，不是因果已被自动证明；仍需人工/语义核验。
- 诊断点击证据，证据再定位实际消息/调用。保留稳定 ID，不以当前页面行号代替来源 ID。
- `flow.nodes[]`：`id`、`label`、`evidence_ids`，可选 `finding_id`。`flow.edges[]`：`from`、`to`、`relation`（`observed` / `inferred`）。图为有向无环压缩图，循环应合并并保留次数；模板布局不增补任何边。
- 图中节点引用 evidence，诊断标签来自 finding。实线表示记录顺序，虚线表示推断关系，均不能单靠箭头证明因果。
- `flow` 可以是空节点/空边，并给非空 `note` 说明证据不足或省图理由；不为美观补造路径。

## 附件与安全

- `attachments[]`：`id`、`name`、`status`（`available` / `missing` / `redacted`），可有 `path`、`thumbnail`、`note`。
- `available` 的 `path` 必须是相对 `case.json` 所在目录的真实文件；拒绝绝对路径、`..`、外链及越界符号链接。`thumbnail` 同样受检。
- 脚本按文件字节哈希复制附件到报告目录，保留下载入口。内联只预览 PNG/JPEG/WebP/GIF，其他格式仅提供本地文件链接，不执行 HTML/SVG。
- 大图先在上游制作合适缩略图并填 `thumbnail`；没有附件授权时保持 `missing/redacted`，不要自动补抓签名 URL。
- 内容始终转义，CSP 禁止网络连接。仍须在输入前检查凭据、签名 URL、客户数据、隐藏思考与不应共享的本地路径；模板不会自动识别全部秘密。
- 发布只含通用技能、模板和合成 fixture。真实输入、附件、报告和截图留在用户授权的本地目录，不进入公开仓。
