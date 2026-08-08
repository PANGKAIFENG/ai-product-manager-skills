# State Model Template

```markdown
# State Model

| State | Trigger | Visible regions | Primary actions | Next state | Recovery path | Source trace |
| --- | --- | --- | --- | --- | --- | --- |
| Empty | <trigger> | <regions> | <actions> | <next> | <recovery> | <PRD section> |
| Loading | <trigger> | <regions> | <actions> | <next> | <recovery> | <PRD section> |
| Success | <trigger> | <regions> | <actions> | <next> | <recovery> | <PRD section> |
| Error | <trigger> | <regions> | <actions> | <next> | <recovery> | <PRD section> |
```

Add queued, running, stopped, partial failure, permission/login, settings, and
recovery states whenever the PRD workflow makes them relevant. Do not hide a
failure or recovery path in a toast-only note.
