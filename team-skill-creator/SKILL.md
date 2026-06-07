---
name: team-skill-creator
description: >
  团队 Skill 创建器 / 能力沉淀判断：当用户想把一个可重复能力沉淀下来，或不确定应该做成 Prompt、
  Workflow、Tool、Plugin、App 还是 Skill 时使用。可用中文唤起：“帮我创建一个 Skill”
  “这个能力要不要沉淀成 Skill”“把这个流程固化成 Skill”“导入这个 GitHub Skill”。会先查重、
  对齐 GitHub Skill 仓库分类和目标应用 Skill 目录，澄清关键需求、给 Creation Decision，
  只有用户确认后才创建，并运行系统和团队校验。
---

# 团队 Skill 创建器（team-skill-creator）

## 中文速查

- 中文名：团队 Skill 创建器 / 能力沉淀判断
- 英文稳定名：`team-skill-creator`
- 分类：Skill/Agent 治理
- 你可以这样叫我：`帮我创建一个 Skill`、`这个能力要不要沉淀成 Skill`、`把这个流程固化成 Skill`、`导入这个 GitHub Skill`
- 适合：新建、导入、合并、评估一个可复用能力是否应成为 Skill，并按团队标准验证
- 不适合：已经有 Skill 只需要评审，改用 `skill-reviewer`；一次性任务不应创建 Skill

## Overview

使用这个 Skill 做团队级 Skill 工厂。它在系统 `skill-creator` 外增加团队门槛：先判断请求是否真的应该变成 Skill，只澄清关键问题，只有确认后才创建或导入，并用系统和团队检查一起验证结果。

默认治理链路是：GitHub 线上 Skill 仓库 `PANGKAIFENG/skill` 的默认分支 -> 已刷新到该分支的本地 checkout -> 本地 `multica-skill` 目录 -> Codex/Claude 可引用目录。GitHub 线上仓库是唯一标准源，负责先查重、分类、版本化、中文可发现性和云端留存；本地 checkout 只是读写工作副本；`multica-skill` 负责给 Multica 应用使用；Codex/Claude 目录负责让本机 agent 运行时可引用。`skillshare sync` 只是可选的分发辅助，不是默认必走步骤。

它也处理“导入式创建”：候选 Skill 来自 Git 仓库、市场下载、本地 clone 或另一个 agent 的 Skill 目录。此时把上游 Skill 当作候选来源，而不是自动接受为最终产物。

不要替换系统 `.system/skill-creator`。应把它作为 Codex Skill 结构和脚手架的基线。

## Workflow

1. 捕获用户请求，并用一句话复述想沉淀的可复用能力。
2. 推荐创建新 Skill 前先跑相似度和分类扫描。前置先确认本地 checkout 指向 `git@github.com:PANGKAIFENG/skill.git` 或用户指定的 GitHub Skill 仓库，`git fetch` 后对齐线上默认分支，再扫描该 checkout、`multica-skill`、Codex、Claude、`.agents`、系统 Skills，以及任何导入来源目录：

```bash
python3 <this-skill>/scripts/inspect_existing_skills.py --name "<candidate-name>" --description "<request summary>"
python3 <this-skill>/scripts/inspect_existing_skills.py --name "<candidate-name>" --description "<request summary>" --catalog-root /Users/linctex/.config/skillshare/skills --multica-root /path/to/multica-skill --import-root /path/to/imported/skills --json
```

3. 判断最佳实现形态。对非平凡或模糊请求，读取 `references/creation-rubric.md`。
4. **认知类 Skill 调研门（新增）**：如果候选 Skill 的核心价值来自「封装一套认知/协作/问题解决方法论」，在写 Creation Decision 之前，先做一轮领域方法论调研。判断标准：Skill 的 workflow 主体是「AI 如何思考、如何追问、如何判断」而不是「AI 如何操作工具或执行步骤」。
   - 调研内容：该领域有哪些被验证的框架（有实证支撑 vs 流行但缺乏证据）、常见失败模式及其防御机制、AI 协作场景下哪些方法可操作。
   - 调研完成后，把关键方法论结论写进 Creation Decision 的 Resource Plan，并在生成 reference 文件时直接体现，而不是事后补充。
   - 跳过条件：技术操作类 Skill（如 git workflow、代码格式化、文件操作）不需要调研，其方法论已隐含在领域规范里。
