# Project Context Document Model

## Purpose

`PROJECT_CONTEXT.md` is the first-read map for future AI sessions and project members. It should reduce repeated global exploration by recording stable product context, repository boundaries, architecture routes, domain language, entry points, and reusable pitfalls.

It is not a replacement for PRDs, research notes, ADRs, runbooks, implementation plans, or handoff notes.

## Best-Practice Sources

Use these practices as light guidance, not as rigid templates:

- [Diataxis](https://diataxis.fr/): separate documentation by user need. A global context document is mostly explanation plus navigation, not a tutorial or task guide.
- [Architecture Decision Records](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions): accepted architectural decisions should live in decision records, while the context document can link to them and summarize their current effect.
- [Docs as Code](https://www.writethedocs.org/guide/docs-as-code/): keep context docs in version control, review diffs, use plain text, and verify references.
- [arc42](https://arc42.org/overview): borrow architecture dimensions such as goals, stakeholders, building blocks, runtime flow, and risks without forcing the whole template.
- [Google developer documentation style guide](https://developers.google.com/style): write for clarity, consistency, and the reader's next action.

## What Belongs

Put information here when it is durable across multiple future requests:

- product identity, positioning, and non-negotiable boundaries;
- core users, jobs-to-be-done, and recurring workflows;
- repository and module map, especially in multi-checkout workspaces;
- main architecture, data flow, runtime, and integration routes;
- domain terms, entities, and naming conventions;
- first-read paths for future AI sessions;
- verification entry points and local development commands that are broadly useful;
- repeated pitfalls with prevention rules.

## What Does Not Belong

Move these elsewhere:

- detailed scope for a single feature or release;
- competitor research or unresolved option analysis;
- full implementation plans, tickets, task lists, and current sprint status;
- long command transcripts, trace payloads, or debugging logs;
- secrets, credentials, customer data, or private production artifacts;
- decisions that need status, rationale, and consequences. Use `decisions/` or ADR files.

## Recommended Sections

Use the project language and existing docs conventions, but keep these concepts visible:

1. Document purpose and maintenance rules.
2. Product identity and current positioning.
3. Core users and recurring workflows.
4. Repository and module map.
5. Architecture and data flow.
6. Domain language and key entities.
7. Future AI entry routes.
8. Topic index for PRDs, research, decisions, runbooks, and handoffs.
9. Pitfalls to avoid.
10. Verification notes and open research points.

## Fact Labels

Separate evidence quality:

- **已验证事实**: confirmed by current files, commands, runtime, or user statement.
- **当前判断**: a working interpretation that is useful but may change.
- **待研究点**: important unknowns that should not be treated as decisions.

## Granularity Test

Before adding a paragraph, ask:

- Will this still help after the current requirement is done?
- Would a future AI session need this before touching any specific feature?
- Is the detail shorter here than reading the source file directly?
- Is this a fact, a judgment, or an open question?
- Should this be a link to a PRD, ADR, research note, or runbook instead?

If the answer points to one requirement, one incident, or one implementation branch, do not put the detail in global context. Add a short route or summary only.
