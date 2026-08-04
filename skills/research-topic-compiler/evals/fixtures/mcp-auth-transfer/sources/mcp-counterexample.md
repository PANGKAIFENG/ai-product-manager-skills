# Local Stdio Incident Note - Frozen Eval Excerpt

- Fixture ID: `mcp-counterexample`
- Evidence role: Counterexample

A local MCP server exposed excessive filesystem permissions even though it was not reachable over HTTP. Adding OAuth would not have reduced the local process's filesystem authority. The incident was mitigated through sandboxing, narrower tool permissions, and explicit path allowlists.

This challenges an OAuth-only security framework without proving remote authorization is unnecessary.
