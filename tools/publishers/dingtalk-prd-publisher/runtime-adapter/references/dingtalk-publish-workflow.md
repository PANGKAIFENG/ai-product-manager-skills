# DingTalk Publish Workflow

Use this reference after an enriched PRD copy exists and the user wants it published to DingTalk Docs or Drive.

## Product Delivery Package Mode

When `product-delivery-manifest.yaml` exists, use the explicit Package path instead of Legacy direct mode:

```bash
<skill>/scripts/publish-prd \
  --manifest "<PACKAGE>/product-delivery-manifest.yaml" \
  --validator "<prd-architect>/scripts/validate_product_delivery_manifest.py" \
  --expected-payload-fingerprint "<HUMAN_APPROVED_SHA256>" \
  --actor-identity "<PUBLISHER_RUN_ID>" \
  --dry-run
```

The preflight is fail closed and runs before `dws auth status` or any other DingTalk call. It requires a current independent Package verdict with exactly `content`, `artifacts`, and `publish` checks passed; a Human publish approval bound to the derived payload fingerprint; valid relative artifact paths and hashes; a publishable Package state; and a valid PRD version history table. A failed preflight must leave both DingTalk and the Manifest untouched.

Package mode consumes only the ordered content / HTML / screenshot allowlist, title, mode, and target emitted by the canonical validator. Do not add a positional Markdown path, `--parent`, `--folder`, `--workspace`, `--name`, or `--html`. In particular, do not discover or publish a newer sibling HTML that is absent from the Manifest.

Package `file` mode accepts an empty HTML/screenshot allowlist only because it uploads the content file as one Drive object. Use `doc` mode when the approved payload includes HTML or screenshots; fail before any `dws` call rather than silently dropping media.

The current Agent Runtime stops here. Removing `--dry-run` returns `authorization_required` before any `dws` call or Manifest mutation because the host cannot inject an approval capability that the Agent cannot forge. CLI flags, environment variables, ordinary receipt or nonce files, caller-supplied previous Manifests, and the approval object inside the current Manifest are not trusted host capabilities.

Do not fall back to Legacy direct mode for a Package. The validator retains a publish-event, retry, read-back, and browser-verification state model for a future trusted host integration, but this wrapper does not execute that state model in v0.3.3.

Legacy direct mode below remains available only when the user explicitly chooses non-Package direct publishing. Its sibling HTML discovery and direct CLI target selection do not apply to Package mode and cannot be used as a Package bypass.

## Preflight

1. Validate the PRD version history before auth or target discovery:

```bash
python3 <prd-architect>/scripts/check_prd_version_history.py "<ENRICHED.md>"
```

The first H2 after the title must be `版本记录`; the table columns are `版本 / 日期 / 修改内容`; versions are newest-first; the oldest row is `V1.0` with `首次创建`; and change summaries are concrete. The Publisher does not repair the table. Return invalid content to `prd-architect`.

2. Confirm the target behavior:
   - If the user gives no target, use the default parent anchor `https://alidocs.dingtalk.com/i/nodes/MNDoBb60VLrdedxLSrZmae9N8lemrZQ3?utm_scene=team_space` ("智能体需求文档") and create the requirement PRD as a direct second-level child document.
   - If the user gives `--folder`, publish directly there unless they also request `--create-run-folder`.
   - If the user gives `--parent`, probe it first: create a direct child document under an `ALIDOC/adoc` anchor; for an ordinary folder, create a per-run child folder before publishing.
   - If the user gives a DingTalk URL in natural language and says "建到下面", "放到下面", or "创建到这个目录下", treat it as `--parent <url>` rather than `--folder <url>`.
3. Check auth:

```bash
dws auth status --format json
```

4. Confirm command shape with `--help` when flags are uncertain:

```bash
dws doc create --help
dws doc folder create --help
dws drive upload --help
dws doc media insert --help
```

5. Run dry-run when the target or mode is new:

```bash
<skill>/scripts/publish-prd "<ENRICHED.md>" --dry-run
```

6. Lint the enriched PRD before publishing. The online copy should not contain local-only sections or links such as `待确认事项`, `关联产物`, `关联 mock`, `.html`, `.png`, `dingtalk-assets`, `file://`, `localhost`, or failed screenshots unless the user explicitly asked to publish draft material. A related HTML prototype is delivered as an attachment block, not as a local path in Markdown. Cleanup must preserve the version table as the first PRD section.

## HTML Prototype At The Front (Legacy Direct Mode)

Online-doc mode automatically looks for `.html` and `.htm` files directly beside the enriched PRD and selects the one with the newest modification time. It does not recursively scan the project.

Selection order:

1. `--html <file>`: explicit approved artifact; relative paths resolve from the command working directory.
2. Newest sibling `.html` / `.htm` beside the enriched PRD.
3. No attachment when no candidate exists, `--no-html` is set, or `--mode file` is used.

