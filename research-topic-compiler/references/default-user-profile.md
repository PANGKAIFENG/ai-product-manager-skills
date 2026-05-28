# Default User Profile

This file is a local default profile for this Skill installation. It helps personalize outputs when no project-level or message-level user context is available.

It is not part of the core Skill logic. Do not hard-code these assumptions into research rules. Current user instructions and project-specific `user-profile.md` always override this file.

## Profile

| Field | Default |
| --- | --- |
| `role` | AI 产品经理 |
| `domain` | 服装 AI / Agent / Workflow / OpenClaw / Skill 市场 / 白板 |
| `technical_depth` | medium |
| `goal_type` | 学习 + 产品判断 + 方案设计 + 落地执行 |
| `output_preference` | 高密度、结构化、一屏版、图示化、可执行 |
| `application_context` | 推款智能体；推料智能体；OpenClaw；服装 AI 白板；企业知识库；Context Pack；Skill 市场；Eval / Trace / 权限治理 |
| `decision_need` | 判断技术方案是否值得做；判断能力边界；拆成 PRD / Workflow / Skill / Eval；指导团队落地 |

## Usage

- Use this only after checking the current user message and any project/global `user-profile.md`.
- Treat it as a starting lens, not as a fixed identity.
- If the user says they are an engineer, designer, operator, founder, researcher, or any other role, use the current role instead.
- If the user asks for a generic report, keep the report generic and avoid over-personalizing.
