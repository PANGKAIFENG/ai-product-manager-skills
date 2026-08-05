# Product Delivery Manifest v1

Use this contract when a PRD must become a reviewable and publishable Product Delivery Package. The file name is `product-delivery-manifest.yaml`; it is the Package root record, not a second PRD or an orchestration service.

## Ownership

| Role | May write | Must not write |
| --- | --- | --- |
| Maker | Package identity, revision, UI applicability, sources, decisions, PRD artifact | Review, approval, or release facts |
| UI Producer | Action Contract, HTML/preview, screenshots, UI baselines, anchors | Product decisions or verdict |
| Validator | Computed fingerprints, validation result, derived state, last transition | Professional judgment |
| Independent Reviewer | One `review` record with `content`, `artifacts`, and `publish` checks | Artifacts under review |
| Human Approver | `approvals.publish` bound to the exact payload fingerprint | Review or release facts |
| Publisher | `release.dingtalk` attempts and remote/read-back facts through the validator | Product decisions, artifacts, review, or approval |

Maker and Reviewer identities must differ for the current revision. `review.maker_identities` must include the authoritative `ui_requirement.decided_by`; changing the Reviewer-owned list cannot hide self-review. An Agent identity is a non-empty task, thread, or run ID. A human identity uses `human:<stable-label>`.

## Minimal Shape

```yaml
schema_version: 1
work_item_id: WI-123
title: Refund approval drawer
revision: 1
package_status: review_pending
current_stage: review
package_input_fingerprint: "<computed sha256>"

ui_requirement:
  required: true
  reason: user_visible_surface
  decided_by: run-maker-1

sources: []
decisions: []
artifacts:
  prd:
    artifact_id: ART-PRD
    path: PRD.md
    sha256: "<sha256>"
  action_contract:
    artifact_id: ART-ACTION
    path: ui/screen-contract.md
    sha256: "<sha256>"
  html:
    - artifact_id: ART-HTML
      path: ui/mockup.html
      sha256: "<sha256>"
      baseline_ref: BASE-1
  screenshots:
    - artifact_id: ART-SHOT-DEFAULT
      path: ui/screenshots/default.png
      sha256: "<sha256>"
      source_html_ref: ART-HTML
      source_html_sha256: "<sha256>"
      state: default
      viewport: 1440x900

ui_baselines:
  - baseline_id: BASE-1
    kind: frontend-repo
    source: verified project reference
    revision: "<git revision or source hash>"

anchors:
  - anchor_id: ANCHOR-DEFAULT
    prd_artifact_ref: ART-PRD
    heading_path: 7.3 Default state
    content_sha256: "<normalized section sha256>"
    screenshot_ref: ART-SHOT-DEFAULT
    state_refs: [default]

validations: []
review: null
approvals:
  publish: null
release:
  dingtalk:
    mode: doc
    title: Refund approval drawer
    target:
      selector: folder
      value: fake-folder-for-tests
    content_artifact_ref: ART-PRD
    html_artifact_refs: [ART-HTML]
    screenshot_artifact_refs: [ART-SHOT-DEFAULT]
    payload_fingerprint: "<computed sha256>"
    status: pending
    node_id: null
    doc_url: null
    completed_artifact_refs: []
    readback: null
    browser_visibility: null
    attempts: []
last_transition: null
extensions: {}
```

Top-level fields outside this shape are rejected for `schema_version: 1`; optional extensions belong only under `extensions`. Unsupported schema versions fail closed.

## UI Applicability

Every Package declares `ui_requirement.required` explicitly.

- Every Package requires one valid `artifacts.prd` record, including a genuine no-UI Package.
- `true` requires PRD, HTML/preview, Screen/Action Contract, screenshot evidence, an anchor, and a UI baseline.
- `false` is valid only with `reason: no_user_visible_surface`. Missing frontend access, browser failure, schedule pressure, or an unresolved page decision is not an exemption.

Each screenshot binds to the current HTML hash through `source_html_ref` and `source_html_sha256`. Each anchor binds a screenshot to a stable PRD anchor identity and normalized content fingerprint. File modification time never restores freshness.

The validator resolves `heading_path` against current ATX Markdown headings. A leaf title is allowed only when unique; `Parent > Child` may disambiguate a hierarchy. Anchor content is the section body through the next heading of the same or higher level, with line endings normalized to LF, trailing spaces removed, and outer blank lines removed. `content_sha256` is the SHA-256 of that UTF-8 text. The referenced screenshot must also appear as a Markdown image or HTML `img` inside the resolved section.

## Paths And Hashes

