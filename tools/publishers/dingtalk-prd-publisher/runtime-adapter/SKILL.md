---
name: dingtalk-prd-publisher
description: "Use when publishing local PRD Markdown files or an approved Product Delivery Package manifest to DingTalk Docs or Drive, especially when the delivery has an explicit content/HTML/screenshot allowlist, payload fingerprint, related prototype, or browser verification requirement."
---

# 钉钉 PRD 发布器（dingtalk-prd-publisher）

## 中文速查

- 中文名：钉钉 PRD 发布器 / PRD 证据截图发布
- 分类：产品交付 / PRD 发布
- 你可以这样叫我：`把这个 PRD 发到钉钉文档`、`PRD 里有 Look up 地址，截图后插进去再上传钉钉`、`把本地 PRD 发布到指定钉钉目录`
- 适合：本地 Markdown PRD、关联 mock / Look up / HTML 预览、截图证据、默认钉钉 PRD 锚点目录或用户指定目录发布。
- 不适合：从零写 PRD、评审 PRD 内容、创建钉钉表格/AI 表格、删除或覆盖已有钉钉文档。

## Overview

这个 Skill 把“本地 PRD → 发布版清理 → 关联页面截图 → 插图后的 PRD copy → 最新 HTML 前置附件 → 钉钉文档/钉盘发布 → 浏览器可见性验证”固化成可重复流程。默认保护源文件：不覆盖原 PRD。用户没有指定钉钉目标时，默认在“智能体需求文档”锚点下创建一篇需求专属二级文档并写入 PRD，避免每次重复粘贴目录地址。

对 Product Delivery Package，必须使用显式 `--manifest` mode。它只消费 `product-delivery-manifest.yaml` 中通过确定性 validator 校验的 content / HTML / screenshot allowlist 和目标，不执行 sibling discovery，也不接受 CLI 改写 title、target 或 artifact。Legacy direct mode 保持兼容，但不能替代 Package approval、payload fingerprint 或状态记录。

真实钉钉操作必须加载并遵守 `dws` Skill；浏览器截图问题需要加载 `playwright` Skill排查。DingTalk 写入以本地 `dws --help/schema` 为准，不猜命令或 flag。

## Required Inputs

优先从用户消息或本地文件发现，不足时最多问 3 个问题：

- PRD Markdown 路径。
- Product Delivery Package：Manifest 路径、`prd-architect` 的 canonical validator 路径，以及 Human approval 绑定的 `publish_payload_fingerprint`。这三项均不可由 Publisher 自行推断。
- 钉钉目标：默认可省略；省略时使用默认父节点 `https://alidocs.dingtalk.com/i/nodes/MNDoBb60VLrdedxLSrZmae9N8lemrZQ3?utm_scene=team_space`（智能体需求文档），并在其下直接创建需求专属二级文档。需要覆盖时传 `--parent <alidocs node URL/nodeId>`、`--folder <folder URL/nodeId>` 或 `--workspace <workspaceId>`。
- 发布方式：默认 `doc` 在线文档；需要保留原文件时用 `file` 上传。
- 源文件策略：默认生成 enriched copy；只有用户明确要求才覆盖源 PRD。
- HTML 策略：在线文档模式默认选择 enriched PRD 同目录修改时间最新的 `.html` / `.htm`，作为正文第一个附件块；用 `--html <file>` 明确指定，用 `--no-html` 关闭。显式路径不存在时必须在创建钉钉文档前失败。
- 截图策略：默认用 Playwright 抓真实截图；网络或登录态受限时先报告 blocker，不伪造截图。
- 发布版清理策略：默认从钉钉正文移除 `待确认事项`、`关联产物`、文档信息里的 `关联 mock` 本地路径、失败图和本地-only 链接；只有用户明确要求保留草稿信息时才关闭。

## Workflow

Product Delivery Package 先走独立分支：

