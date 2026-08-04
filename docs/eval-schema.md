# Skill Eval Schema

This repository uses lightweight JSON eval files to make Skill routing and output behavior reviewable across Codex, Claude Code, and other agent runtimes.

Each public Skill should eventually include:

```text
<skill>/evals/evals.json
```

## File Shape

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": "happy-path",
      "type": "trigger",
      "prompt": "User-facing request that should trigger the Skill.",
      "should_trigger": true,
      "expected_route": "example-skill",
      "expected_output": "Short statement of the expected behavior.",
      "assertions": [
        {
          "text": "Observable invariant the response or artifact must satisfy."
        }
      ],
      "known_regression": "Optional historical failure this eval protects."
    }
  ]
}
```

## Required Fields

| Field | Required | Meaning |
| --- | --- | --- |
| `skill_name` | yes | Must match the Skill folder name. |
| `evals` | yes | Non-empty array of eval cases. |
| `id` | yes | Stable, non-empty string. IDs must be unique within this eval file. |
| `type` | yes | Non-empty string describing the case type, such as `trigger`, `non-trigger`, or `routing-regression`. |
| `prompt` | yes | Realistic user wording. Do not leak the expected fix. |
| `should_trigger` | yes | JSON boolean: `true` for trigger cases, `false` for non-trigger or handoff cases. |
| `expected_route` | yes | Non-empty string naming a Skill in this repository, or an explicit `external:<skill-id>` handoff. Trigger cases must name their own Skill; non-trigger cases must name another route. |
| `expected_output` | yes | Human-readable expected behavior. |
| `assertions` | yes | Non-empty list of assertion objects. Each object must contain a non-empty string `text`. |
| `known_regression` | optional | Link to a prior failure, report, or issue. |

All required string fields must contain at least one non-whitespace character. Eval IDs
that previously used numbers have been migrated to strings; numeric IDs are not accepted.
IDs are checked for duplicates per file, so the same paired-case ID may intentionally
appear in different Skills' eval files.

Repository routes must match a canonical `skills/<skill-id>/SKILL.md` directory. External
handoffs must use `external:<skill-id>`, where `<skill-id>` follows the same lowercase,
hyphen-separated ID format. Bare unknown routes, empty external routes, trigger cases
pointing elsewhere, and non-trigger cases pointing back to their own Skill fail CI.

## Minimum Coverage

CI enforces the following deterministic minimum for every active Skill:

- 2 cases whose `should_trigger` value is the JSON boolean `true`.
- 2 cases whose `should_trigger` value is the JSON boolean `false`.
- 1 known-risk or historical-regression case.

Only strict JSON booleans count toward trigger and non-trigger coverage. A case counts as
known-risk when `known_regression` is a non-empty string, or when its valid string `type`
contains `risk` or `regression`, case-insensitively.

High-risk output-producing Skills should also include capability assertions:

- Required sections or files.
- Side-effect gates.
- Verification or checker expectations.
- Handoff boundaries to adjacent Skills.

## Review Rules

- Evals are not a substitute for deterministic scripts.
- Schema compliance proves only that routing intent and minimum coverage are documented.
  It does not prove that a model selects the expected route when each prompt is run in a
  clean context.
- Use scripts for format and package invariants; use evals for routing, judgment, and semantic output shape.
- Keep eval prompts realistic and clean-context friendly.
