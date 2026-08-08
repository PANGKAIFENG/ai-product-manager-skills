# Trace Visualization Guide

Use this guide to turn a trace timeline into a compact, auditable diagram. The diagram is a navigation layer over the evidence, not a substitute for evidence and not a reconstruction of hidden chain-of-thought.

## Default Diagram

Use Mermaid `flowchart LR` for most traces. Switch to `flowchart TD` when labels are long or the graph has several branches. Use `sequenceDiagram` only when actor boundaries, concurrency, waits, or latency attribution are the main question.

Include only nodes that exist in the available evidence:

1. User intent or input.
2. Selected route, capability, or Skill.
3. Intended main-path tool or operation.
4. Earliest failure on that intended path.
5. Retry, branch, or fallback transition.
6. Final tool result or user-visible result.

Omit absent stages. Do not invent a complete-looking path to fill the template.

## Evidence Mapping

- Give every material node a stable evidence ID: `E1`, `E2`, `E3`, and so on.
- Reuse the same ID in the chronological evidence list.
- Keep each label short: `E3 PDF 解析失败` is better than pasting the exception into the diagram.
- Put exact commands, errors, URLs, durations, and file paths in the evidence list, not in diagram nodes.
- Use solid arrows for observed transitions and dotted arrows (`-.->`) for inferred transitions. Label inferred edges `推断`.

## Causal Emphasis

Visually distinguish causal roles instead of coloring every tool differently:

```mermaid
flowchart LR
  A["E1 用户请求"] --> B["E2 主链路调用"]
  B --> C["E3 主因：首个失败"]
  C --> D["E4 fallback"]
  D --> E["E5 最终错误"]
  class C root
  class D,E amplifier
  classDef root fill:#FDECEC,stroke:#B42318,color:#7A271A
  classDef amplifier fill:#FFF4E5,stroke:#B54708,color:#7A2E0E
```

- `root`: the earliest supported failure that explains why the intended path stopped.
- `amplifier`: downstream fallback limits, retries, or output-policy problems that worsen or obscure the failure.
- Do not classify a node as `root` solely because it is the final visible error.

## Compression Rules

- Aim for 5-10 nodes; do not exceed 12 unless the user explicitly requests a full event map.
- Collapse identical retries into one node such as `E5 search retry x4`.
- Collapse low-value polling into a duration/count annotation such as `wait x8 / 16s`.
- Preserve branches that change causal interpretation, especially main path versus fallback.
- If several agents or services run concurrently, use subgraphs or a sequence diagram instead of forcing a misleading single line.

## Fallback When Mermaid Is Unavailable

Use a readable text flow with the same evidence IDs and causal labels:

```text
[E1 用户请求] -> [E2 主链路] -X-> [E3 主因]
                                      |
                                      +-> [E4 fallback] -> [E5 最终错误/放大因素]
```

If fewer than two meaningful trace events are available, say `证据不足，无法可靠成图` and show the known event plus the missing predecessor as `待验证`; do not manufacture a route.

## Final Check

- The reading order is unambiguous.
- Every `E#` in the diagram exists in the evidence list, and vice versa for material events.
- Root cause and downstream amplifier are visually distinct.
- Dashed edges and `待验证` labels expose uncertainty.
- The diagram contains observable trace facts and concise diagnostic labels, not hidden reasoning.
