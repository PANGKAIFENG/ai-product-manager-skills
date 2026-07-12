# Source Quality and Evidence Lineage Rules

Use these rules when identifying Sources, extracting Evidence, linking Claims, evaluating independence, and writing conclusions.

## Keep Source, Evidence, and Claim Separate

These objects are related but not interchangeable:

- **Source**: the artifact that was retrieved, such as a document, repository, issue, video, dataset, or local file. Store identity, owner, provenance, access, and quality metadata here.
- **Evidence**: a locatable excerpt, observation, code location, result, or data point extracted from one Source. Store directness, freshness, limitations, and its relationship to a Claim here.
- **Claim**: a falsifiable statement in the research Framework. A Claim may have multiple supporting, challenging, or contextual Evidence items.

Use the explicit relationship:

```text
Source ─extracts→ Evidence ─supports/challenges/context_for→ Claim
```

Do not treat a URL, article title, source summary, search snippet, or the model's interpretation as Evidence by itself. Do not let several Evidence excerpts from one Source appear as several independent Sources.

Minimum records:

```markdown
Source: source_id, title, owner, URL/path, source_type, primary/secondary,
        evidence_level, lineage_root, independence_group, access_status,
        published/updated_at, accessed_at
Evidence: evidence_id, source_id, claim_id, locator/excerpt,
          support/challenge/context, directness, freshness,
          independence_group, limitations
Claim: claim_id, statement, decision_impact, required_evidence,
       status, confidence, evidence_ids, open_gaps
```

## Source Graph and Lineage

Record relevant Source-to-Source relations using the canonical edges below:

- `derived_from`: translation, summary, repost, adaptation, or generated digest derives materially from another source.
- `cites`: one source points to another but retains its own evidence-bearing content.
- `same_publisher_as`: sources share the same authoring organization or controlling publisher.
- `fork_of`: a repository or artifact descends from another implementation.
- `implementation_of`: code or a working artifact implements a specification, method, or design from another source.
- `responds_to`: a critique, replication, issue, or counterargument directly addresses another source.

`same_publisher`, `fork`, and `implementation` are shorthand labels only; normalize them to `same_publisher_as`, `fork_of`, and `implementation_of` in the Source Graph.

Assign:

- **lineage_root**: the earliest identifiable source from which the substantive Claim or artifact derives. Reposts, translations, summaries, mirrors, and forks normally inherit that root.
- **independence_group**: the set of sources that should count as one corroboration unit because they share origin, publisher control, data, implementation ancestry, or coordinated authorship.

Two sources may have different URLs and still be non-independent. Sources may share a publisher without being derived from the same document; retain the `same_publisher_as` edge and place them in the same independence group when publisher control matters to the Claim. Explain uncertain lineage rather than inventing independence.

When resuming a run, de-duplicate by canonical source identity, lineage root, and independence group before counting corroboration. Newer timestamps alone do not make a source independent or allow it to supersede older Evidence.

## Origin Verification and Pseudo-Official Sources

Terms such as “official,” “from the team,” “according to,” logo use, matching titles, repository organization names, and search ranking are not proof of origin.

Verify origin through a canonical owner-controlled domain or repository, an explicit first-party cross-link, signed/verified publication metadata, or another traceable ownership path. If origin cannot be verified:

- set `origin_status: unverified` and label the item `unverified origin`;
- keep it secondary or discovery-only even if it appears authoritative;
- do not give it Level A solely because it claims to quote an official source;
- create an origin-tracing Gap when the Claim is important;
- disclose the confidence loss if no accessible primary source exists.

An inaccessible or missing original source does not permit a repost to inherit primary-source quality. API providers, aggregators, mirrors, and Obsidian ingestion paths preserve access provenance, not authority.

## Evidence Strength

| Level | Source type | Can support |
| --- | --- | --- |
| A | Verified official docs, standards, regulator docs, source code, release notes, filings, reproducible benchmarks | Core definitions, mechanisms, constraints, timelines |
| B | Maintainer issues/discussions, engineering blogs, SDK examples, package metadata, credible technical reports | Implementation patterns, adoption friction, best practices |
| C | Reputable secondary analysis, high-quality tutorials, analyst reports, structured reviews | Market interpretation, learning paths, product comparison |
| D | Community posts, X, Reddit, HN, forums, newsletters, videos | Trend signals, pain discovery, hypotheses |
| E | Unverified Claims, reposts, SEO pages, anonymous screenshots, unresolved pseudo-official sources | Discovery only; not core conclusions |

