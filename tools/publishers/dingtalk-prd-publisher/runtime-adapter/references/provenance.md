# Provenance

- Canonical repository since v0.3: `PANGKAIFENG/ai-product-manager-skills`.
- Skill name: `dingtalk-prd-publisher`.
- Created date: 2026-07-02.
- Source request: publish local PRD Markdown files to DingTalk, capture associated Look up/mock screenshots, insert screenshots into the corresponding PRD sections, and publish to a specified DingTalk folder or workspace.
- Local prototype absorbed during initial implementation; its machine-specific path is intentionally excluded from the public contract.
- Prototype license: local personal prototype, no external upstream license found.
- DingTalk substrate: local `dws` CLI and local `dws` Skill documentation.
- Browser substrate: Playwright CLI through local Node/npm `npx`.

## Merge Notes

This originated as a local operation adapter, not a marketplace import. The prototype contributed the `publish-prd` wrapper pattern. The public Tool adapter adds PRD lookup detection, screenshot capture, image-placement rules, dry-run behavior, and regression tests.

2026-07-02 update: the user provided the DingTalk anchor `https://alidocs.dingtalk.com/i/nodes/MNDoBb60VLrdedxLSrZmae9N8lemrZQ3?utm_scene=team_space` and asked to avoid supplying a target address every time. Live `dws doc info` identified it as the `ALIDOC/adoc` node "智能体需求文档"; live `dws doc list --folder <node>` confirmed it can hold child nodes. This historical implementation initially attempted an intermediate per-run folder; the 2026-07-17 correction below records the validated direct-child-document behavior.

2026-07-03 update: the default PRD publish anchor was narrowed from "智能体需求文档" to the child ALIDOC node "TP翻译相关" at `https://alidocs.dingtalk.com/i/nodes/6LeBq413JAz3n3Zau303nQzz8DOnGvpb?utm_scene=team_space`. Live `dws doc info` confirmed this node belongs under the previous anchor via `folderId=MNDoBb60VLrdedxLSrZmae9N8lemrZQ3`. Natural-language target links that say "建到下面" should be executed as `--parent <url>`.

2026-07-17 update: the user restored "智能体需求文档" as the default parent and clarified the hierarchy contract: create one requirement-specific second-level file beneath it and put the PRD into that file. Live child-node inspection showed this anchor contains direct `adoc` child documents, while both `doc folder create` and `wiki node create --type folder` return `invalidParameter.creationNotAllowed`. The wrapper therefore creates the PRD directly with `doc create --folder <anchorNodeId>`, while preserving the ordinary document-folder path.

## Maintenance Boundary

Keep this Skill focused on PRD publishing. Do not add generic DingTalk document editing, PRD writing, or PRD review responsibilities here; route those to the appropriate PRD or `dws` Skills.
