# Install For Claude Code

Claude Code uses the common Agent Skill shape: one directory with a
`SKILL.md` containing `name` and `description` frontmatter. Copy or symlink the
15 child directories under `skills/` into the directory your Claude Code setup
scans.

## Copy Or Symlink

```bash
git clone https://github.com/PANGKAIFENG/ai-product-manager-skills.git
cd ai-product-manager-skills
mkdir -p "$HOME/.claude/skills"
for skill_dir in skills/*; do
  skill="$(basename "$skill_dir")"
  ln -sfn "$(pwd)/$skill_dir" "$HOME/.claude/skills/$skill"
done
```

Do not copy `archive/`, `loops/`, `workflows/`, or `tools/` into the atomic
Skill directory.

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
```

The Skill should follow its own boundary and output contract. Publishing to
DingTalk, creating Yunxiao work items, and local distribution remain separate
authorized Tool operations.
