# Install For Codex

Codex discovers Runtime entries from directories containing `SKILL.md`. This
repository keeps 15 atomic Skills under `skills/` and five optional explicit
composition adapters under `loops/` and `workflows/`.

## User-Level Symlinks

```bash
git clone https://github.com/PANGKAIFENG/ai-product-manager-skills.git
cd ai-product-manager-skills
mkdir -p "$HOME/.agents/skills"
for skill_dir in skills/*; do
  skill="$(basename "$skill_dir")"
  ln -sfn "$(pwd)/$skill_dir" "$HOME/.agents/skills/$skill"
done

# Optional: install the two Workflows and three Loops as explicit-only entries.
for entry_dir in loops/* workflows/*; do
  entry="$(basename "$entry_dir")"
  ln -sfn "$(pwd)/$entry_dir" "$HOME/.agents/skills/$entry"
done
```

Use the user-level directory reported by your Codex installation if it differs
from `$HOME/.agents/skills`. Do not symlink `archive/`. Loop and Workflow
adapters remain cataloged as composition assets, even though Codex discovers
their compatibility `SKILL.md` entrypoints.

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

For all 15 atomic Skills, repeat the metadata-backed install/update for each
`skills/<id>`. Install composition entries directly from their canonical paths:

```bash
skillshare install \
  https://github.com/PANGKAIFENG/ai-product-manager-skills/workflows/problem-to-solution \
  --name problem-to-solution
skillshare install \
  https://github.com/PANGKAIFENG/ai-product-manager-skills/loops/decision-loop \
  --name decision-loop
skillshare sync --dry-run
```

Repeat for `solution-to-delivery`, `solution-loop`, and `delivery-loop`. Do not
use a mixed aggregate source as a GitHub push source.

## Verify

```text
$prd-architect 把这个想法整理成 PRD
$ui-mockup-desktop-workbench 基于 PRD 先出结构，再做 UI handoff
$prd-to-issues 把 ready PRD 拆成 V1/V2/V3，先不要发布
$problem-to-solution 从这个模糊问题推进到确认方案
$solution-to-delivery 把已确认方案做成完整交付包
$decision-loop 关闭这个决策的关键证据 gap
$solution-loop 挑战并修订这个候选方案
$delivery-loop Review 并修订这份 PRD/UI 交付包
```

Expected behavior: Codex lists all five composition entries for explicit use,
does not invoke them implicitly, asks only necessary questions, and does not
claim external publication without a dedicated Tool and current authorization.
