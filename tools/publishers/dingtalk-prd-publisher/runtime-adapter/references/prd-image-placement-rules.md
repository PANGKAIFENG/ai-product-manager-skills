# PRD Image Placement Rules

Use this reference when the PRD contains Look up, mock, prototype, preview, screenshot, local HTML, or URL references that should become evidence screenshots.

## Candidate Detection

Treat these as screenshot candidates:

- Markdown links whose label, URL, or nearby text contains `Look up`, `lookup`, `mock`, `prototype`, `preview`, `demo`, `关联`, `产物`, `原型`, `预览`, `截图`, or `页面`.
- Markdown links or raw paths ending in `.html` / `.htm`.
- Remote `http` / `https` URLs when nearby PRD text says they are mock, preview, lookup, or evidence.
- Local relative paths, resolved against the PRD file directory.

Do not screenshot:

- `mailto:`, anchors, issue links, ordinary docs, or image files unless nearby text explicitly asks for a screenshot.
- Missing local files without reporting the missing path.
- Logged-in remote pages if the browser cannot access the required session; report the login/session blocker.

## Deduplication

Group candidates by resolved local path or absolute URL. If the same link appears multiple times:

1. Prefer the occurrence under a semantic feature, page, state, interaction, layout, or UX section.
2. Avoid selecting occurrences under `文档信息`, `关联产物`, `本地草稿附录`, `待确认事项`, or local mock indexes.
3. Capture once; insert once unless the user explicitly wants repeated screenshots.

## Placement

Insert the screenshot near the chosen occurrence:

- If the link appears in a normal paragraph or list item, insert immediately after that paragraph/list item.
- If the link appears in a Markdown table, insert after the table to avoid breaking table syntax.
- If the PRD has both a semantic feature section and `关联产物`, prefer the semantic section and remove the `关联产物` copy from the DingTalk publishing version.
- If the only occurrence is under a local-only section, move placement to the first non-local semantic section and report the original section in the JSON warnings.
- Add a marker comment before each image:

```markdown
<!-- dingtalk-prd-screenshot: {"source":"...","url":"...","section":"..."} -->
![mock screenshot](path/to/image.png)
```

The marker is intentionally visible in Markdown source so later DingTalk media insertion can find the intended block/caption after publication.

## Output Policy

- Never overwrite the source PRD by default.
- The enriched Markdown is DingTalk publish-ready by default: remove `待确认事项`, `关联产物`, local-only `关联 mock` table rows, failed images, and local path indexes from the published copy.
- Use `--no-publish-cleanup` only when the user explicitly asks to keep the local draft structure.
- Put generated screenshots in a PRD-adjacent assets directory.
- Keep screenshot filenames stable and readable: `<index>-<source-stem>.png`.
- Return a JSON report mapping source link -> resolved URL/path -> screenshot path -> insertion section.

## Failure Handling

- If Playwright capture fails, stop and report the specific URL/path and stderr.
- If a local HTML file exists but renders blank, capture a screenshot anyway and recommend a visual check.
- If there are more than 10 candidates, stop by default and ask whether this is intended; large screenshot batches often mean the detection was too broad.
