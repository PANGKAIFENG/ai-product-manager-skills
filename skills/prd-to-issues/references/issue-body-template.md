# Issue Body Template

Use this as the fallback when the repository does not provide a better `.github/ISSUE_TEMPLATE/`.

```markdown
## Parent PRD

<PRD file path, GitHub issue, document link, or "None">

## Source Sections

- <PRD section / user story / requirement id>

## What To Build

<Describe the end-to-end behavior this issue delivers. Avoid stale file paths and low-level implementation detail unless a prior prototype captured a durable decision.>

## Acceptance Criteria

- [ ] <Observable criterion>
- [ ] <Observable criterion>
- [ ] <Observable criterion>

## Verification

- <Manual check, test command, screenshot, API call, or review evidence>

## Blocked By

None - can start immediately.

<!-- Or:
- Blocked by #<issue-number>
-->

## Open Questions

None.

<!-- Or:
- <Question that must be resolved before AFK implementation>
-->
```

## Required Fields

Every implementation issue should include:

- Parent PRD or source reference.
- Source sections or requirement ids.
- What to build.
- Acceptance criteria.
- Verification.
- Blocked by.
- Open questions.

## Optional Fields

Add only when useful:

- Suggested labels.
- Milestone.
- Risk level.
- Rollout or migration notes.
- Screenshots, mockups, or diagram links.
- Non-goals.
