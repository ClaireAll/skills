---
name: codex-session-timeline
description: Use when querying Codex Desktop sessions by Shanghai calendar date, viewing per-session token usage, or generating a local HTML session timeline.
---

# Codex Session Timeline

Use the imported `codex_log` records to maintain a metadata-only JSON index and a standalone, date-filtered HTML timeline. The page has three visual themes in its upper-right corner; its session rows are static and never expand.

## Run

1. Refresh the local index and generate the page. The script reads `D:\Claire\storage\.env.local` for read-only access to Supabase; set `CODEX_SESSION_TIMELINE_ENV` to use another env file.

   ```powershell
   node D:\Claire\skills\codex-session-timeline\scripts\refresh.mjs
   ```

2. Open the generated HTML directly. The session data is embedded in the page, so it works from a local file without a server. To create a page that opens on a specific date:

   ```powershell
   node D:\Claire\skills\codex-session-timeline\scripts\refresh.mjs --date 2026-09-23
   ```

   This also writes `D:\Claire\codex-session-timeline\2026-09-23.html`, with that date preselected. The general page remains `index.html`.

The persistent output is `D:\Claire\codex-session-timeline\sessions.json` and `index.html`. Set `CODEX_SESSION_TIMELINE_DIR` to change that directory. The date-specific HTML is generated from the same index.

## Data rules

- Read only `codex_thread_id`, `date`, `created_at`, `thread_title`, `category`, and `token_count` from `codex_log`. Do not derive a second, competing session list from raw JSONL or overwrite the curated daily titles.
- The daily import pipeline owns title cleanup, segmentation, timezone handling, categorization, and token attribution. Display those stored values as-is; sum `codex_log.token_count` only for the selected date.
- Do not read or persist user messages, assistant replies, tool output, environment context, or other transcript text. Do not write to Supabase or generate daily-report summaries.
- Keep session IDs in the local JSON only for identity; never display them.
- The selected date is a single `Asia/Shanghai` calendar day. The total is the sum of known per-session usage for that date. Show `暂无` when no usage exists; if some sessions lack usage, mark the total as partial and show `暂无` on those rows.

## UI and data boundaries

- Keep the date picker, selected-day total, and chronological session timeline. Each non-expandable row shows time, title, category, and token count.
- Preserve the decorative corner artwork and distinct paper, forest, and geometric themes in `assets/index.html`. The three theme buttons sit at the upper right and show only their theme names; do not add a visible “样式” label.
- The HTML embeds the same metadata index and can be opened directly. `sessions.json` is refreshed read-only from `codex_log`.
- If credentials, the user identity, or the database is unavailable, report the error and preserve the existing JSON and HTML.