```bash
<skill>/scripts/publish-prd \
  --manifest "<PACKAGE>/product-delivery-manifest.yaml" \
  --validator "<prd-architect>/scripts/validate_product_delivery_manifest.py" \
  --expected-payload-fingerprint "<HUMAN_APPROVED_SHA256>" \
  --actor-identity "<PUBLISHER_RUN_ID>" \
  --dry-run
```

- Dry-run 必须完成 Manifest、Package verdict、publish approval、payload fingerprint、artifact 路径/hash 和 allowlist 校验，且 `dws` 调用数为 0。
- 真实执行仅允许在相同参数去掉 `--dry-run` 后发生；CLI 不得再传 Markdown、target、title 或 HTML override。
- 创建成功后立即记录 `nodeId`；媒体失败时记录 attempt，重试复用同一 `nodeId` 并跳过 `completed_artifact_refs`。
- create 结果未知且没有 `nodeId` 时 fail closed，必须先 lookup/read-back 并把远端身份记录回 Manifest，不能盲目重建。
- `doc` 模式的 read-back 必须匹配当前 `nodeId`、批准标题和正文关键标题；`file` 模式必须用 `doc info` 匹配 node 和文件名。通过后只进入 `published_unverified`。只有独立 browser actor 生成且绑定当前 node、URL 和 payload fingerprint 的结构化证据通过后，才可用 `--browser-evidence <json>` 进入 `verified`；Publisher 不能自证可见性。

以下步骤用于 Legacy direct mode 和 Package 上游的 enriched copy 准备：

1. Inspect source PRD.
   - 确认文件存在、是 Markdown、源 PRD 不会被覆盖。
   - 识别 `Look up`、`lookup`、`mock`、`原型`、`预览`、`关联产物`、`.html`、URL 或本地 HTML 路径。
   - 相对路径按 PRD 所在目录解析。
2. Dry-run lookup discovery.

```bash
python3 <skill>/scripts/enrich_prd_with_screenshots.py "<PRD.md>" --dry-run --json
```

3. Capture screenshots and create enriched copy.

```bash
python3 <skill>/scripts/enrich_prd_with_screenshots.py "<PRD.md>" --json
```

默认输出：

- `<PRD stem>.dingtalk.enriched.md`
- `<PRD stem>.dingtalk-assets/*.png`
- enriched copy 默认是钉钉发布版：移除 `待确认事项`、`关联产物` 和文档信息里的本地 mock 行；源 PRD 不覆盖。

4. Review placement.
   - 同一链接多处出现时只截图一次。
   - 优先把截图插到对应功能模块、页面状态或交互章节；不要优先放到 `关联产物`、文档信息表或本地 mock 索引。
   - 图片块带 `<!-- dingtalk-prd-screenshot: ... -->` marker，方便发布后定位。
5. Pre-publish lint.
   - 发布前检查 enriched copy 不应残留 `待确认事项`、`关联产物`、`关联 mock`、本地 `.html`、本地 `.png`、`dingtalk-assets`、`file://`、`localhost` 等正文入口。HTML 通过附件块发布，不依赖正文里的本地路径。
   - 如果这些内容是用户明确要求保留的草稿材料，先说明会影响钉钉正文阅读，再继续。
6. Publish with dws wrapper.

Default path when the user does not provide a DingTalk target:

```bash
<skill>/scripts/publish-prd "<ENRICHED.md>" --name "<PRD title>" --read-back
```

This resolves the default parent anchor. For the default `ALIDOC/adoc` anchor, it creates the DingTalk Doc directly as a second-level child; ordinary folder targets keep the optional per-run-folder behavior. In online-doc mode, the wrapper then inserts the newest sibling HTML at document index `0` before read-back.

显式指定原型或关闭自动附件：

```bash
<skill>/scripts/publish-prd "<ENRICHED.md>" --html "<APPROVED.html>" --name "<PRD title>" --read-back
<skill>/scripts/publish-prd "<ENRICHED.md>" --no-html --name "<PRD title>" --read-back
```