After `dws doc create` succeeds, the wrapper runs:

```bash
dws doc media insert --node "<NODE_ID>" \
  --file "<HTML_FILE>" \
  --name "<HTML_BASENAME>" \
  --index 0 \
  --format json \
  --yes
```

The attachment call must return `success=true` and `index=0`. Insert it before the ordinary document read-back so a failed attachment cannot be hidden by a successful Markdown read. Use `--no-html` only when the user explicitly does not want to publish the prototype or the sibling HTML is known to be unrelated.

## Online Doc Mode

Default publish path:

```bash
<skill>/scripts/publish-prd "<ENRICHED.md>" \
  --name "<PRD title>" \
  --read-back
```

This probes the default parent anchor with `dws doc info`. The current default anchor is the DingTalk Doc URL for "智能体需求文档". Its existing hierarchy uses direct child documents, so when the anchor is an `ALIDOC/adoc` node, create the editable PRD directly with `dws doc create --folder <nodeId>` and do not create an intermediate folder. Ordinary document folders retain the optional `dws doc folder create` path. If a supplied parent is a normal file that cannot hold child nodes, fall back to the returned `folderId` and report that fallback.

Create an editable DingTalk document from Markdown:

```bash
<skill>/scripts/publish-prd "<ENRICHED.md>" \
  --folder "<DINGTALK_FOLDER_URL>" \
  --name "<PRD title>" \
  --read-back
```

Rules:

- `--name` becomes the document title/H1 in DingTalk; the Markdown body should normally start at `##`.
- Use `--folder` for a document folder URL/nodeId, or `--workspace` for a knowledge-base workspace.
- Use `--parent` when the user gives an anchor document/folder and wants a fresh child artifact each run. An `ALIDOC/adoc` anchor produces a direct child document; an ordinary folder produces a child folder first.
- Use `--run-folder-name "<name>"` when the generated timestamped folder name is not desired.
- Use `DINGTALK_PRD_DEFAULT_PARENT=<url-or-node>` to override the built-in default parent for one invocation.
- Always read back. Verify important headings, the complete latest version row, other tables, acceptance criteria, screenshot marker/caption, and image/attachment presence.
- When HTML was selected, verify the first content block is the HTML attachment and that a browser user can see and open or download it before the PRD body.
- Read-back is not enough. After the document URL exists, open it in a browser and verify what a human reader sees.

## File Upload Mode

Upload the enriched Markdown as a standalone file:

```bash
<skill>/scripts/publish-prd "<ENRICHED.md>" \
  --mode file \
  --folder "<DINGTALK_FOLDER_URL>"
```

Use this when the user wants archival fidelity more than editable online-doc formatting.
When no target is provided, the default anchor is optimized for online-doc mode. File mode against an `ALIDOC/adoc` anchor is not a supported default path; pass an explicit ordinary `--folder` for archival file uploads.

## Screenshot Images In DingTalk

Local Markdown image links may not become rendered DingTalk images automatically. If read-back shows broken local image paths or only marker text:

1. List blocks:

```bash
dws doc block list --node "<NODE_ID>" --content-format jsonml --format json
```

2. Find the block near the screenshot marker, caption, or target section.
3. Insert the local screenshot after that block:

```bash
dws doc media insert --node "<NODE_ID>" \
  --file "<SCREENSHOT.png>" \
  --name "<caption>.png" \
  --ref-block "<BLOCK_ID>" \
  --where after \
  --format json
```

4. Read back or block-list again to verify the attachment/image block exists.

Do not claim the PRD is fully published with screenshots until this is verified. If exact placement is blocked by DingTalk block structure, report the blocker and the fallback placement.

## Browser Visibility Verification

Every PRD published to DingTalk needs a browser-visible check before completion.

1. Open the `docUrl` in the available browser tool.
2. Verify the document title and top version table look clean; confirm the latest version, date, and modification summary match the local PRD.
3. Scroll through the sections that should contain screenshots and confirm the images render in the corresponding modules.
4. Check the bottom of the document for unwanted draft sections.
5. Use in-page search where possible for these residual terms:
   - `待确认事项`
   - `关联产物`
   - `关联 mock`
   - `.html`
   - `.png`
   - `dingtalk-assets`
   - `本地`
6. If any residual term or failed image is visible, fix the DingTalk doc with `dws doc block update/delete` or regenerate the enriched PRD, then verify again.

If the browser cannot access the document because of login, permission, network, or tool limitations, report that as a blocker. Do not replace browser visibility verification with API read-back.

## Completion Evidence

Return:

- `nodeId` and `docUrl` when available.
- Target folder/workspace.
- Enriched PRD path.
- Screenshot files inserted.
- Read-back or block-list verification summary.
- Local and remote latest PRD version row.
- Browser visibility verification summary.
- Any unrendered image or placement gaps.
