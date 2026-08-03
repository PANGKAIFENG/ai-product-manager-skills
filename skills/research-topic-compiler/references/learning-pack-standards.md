# Learning Pack Standards

Use Learning Pack Mode when the user wants to understand an unfamiliar domain, build a learning framework, or avoid shallow evidence-card summaries.

## Trigger Conditions

Enable Learning Pack Mode when the user says or implies:

- "陌生领域", "系统学习", "学习路线", or "教程式理解".
- "不要只给证据卡片" or "不要太表面".
- "像 Agent-Learning-Hub，但轻一点".
- They want a durable cognitive framework for a topic.

Do not turn every research task into a course. Learning Pack Mode should stay lightweight and directly useful for the user's role and application context.

## Required Content

| Component | Required answer |
| --- | --- |
| First-principles explanation | What problem does this topic fundamentally solve? |
| Topic map | What are the core modules, dependencies, and boundaries? |
| Concept translation | What does each core concept mean, with examples, counterexamples, and common mistakes? |
| Mechanism breakdown | What layers or mechanisms make the system work, and what does each layer own? |
| Case comparison | Which cases are worth learning from, and what should not be copied? |
| Learning route | What should be learned first, next, and skipped for now? |
| Practice tasks | What 1-3 minimal tasks can the user do, with deliverable and acceptance criteria? |
| Judgment framework | What judgment should the user be able to make after learning? |

## Persona Adaptation

Adapt the learning pack to the resolved user context:

- Product manager: translate mechanisms into product decisions, capability boundaries, PRD inputs, workflow design, eval criteria, and launch risks.
- Engineer: translate mechanisms into architecture, interfaces, state, permission, trace, test cases, and implementation risks.
- Designer: translate mechanisms into user flows, information architecture, cognitive load, diagrams, and interaction decisions.
- Operator: translate mechanisms into SOP, execution flow, content production, metrics, and review cadence.
- Manager/founder: translate mechanisms into strategy, ROI, roadmap, resource allocation, risk, and staged investment.
- Unknown role: use a generic explanation and ask only if the topic is complex and the goal is unclear.

## Output Placement

Default placement:

- Put the main learning flow in `05_研究报告.md`.
- Put stable conclusions in `03_阶段结论.md`.
- Put case lessons in `07_行业案例对照.md` when L4/L5.
- Put reusable application templates in `08_最佳实践与应用模板.md` when L4/L5.

Only suggest independent files when one of these is true:

- The user explicitly asks for an independent learning package.
- The topic is L4/L5 and the report would become too long.
- The project should be reused by other learners.
- `05_研究报告.md` is already too long to remain the first reading entry.

Optional files:

- `10_学习路线.md`
- `11_概念地图.md`
- `12_实践任务.md`

## Minimum Practice Task Shape

Each practice task must include:

| Field | Meaning |
| --- | --- |
| Task | What to do |
| Deliverable | What artifact should exist after the task |
| Acceptance criteria | How the user knows it is good enough |
| User value | Why this matters for the resolved role and application context |

## Avoid

- Do not only list links.
- Do not only summarize sources.
- Do not write a glossary as an encyclopedia.
- Do not create a heavy course repository by default.
- Do not output generic technical explanations unrelated to the user's role, goal, or business context.
- Do not make the user read `02_证据与卡片.md` before `05_研究报告.md`.
