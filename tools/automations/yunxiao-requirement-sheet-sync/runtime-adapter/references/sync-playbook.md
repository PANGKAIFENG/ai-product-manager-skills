# DingTalk Sync Playbook

Use the current `dws` help as the authority if flags drift. DingTalk writes must not fall back to browser or HTTP calls.

## Command contract

Let `<node-url>` be the user-provided DingTalk sheet URL, `<sheet-name>` the collision-safe name, `<sheet-id>` the ID returned by create, `<csv-path>` the verified local CSV, and `<last-row>` the final CSV row number.

```bash
dws doc info --node "<node-url>" --format json
dws sheet list --node "<node-url>" --format json
dws sheet new --node "<node-url>" --name "<sheet-name>" --format json --yes
dws sheet csv-put --node "<node-url>" --sheet-id "<sheet-id>" --start-cell A1 --csv "@<csv-path>" --allow-overwrite --format json --yes
dws sheet range set-style --node "<node-url>" --sheet-id "<sheet-id>" --range A1:H1 --bg-color '#FCC102' --font-weight bold --format json --yes
dws sheet update --node "<node-url>" --sheet-id "<sheet-id>" --frozen-row-count 1 --index 0 --format json --yes
dws sheet info --node "<node-url>" --sheet-id "<sheet-id>" --format json
dws sheet range read --node "<node-url>" --sheet-id "<sheet-id>" --range "A1:H<last-row>" --value-render-option raw_value --format json
```

`--allow-overwrite` is permitted only because the target is a newly created, empty Sheet. It must never be used to target an existing Sheet selected by name.

## Error handling

- Every call uses `--format json`.
- If a call fails, retry the exact same command once with `--verbose` added.
- Do not change flags, switch tools, create another Sheet, or broaden the operation during retry.
- If the retry fails, stop and report the raw error category, successful prior steps, Sheet name/ID if created, and the next recoverable action.
- Never delete a partially created Sheet without separate user approval.

## Collision handling

1. Compute `智能体{M}月需求-MMDD` in Asia/Shanghai time.
2. Compare it with the exact names returned by `dws sheet list`.
3. On collision, compute `智能体{M}月需求-MMDD-HHmm` using the current time.
4. If the second name also exists, stop. Do not add arbitrary counters or overwrite.

## Verification

- Treat `sheet new` output as the only source of the new Sheet ID.
- Read `sheet info` after update and verify name, frozen row count, and index.
- Read the full expected data range and compare values with the local CSV, including blank separator rows.
- Verify the style command targeted `A1:H1`; if DWS cannot read styles, report command success as style evidence rather than claiming visual inspection.
