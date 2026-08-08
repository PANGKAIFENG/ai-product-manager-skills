# Product Browser Walkthrough Boundaries

Read this reference whenever `product-research` needs login-state browsing,
OAuth, screenshots, recordings, or Computer Use. The goal is the minimum
walkthrough evidence that changes the product judgment, not exhaustive clicking.

## Permission Gate

Before login-state browsing, confirm all of these:

- The user authorized use of the browser session or account for this product.
- The task does not require bypassing paywalls, access controls, CAPTCHAs, rate limits, or terms.
- The walkthrough will not purchase, publish, invite, message, connect production integrations, or mutate real customer data.
- Secrets, tokens, private documents, personal data, and unrelated account information will not be collected.

If any item is unclear, use public information first and ask before the login-state step.

## OAuth And Sensitive Authentication

- Do not enter passwords or handle MFA secrets; let the user take over manually.
- When an OAuth consent screen appears, stop and report the exact scopes before approval.
- Do not grant broad scopes only for research.
- Prefer demos, trials, sandboxes, or user-created throwaway workspaces.

## Allowed Low-Risk Actions

- Open public product, documentation, pricing, changelog, help, blog, and public example pages.
- Inspect visible page text and structure relevant to the research question.
- Navigate an already-authorized account without mutating data.
- Capture relevant screenshots that exclude unrelated private information.

## Explicit Approval Required

- Purchasing, subscribing, upgrading, or entering payment details.
- Sending messages, invitations, comments, posts, emails, or notifications.
- Connecting Drive, Slack, GitHub, calendar, CRM, or production data stores.
- Creating, editing, deleting, importing, exporting, or sharing real user/customer data.
- Creating a trial workspace or account.
- Scraping private pages at scale.

## Walkthrough Plan

```markdown
**Walkthrough Plan**
- Research question:
- Account/session to use:
- Screens to inspect:
- Actions explicitly avoided:
- Evidence to capture:
- Stop condition:
```

Capture value proposition, ICP, time-to-value, first-run path, smallest core
workflow, AI autonomy and recovery, collaboration model, monetization triggers,
and trust/permission signals only when relevant. Pair every screenshot with an
access date, observation, source type, and product implication.

Stop and ask when a flow requests broad permissions, would mutate real data,
requires a paid plan, hits an automation block, or creates legal, compliance,
medical, financial, or security risk beyond product-level interpretation.
