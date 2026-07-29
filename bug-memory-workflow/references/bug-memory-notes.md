# Bug Memory Notes

## Search Locations

Search these before bug edits:

- `C:\Users\Claire\.codex\memories\MEMORY.md`
- `C:\Users\Claire\.codex\memories\extensions\ad_hoc\notes\`
- `D:\Claire\memory\extensions\ad_hoc\notes\` if the junction path needs direct access

Prefer `rg`. If `rg` is unavailable or denied, use PowerShell `Select-String`.

Example PowerShell fallback:

```powershell
$terms = @("repo-name", "module-name", "error text")
Select-String -Path "C:\Users\Claire\.codex\memories\MEMORY.md" -Pattern $terms -SimpleMatch
Get-ChildItem "C:\Users\Claire\.codex\memories\extensions\ad_hoc\notes" -Filter "*.md" |
  Select-String -Pattern $terms -SimpleMatch
```

## Write Location

Write one note per verified bug fix:

`C:\Users\Claire\.codex\memories\extensions\ad_hoc\notes\<timestamp>-bug-<short-slug>.md`

Use local time for `<timestamp>` in `yyyy-MM-ddTHH-mm-ss` format. Keep `<short-slug>` lowercase, short, and searchable.

## Note Template

```md
# Bug Memory: <short title>

scope: <repo/module/page/api>
date: <yyyy-MM-dd>
status: verified

## Symptom
<confirmed user-visible symptom, failing test, error, or regression>

## Root Cause
<confirmed mechanism and code path>

## Fix
<what changed and why it fixed the root cause>

## Verification
<fresh verification command or manual check and result>

## Reuse Hint
<what to check first next time; what mistake to avoid>

## Keywords
<repo>, <module>, <component>, <api>, <error>, <data key>, <symptom words>
```

## Quality Bar

- Mention concrete files, routes, APIs, and data keys when they are relevant.
- Keep the note compact; prefer 100-250 words.
- Include a reuse hint that changes future debugging behavior.
- If the fix involved a repo-specific workflow, link the memory to that repo in `scope` and `Keywords`.
