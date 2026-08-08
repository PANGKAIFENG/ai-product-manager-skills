# Product Evidence Channel Guide

Use this reference in `product-research` mode. Select channels from the research
question and current evidence gap; do not open every possible source by default.

## Channel Selection Matrix

| Evidence need | Primary channels | Secondary channels | Watchouts |
| --- | --- | --- | --- |
| Positioning and ICP | Homepage, landing pages, customer pages, category pages, founder posts | Launch posts, analyst notes | Marketing copy can overstate current depth. |
| Feature maturity | Docs, changelog, release notes, onboarding, authorized live walkthrough | Community complaints, roadmap posts, job posts | A visible feature may be demo-only. |
| Pricing and packaging | Current pricing page, checkout flow, plan limits, sales pages | Reviews, help center, terms | Prices and packaging change often; record the access date. |
| Activation and onboarding | Signup flow, empty states, onboarding checklist, authorized email sequence | Product demos, help docs, templates | Do not create persistent data without permission. |
| AI capability boundary | Docs, product demos, provider disclosures, feature docs | User complaints, changelog, technical blog | Demos can hide reliability, latency, and cost constraints. |
| Trust and security | Security page, privacy policy, compliance pages, permission screens | Enterprise/admin docs, reviews | Treat findings as product signals, not legal advice. |
| Market pull | Reviews, communities, marketplaces, app stores, public social discussion | Search trends, newsletters, podcasts | Public comments are biased samples. |
| GTM and adoption | Case studies, customer logos, testimonials, pricing tiers, sales pages | Job posts, partner pages | Logos do not prove depth of adoption. |
| Operational complexity | Help center, status page, support docs, incident notes, API docs | Engineering blog, job posts | Infer operational burden cautiously. |

For a fast brief, choose three or four channel types that can close the current
gap. For a strategic brief, add adoption, hiring, category alternatives, and
operational evidence only when they change the product implication.

## Evidence Record

```markdown
- claim:
  source:
  accessed_at:
  evidence_level: L1/L2/L3/L4
  supports:
  contradicts:
  product_implication:
  confidence:
```

## Triangulation Rules

- A pricing claim needs a current pricing source or an explicit "not publicly available" note.
- A feature-maturity claim needs a primary source or an authorized live observation.
- A demand claim should combine public user signal with product or positioning evidence.
- A differentiation claim must be translated against the user's product context.
- Login-state evidence must record the account type and the limits of the observation.
- A screenshot is evidence only when paired with a dated observation and product implication.

## Stop Conditions

Stop collecting when one condition is true:

- The implication is stable across three independent channel types.
- A missing private/customer signal would dominate the conclusion and more public research has low value.
- A PoC, interview, sales call, or usage test would close the gap more cheaply.
- The user-specified time or acquisition budget is reached.

Do not stop merely because every candidate link was opened. Do not continue only
to make the source list look complete.

## Failure Modes

- Feature inventory without a product implication.
- Many screenshots with no decision relevance.
- Strong language based on one landing page.
- Stale pricing, feature availability, or leadership claims.
- A login walkthrough that crowds out positioning, packaging, and market evidence.
