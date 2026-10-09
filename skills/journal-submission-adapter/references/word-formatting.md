# Word And Citation-Preserving Format Adaptation

## Route By Document State

For DOCX, discover the host's available Word MCP tools and confirm that they act on the intended absolute path. A live Word server such as `word_mcp_live` is the preferred editing layer. Do not assume a tool is connected because a Python package exists.

Use Word MCP for opening/derived-copy creation, targeted edits, paragraph/style changes, page layout, headers/footers, numbering, revisions, saving and visual inspection. Query actual tool schemas; tool names vary. If the server is exposed through stdio rather than native registration, an MCP client may connect to that installed server. This is still an MCP workflow, not permission to replace its writes with arbitrary COM commands.

Word MCP is mandatory for a live Zotero-linked document and when the user requests it. If it is unavailable, continue literature work and produce the adaptation plan, but identify the Word-editing blocker. For a field-free DOCX, an explicitly accepted alternative may be used when the host has no Word MCP; clearly report the route. Do not convert a linked manuscript to Markdown and rebuild it.

## Preflight

1. Open the correct source and identify whether it has Zotero or other live fields.
2. Record citation/bibliography field counts, figure/table counts, revision status and relevant sections. Read the displayed text as well as field presence.
3. Save a derived copy into the journal working area; keep the source unchanged. Inspect whether WPS/Word holds the destination before replacing it.
4. Change only the intended document. Do not close other projects or kill all Word processes to solve one file lock.

If a copy already exists and user edits are present, work with them. Do not overwrite a newer copy merely to recreate a clean pipeline.

## Live Zotero

Read the local Zotero citation skill before insertion or style conversion. Keep complete field payloads and item identity, not just displayed reference numbers. Broad paragraph replacement can delete a field; prefer bounded text islands around it or field-aware operations.

For changed scientific citations, match the actual library item and metadata, insert using the existing integration, and run Zotero's real Refresh. For section reordering or style conversion, refresh so numbering/order follow the document. Field counts alone do not prove validity.

For formatting or prose edits that do not touch citations/order/style, confirm complete field payloads are unchanged. Do not gratuitously refresh if it would change an already verified bibliography. Never unlink the fields to simplify editing.

## Apply Verified Submission Rules

Use a requirement table with source URLs, stage and check date. Apply the chosen article type's current requirements, not a production PDF's columns or another journal's template.

Check only relevant items:

- Section order, abstract structure and word limits, keywords.
- Title page, authors/affiliations and declarations using supplied facts.
- Required tables/legends, their callouts and any prescribed placement.
- Citation style through Zotero's supported style/preferences workflow.
- Paper size, margins, fonts, spacing and page/continuous line numbering when specified.
- Inline images when required; preserve locked figure pixels and scale bars.
- Revision/comment treatment required for the current stage.

If the journal permits format-free initial submission, keep an existing readable format unless a requirement or concrete layout problem calls for a change. Do not shrink type or compress paragraph spacing to force an unnecessary one-page cover letter.

## Postflight

Save through MCP, close/reopen the final derived document and inspect content and layout. Check the first page, all changed sections, representative image/table pages, bibliography and any known crowded areas. Detect clipped tables, captions separated from their figures, overlapping headers, duplicate page numbers and oversmall text.

Use Word MCP snapshot/layout tools when available. Do not generate an extra PDF if the user does not need one; temporary rendering, if required for inspection, stays in the working area. An empty layout-diagnostics list is useful but not a substitute for visual review.

Confirm numerical values, citation payloads, meaningful formatting and images were preserved except for explicitly authorized changes. Recheck figure/table/supplement callouts after reordering. Close only documents opened for this task after saving to avoid leaving upload files locked. Deliver editable DOCX and accurate validation scope.
