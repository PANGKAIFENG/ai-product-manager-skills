# Install For Claude Code

This repository uses the common Agent Skill shape: each Skill is a directory with a `SKILL.md` file containing frontmatter, a trigger description, and workflow instructions.

Claude Code setups can vary by version and organization policy. Use this guide as a conservative installation pattern: put the eight Skill directories in the location your Claude Code environment scans for Skills, then verify by explicit invocation.

## Recommended Copy List

Copy or symlink these folders:

```text
ai-collaboration-calibration/
research-topic-compiler/
decision-research/
prd-architect/
prd-review/
ui-mockup-desktop-workbench/
grill-me/
ai-work-assetization-diagnoser/
```

Each folder must include its `SKILL.md` file.

## skillshare Path

If your Claude Code setup is managed with `skillshare`, use:

```bash
skillshare install https://github.com/PANGKAIFENG/ai-product-manager-skills --track
skillshare sync
```

Then check:

```bash
skillshare status
skillshare list
```

## Manual Path

If you manage Claude Code Skills manually:

1. Clone this repository.
2. Locate your Claude Code Skills directory.
3. Copy or symlink the eight public Skill folders into that directory.
4. Restart Claude Code if new Skills are not detected.
5. Test explicit invocation by Skill name.

## Verify

Try one prompt:

```text
$prd-review 从研发和测试视角审一下这个 PRD，重点找不可测试点和交付阻断项
```

Expected behavior:

- The agent uses `prd-review`.
- It produces findings before summary.
- It separates blockers, risks, and revision suggestions.

## Compatibility Notes

- The Skills are Chinese-first but include stable English slug names.
- The repository does not require tool-specific wrappers for the first release.
- If your team needs one-click install, track the future plugin packaging work in issues or releases.
