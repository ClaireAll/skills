# Diagram Upload and Verification

Read only when writing or checking a document with diagrams. Keep the embedded style guide's diagram-selection rules; this reference does not make Mermaid the default or require new tools/CLIs.

## Source Inventory and Upload Format

Before writing, identify each requested diagram by its section/caption, source format, and intended output (native board or image). Separate new/changed diagrams from existing diagrams that must remain untouched. For chunked writes, retain each chunk's expected new-board count and returned document/task IDs.

| Available write path | Upload syntax | Response evidence |
| --- | --- | --- |
| Feishu document MCP | Keep supported `mermaid` / `plantuml` fenced blocks; the tool converts them to native boards | `board_tokens` in the completed operation, when provided |
| Already installed and authorized `lark-cli` | Convert diagram fences in an upload-only copy to `<whiteboard type="mermaid">` / `<whiteboard type="plantuml">` | Board entries in `new_blocks`, when provided |
| Other supported board/image tools | Follow the current tool schema and the user's chosen diagram style | Created resource/block IDs and final document read-back |

Prefer the existing MCP route. Do not install CLI tools just to use another upload format. A read-back placeholder such as `<whiteboard token="..."/>` is not creation syntax. Do not replace the local preview file with an upload-only conversion or drop unsupported diagrams silently; use an available supported path or report the blocked diagram.

## Reconcile and Read Back

1. Wait for each write to finish. If it returns `task_id`, query the task through the current tool's supported status parameter; do not start another create/append. For a timeout without a task ID, inspect the original target before retrying. If a create has no returned ID, search the approved parent/location using the available read-only tools; if its outcome still cannot be established, pause the write rather than create a possible duplicate.
2. Check the completed operation's `warning` / `warnings` and actual board IDs against that operation's expected new diagrams. Count unique IDs, not duplicates or all pre-existing boards. A mismatch requires investigation; an empty/omitted list is not proof that no diagrams were expected. On an update, unchanged boards need not appear in its response.
3. Read back the entire relevant scope, including every chunk and later section. Map each requested diagram to its actual section and board/image ID. Equal counts alone do not prove correct placement, and a visible placeholder alone does not prove the board rendered correctly.
4. Use the available board/file/image reading tool to inspect each new or changed diagram for nonblank rendering and the intended content. If the available response is unreadable or lacks needed detail, record that verification gap; do not invent successful rendering. Unrelated warnings need not imply diagram failure, but report warnings that remain relevant to delivery.

For a verification-only request without the original source, verify what can be observed and state that the expected total is unknown. Do not claim complete source-to-document reconciliation without a baseline.

## Localized Repair

- Determine the failed diagram from the warning and source-to-block mapping. For example, three expected diagrams and two returned tokens show a discrepancy, but do not establish that the third diagram is the one missing.
- Confirm whether the original diagram is missing, malformed, or already present before repair. Use a uniquely identified block/range or surrounding section through the current update tool; if it cannot be located unambiguously, clarify rather than replace the first similar diagram.
- Correct the affected diagram's syntax/upload format and replace or insert only that diagram. Do not overwrite the document, append all diagrams again, or recreate the document. Preserve the user's text, tables, and unaffected diagrams.
- Recheck the repaired operation and final content. Report expected/verified counts and the exact pending diagram or tool/permission gap. Delivery is complete only when the requested content and diagrams are actually verified.

Reference: [upstream document upload rules](https://code.fineres.com/projects/FXDATA/repos/skill-manager/browse/plugins/fx-workflow/skills/dev-doc-writer/SKILL.md).
