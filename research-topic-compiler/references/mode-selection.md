# Research Topic Mode Selection

Use this reference before loading heavier research assets. The goal is to select the smallest research mode that satisfies the user's next action.

## Primary Modes

| Mode | Trigger | Output |
| --- | --- | --- |
| `Normal Research` | User wants a topic researched, summarized, or organized with sources. | Research Run Plan, evidence matrix, report. |
| `Lightweight Concept Lens` | User asks for concept origin, semantic drift, paradigm stages, PM questions, or a lightweight dashboard. | Concept lineage, stage model, PM decision questions, optional HTML dashboard. |
| `Learning Pack` | User is unfamiliar with a domain and wants to learn it systematically. | Learning route, concept map, practice tasks when triggered. |
| `Application` | User asks "what does this mean for us" or wants research converted into PRD/workflow/SOP/eval/roadmap input. | Applied judgment, templates, tasks, decision inputs. |
| `Radar` | User wants long-running changes, periodic updates, or a living watchlist. | Watchlist, update log, stable/candidate/weak signals. |
| `Product Candidate` | User wants to discover candidate products, options, tools, scenes, or market references before a final decision. | Candidate Backlog, scoring table, handoff to `decision-research`. |

## Boundary With Adjacent Skills

- Use `decision-research` when the user needs a final recommendation, exclusion logic, confidence, and overturn conditions.
- Use `competitive-analysis` when the primary work is competitor evidence collection and a Product Decision Brief.
- Use `ai-collaboration-calibration` when the topic is still a fuzzy feeling, raw solution, or unclear problem.
- Use `prd-architect` when the next deliverable is a PRD, not a research artifact.

## Output Artifact Selection

Choose the artifact after choosing the research mode and depth:

| Artifact | Route |
| --- | --- |
| `chat-brief` | Direct answer; default for L1 and many L2 runs. |
| `research-project-md` | Obsidian or Markdown research asset. |
| `concept-dashboard-html` | Concept Lens HTML only. |
| `research-dashboard-html` | Normal Research/Application HTML for general or cross-functional readers. |

An HTML request changes the artifact, not the research owner or evidence gate. Do not route a general Dashboard request into Concept Lens solely because it says "HTML" or "dashboard".

## Minimal Loading Rule

Load only the references needed for the selected mode:

- Normal: depth rubric, source quality, report standards.
- Normal + research dashboard: the Normal references plus research-dashboard output contract after the terminal gate.
- Concept Lens: concept-lens source, paradigm, output contract, design quality if HTML.
- Learning Pack: learning-pack standards.
- Application: applied-business-research contract and post-research exits.
- Application + research dashboard: the Application references plus research-dashboard output contract after the terminal gate.
- Radar: radar loop contract.
- Product Candidate: product-decision mode, candidate schema, handoff, taxonomy translation when needed.

## Stop Signal

If research uncovers a concrete A/B/C choice, stop expanding the topic and hand off to `decision-research` with the Candidate Backlog or evidence matrix.
