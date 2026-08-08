# Field Contract

## Output columns

The output must contain exactly eight columns in this order:

| Position | Header | Rule |
| ---: | --- | --- |
| 1 | 标题 | Required; preserve source text. |
| 2 | 负责人 | Preserve blank values. |
| 3 | 创建者 | Keep this exact header; do not rename to 创建人. |
| 4 | 迭代 | Required; must match `YY.M.W`. |
| 5 | 技术难度 | Preserve the source value or blank. |
| 6 | 优先级 | Preserve the source value or blank. |
| 7 | 客户名称 | Preserve the source value or blank. |
| 8 | URL | Required; preserve as traceable source link. |

Do not include `父ID`, `描述`, status, creation time, work-item type, or any other export column. Do not synthesize values from titles.

## Row preservation

- Record the source row count before transforming.
- Preserve every source row, including duplicate titles or duplicate URLs. This Skill is a transfer workflow, not a deduplication workflow.
- Stable-sort only by parsed iteration tuple `(year, month, week)`; preserve source order inside each iteration.
- Insert exactly three rows whose eight cells are all empty between adjacent iteration groups.
- Empty separator rows are formatting rows and are not counted as requirements.

## Blocking anomalies

Stop before DingTalk creation or writing when any row has:

- an empty title;
- an empty URL;
- an empty iteration;
- an iteration that does not match `^\d{2}\.\d{1,2}\.\d{1,2}$`;
- an iteration outside the selected target month.

Report source row number, title when available, invalid value, and suggested user choices. Never append an unknown iteration to the end silently.

## Preflight summary

Provide:

- source filename and worksheet;
- selected month;
- source requirement count;
- count per iteration;
- separator row count: `3 * (iteration_group_count - 1)`;
- final row count including one header row and separator rows;
- blocking and non-blocking anomalies.
