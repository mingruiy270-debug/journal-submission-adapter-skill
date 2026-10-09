# Paper Selection And Full-Text Reading

## Selection

Search the journal's own current article list first, supplemented by native agent web search. An exact journal title plus topic terms is better than a publisher-wide query. Confirm journal identity through its official site and, where ambiguous, ISSN. Exclude editorials/reviews as primary structural comparators for original research; they may provide background separately.

Use the preceding three calendar months as a preference, not a hard quota. For a run on 9 October, the preferred window starts on 9 July, adjusted to the last valid day when needed. Reject future publication dates. An online-first research article can qualify even without its final issue assignment. Metadata dates must be checked against the publisher.

For each candidate record:

| Field | Purpose |
| --- | --- |
| ID, exact title, DOI, journal, online date, article type | Identity and recency |
| Topic and main research question | Scientific fit |
| Human/animal/cell/public-data design, sample scale | Design similarity |
| Observational, perturbation, rescue, or causal evidence | Depth comparison |
| Why selected or excluded | Avoid keyword-only selection |
| Publisher URL, access route, local path | Retrieve and trace |
| Reading status | Full text, partial text, abstract only, unavailable |

Use a small useful set, usually 3-5 papers. Favor a mix that covers the manuscript's main scientific question and evidence design. A close design match six months old is often more useful than an unrelated paper from yesterday. Avoid treating the publication of a similar paper as an acceptance-probability estimate.

## Acquisition

Native browsing identifies the legitimate full-text links. The helper accepts a reviewed manifest; it does not discover or rank papers. Its `format` is `pdf` or `html` and its `access` is `open_access` or `user_authorized`. Authorization must apply to the specific material, not just possession of a URL. Never put passwords, cookies, API keys or reviewer tokens into the public repository, manifest or download report.

```bash
python scripts/acquire_fulltext.py --manifest /work/articles.json --out /work/papers --report /work/download_report.json
python scripts/extract_pdf.py /work/papers/P01.pdf --out /work/readings/P01.txt
```

Paths here are illustrative; run scripts by their actual installed absolute paths when necessary. PDF acquisition validates transport, signature and bounded size. The extractor checks whether the PDF can be opened and records page-level text coverage. Neither validates article identity or proves that an agent has read it.

Do not keep retrying a paywall or anti-bot page. After a failed ordinary request, try a different lawful repository or the user's authorized browser access, with bounded attempts. Ask for manual download when needed:

```text
Please download these full papers and place them in the working papers folder:
1. Exact title | DOI | publisher landing page | reason access failed
```

When full HTML is used, save it locally and read the actual article sections. Figures may need the publisher's separate figure page. Do not automatically download SI; ask when a missing method or figure legend materially affects comparison.

For online-first papers, OA/full-access HTML can contain only the abstract and back matter. Inspect Introduction/Methods/Results/Discussion coverage before declaring full-text access; use the verified PDF link when available. A `downloaded` HTML status validates transport, not completeness.

The downloader defaults to standard-library `urllib`. A separately installed `requests` package can be selected with `--transport requests`, using the same size/type checks and ordinary HTTP headers. Both support HTTP(S) proxy environment settings. Do not automatically loop transports after access denial or browser challenges. One successful PDF route does not validate the failed route or prove scientific reading.

## Per-Paper Reading Card

Keep cards analytical rather than copying the paper. Use PDF page/figure numbers or HTML section headings as locators.

```text
Identity and access: title, DOI, online date, local file, reading coverage
Research question and opening gap:
Main conclusion and evidence strength:
Design and key measurements:
Results sequence: finding -> measurement -> interpretation, section by section
Figure jobs: what each main figure establishes and how it connects to text
Abstract: problem -> approach -> results -> closing emphasis
Introduction/Discussion: framing, comparison with prior work, scope of conclusion
Writing observations: sentence rhythm, paragraph focus, transitions, terminology
Transferable choices for the manuscript:
Choices not transferable because of design/evidence differences:
Source locators for each important observation:
```

Read Methods to determine evidence depth, even when the task is mostly prose. A paper's mechanistic language may be warranted by perturbation/rescue that the current manuscript lacks. Do not borrow that language independently of its experiments.

For long papers, read in page/section chunks until all relevant sections are covered. Record unread or OCR-poor pages explicitly. An extraction file containing all pages is not evidence that all pages were read.

Partial reading can support only an explicitly bounded observation about the sections actually read. For example, an Introduction can inform its opening progression, but not the paper's Results architecture or causal depth. If the planned reading set remains incomplete, identify the completed/partial/abstract-only counts and label the overall paper-informed adaptation as limited or pending. Do not count selected titles as fully read comparators. Continue requirements-based work where useful, without claiming the full workflow is complete.

## Cross-Paper Synthesis

Summarize the common writing pattern, the target readership and important variation. Each proposed adaptation should point to at least one reading-card locator and to a relevant manuscript finding. Label patterns observed in only one paper as examples, not journal rules.

Keep two separate sources of authority:

- Official requirements: must/conditional/recommended/later-stage, with current URLs.
- Empirical conventions: descriptive observations from papers, with actual coverage and sample size.

When these conflict, current official submission requirements prevail. Do not assert a stable journal-wide preference from three papers.
