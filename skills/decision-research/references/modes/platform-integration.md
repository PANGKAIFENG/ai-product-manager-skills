# Platform Integration Mode

Use when the question is how to connect to an external platform, API, SDK, Bot framework, marketplace, browser, desktop app, or enterprise integration surface.

## Required Checks

- Official support path: public API, SDK, marketplace app, webhook, OAuth, enterprise connector, partner program.
- Compliance boundary: reject reverse protocols, scraping private surfaces, credential misuse, or actions that violate platform rules.
- Data model: user identity, workspace/tenant, permission scopes, rate limits, audit logs, retention.
- Operational cost: approval flow, review time, quota, monitoring, fallback, customer support burden.
- Product fit: whether platform integration solves the user's job or only adds a channel.

## Evidence Channels

Prioritize L1 sources: official docs, SDK repos, changelog, platform policy, API console docs, review guidelines. Use community examples only to understand failure cases or missing docs.

## Decision Output

State:

- Whether official integration exists.
- Recommended integration path.
- What cannot be done safely or compliantly.
- Minimum PoC.
- Approval, credential, or partner dependencies.