5. 为候选 Skill 选择分类和发布状态。优先复用 GitHub Skill 仓库 `SKILL_REGISTRY.md` 里的分类；需要新分类时，说明为什么现有分类不够，并把 `categories/README.md`、对应分类 README 和 registry 更新纳入计划。
5. 如果缺少关键上下文，最多问 5 个具体问题。不要询问可以从本地文件中发现的信息。
6. 写文件前先输出 `Creation Decision`。包含推荐形态、是否创建或导入 Skill、触发示例、非触发示例、分类归属、发布状态、资源计划、eval 清单、风险和需要的明确确认。对导入候选，还要包含来源候选、最佳基底、合并决策、借鉴点、来源记录和安装/同步计划。
7. 只有用户明确确认后才创建 Skill。使用：

```bash
python3 <this-skill>/scripts/create_team_skill.py --name "<skill-name>" --description "<trigger description>" --resources scripts,references --path /Users/linctex/.codex/skills
```

8. 替换脚手架占位符，运行两类校验，并在宣布团队级或高价值 Skill ready 前用 `skill-reviewer` 做最终评审：

```bash
python3 /Users/linctex/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/linctex/.codex/skills/<skill-name>
python3 -B /Users/linctex/.codex/skills/skill-reviewer/scripts/check_skill.py /Users/linctex/.codex/skills/<skill-name>
```

9. 验证通过后默认发布到 GitHub 标准源：只暂存本次 Skill 相关文件和必要索引文件，提交到当前分支，推送到 `origin/main` 或配置的上游分支，并用远端树验证新 Skill、分类和 registry 已出现在 GitHub 默认分支。除非用户明确要求“仅本地草稿”或 push 被权限/网络/冲突阻塞，否则不要把创建任务标记为完成。

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
8. After import or merge, run system validation and `skill-reviewer`; fix P0/P1, record P2 if intentionally deferred; then distribute to the confirmed targets. Prefer direct copy/import into GitHub checkout, `multica-skill`, Codex, and Claude directories; use `skillshare sync` only when it is the explicitly chosen distribution mechanism.

## GitHub Catalog / Multica Sync

Treat the user's GitHub Skill repository online default branch as the source of truth. The local checkout is valid only after its remote, branch, and ahead/behind state are checked against GitHub. It is the classification layer and durable upstream for shareable Skills, not merely a target after local creation.

When creating, importing, or updating a Skill:

1. First refresh or inspect the GitHub Skill checkout against `origin/main` or the configured upstream. If it is behind, update before deciding; if it has dirty local edits, report them before changing files.
2. Compare the request against the GitHub Skill catalog, including `SKILL_REGISTRY.md`, `categories/`, and same-name directories.
3. Decide whether the existing GitHub Skill should be optimized, whether a new Skill should be added, or whether the request should be absorbed into another Skill.
4. Choose one existing category before writing. If no category fits, propose a new category with an English folder slug, Chinese label, boundary, and target Skills.
5. Keep stable English `name:` and folder slugs. Add Chinese discoverability through `SKILL_REGISTRY.md`, category README files, and the `中文速查` section.
6. After validation, keep these copies aligned when applicable: the GitHub checkout ready to push, the local `multica-skill` directory, `/Users/linctex/.codex/skills`, and `/Users/linctex/.claude/skills`.
7. For Multica, prefer the application's supported import/list flow or a confirmed `multica-skill` directory over copying into an unknown database-backed workspace.
8. Do not silently overwrite app/workspace/runtime Skills with the same name. First compare the current Multica copy, the GitHub catalog copy, and the Codex/Claude copies, then choose `new`, `merge-into-existing`, `replace-with-source`, or `do-not-import`.
9. Use `skillshare sync` only as an optional implementation detail when the user explicitly wants to use it or when the target paths are known to be managed by Skillshare. Do not present it as the required default path.

