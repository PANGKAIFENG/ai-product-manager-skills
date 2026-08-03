---
name: decision-brief-template
description: competitive-analysis 的 Product Decision Brief 输出模板
---

# Product Decision Brief Template

Use this when the user expects a complete competitive analysis result. Keep the brief decision-oriented: evidence exists to change product judgment, not to prove the agent clicked every page.

```markdown
**Product Decision Brief**

## 1. Decision Question

- Decision question:
- Our product context:
- Target user / ICP:
- Decision deadline or time horizon:
- Competitors / alternatives studied:
- Out of scope:

## 2. Executive Recommendation

- Recommendation: [Do / Do not do / Adapt / Monitor / Validate first]
- Confidence: [High / Medium / Low]
- Why this is the recommendation:
- What would change the recommendation:

## 3. Evidence Base

| Evidence | Source | Level | Supports | Contradicts | Decision implication |
| --- | --- | --- | --- | --- | --- |
|  |  | L1/L2/L3/L4 |  |  |  |

Evidence levels:

- L1: primary source, such as official product page, docs, pricing page, changelog, first-party screenshot, live walkthrough evidence.
- L2: credible third-party source, such as analyst report, high-quality review, benchmark, customer case with attribution.
- L3: community or marketplace signal, such as Product Hunt, G2, Reddit, app store reviews, GitHub issues, social discussion.
- L4: inference, second-hand summary, anecdote, or pattern observed from limited samples.

## 4. Competitor Pattern Map

| Pattern | Where observed | Product job it serves | Maturity | Relevance to us |
| --- | --- | --- | --- | --- |
|  |  |  | Emerging / Common / Table stakes / Differentiating |  |

## 5. Internal Translation

| External observation | Internal taxonomy | Copy / Adapt / Avoid / Validate | Why |
| --- | --- | --- | --- |
|  | User task / Activation / Pricing / Workflow / AI capability / Trust / Collaboration / Growth / Ops |  |  |

Do not leave this as a feature list. Translate every important observation into a product implication.

## 6. Product Implications

- Positioning:
- Roadmap:
- Feature priority:
- Pricing / packaging:
- Onboarding / activation:
- Trust / safety / permissions:
- Sales / GTM:
- Technical or operational constraints:

## 7. What To Copy, Adapt, Avoid

| Action | Item | Reason | Validation |
| --- | --- | --- | --- |
| Copy |  |  |  |
| Adapt |  |  |  |
| Avoid |  |  |  |
| Validate |  |  |  |

## 8. Risks And Unknowns

- Weak evidence:
- Missing private/customer data:
- Possible misread:
- Compliance or permission risk:
- Reversal signals:

## 9. Next Validation

| Validation | Owner | Cost | Deadline | Success signal |
| --- | --- | --- | --- | --- |
|  |  | Low / Medium / High |  |  |

## 10. Handoff

- Recommended next Skill: [none / decision-research / prd-architect / brainstorming / ui-mockup-desktop-workbench / grill-me]
- Suggested next prompt:
- Artifacts produced: [links, screenshots, notes, local paths]
```

## Quality Bar

- The recommendation must be falsifiable.
- The brief must say what changes for the user's product.
- At least one section must describe what not to copy.
- Weak evidence must stay weak; do not upgrade it through confident wording.
- If browser walkthrough was used, include screenshot paths or concrete observations with accessed date.
