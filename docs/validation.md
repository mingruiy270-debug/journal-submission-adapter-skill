# Validation Scope

Checked locally on 2026-10-09 for version 1.0.1. This is a bounded execution record, not a guarantee of access to every publisher, submission readiness or editorial acceptance.

## Automated Tests

29 unit/integration tests passed with the optional requests and PyMuPDF dependencies installed. Coverage includes PDF/HTML discrimination, declared and streamed size limits, existing-file protection, portable names, safe query-free diagnostics, actual PDF parsing, text/page locators, and a local HTTP-to-PDF-to-text transaction using both transports. Redirect tests include a large 302 body followed by a small PDF, invalid/missing destinations and bounded loops. Both transports explicitly handle redirects without reading intermediate bodies.

Skill-creator structural validation, compilation and bundled-resource link checks are performed separately; automated helper tests do not execute scientific reading or Word editing.

## Real Manuscript Run

A local, unpublished multi-omics manuscript was adapted for Cell & Bioscience using native web discovery of current official instructions and three publisher-verified research articles from the preceding three months. All three full PDFs were acquired and extracted locally. Relevant Introduction, Methods, Results, Discussion and main legends were actually read; main figures were visually inspected. Two paper readings received a disjoint subagent review. Individual reference lists and separately hosted supplements were not independently reviewed.

The publisher's online-first HTML pages did not expose complete article bodies. The standard-library PDF transport returned HTML and was correctly rejected. Explicit ordinary requests transport through the user's configured proxy acquired the PDFs. A subsequent independent code review found automatic redirect-body consumption; this was fixed for both transports and covered by regression tests. This does not establish all proxy, TLS or institutional-access routes.

An installed stdio Word MCP was connected successfully (122 tools, 46 live). It edited title, the official three-section abstract, Introduction, Results headings, Discussion and cover letter in derived DOCX files, then applied submission formatting and saved/reopened them. This server lacked open/close tools, so a narrow Office lifecycle bridge opened named files and closed task-owned documents. All content, formatting and SaveAs writes used MCP.

Read-only OOXML comparisons confirmed all 70 complete Zotero citation payloads and the bibliography field were unchanged, together with the editable table and all eight embedded figure media files. The eight separate figure files were also unchanged. No citations were added, reordered or restyled; Zotero Refresh was therefore not invoked. Field preservation here is not proof that insertion or Refresh was tested.

Word captures and page text were inspected for the title/abstract, representative changed sections, table, figures, references and one-page cover letter. Search results that repeated table positions and inherited paragraph formatting were handled explicitly. A source statistical annotation remained inconsistent with its reported adjustment; it was reported as unresolved, not cosmetically certified. No analysis was rerun to resolve it.

The authenticated journal portal, actual file upload, reviewer-token validity and submission were not tested. No manuscript, author details, downloaded full papers or confidential access credentials were placed in this public repository. No hash manifest was generated.

## Earlier Synthetic Test

The initial release included an independent synthetic-manuscript forward test of requirements discovery, partial accessible literature, prose adaptation and truthful access-failure handoff. It did not complete three full-paper readings or Word editing. The real run above extends that coverage without retroactively changing the earlier outcome.

## Remaining Limits

Live citation insertion, citation reorder/style conversion and actual Zotero Refresh; OCR quality; every publisher/access route; a full scientific reanalysis; and authenticated submission form validation remain untested. Behavioral scenarios are test specifications unless an execution above explicitly covers them.