```bash
<skill>/scripts/publish-prd "<ENRICHED.md>" --folder "<DINGTALK_FOLDER_URL>" --name "<PRD title>" --read-back
```

或上传源文件：

```bash
<skill>/scripts/publish-prd "<ENRICHED.md>" --mode file --folder "<DINGTALK_FOLDER_URL>"
```

7. Verify DingTalk result.
   - `publish-prd --read-back` 后检查关键标题、表格、截图 marker 或图片附件是否存在。
   - 如果选中了 HTML，检查 `dws doc media insert` 返回 `success=true` 且 `index=0`；再用 block list 和浏览器确认 HTML 附件确实位于正文第一个块，可打开或下载。
   - 如果本地 Markdown 图片没有在钉钉正文渲染，不要报告完成；改走 `dws doc media insert`，用 `dws doc block list --content-format jsonml` 找到 marker/caption 附近 block，再把截图文件插到对应 block 后。
   - 所有 PRD 发布到钉钉后，都必须打开 `docUrl` 做浏览器可见性验证；检查首屏、关键模块图片、底部是否无不需要章节、页内搜索敏感残留词是否为 0。
   - 最终返回 `docUrl` / nodeId、enriched PRD 路径、截图路径和验证结果。

## DingTalk Rules

- Package mode 只接受 canonical validator 输出的 allowlist；禁止自动发现最新 sibling HTML，禁止上传未列入 Manifest 的文件。
- Package mode 的 `file` 只上传正文文件，因此 HTML / screenshot allowlist 必须为空；需要媒体交付时必须使用 `doc`，不能批准后静默漏发。
- Package mode 在任何 `dws` 调用前校验独立 Reviewer 的 `ready` verdict、`content` / `artifacts` / `publish` 三项检查、Human approval 和精确 payload fingerprint；失败时不得改写 Manifest。
- Package mode 的 Publisher 只能通过 validator 记录 `release.dingtalk`、`last_transition` 和派生状态，不能改 artifacts、review 或 approval。
- Package mode 只保留最近一次状态迁移和最多 20 次 publish attempts；部分失败恢复必须复用已有 `nodeId`。
- Package mode 的 parent 解析失败必须记录 `target_resolution` failure，使下一 attempt 可从 `publish_failed` 恢复，不能卡在 `publishing`。
- 写钉钉前先确认 `dws auth status --format json` 已登录。
- 命令输出必须用 `--format json`；不确定命令时先跑 `dws <cmd> --help`。
- `doc create` 用于在线文档；`drive upload` 用于上传文件。
- 在线文档默认自动附带同目录最新 HTML；选择顺序是 `--html` 显式文件优先，其次同目录修改时间最新的 `.html` / `.htm`。不要递归扫描上级目录或整个项目，避免上传无关原型。
- HTML 必须在 `doc create` 成功后用 `dws doc media insert --index 0` 插入，并在普通正文 read-back 前完成。`--dry-run` 只报告选中文件，不上传；`--mode file` 不存在正文块，不自动附加 HTML。
- 默认父节点是 `https://alidocs.dingtalk.com/i/nodes/MNDoBb60VLrdedxLSrZmae9N8lemrZQ3?utm_scene=team_space`（智能体需求文档）。先用 `dws doc info --node <url> --format json` 探测；如果它是可挂子文档的 `ALIDOC/adoc` 节点，直接使用返回的 `nodeId` 作为 `doc create --folder`，创建需求专属二级文档；不要尝试在该节点下创建文件夹。普通文档文件夹仍按原有规则处理。
- 默认 `ALIDOC/adoc` 父节点下直接创建一篇二级 PRD 文档，不额外创建文件夹。普通目录目标需要隔离每次发布时，运行文件夹命名为 `<PRD title> <YYYYMMDD-HHMM>`；用户给 `--folder` 时默认直接发布到该目录，明确要求再建子目录时加 `--create-run-folder`。
- 用户自然语言给一个钉钉链接并说“建到下面 / 放到下面 / 创建到这个目录下”时，按 `--parent <url>` 处理：`ALIDOC/adoc` 锚点下直接创建二级文档，普通目录按运行文件夹规则处理；只有用户明确说“直接放到这个目录”时才按 `--folder <url>` 直接发布。
- 可用 `DINGTALK_PRD_DEFAULT_PARENT` 临时覆盖默认父节点，用 `--run-folder-name` 固定本次发布文件夹名，用 `--no-create-run-folder` 禁止自动建目录。
- `--folder` 只传文档文件夹 nodeId / alidocs 文件夹 URL；不要传纯数字 dentryId、drive parent-id 或 spaceId。
- 大内容或真实发布后必须回读校验。`success=true` 不等于内容完整。
- 所有 PRD 发布后必须浏览器打开验证可见性；`dws read-back` 只能证明服务端内容存在，不能替代真实页面图片和排版检查。
- 没有明确目标目录时，不再默认发到根目录；使用默认父节点创建需求专属二级文档。若用户要求禁用默认父节点且又没有目标，必须先 `--dry-run` 并追问。
- 删除、覆盖已有文档、改权限等不属于本 Skill 默认范围；需要另行确认并切换到对应 dws 文档流程。

