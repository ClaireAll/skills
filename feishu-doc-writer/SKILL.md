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
3. Write the document:
   - If an exposed Lark/Feishu MCP tool exists, use its document creation/import tool.
   - If the user provides a Feishu MCP server URL, call it directly with MCP HTTP JSON-RPC.
   - Prefer the MCP tool named `create-doc` when available because it supports `wiki_node`.
4. Verify:
   - Read the created document back with `fetch-doc` or the available document-read tool.
   - Confirm the title, non-empty body, and at least one expected section/table.
   - Report the final Feishu link and any blocked permission/tool issue.

## MCP HTTP Pattern

Use this pattern when the user gives a URL like `https://mcp.feishu.cn/mcp/...` and the normal tool surface has stale credentials or lacks `create-doc`.

```js
const url = "https://mcp.feishu.cn/mcp/...";

async function rpc(id, method, params) {
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "content-type": "application/json",
      accept: "application/json, text/event-stream",
    },
    body: JSON.stringify({ jsonrpc: "2.0", id, method, params }),
  });
  return JSON.parse(await res.text());
}

await rpc(1, "initialize", {
  protocolVersion: "2025-03-26",
  capabilities: {},
  clientInfo: { name: "codex-local", version: "1.0.0" },
});

await rpc(2, "tools/call", {
  name: "create-doc",
  arguments: { title, wiki_node: wikiNodeOrUrl, markdown },
});
```

Then verify:

```js
await rpc(3, "tools/call", {
  name: "fetch-doc",
  arguments: { doc_id, limit: 1200 },
});
```

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
| "确认写进去了没" | Call `fetch-doc` and check title/body |

## Common Mistakes

| Mistake | Fix |
|---|---|
| Duplicating the H1 title in the body | Put the title in `title`; remove matching first body H1 |
| Using stale built-in Lark tools after the user provides a new MCP URL | Call the provided MCP URL directly |
| Claiming the doc is written without verification | Always read back with `fetch-doc` |
| Treating `.env.local` or secrets as doc content | Never include secrets unless the user explicitly asks and it is safe |
| Letting PowerShell corrupt Chinese script literals | Read Chinese from UTF-8 files or encode literals safely |

## Success Report

End with:

- the Feishu URL returned by the tool,
- whether read-back verification succeeded,
- the local source file path if one was generated,
- any missing permission or unsupported tool capability if blocked.
