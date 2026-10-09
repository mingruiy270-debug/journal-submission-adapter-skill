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
