# Diagram Upload and Verification

Read only when writing or checking a document with diagrams. Apply the entrypoint's Archify image preference and the style guide's explicit-format exceptions. This reference does not require new tools or CLIs.

## Generate and Export

For new or materially changed diagrams supported by [archify](../../archify/SKILL.md), invoke that skill before drawing. Map architecture, process, request order, data movement, and state transitions to its `architecture`, `workflow`, `sequence`, `dataflow`, and `lifecycle` types respectively. This is the default even when the user does not name a drawing skill. Explicit editable-board requests and unsupported types use the native-board route instead.

1. Derive the diagram from the supplied document or scoped source evidence. Preserve unknown conditions as unknown rather than inventing retry counts, permissions, or relationships. Keep unaffected existing diagrams intact.
2. Follow Archify's type-specific schema, validation, delivery, and visual-review instructions. Reuse the user's established design when present, without changing global Archify presets. Split an unreadable diagram instead of shrinking labels or removing meaningful branches.
3. Read Archify's [canonical export instructions](../../archify/references/viewer-runtime.md#canonical-exports). Use the delivered HTML's existing export menu to save the complete diagram as PNG, without viewer controls, selection overlays, or cropping. A containment screenshot/contact sheet or social Share Card is not the document illustration. Inspect the PNG itself for nonblank rendering, legible Chinese text, complete branches, and unclipped labels at the intended document width.
4. Keep the specification, delivered HTML, and PNG beside the task's local Markdown in its D-drive output directory. Disposable checks belong in a task-specific directory under `D:/Claire/temp`. If export or inspection cannot run, report that gap and keep the source; do not label an unverified preview a finished image. Rendering a local diagram does not authorize business-page tests, a new hosting service, or product changes.

## Check Image Insertion Before Writing

Inspect the current cloud-document tools' schemas before any document write, including whether they can ingest local image bytes and insert the resulting resource. Availability of `create-doc` alone does not prove local-image upload support.

- **Local upload plus image-block tools:** use the supported cloud-document upload path and its returned resource ID to create an image block at the intended section. Record both resource and block IDs. Use a token only in a tool that explicitly accepts it.
- **URL-only Markdown import:** use `<image url="..." .../>` only with a real image URL the importer can access and the user has authorized using. The current `create-doc` interface accepts `url`, not `token`. A local D-drive path, `file://` URL, localhost URL, base64/data URL, or read-back image token is not an interchangeable upload URL.
- **No permitted local-to-image path:** keep the local PNG and source, name the missing upload/insertion capability, and help the user restore or enable that capability. Do not publish a document with silently omitted diagrams or substitute Mermaid without agreement. A missing capability is not necessarily an expired login. An explicitly requested local draft can still be delivered while Feishu publication is pending.

Do not upload internal diagrams to a public image host, repository, or unrelated IM/work-item attachment store to manufacture a URL. Do not install an upload CLI, request broader permissions, or create a new authentication path without approval. Retain the original document/target and resume there when the supported route is restored.

## Source Inventory and Upload Format

Before writing, identify each requested diagram by its section/caption, source files, and intended output (PNG image by default for Archify-supported types; native board when selected). Separate new/changed diagrams from existing diagrams that must remain untouched. For chunked writes, retain each chunk's expected new-image/new-board counts and returned document/task IDs.

| Available write path | Upload syntax | Response evidence |
| --- | --- | --- |
| Supported local image upload and document image blocks | Upload the PNG, then insert the returned resource using that tool's actual schema | Image resource and document block IDs |
| URL-only Feishu document MCP, with an authorized accessible image URL | `<image url="..."/>`; do not pass `token` | Final document image block/resource and successful image read-back |
| Native-board route through Feishu document MCP | Keep supported `mermaid` / `plantuml` fenced blocks only when that route meets the selected style | `board_tokens` in the completed operation, when provided |
| Native-board route through already installed and authorized `lark-cli` | Convert diagram fences in an upload-only copy to `<whiteboard type="mermaid">` / `<whiteboard type="plantuml">` | Board entries in `new_blocks`, when provided |
| Other supported native-board tools | Follow the current tool schema and the user's chosen diagram style | Created resource/block IDs and final document read-back |

Prefer the existing MCP route. Do not install CLI tools just to use another upload format. A read-back placeholder such as `<whiteboard token="..."/>` is not creation syntax. Do not replace the local preview file with an upload-only conversion or drop unsupported diagrams silently; use an available supported path or report the blocked diagram.

## Reconcile and Read Back

1. Wait for each write to finish. If it returns `task_id`, query the task through the current tool's supported status parameter; do not start another create/append. For a timeout without a task ID, inspect the original target before retrying. If a create has no returned ID, search the approved parent/location using the available read-only tools; if its outcome still cannot be established, pause the write rather than create a possible duplicate.
2. Check the completed operation's `warning` / `warnings` and actual image/board IDs against that operation's expected new diagrams. Reconcile image and board counts separately; zero board tokens can be correct for a PNG-only document. Count unique IDs, not duplicates or pre-existing resources. A mismatch requires investigation; an empty/omitted list is not proof that no diagrams were expected. On an update, unchanged resources need not appear in its response.
3. Read back the entire relevant scope, including every chunk and later section. Map each requested diagram to its actual section and board/image ID. Equal counts alone do not prove correct placement, and a visible placeholder alone does not prove the board rendered correctly.
4. Use the available board/file/image reading tool to inspect each new or changed diagram for nonblank rendering and the intended content. For an image, verify the actual inserted resource, not just the local PNG or its URL text. If the available response is unreadable or lacks needed detail, record that verification gap; do not invent successful rendering. Unrelated warnings need not imply diagram failure, but report warnings that remain relevant to delivery.

When the user explicitly requested editable boards, also verify that the result contains editable diagram nodes rather than a single raster image embedded in a board. A board token or preview alone does not establish editability; if node inspection is unavailable, report that part as unverified.

For a verification-only request without the original source, verify what can be observed and state that the expected total is unknown. Do not claim complete source-to-document reconciliation without a baseline.

## Localized Repair

- Determine the failed diagram from the warning and source-to-block mapping. For example, three expected diagrams and two returned tokens show a discrepancy, but do not establish that the third diagram is the one missing.
- Confirm whether the original diagram is missing, malformed, or already present before repair. Use a uniquely identified block/range or surrounding section through the current update tool; if it cannot be located unambiguously, clarify rather than replace the first similar diagram.
- Correct the affected diagram's syntax/upload format and replace or insert only that diagram. Do not overwrite the document, append all diagrams again, or recreate the document. Preserve the user's text, tables, and unaffected diagrams.
- Recheck the repaired operation and final content. Report expected/verified counts and the exact pending diagram or tool/permission gap. Delivery is complete only when the requested content and diagrams are actually verified.

Reference: [upstream document upload rules](https://code.fineres.com/projects/FXDATA/repos/skill-manager/browse/plugins/fx-workflow/skills/dev-doc-writer/SKILL.md).
