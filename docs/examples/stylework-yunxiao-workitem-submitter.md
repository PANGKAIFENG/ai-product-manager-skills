# Example: stylework-yunxiao-workitem-submitter

## Use When

You have a StyleWork discussion or investigation result that should become one evidence-backed Yunxiao requirement or defect.

## Prompt

```text
$stylework-yunxiao-workitem-submitter

把这次“安装 Skill 后必须重启才生效”的排查结果整理成一个云效缺陷。
请区分已验证事实和推断，附上已经脱敏的 evidence.png，描述保持简洁。
先给我看完整预览，我确认后再创建；创建后回读工作项和附件。
```

## Expected Output Shape

- Classifies the current workaround as one defect, not several implementation requirements.
- Shows project, type, title, priority, optional fields, duplicate-check result, and the full description.
- Labels evidence as verified, inferred, weak, or still requiring validation.
- Shows the final attachment filename, MIME type, and size without exposing a local path.
- Waits for explicit confirmation before the first external write.
- Creates exactly once, then reads back the work item and attachment list.
- Reports a stable ID and URL only after readback, or clearly reports partial/unknown status.

## Good Follow-Up

```text
把“缓存没有刷新”从已确认结论改成待验证，并重新生成预览。
```

```text
确认按以上内容创建 1 个云效缺陷。
```
