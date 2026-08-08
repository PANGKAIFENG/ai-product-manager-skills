# Documentation Map

- `quickstart.md`: first-use workflow and invocation examples.
- `install-codex.md`: Codex installation and verification.
- `install-claude-code.md`: Claude Code installation and verification.
- `migration-v0.2.md`: v0.1 root-path to v0.2 `skills/<skill-id>/` migration and local compatibility guidance.
- `migration-v0.3.md`: two-repository convergence, retired IDs, Tool adapters, and local upgrade guidance.
- `release-v0.2.0.md`: v0.2.0 release summary, upgrade notes, and verification evidence.
- `local-distribution.md`: maintainer-only local distribution notes.
- `eval-schema.md`: shared Skill eval schema.
- `audits/skill-overlap-v0.3.0.md`: v0.3 活跃 Skill 重复、边界和归档路由审计。
- `audits/release-gate-v0.3.0.md`: v0.3.0 发布前新鲜验证证据和剩余风险。
- `../loops/`: multi-round state, return-edge, and stop-condition contracts.
- `../workflows/`: stage composition across Skills, Loops, human gates, and Tools.
- `../tools/`: deterministic validators and explicitly authorized publishers/automations.
- `examples/`: copyable prompts and expected output shapes.
- `../packs/`: recommended install combinations; Packs are not triggerable behavior.
- `audits/`: active repository and Skill audit reports; move completed audits to `archive/audits/` after the resulting work is closed.
- `archive/`: completed issues, historical audits, and promotion material.

The installable inventory lives in `../skills/`. The machine-readable catalog is `../catalog/skills.yaml`.
