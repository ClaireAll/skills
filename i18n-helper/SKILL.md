---
name: i18n-helper
description: Use when checking a JavaScript or TypeScript project's i18n JSON usage, finding unused translation keys, duplicate translation values, or preventing false unused-key cleanup caused by quoted characters inside keys.
---

# I18n Helper

Use the bundled report script to analyze configured i18n JSON keys against project source usage. The script separates call-location regexes from first-argument parsing so keys such as `specified_o'clock.opt` are not truncated by naive quote matching.

Reports are generated with Chinese UI text. Keys starting with `BI` are ignored by unused-key and duplicate-value checks.

## Configuration

Read `config.md` before running the report. Its first three lines are the contract:

1. Absolute project path.
2. I18n JSON file path inside the project, or an absolute JSON path.
3. JSON array of regex patterns that locate i18n call openings.

Default:

```text
D:\work\fv-web2
packages\jsy-web\i18n\zh_CN.json
["BI\\.i18nText\\s*\\(", "(?<![A-Za-z0-9_$.])(?:t|i18n\\.t|\\$t)\\s*\\("]
```

Keep the third line as call locators ending near `(`. If older capture regexes are present, the script still starts parsing from the match start and ignores captured groups.

## Run

From this skill directory:

```powershell
python .\scripts\i18n_report.py
```

Useful options:

```powershell
python .\scripts\i18n_report.py --config .\config.md --no-open
python .\scripts\i18n_report.py --output .\i18n-helper-report.html
```

The default output is always `D:\Claire\skills\i18n-helper\i18n-helper-report.html`; each run overwrites that same fixed file. The script opens it unless `--no-open` is passed.

By default, the report script also starts a temporary local action service on `127.0.0.1` for manual refresh, duplicate-key replacement, and unused-key deletion. Use `--no-server` when only a read-only report is needed.

## Manual Refresh

The report title includes a `刷新` button when the local action service is running. It posts to `/refresh`, re-runs the scan, rewrites the same fixed HTML report path, then reloads the page with a cache-busting query parameter. Refresh does not edit source files or locale JSON.

## Report Rules

| Section | Meaning |
| --- | --- |
| Unused-key section | Keys present in the configured JSON that were not found as complete static first arguments or complete quoted source literals; each row can be selected for deletion when the local action service is running. |
| Missing-used-key section | Keys still used by scanned source as static i18n call arguments but absent from the configured JSON; these usually need either source replacement or JSON restoration before cleanup is safe. |
| Duplicate-value section | Used keys with non-empty string values grouped after NFKC width normalization, trimming, and whitespace collapse; unused keys stay only in the unused-key section. |

## Duplicate-Value Replacement

In the duplicate-value table:

- The checkbox before a key marks that key as the source to replace.
- The checkbox after a key marks that key as the replacement target for the same value group.
- Only one replacement target can be selected inside the same value group.
- Multiple checked source keys in one group map to that group's checked target. For example, checked sources `A` and `B` with target `C`, plus checked source `D` with target `E` in another group, must submit `{A: C, B: C, D: E}`.
- Keys starting with `HD` remain visible as source rows but must not render a replacement-target checkbox.
- The execute button submits the full checked source-to-target replacement map to the local service, replaces matching source string literals in project source files, deletes actually replaced source keys from `zh_CN.json`, `en_US.json`, and `zh_TW.json` only after a post-replacement rescan confirms they are no longer used, then re-runs the scan and rewrites the same HTML report path.
- After a successful replacement, the page must reload the whole HTML report with a cache-busting query parameter so the visible data matches the rewritten report.

Replacement is intentionally narrow: it scans source files only, skips the configured i18n JSON directory, ignores comments, and replaces only complete single-quoted, double-quoted, or non-interpolated template string literals whose decoded content exactly matches a selected source key. Replace the literal content while preserving its surrounding quote/backtick; never do bare substring replacement, so a map like `{A: C}` must not turn `A_B` into `C_B`. Locale cleanup runs only for source keys that were actually replaced.

## Scoped HD-Prefix Replacement

Use `scripts/hd_prefix_report.py` when the user wants to find only source keys with a prefix such as `HD` inside one directory and choose same-value replacements in HTML.

```powershell
python .\scripts\hd_prefix_report.py --scan-root D:\work\fv-web2\packages\jsy-web-analysis\src\pages\new-analysis\components\workflow
```

The report overwrites `D:\Claire\skills\i18n-helper\i18n-helper-report.html`, starts a local refresh/replace service unless `--no-server` is passed, and replaces only complete string literals inside `--scan-root`. It does not delete `zh_CN.json`, `en_US.json`, or `zh_TW.json`.

## Unused-Key Deletion

In the unused-key table:

- The checkbox before a key marks that key for deletion from the configured i18n JSON.
- The delete button submits selected keys to the local action service, deletes exact top-level keys first, falls back to nested dot-path deletion, then re-runs the scan and rewrites the same HTML report path.
- Deletion updates `zh_CN.json`, `en_US.json`, and `zh_TW.json` in the configured i18n JSON directory. It does not edit source files.

Both replacement and deletion are implemented in `scripts/i18n_report.py`; avoid adding one-off helper scripts outside this skill for these actions.

## Static Argument Parsing

Use the script's parser rather than raw regex captures for keys. It supports single quotes, double quotes, escaped characters, template literals without interpolation, static string branches in a conditional first argument, and complete source string literals wrapped in single or double quotes. It marks template literals with `${...}` and non-static branches as dynamic.

Example that must remain a complete static key:

```ts
BI.i18nText("fxp.data.data_center.specified_o'clock.opt", index)
```

The extracted key is:

```text
fxp.data.data_center.specified_o'clock.opt
```

Conditional first arguments count each static branch as used, while string literals in the condition do not count:

```ts
BI.i18nText(mode === 'edit' ? 'HD-Basic_Edit_Connection' : 'HD-Basic_Add_Connect')
```

The extracted keys are:

```text
HD-Basic_Edit_Connection
HD-Basic_Add_Connect
```

Complete keys wrapped in single or double quotes anywhere in scanned source also count as used, even outside i18n calls. Comment text is ignored:

```ts
const key = 'HD-Basic_Edit_Connection'
const next = "HD-Basic_Add_Connect"
```

## Verification

After editing this skill, run:

```powershell
python .\scripts\test_i18n_report.py
python D:\Claire\skills\.system\skill-creator\scripts\quick_validate.py D:\Claire\skills\i18n-helper
```
