#!/usr/bin/env python3
"""Extract page-anchored PDF text without treating extraction as paper reading."""

from __future__ import annotations

import argparse
from pathlib import Path


def extract(path: Path, out: Path, *, min_chars: int = 40) -> dict:
    import pymupdf

    if path.resolve() == out.resolve():
        raise ValueError("Text output cannot overwrite its PDF source.")
    if out.exists():
        raise FileExistsError("Text output exists; choose a new path.")
    if min_chars < 0:
        raise ValueError("Minimum character count cannot be negative.")
    pages = []
    poor_pages = []
    with pymupdf.open(path) as document:
        if not document.is_pdf or document.needs_pass:
            raise ValueError("Expected an accessible, unencrypted PDF.")
        if not document.page_count:
            raise ValueError("PDF has no pages.")
        for index, page in enumerate(document, 1):
            text = page.get_text("text", sort=True)
            if len(text.strip()) < min_chars:
                poor_pages.append(index)
            pages.append(f"\n## PDF Page {index}\n\n{text}")
    status = "needs_page_inspection_or_ocr" if poor_pages else "text_extracted_not_read"
    header = f"# Extracted text: {path.name}\n\nStatus: {status}\n"
    header += f"Pages: {len(pages)}; low-text pages: {poor_pages}\n"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("x", encoding="utf-8") as handle:
        handle.write(header + "".join(pages))
    return {"pages": len(pages), "low_text_pages": poor_pages, "status": status}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--min-chars", type=int, default=40)
    args = parser.parse_args()
    try:
        result = extract(args.pdf, args.out, min_chars=args.min_chars)
    except ImportError:
        requirements = Path(__file__).resolve().parents[1] / "requirements-reading.txt"
        print(f"PyMuPDF is unavailable; install {requirements} in a suitable environment.")
        return 1
    except Exception as exc:
        print(f"Extraction failed: {exc}")
        return 1
    print(result)
    return 2 if result["low_text_pages"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
