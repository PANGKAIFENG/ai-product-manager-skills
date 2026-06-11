# Release v0.1.0

Initial public release of AI Product Manager Skills Library.

## Included Skills

- `ai-collaboration-calibration`
- `research-topic-compiler`
- `tech-research`
- `prd-architect`
- `prd-review`
- `grill-me`

## Who This Is For

- AI product managers.
- Product leads using Codex, Claude Code, or Agent workflows.
- Teams that want reusable Chinese-first PM workflows.
- Engineers who need a clearer product-side handoff before using Superpowers.

## Install

```bash
git clone https://github.com/PANGKAIFENG/ai-product-manager-skills.git
```

Codex users: see `docs/install-codex.md`.

Claude Code users: see `docs/install-claude-code.md`.

skillshare users:

```bash
skillshare install https://github.com/PANGKAIFENG/ai-product-manager-skills --track
skillshare sync
```

## Try First

```text
$prd-architect 把这个想法整理成 PRD-lite
$prd-review 从研发和测试视角审一下这个 PRD
$research-topic-compiler 系统研究这个主题，并转成 PM 决策输入
```

## Known Limitations

- Plugin packaging is not included yet.
- The project is Chinese-first.
- Install paths may differ by local Agent tool setup.
- The repository focuses on public AI PM workflows, not private enterprise process automation.

## Next

- Add plugin packaging for easier distribution.
- Add more example outputs.
- Add lightweight validation checks for public Skill metadata.
- Improve English landing materials for international discovery.
