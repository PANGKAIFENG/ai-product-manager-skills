---
name: team-skill-creator
description: >
  团队 Skill 创建器 / 能力沉淀判断：当用户想把一个可重复能力沉淀下来，或不确定应该做成 Prompt、
  Workflow、Tool、Plugin、App 还是 Skill 时使用。可用中文唤起：“帮我创建一个 Skill”
  “这个能力要不要沉淀成 Skill”“把这个流程固化成 Skill”“导入这个 GitHub Skill”。会先查重、
  澄清关键需求、给 Creation Decision，只有用户确认后才创建，并运行系统和团队校验。
---

# 团队 Skill 创建器（team-skill-creator）

## 中文速查

- 中文名：团队 Skill 创建器 / 能力沉淀判断
- 英文稳定名：`team-skill-creator`
- 你可以这样叫我：`帮我创建一个 Skill`、`这个能力要不要沉淀成 Skill`、`把这个流程固化成 Skill`、`导入这个 GitHub Skill`
- 适合：新建、导入、合并、评估一个可复用能力是否应成为 Skill，并按团队标准验证
- 不适合：已经有 Skill 只需要评审，改用 `skill-reviewer`；一次性任务不应创建 Skill

## Overview

使用这个 Skill 做团队级 Skill 工厂。它在系统 `skill-creator` 外增加团队门槛：先判断请求是否真的应该变成 Skill，只澄清关键问题，只有确认后才创建或导入，并用系统和团队检查一起验证结果。

它也处理“导入式创建”：候选 Skill 来自 Git 仓库、市场下载、本地 clone 或另一个 agent 的 Skill 目录。此时把上游 Skill 当作候选来源，而不是自动接受为最终产物。

不要替换系统 `.system/skill-creator`。应把它作为 Codex Skill 结构和脚手架的基线。

## Workflow

1. 捕获用户请求，并用一句话复述想沉淀的可复用能力。
2. 推荐创建新 Skill 前先跑相似度扫描。扫描 Skillshare 源目录、Codex、Claude、`.agents`、系统 Skills，以及任何导入来源目录：

```bash
python3 <this-skill>/scripts/inspect_existing_skills.py --name "<candidate-name>" --description "<request summary>"
python3 <this-skill>/scripts/inspect_existing_skills.py --name "<candidate-name>" --description "<request summary>" --import-root /path/to/imported/skills --json
```

3. 判断最佳实现形态。对非平凡或模糊请求，读取 `references/creation-rubric.md`。
4. 如果缺少关键上下文，最多问 5 个具体问题。不要询问可以从本地文件中发现的信息。
5. 写文件前先输出 `Creation Decision`。包含推荐形态、是否创建或导入 Skill、触发示例、非触发示例、资源计划、eval 清单、风险和需要的明确确认。对导入候选，还要包含来源候选、最佳基底、合并决策、借鉴点、来源记录和安装/同步计划。
6. 只有用户明确确认后才创建 Skill。使用：

```bash
python3 <this-skill>/scripts/create_team_skill.py --name "<skill-name>" --description "<trigger description>" --resources scripts,references --path /Users/linctex/.codex/skills
```

7. 替换脚手架占位符，运行两类校验，并在宣布团队级或高价值 Skill ready 前用 `skill-reviewer` 做最终评审：

```bash
python3 /Users/linctex/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/linctex/.codex/skills/<skill-name>
python3 -B /Users/linctex/.codex/skills/skill-reviewer/scripts/check_skill.py /Users/linctex/.codex/skills/<skill-name>
```

## Decision Gates

Prefer a Skill when the task is repeated, has stable failure modes, needs domain or team context, benefits from bundled resources, and can be evaluated with smoke prompts or deterministic checks.

Do not create a Skill when the request is a one-off answer, a simple prompt, a purely deterministic command-line operation, a full product surface that should be an app, or an integration better packaged as a plugin.

Use `references/skill-template-standards.md` when writing or reviewing the generated `SKILL.md`.

## Import / Clone / Marketplace Skill Intake

Use this flow when the user wants to add Skills from another repository, marketplace, local clone, downloaded bundle, plugin, or another agent's Skill folder.

1. Identify the import root and list every `SKILL.md` under it. Record the upstream repo URL, commit or version, plugin/package name, original relative path, and license when discoverable.
2. Run `inspect_existing_skills.py` with `--import-root` for each candidate. Include roots for any special local source the user mentions.
3. Build a comparison matrix for exact-name and high-overlap candidates:

