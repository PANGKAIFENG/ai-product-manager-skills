---
name: evidence-channel-guide
description: competitive-analysis 的证据渠道选择与证据等级规则
---

# Evidence Channel Guide

Choose channels from the decision question. Do not open every possible source by default.

## Channel Selection Matrix

| Decision need | Primary channels | Secondary channels | Watchouts |
| --- | --- | --- | --- |
| Product positioning | Homepage, landing pages, customer pages, category pages, founder posts | Product Hunt, launch posts, analyst notes | Marketing copy can overstate current product depth. |
| Feature priority | Docs, changelog, release notes, onboarding, live walkthrough | Community complaints, roadmap posts, job posts | A visible feature may be a demo-only surface. |
| Pricing / packaging | Pricing page, checkout flow, plan limits, sales pages | G2/Capterra reviews, help center, Terms | Prices and packaging change often; verify current date. |
| Activation / onboarding | Signup flow, empty states, onboarding checklist, email sequence if authorized | YouTube demos, help docs, templates | Do not create persistent customer data without permission. |
| AI capability boundary | Docs, demo videos, model/provider disclosures, feature docs | User complaints, changelog, technical blog | Demos may hide reliability, latency, or cost constraints. |
| Trust / security | Security page, privacy policy, SOC2/GDPR pages, permission screens | Enterprise docs, admin docs, reviews | Treat as product signal, not legal advice. |
| Market pull | Reviews, communities, Product Hunt, app stores, Reddit, X, Hacker News | Search trends, newsletters, podcasts | Public comments are biased samples. |
| GTM and ICP | Case studies, customer logos, testimonials, pricing tiers, sales pages | LinkedIn, job posts, partner pages | Logos do not prove depth of adoption. |
| Operational complexity | Help center, status page, support docs, incident notes, job posts | Engineering blog, API docs | Infer operational burden cautiously. |

## Default Channel Sets

For a fast brief, choose 3-4:

- Official product page or landing page.
- Pricing or packaging page.
- Docs/help/changelog.
- Public reviews or community signal.

For a product walkthrough brief, add:

- Signup/onboarding flow, only with permission.
- First-run empty state and core workflow screenshot.
- Permissions and integration screens.

For a strategic brief, add:

- Case studies and customer logos.
- Hiring pages and role focus.
- Investor/founder/product posts.
- Category alternatives and indirect competitors.

## Evidence Record Format

Capture evidence in this shape:

```markdown
- claim:
  source:
  accessed_at:
  evidence_level: L1/L2/L3/L4
  supports:
  contradicts:
  decision_implication:
  confidence:
```

## Triangulation Rules

- A pricing conclusion needs current pricing page evidence or an explicit "not publicly available" note.
- A feature maturity conclusion needs at least one primary source or live walkthrough observation.
- A market demand conclusion should combine public review/community signal with at least one product/positioning source.
- A differentiation conclusion must compare against our product context; otherwise it is just a competitor description.
- If evidence comes from login-state browsing, record whether it was public account, user-provided account, trial account, or demo account.

## Stop Conditions

Stop collecting evidence when one is true:

- The decision implication is stable across 3 independent channel types.
- A missing private signal would dominate the decision, and more public research has low ROI.
- A small PoC, user interview, or sales call is cheaper than more desk research.
- The user asked for a time-boxed scan and the time box is reached.

## Common Failure Modes

- Feature inventory trap: listing capabilities without saying what changes for us.
- Screenshot theater: many screenshots, no decision implication.
- One-source certainty: strong recommendation based on one landing page.
- Recency miss: pricing, feature availability, or leadership claims based on stale pages.
- Over-indexing on OAuth walkthrough: login flow detail crowds out positioning, packaging, and market signals.
