# Mockup Output Mode Selection

Choose the output mode before visual work.

| Mode | Use When | Required Outputs |
| --- | --- | --- |
| `project-native-preview` | Real frontend project path exists and implementation should match production. | Preview route/component, fixtures, `screen-contract.md`, `component-map.md`, screenshots. |
| `visual-handoff` | PRD is stable and development needs visual guidance, but direct project edits are risky or not requested. | High-fidelity artifact, screenshots, component map, implementation notes, migration boundary. |
| `concept-html` | Early product/design discussion needs a quick visual reference after structure is modeled. | Standalone `mockup.html`, screen contract, assumptions. |

Default to `project-native-preview` when the user provides a frontend path and asks for implementation alignment. Use `concept-html` only for early concept confirmation.
