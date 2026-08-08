# Investigation Checklist

Use this checklist when diagnosing an agent trace.

## Intake

- Identify the user request and the expected successful path.
- Note explicit constraints such as "read only", "do not modify files", "latest", or "only explain".
- Record the trace source path, timestamp if present, runtime path, workspace path, and relevant environment.

## Timeline

- First selected skill, tool, or capability.
- First command or API call that should have satisfied the request.
- First failure on the intended path.
- Retry or fallback transitions.
- Final visible failure.
- Any user interruption or changed instruction.

## Visual Reconstruction

- Draw the observed path from intent/input to final result with stable `E#` evidence IDs.
- Show the intended main path and fallback as separate branches when the trace contains both.
- Mark the earliest supported failure as `主因`; mark downstream limits or errors as `放大因素`.
- Use solid arrows for observed transitions and dashed arrows for inferred transitions.
- Collapse repeated retries, polling, or duplicated tool calls and retain their count or duration.
- Keep the diagram under 12 nodes unless the user asks for a full event map.
- Check that every material diagram node maps to an evidence-list item and that no unsupported step was added for visual completeness.
- Use a sequence diagram only when actor boundaries, concurrency, or latency attribution are central.

## Root-Cause Ranking

Prefer this order unless the evidence says otherwise:

1. Earliest failure in the intended path.
2. Wrong routing or capability selection.
3. Missing or invalid input contract.
4. Tool implementation bug.
5. Environment or permission issue.
6. Fallback tool limitation.
7. Final user-visible error.

Do not label the final error as the root cause if it only happened after an earlier intended path failed.

## Evidence Types

Mark each point as:

- `confirmed`: directly present in the trace or verified from local code.
- `inferred`: likely from the sequence, but not directly logged.
- `needs verification`: plausible but requires code, dependency, network, or runtime confirmation.

Useful trace facts:

- Error code and exact message.
- Tool name and command line.
- File path, URL, content type, content length, or MIME type.
- Exit code, status code, timeout, or permission error.
- Fallback decision and reason.
- Missing executable or dependency.
- Output schema, validation failure, or empty result.

Assign evidence IDs in chronological order and reuse them in the visualization. If a diagram edge is inferred rather than logged, mark the corresponding evidence item as `inferred` or `needs verification`.

## Code Mapping

Search for:

- Skill name and CLI entrypoint.
- Error code, localized message, or result JSON shape.
- Function names inferred from path segments.
- Config keys and environment variables.
- Fallback tool names.
- Hard-coded temp paths and size limits.

When reporting file and line:

- Use exact line numbers only after reading the file locally.
- Use "likely source location" when runtime paths and local repo paths differ.
- Explain whether the line likely causes the root issue, the fallback issue, or only a contributing issue.

## Fix Recommendation

For every recommended fix, state:

- What behavior should change.
- Where it likely belongs.
- What regression test or trace replay would catch it.
- Whether it is a product policy fix, implementation fix, environment fix, or eval fix.