| Dimension | Existing Skill | Source candidate | Judgment |
|---|---|---|---|
| Trigger contract |  |  |  |
| Workflow completeness |  |  |  |
| Resource split |  |  |  |
| Validation/eval ability |  |  |  |
| Context budget |  |  |  |
| Maintainability |  |  |  |
| Source/license/provenance |  |  |  |

4. Choose one of four merge decisions:
   - `new`: no meaningful overlap; import as a new team Skill.
   - `merge-into-existing`: overlap exists and the local Skill is the stable user-facing entry.
   - `replace-with-source`: source candidate has the better architecture; keep local name only if it avoids breaking existing users.
   - `do-not-import`: capability is already covered or is better absorbed into another Skill.
5. Default policy: preserve the upstream name for new imports; when similar Skills exist, merge rather than duplicate; retain the local name if renaming would break existing Skillshare habits.
6. Preserve provenance in a concise `references/provenance.md` or a `metadata.provenance` frontmatter object. At minimum include source repo, commit/version, plugin/package, original path, license status, import date, and merge notes.
7. Copy all required upstream resources (`references/`, `scripts/`, `assets/`, templates, and directly linked markdown files). Rewrite paths only when needed to keep references one level away and mentioned from `SKILL.md`.
8. After import or merge, run system validation and `skill-reviewer`; fix P0/P1, record P2 if intentionally deferred; sync through Skillshare only after validation is acceptable.

## Context Intake

Confirm these inputs before recommending creation, or record them as assumptions:

- Target users, reuse frequency, and failure cost.
- Trigger examples, non-trigger examples, and similar existing Skills.
- Required user inputs, discoverable local context, expected output, and Definition of Done.
- Tool, API, file-write, credential, network, and production side effects.
- Minimum validation path: smoke prompts, non-trigger prompts, deterministic checks, and regression cases when needed.
- For imports: source repo, commit/version, original path, license, exact-name overlaps, similar Skills, chosen base, borrowed strengths, and sync targets.

Ask only for missing information that changes the creation decision or generated Skill structure.

## Confirmation Rule

Before writing a new Skill under `/Users/linctex/.codex/skills`, get explicit confirmation that includes either the approved Skill name or clear approval of the `Creation Decision`.

If the user asks to skip confirmation, still show the `Creation Decision` first unless they already supplied all of these: final name, install path, trigger description, required resources, and acceptance checks.

## Output Format

For planning, use:

```markdown
**Creation Decision**
- Recommended shape: <Prompt / Workflow / Tool / Plugin / App / Skill>
- Create a Skill: <Yes / No / Needs clarification>
- Candidate name: `<skill-name>`
- Similar existing Skills: <findings from inspect_existing_skills.py>
- Source candidate: <repo/path/version, or none>
- Best base: <existing Skill / source Skill / new scaffold>
- Merge decision: <new / merge-into-existing / replace-with-source / do-not-import>
- Borrowed strengths: <what will be absorbed from each source>
- Provenance: <repo, commit/version, plugin/package, original path, license>
- Install/sync plan: <canonical source path and targets>
- Trigger examples: <3-5 examples>
- Non-trigger examples: <2-3 examples>
- Required context: <known / missing>
- Resource plan: <SKILL.md / references / scripts / assets>
- Eval checklist: <smoke, non-trigger, deterministic, regression if needed>
- Risks: <context budget, overlap, side effects, maintenance>
- Confirmation needed: <exact approval needed before file writes>
```

After creation, use:

```markdown
**Creation Result**
- Created path: <path>
- Key files: <SKILL.md, references, scripts, agents/openai.yaml>
- Imported from: <repo, commit/version, plugin/package, original paths, license>
- Merge decision: <new / merge-into-existing / replace-with-source / do-not-import>
- Commands run: <init, validate, reviewer checks>
- Validation result: <pass/fail with key output>
- Remaining work: <missing references, scripts, evals, review items>
- Next regression: <real prompts or sample artifacts>
```

## Definition of Done

A team Skill creation task is complete only when one of these is true:

- The request is classified as not needing a Skill, with a concrete alternative.
- A `Creation Decision` is delivered and awaits confirmation.
- A confirmed Skill is created, placeholders are removed, system validation passes, team checker results are reported, and remaining review or regression work is explicit.
- An imported Skill is either merged, rejected with reason, or installed into canonical Skillshare source with required resources, provenance, validation results, and sync plan.

## Resource Guide

- Use `references/creation-rubric.md` for the Prompt / Workflow / Tool / Plugin / App / Skill decision.
- Use `references/skill-template-standards.md` for the generated `SKILL.md` structure and quality bar.
- Use `scripts/inspect_existing_skills.py` before proposing a new Skill.
- Use `scripts/create_team_skill.py` only after confirmation.
