# Improvement Record: Front HTML Attachment

- Observed failure: Publishing a PRD with an up-to-date HTML mock creates the DingTalk document and inserts screenshots, but does not attach the HTML artifact itself.
- User-visible impact: Reviewers cannot open or download the latest interactive prototype from the PRD and must return to a local path that is intentionally removed from the online body.
- Evidence / trace: The 2026-07-30 enterprise Skill marketplace PRD publication created node `YQBnd5ExVEw5K57nigGA16lR8yeZqMmz`; six screenshots were inserted, while the sibling `mockup.html` was not uploaded.
- Responsible layer: `dingtalk-prd-publisher` execution reliability and bundled `publish-prd` wrapper.
- General principle: When a PRD is published as an online document, preserve the latest related interactive HTML as a downloadable first-block attachment while keeping local paths out of the Markdown body.
- Best Practice Delta: Execution reliability, deterministic artifact selection, and external-write verification.
- Deterministic checks: Explicit `--html` wins; otherwise select the newest sibling `.html`/`.htm`; `--no-html` disables attachment; dry-run reports selection without side effects; document mode inserts with `--index 0`; file mode performs no document attachment; missing explicit HTML fails before document creation.
- Human-review criteria: The attachment appears before PRD body content, its name is understandable, and unrelated HTML files are not uploaded when an explicit artifact is provided.
- Regression eval: A PRD with `older.html` and newer `mockup.html` attaches only `mockup.html` at index 0.
- Transfer eval: An enriched PRD without a surviving local HTML link still discovers the newest sibling `.htm` artifact.
- Negative eval: `--no-html`, file mode, and a directory without HTML do not call `dws doc media insert`.
- Independent holdout: A PRD with an explicit HTML path outside the PRD directory and a newer unrelated sibling HTML must attach the explicit path only.
- Trace / time / token evidence: The prior publication trace (2026-07-30) showed six successful `dws doc media insert` calls for PNG screenshots, but no call for the sibling `mockup.html`. On 2026-07-31, the updated wrapper passed 12 focused tests, 2 screenshot-enrichment tests, and the private-repo suite (40 tests); `bash -n` and `git diff --check` also passed. Live `dws doc media insert --help` confirms `--index`, and historical successful output confirms the response contract `success=true` plus `index`.
- Release decision: L3 gate passed for the wrapper contract and regression suite. Real DingTalk HTML upload remains a post-release runtime check because the local `--mock` path cannot provide an OSS upload credential; a real publish must verify the first block in `dws doc block list` and the browser.
- Research / meta-skill feedback: Do not encode local mock paths in the published Markdown merely to preserve artifact access; attach the artifact through the document media API and verify block order separately.
