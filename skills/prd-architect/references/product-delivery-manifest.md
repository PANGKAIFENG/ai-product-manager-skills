# Product Delivery Manifest v1

Use this contract when a PRD must become a reviewable and publishable Product Delivery Package. The file name is `product-delivery-manifest.yaml`; it is the Package root record, not a second PRD or an orchestration service.

## Ownership

| Role | May write | Must not write |
| --- | --- | --- |
| Maker | Package identity, revision, UI applicability, sources, decisions, PRD artifact | Review, approval, or release facts |
| UI Producer | Action Contract, HTML/preview, screenshots, UI baselines, anchors | Product decisions or verdict |
| Backlog Splitter | Requested version plan, issue drafts, and PRD-to-issue coverage matrix | PRD, UI evidence, review, approval, or release facts |
| Validator | Computed fingerprints, validation result, derived state, last transition | Professional judgment |
| Independent Reviewer | `pre_split_review` before planning and final `review` for the complete Package | Artifacts under review |
| Human Approver | `approvals.publish` bound to the exact payload fingerprint | Review or release facts |
| Publisher | `release.dingtalk` attempts and remote/read-back facts through the validator | Product decisions, artifacts, review, or approval |

Every artifact records its authoritative `producer_identity`. Each Review's `maker_identities` must include every producer covered by that Review plus `ui_requirement.decided_by`; changing the Reviewer-owned list cannot hide self-review. The Reviewer identity must differ from all covered producers for the current revision. Actor-scoped Reviewer and Approver writes bind `--actor-identity` to the identity persisted in their record. An Agent identity is a non-empty task, thread, or run ID. A Human Approver identity must use `human:<stable-label>`.

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
    producer_identity: run-maker-1
    path: PRD.md
    sha256: "<sha256>"
  action_contract:
    artifact_id: ART-ACTION
    producer_identity: run-ui-1
    path: ui/screen-contract.md
    sha256: "<sha256>"
  html:
    - artifact_id: ART-HTML
      producer_identity: run-ui-1
      path: ui/mockup.html
      sha256: "<sha256>"
      baseline_ref: BASE-1
  screenshots:
    - artifact_id: ART-SHOT-DEFAULT
      producer_identity: run-ui-1
      path: ui/screenshots/default.png
      sha256: "<sha256>"
      source_html_ref: ART-HTML
      source_html_sha256: "<sha256>"
      state: default
      viewport: 1440x900
  # Include all three groups before Review when version/issue splitting is requested.
  version_plan:
    artifact_id: ART-VERSION-PLAN
    producer_identity: run-backlog-1
    path: delivery/version-plan.md
    sha256: "<sha256>"
  issue_drafts:
    - artifact_id: ART-ISSUES
      producer_identity: run-backlog-1
      path: delivery/issues.md
      sha256: "<sha256>"
  coverage_matrix:
    artifact_id: ART-COVERAGE
    producer_identity: run-backlog-1
    path: delivery/prd-issue-coverage.md
    sha256: "<sha256>"

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
pre_split_review:
  review_id: REVIEW-PRE-SPLIT-1
  reviewer_identity: run-pre-split-reviewer-1
  maker_identities: [run-maker-1, run-ui-1]
  input_fingerprint: "<pre_split_input_fingerprint>"
  verdict: ready
  checks:
    content: passed
    artifacts: passed
    publish: passed
  findings: []
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
- Every PRD, UI, and planning artifact records its actual producer's
  `producer_identity`; a Reviewer cannot delete that identity or omit it from
  `maker_identities` to manufacture independence.
- When version or issue splitting is requested, a current `pre_split_review`
  with `verdict: ready` must exist before the Backlog Splitter adds `version_plan`,
  `issue_drafts`, or `coverage_matrix`.
- Once any planning artifact exists, `pre_split_review` is immutable; a Reviewer
  cannot add or rewrite it to retroactively authorize the split.
- Actor-scoped validation binds every changed Maker, UI Producer, or Backlog
  Splitter artifact's `producer_identity` to `--actor-identity`; a removed
  artifact must belong to that actor. All three planning groups then become
  Package inputs even when they are not part of the DingTalk publish allowlist.

## Fingerprints

The validator serializes fingerprint inputs as UTF-8 canonical JSON with sorted keys and compact separators.

`pre_split_input_fingerprint` uses the same canonical input shape but excludes
`version_plan`, `issue_drafts`, and `coverage_matrix`. `pre_split_review` must
bind this computed value before any planning artifact is added.

`package_input_fingerprint` covers:

- schema version, work item ID, revision;
- UI applicability;
- sources and decisions;
- artifact IDs, kinds, paths, verified hashes, and producer identities for all
  PRD, UI, version-plan, issue-draft, and coverage artifacts;
- UI baselines and anchors;
- validator contract version.

It excludes timestamps, both Review records, approval, release results, status, and last transition. A changed input makes the affected Review stale and makes any old approval unusable.

`publish_payload_fingerprint` covers the DingTalk mode, title, target selector/value, ordered content/HTML/screenshot allowlist, and each allowlisted artifact's verified hash. Approval must bind this exact value.

## Review Gates

`pre_split_review` covers the PRD and applicable UI artifacts before planning.
It is required only when planning artifacts will be added and must bind the
current `pre_split_input_fingerprint`.

The final `review` covers the complete Package, including all planning artifacts
and every authoritative producer. Both records use `ready` or
`changes_requested` and contain all three checks:

```yaml
review:
  review_id: REVIEW-1
  reviewer_identity: run-reviewer-1
  maker_identities: [run-maker-1, run-ui-1, run-backlog-1]
  input_fingerprint: "<package_input_fingerprint>"
  verdict: ready
  checks:
    content: passed
    artifacts: passed
    publish: passed
  findings: []
```

`ready` is valid only when all checks are `passed`, the fingerprint is current,
all covered producer identities are listed, and the Reviewer is independent.
`Ready with assumptions` may be ordinary PRD advice but cannot create Package
readiness. Planning artifacts without a current ready `pre_split_review` fail
closed; a final Review cannot retroactively authorize the split.

## Publish Approval And Recovery

```yaml
approvals:
  publish:
    approver_identity: human:product-owner
    payload_fingerprint: "<publish_payload_fingerprint>"
    approved_at: "2026-08-06T12:00:00+08:00"
```

An approval whose `payload_fingerprint` is stale is ignored as non-current
Package intent. It does not invalidate a current independently reviewed Package:
the Package remains `package_ready`, while publication remains
`authorization_required`. A current approval may raise the deterministic state
to `publish_approved`, but it is still data inside an Agent-writable Manifest and
does not authorize a real external write. Actor-scoped approval changes require
a matching `human:<stable-label>` actor and persisted `approver_identity`; an
Agent producer cannot approve its own payload.

In the current Agent Runtime, Package mode supports complete `--dry-run` only.
Real DingTalk writes require a trusted host capability that the Agent cannot
generate, that is one-time, and that is bound to the exact payload. Until such a
host integration exists, non-dry-run Package publication returns
`authorization_required` before `dws` or Manifest mutation. CLI flags,
environment variables, ordinary receipt or nonce files, caller-supplied
previous Manifests, and the Manifest approval itself are not that capability.

Package mode consumes only `content_artifact_ref`, `html_artifact_refs`, `screenshot_artifact_refs`, and `target`. It never discovers the newest sibling HTML.

`mode: file` uploads only `content_artifact_ref`, so its HTML and screenshot allowlists must both be empty. A Package that needs HTML or screenshots uses `mode: doc`; the validator rejects a file-mode payload that would silently omit media.

The validator defines and records Publisher events atomically for a future
trusted host integration:

```bash
python3 scripts/validate_product_delivery_manifest.py product-delivery-manifest.yaml \
  --record-publish-event started --actor-role publisher \
  --expected-payload-fingerprint <sha256> --attempt-id attempt-1
```

Supported events are `started`, `remote_created`, `artifact_completed`, `failed`, `readback_passed`, and `browser_verified`. Every event requires the current Human approval and payload fingerprint; non-start events also require the current attempt to have started and must follow the allowed state transition. A retry reuses `release.dingtalk.node_id` and skips `completed_artifact_refs`. Only the most recent transition and at most 20 publish attempts are retained. The v0.3.3 Agent wrapper cannot start these events because it has no trusted host capability.

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

Producer changes must bind the runtime identity recorded on every changed
artifact. For example, Backlog Splitter changes use:

```bash
python3 scripts/validate_product_delivery_manifest.py product-delivery-manifest.yaml \
  --previous-manifest previous.yaml --actor-role backlog_splitter \
  --actor-identity run-backlog-1
```

Publisher preflight:

```bash
python3 scripts/validate_product_delivery_manifest.py product-delivery-manifest.yaml \
  --require-status publish_approved \
  --expected-payload-fingerprint <sha256> --json
```

The validator is a deterministic gate, not an independent Product Reviewer and not authorization for a real DingTalk write. In v0.3.3 this command supports Package dry-run evidence only; a real Package write remains `authorization_required`.