## Resource Guide

- `scripts/enrich_prd_with_screenshots.py`：发现 PRD lookup/mock/HTML 链接，Playwright 截图，默认清理本地-only 发布污染，生成 enriched Markdown copy。
- `scripts/publish-prd`：封装 `dws doc create` / `dws drive upload`；Legacy direct mode 支持 sibling HTML，显式 Package mode 只消费 Manifest allowlist，并记录 attempt、恢复和 read-back 状态。
- `scripts/test_enrich_prd_with_screenshots.py`：本地回归测试，覆盖重复 mock 链接去重、语义章节优先插图和发布版清理。
- `scripts/test_publish_prd.py`：本地回归测试，覆盖默认 `ALIDOC/adoc` 父节点下直接创建二级文档，以及普通 `--folder` 的直接发布和可选子目录行为。
- `references/prd-image-placement-rules.md`：截图识别、去重、插入位置和 marker 规则。
- `references/dingtalk-publish-workflow.md`：钉钉发布、图片正文插入和验证流程。
- `references/provenance.md`：原型脚本来源、创建记录和维护边界。

## Output Contract

完成后输出：

- Source PRD：原始文件路径。
- Enriched PRD：生成的 enriched copy 路径。
- Screenshots：每张截图对应的源链接、截图文件、插入章节。
- HTML attachment：选中的 HTML 路径、选择方式（显式 / 最新同目录）、附件文件名、插入索引与验证结果；没有候选或主动关闭时明确说明。
- DingTalk publish：目标 folder/workspace、创建方式、`nodeId` / `docUrl`。
- Verification：dry-run / screenshot / dws read-back / media insert / browser visibility 结果。
- Package mode：Manifest 路径、input / payload fingerprint、三项 Package verdict、最近 transition、attempt 结果和最终 `published_unverified` / `verified` 状态。
- Remaining gaps：登录态、图片未渲染、目标目录不明确或权限失败等。

## Definition Of Done

