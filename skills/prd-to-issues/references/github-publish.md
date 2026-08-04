# GitHub Publish Rules

Use these rules only after the user approves the draft issue plan.

## Before Creating Issues

Check:

- `gh auth status`
- target repository remote with `git remote -v` or explicit user-provided repo
- existing labels with `gh label list`
- issue templates under `.github/ISSUE_TEMPLATE/`
- existing related issues with `gh issue list --search "<feature keywords>"`

If the target repo or auth state is unclear, stop and ask.

Do not create issues just because `gh` is already authenticated. The user must confirm the target repository and approve publishing the draft issue plan first.

## Creation Rules

- Create issues in dependency order.
- Use temporary Markdown files and `gh issue create --body-file <file>` for multi-line bodies.
- Prefer the repository's issue template when available.
- Use suggested labels only if they already exist or the user asks to create labels.
- Do not close, edit, or relabel the parent PRD issue unless explicitly asked.
- Do not create duplicate issues when an existing issue covers the same source requirement.

## Safe Command Pattern

```bash
gh issue create \
  --title "<title>" \
  --body-file /tmp/<safe-issue-body>.md \
  --label "<existing-label>"
```

For dependency references, create blocker issues first, then update later issue bodies to reference their numbers.

## Publish Result

Report:

- Created issue numbers and URLs.
- Any skipped issues and reasons.
- Coverage gaps.
- Any labels/templates/milestones not found.
- Next recommended handoff step.
