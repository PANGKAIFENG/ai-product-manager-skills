# User Context Standards

Use this reference to make research outputs persona-adaptive without hard-coding one identity into the Skill.

## Purpose

User context changes how a topic should be explained, which examples matter, what depth is useful, and what action the research should enable. It must not change evidence strength, access rules, or the user's explicit current request.

## User Context Fields

| Field | Meaning | Examples |
| --- | --- | --- |
| `role` | User role or work lens | product manager, engineer, designer, operator, researcher, founder, manager |
| `domain` | User's business or technical domain | AI SaaS, apparel, education, finance, hardware, developer tools |
| `technical_depth` | Expected technical depth | `low`, `medium`, `high` |
| `goal_type` | Why this research is being done | learning, research, decision, PRD, technical selection, solution design, execution, training |
| `output_preference` | Preferred output format | one-screen summary, detailed document, diagram, table, tutorial, executable checklist |
| `application_context` | Current business or project context | recommendation agent, enterprise knowledge base, developer platform, content operations, Skill marketplace |
| `decision_need` | The final decision or judgment needed | choose a tool, define requirements, assess feasibility, guide development, set roadmap |

## Resolution Priority

Resolve context in this order:

1. Current user message.
2. `user-profile.md` in the current project, target Research Project, or nearby workspace.
3. Global `user-profile.md`, if the user has one and the path is discoverable.
4. `references/default-user-profile.md`, if present.
5. Lightweight questions only when missing context would materially harm the output.

Current instructions always override saved or default profiles.

## Lightweight Questions

Ask at most five questions, and only when context materially changes the output:

1. What is your role, such as product manager, engineer, designer, operator, founder, or researcher?
2. What domain are you applying this to, such as AI SaaS, apparel, education, finance, hardware, or developer tools?
3. How deep should the research go: enough to judge, enough to write a plan, enough to guide development, or enough to implement?
4. What should this research produce: learning framework, technical selection, PRD, implementation plan, training material, or practice tasks?
5. What output style do you prefer: one-screen summary, detailed report, diagram, table, or executable checklist?

Do not ask these every time. Reuse current message, local profiles, and default profile when available.

## Persistence Rules

- Do not create or update `user-profile.md` unless the user asks for persistent reuse, the task explicitly includes Obsidian write-back, or a profile file is an agreed output.
- If a profile is created, keep it concise and editable. Record only reusable preferences, not private secrets or one-off instructions.
- Never write API tokens, passwords, private customer data, or sensitive identity details into a profile.

## Persona Effects

User context may affect:

- Explanation depth and terminology.
- Which examples are selected.
- Which cases are considered relevant.
- Which practice tasks are suggested.
- Whether output becomes PRD, architecture notes, SOP, roadmap, eval, checklist, or learning plan.

User context must not affect:

- Evidence labels or source quality.
- Access boundaries.
- Whether weak evidence can support stable conclusions.
- Whether automation is created.
- Whether the user's explicit current instruction is followed.

## Role-Specific Adaptation

| Role | Emphasize | Convert conclusions into |
| --- | --- | --- |
| Product manager | Product judgment, capability boundaries, business mapping, PRD inputs, workflow design, eval criteria | PRD snippets, capability tables, workflow maps, acceptance criteria |
| Engineer | Architecture, interfaces, data structures, state, permission, testing, traceability, implementation risk | module boundaries, interface drafts, log fields, test cases, security checks |
| Designer | User scenarios, interaction flow, information architecture, cognitive load, visual explanation | user journeys, screen structure, decision paths, diagram requirements |
| Operator | SOP, execution flow, content production, metrics, conversion, review cadence | operating checklists, metric tables, content workflow, retrospective template |
| Manager/founder | Strategy, ROI, cost, risk, roadmap, organization, resource allocation | staged roadmap, risk matrix, investment decision, org responsibilities |
| Researcher/analyst | Concept boundaries, methodology, evidence strength, limitations, reproducibility | research questions, evidence gaps, validation plan, comparison framework |

When the role is unknown, use general explanations first. Ask for context only if the topic is complex and the user's goal is unclear.
