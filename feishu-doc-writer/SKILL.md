---
name: feishu-doc-writer
description: Use when creating, importing, updating, or verifying Feishu/Lark cloud documents or wiki pages from Markdown, especially when the user asks to generate a Feishu doc, write under a wiki node, use a Feishu MCP URL, follow a Feishu doc style guide, or read back a created document.
---

# Feishu Doc Writer

## Overview

Create Feishu/Lark documents from Markdown with the user's preferred document style, then verify the created document by reading it back. Prefer MCP tools over browser/manual instructions whenever a Feishu MCP server or Lark MCP tools are available.

## Required Reference

Before writing a Feishu document, read:

```text
references/feishu-doc-style-guide.md
```

This embedded reference is copied from the user's Feishu document style guide. Treat it as the source of truth for structure, tone, tables, callouts, and "do not invent" rules.

## Workflow

1. Identify the target:
   - `wiki_node`: a Feishu wiki URL or wiki node token when the user says "挂在这个下方" or gives a wiki page.
   - `folder_token`: only when the user explicitly gives a folder.
   - no location: create in the default personal space only if the user did not provide a target.
2. Prepare Markdown:
   - Follow the embedded style guide.
   - Put the document title in the MCP `title` field.
   - Remove a matching first-level `# Title` from the Markdown body to avoid duplicate titles.
   - Do not hand-write a table of contents.
   - Convert GitHub callouts like `> [!IMPORTANT]` into Feishu `<callout>` blocks when using `create-doc`.
   - If the requested content contains diagrams, read [references/diagram-verification.md](references/diagram-verification.md). Record their sections, intended output types, and expected counts before writing; keep the local preview source unchanged.
3. Write the document:
   - If an exposed Lark/Feishu MCP tool exists, use its document creation/import tool.
   - If the user provides a Feishu MCP server URL, call it directly with MCP HTTP JSON-RPC.
   - Prefer the MCP tool named `create-doc` when available because it supports `wiki_node`.
4. Verify:
   - Read the created document back with `fetch-doc` or the available document-read tool.
   - Confirm the title, non-empty body, and requested sections/tables. Read the relevant scope in full, including later diagrams; a truncated first-page response is not complete verification.
   - For diagrams, reconcile each write's returned board tokens/blocks and warnings with the source inventory, then verify the final document's corresponding diagrams. If tokens/counts are unavailable, use actual read-back evidence; do not infer completeness from the body or an absent warning.
   - Fix a failed diagram only in its uniquely identified location, preserve unrelated content, and read back again. Report the final Feishu link, verified diagram count when applicable, and any pending issue; partial diagram conversion is not complete delivery.

## Connection and Uncertain Writes

- If tools are missing, disconnected, or unauthorized, help the user reconnect through the available entry point; cloud-document renewal may use `https://open.feishu.cn/page/mcp`. Preserve the target and progress, and distinguish permission/scope errors from expired authorization. After user authorization, verify the original target with a read-only MCP call before resuming; browser login alone does not prove MCP recovery.
- If a write returns `task_id`, query that task's status with the available tool instead of submitting the write again. On a timeout or uncertain result, inspect the original target before retrying; an unresolved result stays pending, not failed or completed.
- Do not create a replacement document or duplicate append to recover a diagram. Keep the original document ID/URL and update only confirmed missing or failed content within the user's approved scope.

## MCP HTTP Pattern

Use this pattern when the user gives a URL like `https://mcp.feishu.cn/mcp/...` and the normal tool surface has stale credentials or lacks `create-doc`.

- Use an available MCP-compatible HTTP client that handles both JSON and SSE responses, session state, and initialization. Do not treat a raw `text/event-stream` body as JSON or build a second authentication system.
- Initialize the connection and list tools to inspect their current schemas before calling them. Keep credential-bearing server URLs out of reports, artifacts, and logs.
- Call the available creation tool with the requested `title`, `markdown`, and mutually exclusive location argument such as `wiki_node`. Preserve the returned document/task ID, then read back the original document with `fetch-doc` or its equivalent without an arbitrary short character limit.
- If no compatible client is available, help reconnect the built-in MCP tools instead of installing dependencies or retrying raw writes whose results cannot be interpreted safely.

## Markdown Preparation Notes

Use UTF-8 file reads for Chinese content. If PowerShell pipelines corrupt Chinese text into question marks, avoid inline Chinese scripts and read titles/content from files instead.

Minimal title/body split:

```js
let markdown = fs.readFileSync(markdownPath, "utf8");
const firstLine = markdown.split(/\r?\n/, 1)[0] || "";
const title = firstLine.replace(/^#\s*/, "").trim() || fallbackTitle;
markdown = markdown.replace(/^#\s+[^\r\n]+\r?\n\r?\n?/, "");
```

Callout conversion:

```js
function convertCallout(md, tag, emoji, bg) {
  const pattern = new RegExp("> \\\\[!" + tag + "\\\\]\\\\n> ([^\\\\n]*(?:\\\\n> [^\\\\n]*)*)", "g");
  return md.replace(pattern, (_, body) =>
    `<callout emoji="${emoji}" background-color="${bg}">\n${body.replace(/^> /gm, "")}\n</callout>`
  );
}
```

## Quick Reference

| User request | Action |
|---|---|
| "生成飞书文档" | Read style guide, create Markdown, call `create-doc` |
| "挂在这个 wiki 下方" | Pass the wiki URL/token as `wiki_node` |
| "我给你飞书 MCP URL" | Use HTTP JSON-RPC, list tools if needed, call `create-doc` |
| "重新完善飞书文档" | Create/update content using the embedded style guide, then verify |
| "确认写进去了没" | Read back the requested content; verify corresponding diagrams when present |

## Common Mistakes

| Mistake | Fix |
|---|---|
| Duplicating the H1 title in the body | Put the title in `title`; remove matching first body H1 |
| Using stale built-in Lark tools after the user provides a new MCP URL | Call the provided MCP URL directly |
| Claiming the doc is written without verification | Always read back with `fetch-doc` |
| Treating a successful body read-back as proof all diagrams converted | Check the source inventory, returned boards/warnings, and final diagram content |
| Retrying a timed-out create/append immediately | Query the task or original target first; do not duplicate content |
| Treating `.env.local` or secrets as doc content | Never include secrets unless the user explicitly asks and it is safe |
| Letting PowerShell corrupt Chinese script literals | Read Chinese from UTF-8 files or encode literals safely |

## Success Report

End with:

- the Feishu URL returned by the tool,
- whether read-back verification succeeded,
- expected versus verified diagrams, when diagrams were requested,
- the local source file path if one was generated,
- any missing permission or unsupported tool capability if blocked.
