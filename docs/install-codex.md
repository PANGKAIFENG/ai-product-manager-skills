# Install For Codex

Codex discovers Skills from a directory containing one child folder per Skill.
This repository keeps all 15 public Skills under `skills/`.

## User-Level Symlinks

```bash
git clone https://github.com/PANGKAIFENG/ai-product-manager-skills.git
cd ai-product-manager-skills
mkdir -p "$HOME/.agents/skills"
for skill_dir in skills/*; do
  skill="$(basename "$skill_dir")"
  ln -sfn "$(pwd)/$skill_dir" "$HOME/.agents/skills/$skill"
done
```

Use the user-level directory reported by your Codex installation if it differs
from `$HOME/.agents/skills`. Do not symlink `archive/`, `loops/`, `workflows/`,
or `tools/` as atomic Skills.

## skillshare

For a Skillshare-managed installation, install each public Skill from its
canonical subdirectory. Existing local changes must be previewed before an
update:

```bash
skillshare install \
  https://github.com/PANGKAIFENG/ai-product-manager-skills/skills/prd-architect \
  --name prd-architect
skillshare update prd-architect --dry-run --json
skillshare sync --dry-run
```

For all 15 Skills, repeat the metadata-backed install/update for each `skills/<id>`.
Do not use a mixed aggregate source as a GitHub push source.

## Verify

```text
$prd-architect 把这个想法整理成 PRD
$ui-mockup-desktop-workbench 基于 PRD 先出结构，再做 UI handoff
$prd-to-issues 把 ready PRD 拆成 V1/V2/V3，先不要发布
```

Expected behavior: Codex recognizes the named Skill, asks only necessary
questions, and does not claim external publication without a dedicated Tool and
current authorization.
