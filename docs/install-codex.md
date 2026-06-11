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
  decision-research \
  brainstorming \
  prd-architect \
  prd-review \
  prd-to-issues \
  ui-wireframe-to-html \
  ui-mockup-desktop-workbench \
  grill-me \
  ai-work-assetization-diagnoser
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
  decision-research \
  brainstorming \
  prd-architect \
  prd-review \
  prd-to-issues \
  ui-wireframe-to-html \
  ui-mockup-desktop-workbench \
  grill-me \
  ai-work-assetization-diagnoser
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
$prd-to-issues 把这个 PRD 拆成 GitHub issues，先不要发布
```

or:

```text
$brainstorming 先不要写 PRD，帮我脑暴 2-3 个设计方案
```

or:

```text
$ui-wireframe-to-html 基于这份 PRD 先出 UI 结构、状态模型和 ASCII 布局
```

or:

```text
$research-topic-compiler 系统研究“AI 产品经理工作流”，输出 PM 决策输入
```

or:

```text
$ai-work-assetization-diagnoser 这个 prompt 应该沉淀成 workflow 还是 Skill？
```

Expected behavior:

- Codex recognizes the Skill name.
- The response follows the workflow in the Skill.
- It does not jump directly to implementation unless the prompt asks for that.

## Notes

- Keep the Skill directory names stable; they are the public invocation names.
- Some Codex setups scan `$HOME/.codex/skills` instead of `$HOME/.agents/skills`; use the directory your local Codex reports.
- If you copy instead of symlink, pull updates from this repository and copy again when upgrading.
- For team distribution, consider packaging these Skills as a Codex plugin in a future release.
