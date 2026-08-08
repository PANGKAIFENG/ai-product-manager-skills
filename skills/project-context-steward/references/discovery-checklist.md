# Discovery Checklist

Use this checklist when entering a new project or maintaining a global context document. Stop once you have enough evidence for a useful first-read map.

## Project Scope

- Identify whether the target is a single repo, monorepo, product workspace, or parent folder containing several independent checkouts.
- Check `git status --short --branch` and remotes for each relevant repo.
- Confirm the intended context file location.
- Preserve repo boundaries. Do not describe sibling checkouts as one repository unless the product workspace explicitly treats them that way.

## Existing Documentation

- Read the top-level `README.md`, `PROJECT_CONTEXT.md`, `CONTEXT.md`, `AGENTS.md`, `CLAUDE.md`, and docs index files if they exist.
- Look for `prd/`, `research/`, `decisions/`, `runbook/`, `handoff/`, `docs/`, and `architecture/`.
- Identify stale or requirement-specific content already mixed into global context.

## Product And Users

- Capture product name, current positioning, and what the product is not.
- Identify core users, operators, admins, developers, and integration actors.
- Extract recurring workflows from docs, UI routes, tests, examples, and user-provided business context.
- Separate SaaS, desktop, internal tool, and runtime-only surfaces when they exist.

## Technical Map

- Read package manifests and workspace files: `package.json`, `pnpm-workspace.yaml`, `turbo.json`, `nx.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`.
- Map app, package, service, backend, frontend, shared, skills, scripts, tests, and e2e folders.
- Identify framework choices, app entry points, routing conventions, API boundaries, state/data layers, and build commands.
- For multi-repo workspaces, explain what each checkout owns and what it consumes from the others.

## Runtime And Verification

- Find local development commands, test commands, build commands, and smoke-test routes.
- Distinguish documented commands from commands verified in the current session.
- Record environment assumptions only when they are reusable and safe.
- Do not include secrets or private tokens.

## Data Flow And Domain Language

- Identify key entities, IDs, task/session models, artifacts, workspace concepts, billing/permission concepts, and sync boundaries.
- Capture the main user-action-to-service-to-output flow.
- Note which flows are online, local, sandboxed, offline, or hybrid.

## Pitfalls

Look for repeated failure modes:

- similar repo names or sibling checkouts;
- one requirement being mistaken for global product positioning;
- stale paths;
- generated docs placed in the wrong docs root;
- local runtime assumptions copied into SaaS or production paths;
- verified facts mixed with product hypotheses.

Write each pitfall as: `Symptom -> cause -> durable prevention rule`.
