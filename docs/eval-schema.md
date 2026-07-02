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
| `id` | yes | Stable string or number. Prefer strings for long-lived cases. |
| `prompt` | yes | Realistic user wording. Do not leak the expected fix. |
| `expected_output` | yes | Human-readable expected behavior. |
| `assertions` | recommended | List of observable invariants. |
| `should_trigger` | recommended | `true` for trigger cases, `false` for non-trigger cases. |
| `expected_route` | recommended | Expected Skill or handoff target. |
| `known_regression` | optional | Link to a prior failure, report, or issue. |

## Minimum Coverage

Every active Skill should include at least:

- 2 happy-path trigger cases.
- 2 non-trigger or handoff cases.
- 1 known-risk or historical-regression case.

High-risk output-producing Skills should also include capability assertions:

- Required sections or files.
- Side-effect gates.
- Verification or checker expectations.
- Handoff boundaries to adjacent Skills.

## Review Rules

- Evals are not a substitute for deterministic scripts.
- A passing eval file means the intended behavior is documented, not automatically proven.
- Use scripts for format and package invariants; use evals for routing, judgment, and semantic output shape.
- Keep eval prompts realistic and clean-context friendly.
