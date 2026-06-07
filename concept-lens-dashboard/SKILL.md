---
name: concept-lens-dashboard
description: >
  概念透镜看板 / 高阶概念解构：当用户要研究复杂概念、概念源流与语义演化、行业演进、技术/商业范式断代、PM 技术评审提问脚本、反模式诊断，或生成带来源引用且验证过的 Tailwind CSS +
  Alpine.js HTML 决策看板时使用。
---

# 概念解构看板


## 中文速查

- 中文名：概念透镜看板
- 英文稳定名：`concept-lens-dashboard`
- 分类：产品与 PRD
- 你可以这样叫我：`帮我解构一个概念`、`做行业演进看板`、`PM 技术评审提问脚本`
- 适合：冷启动或基于材料研究一个复杂领域，输出带来源的概念源流、语义演化、范式演进、PM 决策矩阵和 Tailwind + Alpine.js 交互 HTML 看板。
- 不适合：不适合只要百科科普、无需来源引用、或不需要文件验证的轻量回答。

## Overview

Use this Skill to turn a complex concept, industry, technology, business model, or operating method into a PM-oriented lineage analysis, evolution matrix, and verified local HTML decision dashboard. The output must help a product manager understand where the concept came from, what original problem it solved, how its meaning changed, where the field's paradigm shifts happened, and how to ask sharper questions in technical or business reviews.

This is not a generic explainer. The work must be source-cited, concept lineage must calibrate the structure, stage evidence must drive the paradigm boundaries, and the generated dashboard must run locally with Tailwind CSS and Alpine.js CDN dependencies.

## Workflow

1. Classify the request.
   - Use this Skill when the user asks for 概念解构, 行业演进, 范式断代, PM 视角, 技术评审提问, 反模式诊断, or an interactive HTML decision dashboard for a complex domain.
   - Do not use it for a simple definition, a short summary, a pure article rewrite, or a persistent product UI.

2. Decide whether more context is needed.
   - If the user asks for general field literacy or pure cold-start research, proceed with web research.
   - If the user asks for diagnosis of their own business, architecture, product, or workflow and has not provided enough background, ask up to 3 focused questions before generating.
   - If missing context is useful but not blocking, proceed and label assumptions explicitly.

3. Research and cite sources.
   - Read `references/source-and-factuality.md` before cold-start or factual work.
   - Browse for current or source-sensitive claims unless the user explicitly forbids browsing.
   - Prefer primary sources, official documentation, standards, reputable industry analysis, high-signal case studies, and early materials that show how the concept was originally used.
   - Carry source links into both the Markdown answer and the HTML dashboard.

4. Trace concept lineage before building the paradigm structure.
   - Identify the earliest available context where the concept emerged, or clearly state when the origin is uncertain.
   - Explain the original problem, original users, original use case, and the contradiction the concept was meant to resolve.
   - Map major semantic shifts: technical adoption, business packaging, cross-domain reuse, standardization, and common misuse.
   - Compare the original meaning with current mainstream usage, and call out where current vendor or market definitions may be narrowing, inflating, or repackaging the concept.
   - Separate historical evidence from model inference. Do not let today's dominant product category overwrite the original context.

5. Build the paradigm structure.
   - Read `references/paradigm-framework.md` before drafting stages.
   - Do not force a fixed four-stage pattern. Derive 3-6 stages from evidence.
   - Use the lineage findings to calibrate stage boundaries, but do not use a simple timeline as the final structure.
   - For every stage, name the user demand, the underlying contradiction, the mature solution pattern, the PM-level operating logic, lineage evidence, and 1-2 review questions.

6. Generate deliverables.
   - Read `references/output-contract.md`, `references/html-dashboard-template.md`, and `references/design-quality.md`.
   - Create files under `./concept-lens-outputs/<concept-slug>/` unless the user specifies another path.
   - Generate at minimum `dashboard.html`; include a concise `summary.md` when the Markdown matrix is substantial.
   - The HTML must be self-contained except CDN references and must include inline data, concept lineage, timeline or tabs, jargon copy controls, a debt detector, and a sources section.
   - Treat the page as a PM decision dashboard, not a landing page: dense, scannable, source-aware, and visually polished without decorative spectacle.

7. Verify before completion.
   - Run `python3 scripts/validate_html_artifact.py <path-to-dashboard.html>`.
   - Run the visual quality preflight in `references/design-quality.md`.
   - Open or render the HTML with the available browser capability when possible and confirm that concept lineage, key stage sections, interaction hooks, and desktop/mobile layouts are visible without overlap.
   - If browser verification is unavailable, report that limitation and include the static validation result.

## Context Intake

Ask only questions that change the output:

- Business setting: What product, team, customer, process, or decision is this concept connected to?
- Current pain: What mismatch, review, purchase, architecture choice, or strategy question triggered the request?
- Audience and depth: Is this for self-learning, executive communication, technical review, or vendor evaluation?

Continue without questions when the user only needs a general concept/industry dashboard.

## Output Contract

Final delivery must include:

- A short essence statement that avoids generic openings.
- A concept lineage summary covering origin, original use, major semantic shifts, and current usage drift.
- A Markdown evolution matrix with source-backed stages.
- A local file link to `dashboard.html`.
- Validation commands and results.
- Source links used for cold-start or factual claims.
- Any assumptions or weak-confidence areas.

Default language is Chinese. Preserve professional terms in their original language when translation would reduce precision. Switch to English only when the user asks.

## Resource Guide

- `references/paradigm-framework.md`: use for stage induction, PM matrix dimensions, and anti-template rules.
- `references/source-and-factuality.md`: use for concept lineage research, browsing, citations, freshness, and uncertainty handling.
- `references/output-contract.md`: use for the exact Markdown and file deliverable shape.
- `references/html-dashboard-template.md`: use for Tailwind + Alpine component requirements and required validation markers.
- `references/design-quality.md`: use for dashboard-specific typography, layout, color, density, and visual preflight rules.
- `scripts/validate_html_artifact.py`: run against generated HTML before saying the work is complete.

## Evaluation

Smoke prompts:

- "用概念解构看板拆一下向量数据库，生成 HTML 文件并验证。"
- "我只知道 CRM 很复杂，帮我按范式演进做一个 PM 能看的交互看板。"
- "分析现代仓储物流的阶段演进、反模式和技术评审提问。"

Non-trigger prompts:

- "一句话解释什么是向量数据库。"
- "把这段文章润色一下。"
- "帮我做一个长期运行的 SaaS 管理后台。"

Regression checks:

- The generated stages are not always four.
- Cold-start outputs include the concept's earliest available context, original use case, and current semantic drift.
- Every stage has an explicit underlying contradiction.
- Stage boundaries distinguish historical evidence from model inference.
- Cold-start outputs include source links across origin, evolution, and current usage when available.
- The HTML contains concept lineage, timeline/tabs, copyable review questions, debt detector, and sources.
- The visual style reads as a polished decision dashboard, not a generic card grid or marketing hero.
- Static validation passes, and browser verification is attempted when available.

## Definition of Done

The Skill run is complete only when the concept lineage, PM matrix, and local dashboard file are generated, factual claims are source-cited, the dashboard passes static validation, visual preflight is completed, browser verification is attempted, and the final answer links the generated files with any limitations clearly stated.