## GitHub Publish Gate

After a confirmed Skill create, import, merge, or update passes validation, publish it by default:

1. Re-check `git status --short --branch`, `git rev-list --left-right --count <upstream>...HEAD`, and the configured remote before staging.
2. Stage only the files created or modified for this Skill plus required catalog files such as `README.md`, `SKILL_REGISTRY.md`, `categories/README.md`, and the relevant category README. Never use `git add .` in a dirty catalog checkout.
3. Run deterministic checks before commit: system `quick_validate.py`, team `skill-reviewer/scripts/check_skill.py`, and `git diff --cached --check`.
4. Commit with a concise message such as `Add <skill-name> skill`, `Update <skill-name> skill`, or `Import <skill-name> skill`.
5. Push to `origin/main` or the configured upstream branch.
6. Fetch and verify the remote default branch contains the Skill directory and all required catalog entries, for example with `git ls-tree -r --name-only origin/main`.
7. If push fails because of authentication, remote rejection, network failure, protected branch policy, or conflicting local changes, stop and report the exact blocker, staged/committed state, and the command needed to finish. Do not silently downgrade to local-only completion.

Only skip this gate when the user explicitly asks for a local draft, private-only experiment, or no-push mode. In that case, the final answer must say the Skill is not published to GitHub and name the exact follow-up required.

## Context Intake

Confirm these inputs before recommending creation, or record them as assumptions:

- Target users, reuse frequency, and failure cost.
- Trigger examples, non-trigger examples, and similar existing Skills.
- Required user inputs, discoverable local context, expected output, and Definition of Done.
- Tool, API, file-write, credential, network, and production side effects.
- Minimum validation path: smoke prompts, non-trigger prompts, deterministic checks, and regression cases when needed.
- For imports: source repo, commit/version, original path, license, exact-name overlaps, similar Skills, chosen base, borrowed strengths, and sync targets.
- Catalog placement: GitHub remote/upstream status, update decision, category, Chinese name, status (`core`, `active`, `keep`, `review`, or `private-only`), and category README/registry updates.
- App/runtime distribution targets: GitHub checkout, local `multica-skill`, Codex/Claude/other runtime paths, Multica workspace/API/UI import, and any app-local Skill root.

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
- Category/status: <existing or proposed category, Chinese label, public/private status>
- GitHub source status: <remote URL, branch/upstream, ahead/behind/dirty status>
- Install/sync plan: <GitHub checkout path, multica-skill path, Codex/Claude targets, optional skillshare command if used>
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
- Category/status: <category and catalog status applied>
- Commands run: <init, validate, reviewer checks>
- Validation result: <pass/fail with key output>
- GitHub publish: <commit hash, push target, remote verification result, or explicit no-push reason>
- Remaining work: <missing references, scripts, evals, review items>
- Next regression: <real prompts or sample artifacts>
```

## Definition of Done

A team Skill creation task is complete only when one of these is true:

- The request is classified as not needing a Skill, with a concrete alternative.
- A `Creation Decision` is delivered and awaits confirmation.
- A confirmed Skill is created, placeholders are removed, system validation passes, team checker results are reported, relevant files are committed and pushed to the GitHub default branch, remote verification passes, and remaining review or regression work is explicit.
- An imported Skill is either rejected with reason, or merged/installed with required resources, provenance, category/status decision, validation results, GitHub commit/push, remote verification, and sync plan.
- GitHub catalog, `multica-skill`, and Codex/Claude distribution work is either completed or explicitly left as a named follow-up with the exact target path/API/UI path and reason.

## Resource Guide

- Use `references/creation-rubric.md` for the Prompt / Workflow / Tool / Plugin / App / Skill decision.
- Use `references/skill-template-standards.md` for the generated `SKILL.md` structure and quality bar.
- Use `scripts/inspect_existing_skills.py` before proposing a new Skill.
- Use `scripts/create_team_skill.py` only after confirmation.