- Artifact paths are relative to the Manifest directory.
- Absolute paths, `..` traversal, missing files, symlink escapes, and SHA-256 mismatches fail closed.
- `ui_baselines.source` is provenance text and is not an artifact allowlist path.
- Artifact IDs are unique across all artifact kinds.

## Fingerprints

The validator serializes fingerprint inputs as UTF-8 canonical JSON with sorted keys and compact separators.

`package_input_fingerprint` covers:

- schema version, work item ID, revision;
- UI applicability;
- sources and decisions;
- artifact IDs, kinds, paths, and verified hashes;
- UI baselines and anchors;
- validator contract version.

It excludes timestamps, review, approval, release results, status, and last transition. A changed input makes the old review and approval stale.

`publish_payload_fingerprint` covers the DingTalk mode, title, target selector/value, ordered content/HTML/screenshot allowlist, and each allowlisted artifact's verified hash. Approval must bind this exact value.

## Package Verdict

There is one Package verdict: `ready` or `changes_requested`. It contains all three checks:

```yaml
review:
  review_id: REVIEW-1
  reviewer_identity: run-reviewer-1
  maker_identities: [run-maker-1, run-ui-1]
  input_fingerprint: "<package_input_fingerprint>"
  verdict: ready
  checks:
    content: passed
    artifacts: passed
    publish: passed
  findings: []
```

`ready` is valid only when all checks are `passed`, the fingerprint is current, and the Reviewer is independent. `Ready with assumptions` may be ordinary PRD advice but cannot create Package readiness.

## Publish Approval And Recovery

```yaml
approvals:
  publish:
    approver_identity: human:product-owner
    payload_fingerprint: "<publish_payload_fingerprint>"
    approved_at: "2026-08-06T12:00:00+08:00"
```

Package mode consumes only `content_artifact_ref`, `html_artifact_refs`, `screenshot_artifact_refs`, and `target`. It never discovers the newest sibling HTML.

`mode: file` uploads only `content_artifact_ref`, so its HTML and screenshot allowlists must both be empty. A Package that needs HTML or screenshots uses `mode: doc`; the validator rejects a file-mode payload that would silently omit media.

The validator records Publisher events atomically:

```bash
python3 scripts/validate_product_delivery_manifest.py product-delivery-manifest.yaml \
  --record-publish-event started --actor-role publisher \
  --expected-payload-fingerprint <sha256> --attempt-id attempt-1
```

Supported events are `started`, `remote_created`, `artifact_completed`, `failed`, `readback_passed`, and `browser_verified`. Every event requires the current Human approval and payload fingerprint; non-start events also require the current attempt to have started and must follow the allowed state transition. A retry reuses `release.dingtalk.node_id` and skips `completed_artifact_refs`. Only the most recent transition and at most 20 publish attempts are retained.

Document read-back records the matching `node_id`, approved title, and returned Markdown hash. File-mode read-back records the matching node and approved file name. A successful API flag without these identity checks cannot create `readback_passed`.

`browser_verified` requires a structured local evidence file produced by a separate browser-capable actor:

```json
{
  "passed": true,
  "verifier_identity": "human:browser-checker",
  "checked_at": "2026-08-06T12:10:00+08:00",
  "node_id": "<release.dingtalk.node_id>",
  "doc_url": "<release.dingtalk.doc_url>",
  "payload_fingerprint": "<publish_payload_fingerprint>",
  "checks": {
    "title_visible": true,
    "content_visible": true,
    "artifacts_visible": true,
    "publish_pollution_absent": true
  }
}
```

The Publisher cannot self-assert browser success or reuse evidence from another node or payload. Read-back alone leaves the Package `published_unverified`; that status still requires a node, completed content artifact, current attempt, and complete read-back record. `verified` additionally requires every allowlisted artifact to be completed, the full browser evidence schema, a verified attempt, and a consistent final transition. Handwritten partial objects do not create a trusted state.

## Commands

Validate and print derived state/fingerprints:

```bash
python3 scripts/validate_product_delivery_manifest.py product-delivery-manifest.yaml --json
```

Check an actor-scoped edit against the previous Manifest:

```bash
python3 scripts/validate_product_delivery_manifest.py product-delivery-manifest.yaml \
  --previous-manifest previous.yaml --actor-role reviewer
```

Publisher preflight:

```bash
python3 scripts/validate_product_delivery_manifest.py product-delivery-manifest.yaml \
  --require-status publish_approved \
  --expected-payload-fingerprint <sha256> --json
```

The validator is a deterministic gate, not an independent Product Reviewer and not authorization for a real DingTalk write.
