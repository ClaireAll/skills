---
name: codex-session-timeline
description: Use when browsing local Codex Desktop sessions by Shanghai calendar date, checking per-session token usage, or generating a standalone HTML timeline.
---

# Codex Session Timeline

Generate a local HTML timeline from the current user's Codex session files. This works with the user's own Codex installation and does not require the original author's database, credentials, or machine paths.

## Run

Run the bundled script with Node.js, using the installed skill's actual path:

```text
node <skill-directory>/scripts/refresh.mjs
```

To generate a page with a date preselected:

```text
node <skill-directory>/scripts/refresh.mjs --date YYYY-MM-DD
```

The general page is `index.html`; the dated page is `<YYYY-MM-DD>.html`. Both open directly in a browser without a server. Output defaults to `<CODEX_HOME>/codex-session-timeline`, or `~/.codex/codex-session-timeline` when `CODEX_HOME` is unset. Set `CODEX_SESSION_TIMELINE_DIR` to choose another output directory.

## Data rules

- Read session IDs and timestamps from local rollout metadata, titles from `session_index.jsonl`, and usage only from saved `token_count` events. Do not parse, display, or persist message text, tool output, prompts, environment context, or credentials.
- Use the latest saved cumulative `total_tokens` value for each session. If the local record has no usage snapshot, show `暂无`; do not estimate usage or send transcript data to a service to recover it.
- Convert each session timestamp to its `Asia/Shanghai` calendar date. Show sessions in chronological order for the selected date.
- Session categories are not consistently available in local Codex records. Omit the category badge when there is no category instead of inventing one.
- Keep session IDs only as local JSON identity keys; never display them in the page.
- Keep a local file-signature cache in `sessions.json` so unchanged rollout files are not re-read. Do not embed that cache in the HTML.
- If the Codex sessions directory is unavailable or no session metadata can be read, report the error and preserve existing output files.

## Page

Keep the single-date picker, selected-day total, and non-expandable chronological rows. Each row shows its time, title, and known token count. Preserve the three themes, their upper-right controls, and the decorative corner artwork in `assets/index.html`.
