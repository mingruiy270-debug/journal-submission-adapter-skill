# Independent Behavioral Testing

Use an independent agent with the skill, one synthetic manuscript and a clean isolated output area. Do not disclose a preferred abstract or expected narrative. Allow native browsing, but do not permit remote submission, payments, changes to a real manuscript or uploading private documents.

## Representative Task

Use this skill to adapt `fixtures/synthetic_manuscript.md` for a named research journal. Prefer recent comparable research, read accessible full papers, write a revised abstract and cover-letter core, and report current initial-submission requirements. Do not add analyses or missing author facts. The input is Markdown, so Word editing is out of scope for this particular test.

Inspect the actual generated requirements record, selected papers, reading cards, adaptation and final review. This tests decisions and source grounding, not exact phrasing.

## Observable Outcomes

- Uses native search and opens official journal instructions and publisher paper pages.
- Verifies online dates and journal identity; labels older or partial matches.
- Reads actual full sections with locators, or accurately reports access limits.
- Moves from a methods list to a specific evidence-supported question and answer.
- Preserves numerical results, effective n and measurement/inference distinctions.
- Does not invent an ethics number, animal procedure, disclosure or author approval.
- Keeps comparator papers out of the submission materials.
- Separates mandatory, optional and later-stage requirements.
- Reports absent tools or unresolved facts rather than declaring every check passed.

## Additional Failure Scenarios

1. Recent articles do not fit: does the agent expand dates transparently instead of choosing irrelevant papers?
2. PDF endpoint returns sign-in HTML: does it reject the disguised file and provide a manual-download list?
3. A comparator has knockdown and rescue, while the manuscript has associations: does it borrow structure without borrowing causality?
4. Word MCP is absent but the DOCX has Zotero fields: does it continue research without silently rebuilding the document?
5. A file is optional but explicitly cited in the manuscript: does it preserve accessible support or revise the callout transparently?
6. A locked statistical star conflicts with adjusted P: does it flag the mismatch rather than assert readiness?

Record executed and unexecuted scenarios separately. Unit tests do not cover live Word/Zotero operations or every publisher access path.

## Real-Run Regression Scenarios

7. An online-first OA page contains only an abstract and back matter, with a verified full PDF link: check section coverage and attempt the legal PDF route. If it fails, label the item abstract-only, not fully read.
8. An old working-folder master conflicts with a renamed, author-edited upload manuscript: compare content and provenance, select the author-current file, and preserve it when creating a derived copy. Do not choose solely by filename or timestamp.
9. The source abstract has four headings but official target rules prescribe Background/Results/Conclusions: use exactly the target headings and retain necessary study-design information without inventing a Methods requirement.
10. Word MCP is connected and citations are unchanged: edit text islands around live fields, save/reopen, compare complete citation payloads, bibliography and item identity. If citation order/style changes, perform real Zotero Refresh and check the rendered numbering; do not substitute a field count.
11. `urllib` returns HTML for a verified OA PDF while an ordinary `requests` route on the user-configured proxy succeeds: select the explicit transport, preserve PDF validation/size limits, and record the successful route. Do not claim a CAPTCHA/paywall bypass or all network paths passed.
12. A live search repeats table hits or reaches its cap: do not treat deduplicated hits as complete coverage. Verify the required text/ranges and use a scoped supported operation; treat partial errors as incomplete.
13. Inserted prose inherits heading formatting, or a capture shows a different page from its requested page: inspect the actual displayed anchor, restore intended body formatting via MCP, and do not certify layout from metadata alone.
