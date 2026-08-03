# Source And Factuality

## Source Modes

Cold-start mode:

- Use web research for the concept, market, technical standard, or industry practice.
- Cite sources in the Markdown output and include them in the HTML sources section.
- Prefer current sources when the field is changing quickly.
- Include lineage research: early usage, original context, major semantic shifts, and current mainstream usage.

User-material mode:

- Treat supplied files, excerpts, or notes as first-class sources.
- Cite local files with paths when possible.
- Use web research only to fill gaps, verify claims, or update time-sensitive information.

Mixed mode:

- Distinguish user-provided facts, sourced facts, and model inferences.
- Label uncertain conclusions as hypotheses.

## Source Hierarchy

Prefer, in order:

1. Official documentation, standards, laws, filings, and product docs.
2. Research papers, benchmark reports, or technical architecture documents.
3. Reputable industry analysis and case studies.
4. High-signal practitioner writing when primary sources are unavailable.

Do not base the evolution matrix on generic SEO explainers unless they are only used for vocabulary orientation.

## Lineage Source Coverage

For complex concepts, seek at least one useful source from each available category:

- Origin evidence: early paper, standard, book excerpt, product documentation, historical announcement, or archived material that shows how the term was first or early used.
- Original use evidence: material showing the initial users, task, workflow, or decision context.
- Evolution evidence: later standards, product categories, architecture patterns, case studies, or industry shifts that changed usage.
- Current usage evidence: current official docs, market categories, vendor docs, or widely cited industry analysis.
- Boundary or critique evidence: source showing ambiguity, misuse, controversy, or overextension when available.

If one category is unavailable, say so explicitly. Do not fill the gap with unsourced narrative.

## Citation Requirements

Every cold-start output must include:

- At least 3 source links for normal complexity.
- Source-backed claims for stage boundaries, standard solutions, and important anti-patterns.
- Source-backed claims for concept origin, original use, and major semantic shifts when available.
- A clear note when a stage is inferred from multiple sources rather than directly named by one source.

The HTML dashboard must include a visible "Sources" section with source title, URL, and the claim area it supports.

## Freshness

Browse by default for:

- Current technologies, vendors, standards, regulations, APIs, pricing, market structure, or product capabilities.
- Any claim where being wrong would affect a purchase, architecture choice, compliance issue, or public deliverable.

Use absolute dates for time-sensitive claims.

## Uncertainty Handling

If evidence is thin:

- Say what is known.
- Say what is inferred.
- Reduce confidence in the stage boundary.
- Use the earliest reliable context instead of claiming a definitive origin.
- Label semantic drift as a hypothesis when it is inferred from usage patterns rather than directly documented.
- Ask for domain material when the user's business context is necessary.
