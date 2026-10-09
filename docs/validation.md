# Validation Scope

Checked locally on 2026-10-09. This records the scope of the first release, not a guarantee of editorial acceptance or successful access to every publisher.

## Executed

- Codex skill-creator structural validation: passed.
- Python compilation and bundled-resource link checks: passed.
- 18 unit/integration tests: passed, including download failures, existing-file protection, portable filenames, safe network diagnostics, real PDF parsing and a local HTTP-to-PDF-to-page-text transaction.
- Word MCP handshake: passed; 122 tools listed, including 46 live tools. No real manuscript was opened or edited.
- Independent native-browsing forward test on an explicitly synthetic manuscript: produced a current official-requirements table, selected-paper/reading record, revised abstract and cover-letter core, and review findings.

## Live Access Limits

Three publisher PDF links tested by the main agent returned non-PDF responses and were rejected. The independent test's ordinary requests obtained no local full-text files. It read an abstract, a partial Introduction and a substantial but incomplete HTML article. It explicitly did not report three full-paper readings or completed paper-informed submission preparation.

These outcomes validate failure handling and honest completion reporting, not successful publisher acquisition or a complete real-paper adaptation. Manual title/DOI/official-link handoff remains available. No access challenge was bypassed, no private manuscript was uploaded and no hash manifest was generated.

## Corrections From Validation

The skill distinguishes browser-readable fallback from local acquisition, and selected-paper count from completed-reading count. Partial reading can support only section-specific observations. Download failures now record safe error classes/categories without exception messages or URL query secrets. Narrative guidance explicitly checks abstract endings and cover letters for repeated negative limitations.

The portable-filename checks reject case-insensitive collisions and Windows reserved names. Optional PDF dependencies are bundled inside the installable skill; their minimum version matches the actual `pymupdf` module interface.

## Not Covered

Live Zotero insertion/Refresh, Word document editing, all publisher/institutional access routes, OCR quality, a full comparable-paper reading set, and an actual journal portal upload were not exercised by this release test. The skill requires their relevant checks during a real manuscript task instead of inferring success from these helper tests.