Evidence level is a ceiling, not an automatic score. Also evaluate:

- **directness**: whether the Evidence directly observes the Claim or merely interprets it;
- **freshness**: whether the publication and observation dates fit a changing topic;
- **independence**: whether it adds a new corroboration unit;
- **locator quality**: whether another reviewer can find the exact excerpt, code, or result;
- **limitations**: domain, sample, method, conflict of interest, missing context, or access constraints.

Label each important Claim with its strongest Evidence, independence coverage, contrary Evidence, and remaining Gap. Several same-lineage Level A sources do not equal independent validation.

## Evidence Admission and Claim Update

Before admitting Evidence to a stable conclusion:

1. Confirm the Source identity, origin status, lineage root, and access status.
2. Capture a stable locator or excerpt. If none exists, keep the item as context or a lead.
3. Link the Evidence to a specific Claim as `support`, `challenge`, or `context`.
4. Record directness, freshness, independence group, and limitations.
5. Compare it with existing Evidence rather than replacing older material because it is newer.
6. Update the Claim only when the evidence contract is met; otherwise preserve the open Gap.

Contradictory Evidence makes a Claim `contested` and creates a verification Gap. It is not an execution failure. A new conclusion supersedes an old one only when the relationship is explicit and the Evidence is stronger, more direct, sufficiently current, and appropriately independent for the Claim.

## Screening Rules

- Prefer primary sources for definitions and platform behavior.
- Prefer implementation Evidence for engineering Claims.
- Prefer recent Sources when product behavior, APIs, pricing, law, or market state can change.
- Cross-check social or community Claims with official, implementation, or repeated independent Evidence.
- Avoid using search snippets as Evidence when full Sources are accessible.
- Mark stale Sources and date-sensitive Claims explicitly.
- Keep evidence-backed Claims separate from inferred product or persona implications.
- Do not let the user's desired application upgrade weak Evidence into a stable recommendation.

## Closed and Sensitive Sources

- Use only content the user is authorized to access.
- Do not bypass paywalls, login flows, API limits, robots restrictions, captcha, or private boundaries.
- Do not put private customer data, workspace content, or confidential excerpts into public-facing files.
- If private Evidence shapes a conclusion, summarize it at the appropriate abstraction level and mark it private.
- If an exact citation is unsafe, cite the artifact class and access date, for example: `Private customer-support export, reviewed 2026-05-28`.

## GitHub and Implementation Rules

- Read docs, source, tests, examples, issues, discussions, config, releases, and package metadata according to the target Gap.
- Do not run third-party code unless the user explicitly asks and the risk is acceptable.
- Check recency with commits and releases when maintainability matters.
- Record `fork_of`, `implementation_of`, shared maintainers, copied docs, and shared test/data dependencies before calling projects independent.
- Treat Stars and forks as weak discovery or popularity signals. Combine them with the actual evidence-bearing artifacts; never use them as proof of correctness, quality, production readiness, or independent validation.

## Social and Semi-Closed Discovery

- Treat X, Reddit, HN, Discord, Slack, comments, and most WeChat articles as weak Evidence unless confirmed elsewhere.
- Use social sources to discover projects, arguments, authors, launch timing, pain, and counterexamples.
- Treat Sogou Weixin, Web search, adapters, and third-party APIs primarily as candidate discovery. Search snippets are not core Evidence.
- Prefer original full-text WeChat articles with account, date, and provenance. Mark reposts, unattributed summaries, and generated digests as derived or discovery-only.
- Stop on anti-spider, login, captcha, phone confirmation, paywall, or other access controls and preserve the affected Gap.
- Record forwarding or Obsidian sync as ingestion provenance only; it does not increase evidence strength.
- Without official API access, mark systematic social search as partial.

## Persona and Application Claims

- Label persona-specific takeaways as interpretation when Sources do not state them directly.
- Templates such as PRD snippets, workflows, evals, SOPs, roadmaps, and interface drafts may be synthesized, but cite the evidence-backed principles they depend on.
- If a useful application judgment relies only on trend or community Evidence, label it a candidate judgment or experiment rather than a stable recommendation.

## Citation in Reports

Use short citations inside `05_研究报告`:

```markdown
### 关键依据

- Source title (`path-or-url`) - Evidence A/B/C; supports <claim>.
```

Use `02_证据与卡片` for Source identity, Evidence locators, lineage, comparison, and source-by-source detail.
