# State Model Template

```markdown
# State Model

| State | Trigger | Visible regions | Primary actions | Next state | Recovery path | Source trace |
| --- | --- | --- | --- | --- | --- | --- |
| Empty | <trigger> | <regions> | <actions> | <next> | <recovery> | <PRD section> |
| Loading | <trigger> | <regions> | <actions> | <next> | <recovery> | <PRD section> |
| Success | <trigger> | <regions> | <actions> | <next> | <recovery> | <PRD section> |
| Error | <trigger> | <regions> | <actions> | <next> | <recovery> | <PRD section> |

## Notes
- Do not hide failure states in toast-only descriptions.
- Mark assumptions explicitly when PRD trace is missing.
```