- 已发现 PRD 内所有候选 Look up/mock/HTML/URL 目标，或明确说明未发现。
- 已生成 enriched copy；源 PRD 未被静默覆盖。
- 在线文档模式已显式选择 HTML、自动选择最新同目录 HTML，或确认没有候选 / 用户已关闭；选中时附件位于正文第一个块。
- 截图文件存在且与目标链接一一对应；失败时报告具体 URL 和错误。
- 真实发布前目标 folder/workspace 明确，或用户确认默认位置。
- 未指定目标时已使用默认父节点创建需求专属二级文档，或明确说明该步骤因权限/类型受阻。
- 发布后已 read-back；关键标题和截图/附件存在性已验证。
- 如果钉钉正文图片未渲染，已用 `doc media insert` 补齐或把该问题列为未完成 blocker。
- 已用浏览器打开钉钉 `docUrl` 做可见性验证；确认关键模块图片可见、没有失败图、底部没有 `待确认事项` / `关联产物` / 本地 mock 链接等不应发布内容。若登录态或权限阻止浏览器验证，必须作为未完成 blocker 报告。
- Package mode 发布前已由 canonical validator 确认 current verdict、Human approval、payload fingerprint、allowlist 路径/hash；任何失败均发生在首个 `dws` 调用前。
- Package mode 的 read-back 已匹配当前 node、批准标题及正文关键标题或文件元信息，且未被误报为 `verified`；独立且绑定当前 payload 的 browser evidence 缺失时停在 `published_unverified`。
- Package mode 的失败 attempt 可在同一 `nodeId` 上恢复，且未重复发布已完成 artifact；未知 create 结果未触发第二次创建。

## Evaluation

Smoke prompts:

- `把 /path/PRD.md 发布到这个钉钉目录，里面的 mock 页面先截图插进去。`
- `这个 PRD 里有 Look up 地址，打开截图，放回对应章节，然后发钉钉文档。`
- `先 dry-run 看看会抓哪些截图，不要发布。`
- `把这个 PRD 发到默认钉钉目录，每次自动新建一个文件夹。`
- `把这个 PRD 发到钉钉，上传后打开浏览器检查图片和底部模块。`

Non-trigger prompts:

- `帮我写一个 PRD。`（用 PRD 起草 Skill）
- `帮我评审这个 PRD。`（用 PRD 评审 Skill）
- `上传一个普通 PDF 到钉盘。`（直接用 dws drive）

Regression checks:

- `EVAL-B2-05`：失效 approval 或 payload fingerprint 必须使 `dws` 调用数为 0，Manifest 不变。
- `EVAL-B2-06`：只发布 allowlist artifact；媒体中途失败后复用同一 `nodeId`，跳过已完成 artifact，不上传更新但未列入清单的 sibling HTML。
- `EVAL-B2-07`：read-back 后状态只能是 `published_unverified`；独立结构化 browser evidence 通过后才进入 `verified`。
- `EVAL-B2-08`：路径 traversal 或 CLI target override 在任何副作用前失败，且不改 review / approval 分区。
- Package `file` mode 带非空 HTML / screenshot allowlist 时必须在首个 `dws` 调用前失败。
- Package parent 解析失败必须进入可重试的 `publish_failed`，修复 target 后下一 attempt 可以继续且不重复 create。
- 同一 mock 链接同时出现在文档信息表、功能模块和“关联产物”时，只截图一次，并优先插到功能模块。
- enriched copy 默认去掉 `待确认事项`、`关联产物` 和文档信息表里的本地 `关联 mock` 行。
- 相对 HTML 路径必须按 PRD 目录解析，而不是当前 shell 目录。
- `--dry-run` 不创建截图、不写 enriched copy、不发布钉钉。
- `--html` 必须覆盖自动发现；没有显式参数时只在 PRD 同目录选择修改时间最新的 `.html` / `.htm`；`--no-html`、无候选和 `--mode file` 不调用 `doc media insert`。
- HTML 附件必须使用 `doc media insert --index 0`，插入成功后再执行 PRD read-back；不能把“正文已移除本地 HTML 路径”误报为“HTML 已交付”。
- 未指定目标目录时必须使用默认父节点创建需求专属二级文档，不得静默发布到根目录。
- 显式传 `--folder` 时默认不额外创建子目录；加 `--create-run-folder` 才在该 folder 下再建本次发布目录。
- 真实发布后必须执行浏览器可见性验证，不能只以 `dws doc read` 成功作为完成。

## Catalog Notes

- Category: product delivery / PRD operations.
- Status: `active`.
- Public boundary: the adapter is public, but credentials, target node IDs, unpublished PRDs, screenshots, customer data, and real publish evidence must remain local unless explicitly approved for disclosure.
