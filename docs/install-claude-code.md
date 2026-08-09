# Install For Claude Code

Claude Code uses the common Agent Skill shape: one directory with a
`SKILL.md` containing `name` and `description` frontmatter. Copy or symlink the
15 child directories under `skills/` into the directory your Claude Code setup
scans. The two Workflows and three Loops also contain compatibility `SKILL.md`
entrypoints and may be installed explicitly from `workflows/` and `loops/`.

## Copy Or Symlink

```bash
git clone https://github.com/PANGKAIFENG/ai-product-manager-skills.git
cd ai-product-manager-skills
mkdir -p "$HOME/.claude/skills"
for skill_dir in skills/*; do
  skill="$(basename "$skill_dir")"
  ln -sfn "$(pwd)/$skill_dir" "$HOME/.claude/skills/$skill"
done
for entry_dir in workflows/* loops/*; do
  if [ -f "$entry_dir/SKILL.md" ]; then
    entry="$(basename "$entry_dir")"
    ln -sfn "$(pwd)/$entry_dir" "$HOME/.claude/skills/$entry"
  fi
done
```

Do not copy `archive/`. Keep Workflow and Loop adapters separate from the 15
atomic Skills and invoke them by their stable IDs.

## skillshare

Use metadata-backed installs for individual Skills, then preview the target
changes before syncing:

```bash
skillshare install \
  https://github.com/PANGKAIFENG/ai-product-manager-skills/skills/prd-review \
  --name prd-review
skillshare update prd-review --dry-run --json
skillshare sync --dry-run
```

## Verify

```text
$prd-review 从研发和测试视角审一下这个 PRD
$research-topic-compiler 系统研究这个产品方向
$team-skill-creator 判断这类重复工作该沉淀成什么
$problem-to-solution 把这个模糊问题推进到确认方案
$delivery-loop 继续 Review 这份已有交付包并定点修订
```

The Skill should follow its own boundary and output contract. Product Delivery
Package publishing is dry-run-only in the current Agent runtime and returns
`authorization_required` for real writes; DingTalk Legacy direct publishing,
Yunxiao work items, and local distribution remain separate Tool operations.
