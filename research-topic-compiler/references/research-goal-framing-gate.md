---
name: research-goal-framing-gate
description: Convert fuzzy user language into an explicit research goal, question set, and output contract before research starts
---

# Research Goal Framing Gate

Use this file when the user provides vague, colloquial, broad, or solution-shaped research intent and the real research goal is not yet explicit.

The gate prevents the research run from starting with a shallow topic label. It turns the user's words into a usable research brief before source collection, Obsidian writes, Radar runs, or Product Candidate work begins.

## Trigger Signals

Run this gate before `Research Run Plan` when any of these are true:

- The user gives a broad phrase such as "研究一下 Agent", "看看行业怎么做", "帮我调研这个方向".
- The input is business-language or colloquial rather than a defined research topic.
- The user gives a desired artifact, such as Roadmap, PRD, strategy, or framework, but not the research questions.
- The user mixes multiple layers: industry narrative, product positioning, user tasks, capabilities, competitors, implementation, or roadmap.
- The user states a solution before the underlying research goal is clear.
- The expected output audience, usage, or decision is implicit.

Skip this gate only when the user already provides a clear topic, key questions, output format, depth, and source boundary.

## Framing Steps

1. **Capture raw intent**
   - Preserve the user's wording.
   - Identify the surface ask and the likely underlying need.

2. **Infer the research job**
   - Is the user trying to understand a concept, map an industry, translate a trend into a business domain, discover candidates, build a learning pack, prepare roadmap input, or maintain a radar?
   - If there are multiple jobs, split them instead of forcing one topic.

3. **Name the research goal**
   - Write one explicit research goal in operational language.
   - The goal should answer: "After this research, what can the user do that they cannot do now?"

4. **Choose goal type**
   - `Concept Lens`: concept lineage, semantic drift, paradigm stages, hype vs substance.
   - `Industry Evolution`: market narrative, product direction, mature vs emerging patterns.
   - `Application Translation`: mapping a general trend into the user's domain, users, tasks, artifacts, and capability barriers.
   - `Product Candidate`: candidate discovery, candidate backlog, comparison dimensions.
   - `Roadmap Input`: research material that informs roadmap choices but does not yet decide the roadmap.
   - `Learning Pack`: structured learning for an unfamiliar domain.
   - `Research Radar`: living knowledge base for an evolving topic.

5. **Split research questions**
   - Create one primary question.
   - Create 3-7 sub-questions.
   - Mark each sub-question as `understanding`, `judgment`, `translation`, `design`, `validation`, or `decision-input`.

6. **Define output requirements**
   - Reader or audience.
   - Output artifact type.
   - What the output must enable next.
   - Required sections or tables.
   - Evidence standard and uncertainty labeling.
   - What is explicitly out of scope.

7. **Set mode and depth**
   - Select the recommended research mode.
   - Select depth `L1-L5`.
   - If Radar, Product Candidate, or Application Mode applies, say why.

8. **Decide whether to ask or proceed**
   - Ask at most 3 clarifying questions only when ambiguity changes the research goal, output artifact, source boundary, or write location.
   - If a reasonable interpretation is safe, proceed with assumptions and label them.

## Output Template

Use this compact section before `Research Run Plan`:

```markdown
**Research Goal Framing**
- User raw intent: <preserve the user's words in short form>
- Interpreted research goal: <one operational goal>
- Goal type: <Concept Lens / Industry Evolution / Application Translation / Product Candidate / Roadmap Input / Learning Pack / Research Radar>
- Primary research question: <one question>
- Sub-questions:
  - [understanding] ...
  - [judgment] ...
  - [translation] ...
- Output requirements:
  - Audience: ...
  - Artifact: ...
  - Must enable: ...
  - Evidence standard: ...
  - Out of scope: ...
- Recommended mode/depth: <mode + L1-L5>
- Assumptions to proceed: ...
- Confirmation needed: <none / specific question>
```

If confirmation is needed, stop after this section and wait. If the user explicitly asks only to frame the research brief, rewrite vague intent, define research goals, or says not to start source collection yet, stop after this section even when no confirmation is needed. Otherwise, continue into `Research Run Plan`.

## Examples

### Broad Industry Topic

User says:

> 研究一下 Agent 从聊天到做事这个方向，后面要做 Roadmap。

Framing:

- Goal type: `Industry Evolution` + `Roadmap Input`
- Primary question: How are Agent products moving from conversational interfaces to action-oriented work systems, and which patterns are becoming baseline product capabilities?
- Out of scope: choosing the user's roadmap priorities in this run.
- Recommended mode/depth: Lightweight Concept Lens + Application preparation, `L3/L4`.

### Vertical Translation

User says:

> 这些通用 Agent 方向落到服装行业后分别是什么？

Framing:

- Goal type: `Application Translation`
- Primary question: Which general Agent product directions map to apparel users, tasks, deliverables, and defensible capability barriers?
- Output requirements: mapping table by user / task / artifact / capability / moat / validation signal.
- Recommended mode/depth: Application Mode, `L4`.

### Candidate Discovery

User says:

> 看看市面上有哪些 AI 视频工具适合我们参考。

Framing:

- Goal type: `Product Candidate`
- Primary question: Which AI video products are relevant candidates for the user's product decision, and how should they be compared?
- Output requirements: Candidate Backlog, scoring dimensions, cross-session handoff.
- Recommended mode/depth: Product Candidate Research, `L3/L4`.

## Common Mistakes

- Starting web search from the user's first noun phrase instead of reframing the research job.
- Treating a roadmap-prep research run as a roadmap decision.
- Creating a Research Radar Loop just because the topic is current; the user must need ongoing updates.
- Asking too many questions when the research goal can be safely inferred.
- Leaving output requirements vague, which causes generic summaries instead of usable research material.
