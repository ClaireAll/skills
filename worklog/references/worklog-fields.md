# Feishu Bug Worklog Fields

## Page

Open:

```text
https://project.feishu.cn/b2rl2h/meegoPlg/MII_686B6DA98EC9C002_board_f3d5nl
```

The page is a Feishu Project/Meego work-hour calendar. Selecting a time block opens a worklog modal.

## Field Mapping

| Purpose | UI field | Value |
|---|---|---|
| Work item type | `* 工作项类型` | Select `缺陷` |
| Work item instance | `* 工作项实例` | Search and select the repaired bug by exact id/title |
| Duration | `* 记录工时` | Keep or enter the selected hour/minute duration |
| Start time | `* 开始时间` | Keep or enter the selected start datetime |
| Log body | `登记日志` | Bug description and fix plan |
| Submit | `提交工时` | Click only after exact values are confirmed |

`工作项实例` may stay disabled until `工作项类型` is set.

## Browser Automation Notes

- The worklog app runs inside a Feishu iframe. The parent page can expose the iframe in snapshots, but direct DOM evaluation from the parent cannot read the iframe body.
- If the page shows a login screen, expired-session prompt, or API calls indicate authentication has expired, notify the user to manually log in in the browser. Do not ask for credentials, do not try to automate password entry, and resume the worklog flow after the user completes login.
- The direct plugin URL may render as an empty shell outside the Feishu runtime context. Do not spend time debugging the blank direct page if the embedded app works. A same-origin blank plugin page can still be useful for authenticated `fetch` calls to the worklog API.
- Calendar drag can open a modal with the wrong range. After the modal opens, fill `记录工时` and `开始时间` directly from the requested time block.
- Semi Select dropdowns may not select when clicking visible option text. Prefer: open combobox, type/filter the value, use `ArrowDown`/`Enter`, then verify the combobox value changed.
- After refresh, the page may default to month view. Switch to week view to verify personal worklog entries.

## Log Template

Use this compact format:

```text
问题描述：<bug description>
修复方案：<fix plan>
```

If the current project has an established bug-comment template, reuse its confirmed `问题描述` and `修复方法/修复方案` content and keep the same meaning. The issue body may contain only reproduction details; in that case, inspect issue comments/remarks for the confirmed bug template. Do not include raw diffs, long code snippets, speculation, root-cause analysis, or unrelated verification notes unless the user asks for them.

## Matching Rules

- Prefer a Feishu bug id, URL, or issue key from the current task.
- If no id is available, search by the exact bug title from the just-fixed bug.
- If search returns multiple plausible bugs, stop and ask the user which one to use.
- If exact UI search returns `暂无数据`, do not stop immediately when an exact Feishu issue URL/id is available. Use the API fallback below to confirm the work item from Feishu Project itself.
- If the selected calendar block already populated duration/start time, treat those visible values as the source of truth unless the user requested a different time range.

## Time Block Selection

- If the user supplies an exact start time and duration, use those values.
- If the user does not supply a start time or duration, use the default random/free-slot rule: no overlap with existing worklogs, duration 1-3 hours, and start time after 09:00 and before 20:00 local time.
- If the user supplies different random/free-slot constraints, use the user's latest constraints instead of the default rule.
- For any random/free slot, query existing worklogs for the target local day before choosing. If no date is specified, use the current local date or the visible worklog date/week implied by the current page context.
- Convert each existing `date_started` from UTC ISO to local time and compute `[start, start + time_spent]`.
- Choose a slot that does not overlap any existing interval and satisfies the active constraints. `开始时间在 9 点以后，晚上 8 点之前，时长 1-3h` means the start time must be within `[09:00, 20:00)` and the duration must be between 60 and 180 minutes.
- Prefer a small buffer between intervals when convenient, but non-overlap is the hard requirement. Stop and ask if no valid slot exists.
- Do not use issue status or elapsed fields such as `已进行 8 小时` as the worklog duration.

## API Fallback

Use this only after the UI cannot select an exact instance and the user has asked to submit.

1. Capture the current `x-worklog-key` from an existing worklog request such as `POST https://feishu-worklog.sre.jdydevelop.com/api/worklogs/query`. Do not store or reuse old keys across sessions.
2. Confirm the bug from Feishu Project detail:

```text
GET https://project.feishu.cn/goapi/v2/projects/<space_id>/work_item/issue/<issue_id>?
```

The response must confirm:

- `project_key` equals the worklog `space_id`
- `work_item_type_key` is `issue`
- `work_item_id` equals the requested issue id
- `field_8c1141` is the exact issue title

3. Check for duplicates before creating:

```text
POST https://feishu-worklog.sre.jdydevelop.com/api/worklogs/query
```

Use the current user id, the exact space id, and the local day converted to UTC ISO range. Stop if the same work item and time block already exist. Also stop or choose another allowed slot if the target interval overlaps any existing interval on that local day.

4. Create the worklog with `POST https://feishu-worklog.sre.jdydevelop.com/api/worklogs`.

Required payload fields:

| Field | Value |
|---|---|
| `work_item_id` | Exact issue id from Feishu detail, numeric |
| `work_object_id` | `issue` |
| `work_object_name` | `缺陷` |
| `work_item_name` | Exact issue title |
| `space_id` | Feishu project key |
| `time_spent` | Duration in minutes |
| `date_started` | Start time as UTC ISO; for China time `2026-07-29 08:30:00`, use `2026-07-29T00:30:00.000Z` |
| `user_id` | Current logged-in worklog user id |
| `work_description` | Rich text object below |

Rich text description shape:

```json
{
  "doc": "{\"0\":{\"ops\":[{\"insert\":\"问题描述：...\\n修复方案：...\\n\"}],\"zoneId\":\"0\",\"zoneType\":\"Z\"}}",
  "doc_text": "问题描述：...\n修复方案：...\n",
  "is_empty": false
}
```

5. Verify by querying the same day again. Then refresh the page, switch to week view if needed, and confirm:

- `本周总工时` includes the submitted duration.
- The target date cell shows the submitted duration.
- The entry resolves to `缺陷/<exact issue title>`; it may briefly show `未知工作对象/未知工作项` while the app resolves names.
- The visible log snippet matches the description.
