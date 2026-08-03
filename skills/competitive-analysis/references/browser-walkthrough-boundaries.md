---
name: browser-walkthrough-boundaries
description: competitive-analysis 中使用浏览器、登录态、OAuth、截图、Computer Use 的权限与取证边界
---

# Browser Walkthrough Boundaries

Use this reference whenever the user asks to open a product, log in, click through features, use Google/OAuth, collect screenshots, record flows, or operate with Computer Use.

## Principle

The goal is not to click every feature. The goal is to collect the minimum walkthrough evidence that changes a product decision.

## Permission Gate

Before using login-state browsing, confirm or infer all of these:

- The user authorized using their browser/session/account for this product.
- The task does not require bypassing paywalls, access controls, CAPTCHAs, rate limits, or terms.
- The walkthrough will not modify real customer data, send messages, invite users, purchase, delete, export private data, or publish content.
- The agent will avoid collecting secrets, tokens, personal data, private documents, and unrelated account information.

If any item is unclear, use public information first and ask before login-state steps.

## OAuth / Google Login

- Do not enter passwords or handle MFA secrets unless the user takes over manually.
- If OAuth consent screens appear, stop and summarize what permission is being requested; ask the user to approve or deny.
- Do not grant broad scopes just for research unless the user explicitly approves.
- Prefer demo accounts, trials, sandboxes, or user-created throwaway workspaces.

## Allowed Low-Risk Actions

- Open public pages.
- Navigate product docs, pricing, changelog, help center, blog, and public examples.
- Create a trial workspace only if the user explicitly authorizes it.
- Take screenshots of relevant public or authorized screens.
- Record UI observations needed for the decision brief.
- Inspect visible page text and structure for evidence.

## Disallowed Without Explicit User Approval

- Purchasing, subscribing, upgrading, or entering payment details.
- Sending emails, messages, invites, comments, posts, or notifications.
- Connecting real integrations such as Google Drive, Slack, GitHub, calendar, CRM, or production data stores.
- Creating, editing, deleting, importing, exporting, or sharing real user/customer data.
- Scraping private pages at scale.
- Circumventing bot checks, paywalls, access controls, or rate limits.

## Walkthrough Plan Template

Before acting, state a narrow plan:

```markdown
**Walkthrough Plan**
- Decision question:
- Account/session to use:
- Screens to inspect:
- Actions explicitly avoided:
- Evidence to capture:
- Stop condition:
```

## Evidence Capture Checklist

Capture only decision-relevant observations:

- First impression: value prop, ICP, job-to-be-done.
- Signup/onboarding: friction, time-to-value, required data, permission asks.
- Empty state: what the product wants users to do first.
- Core workflow: the smallest path that proves the product's real job.
- AI behavior: prompt surface, autonomy level, guardrails, editability, failure recovery.
- Collaboration: roles, sharing, comments, notifications, approvals.
- Monetization triggers: plan gates, upgrade prompts, limits, trials.
- Trust markers: security, data usage, integrations, admin controls.

## Screenshot And Notes

When screenshots are captured:

- Use descriptive filenames.
- Do not include unrelated account data.
- Redact or avoid personal/private details when possible.
- Link screenshots from the final brief if they are local artifacts.
- Pair each screenshot with a decision implication.

## Stop And Escalate

Stop and ask the user when:

- Login asks for broad permissions or sensitive account access.
- A product flow would mutate real data.
- The site blocks automation or requires CAPTCHA.
- The analysis needs a paid plan.
- The evidence suggests legal, compliance, medical, financial, or security risk beyond product-level interpretation.
