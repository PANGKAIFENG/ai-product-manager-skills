# Install For Codex

Codex supports Agent Skills as directories that contain a `SKILL.md` file. Skills can be discovered from user-level and repo-level locations. This repository keeps each public Skill as a root-level folder for stable names and simple copying.

## Option A: User-Level Skills

Use this when you want the Skills available across many repositories.

```bash
git clone https://github.com/PANGKAIFENG/ai-product-manager-skills.git
mkdir -p "$HOME/.agents/skills"

for skill in \
  ai-collaboration-calibration \
  research-topic-compiler \
  tech-research \
  prd-architect \
  prd-review \
  grill-me
do
  ln -sfn "$(pwd)/$skill" "$HOME/.agents/skills/$skill"
done
```

Restart Codex if the Skills do not appear immediately.

## Option B: Repo-Level Skills

Use this when you want the Skills only inside one project.

```bash
mkdir -p /path/to/your-project/.agents/skills

for skill in \
  ai-collaboration-calibration \
  research-topic-compiler \
  tech-research \
  prd-architect \
  prd-review \
  grill-me
do
  cp -R "$skill" "/path/to/your-project/.agents/skills/$skill"
done
```

## Option C: skillshare

If you use `skillshare`, install and sync from the GitHub repository:

```bash
skillshare install https://github.com/PANGKAIFENG/ai-product-manager-skills --track
skillshare sync
```

Run:

```bash
skillshare status
skillshare list
```

to inspect what was installed and synced.

## Verify

In Codex, try:

```text
$prd-architect 把这个想法整理成 PRD-lite
```

or:

```text
$research-topic-compiler 系统研究“AI 产品经理工作流”，输出 PM 决策输入
```

Expected behavior:

- Codex recognizes the Skill name.
- The response follows the workflow in the Skill.
- It does not jump directly to implementation unless the prompt asks for that.

## Notes

- Keep the Skill directory names stable; they are the public invocation names.
- If you copy instead of symlink, pull updates from this repository and copy again when upgrading.
- For team distribution, consider packaging these Skills as a Codex plugin in a future release.
