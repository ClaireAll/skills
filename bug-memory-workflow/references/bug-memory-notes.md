# Bug Memory Notes

## Search Locations

Search these before bug edits:

- `D:\Claire\memory\bug-fix.md` (primary Bug history)
- `C:\Users\Claire\.codex\memories\MEMORY.md`
- `C:\Users\Claire\.codex\memories\extensions\ad_hoc\notes\`
- `D:\Claire\memory\extensions\ad_hoc\notes\` if the junction path needs direct access

Prefer `rg`. Search `bug-fix.md` by work item, repo, module, API, error, or symptom before reading a narrow matching section. If `rg` is unavailable or denied, use PowerShell `Select-String`.

Example PowerShell fallback:

```powershell
$terms = @("repo-name", "module-name", "error text")
Select-String -Path "C:\Users\Claire\.codex\memories\MEMORY.md" -Pattern $terms -SimpleMatch
Get-ChildItem "C:\Users\Claire\.codex\memories\extensions\ad_hoc\notes" -Filter "*.md" |
  Select-String -Pattern $terms -SimpleMatch
```

## Write Location

Write every verified Bug fix to the unified file:

`D:\Claire\memory\bug-fix.md`

Before writing, search for the same work item or confirmed problem. Update that entry when it already exists; otherwise append a new entry under `## 后续记录`. Do not create a per-Bug Markdown file under `extensions/ad_hoc/notes`.

## Entry Template

```md
### <yyyy-MM-dd> | <short title>

scope: <repo/module/page/api>
date: <yyyy-MM-dd>
status: verified
issue: <work item key or link, when known>

#### Symptom
<confirmed user-visible symptom, failing test, error, or regression>

#### Root Cause
<confirmed mechanism and code path>

#### Fix
<what changed and why it fixed the root cause>

#### Verification
<fresh verification command or manual check and result>

#### Delivery
<commit, comment, push, PR, or worklog status when relevant>

#### Reuse Hint
<what to check first next time; what mistake to avoid>

#### Keywords
<repo>, <module>, <component>, <api>, <error>, <data key>, <symptom words>
```

## Quality Bar

- Mention concrete files, routes, APIs, and data keys when they are relevant.
- Keep the entry compact; prefer 100-250 words.
- Include a reuse hint that changes future debugging behavior.
- If the fix involved a repo-specific workflow, link the memory to that repo in `scope` and `Keywords`.
- Preserve confirmed delivery status, but do not copy full diffs, full comments, or unresolved investigation branches.
