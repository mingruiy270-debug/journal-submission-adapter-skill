from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

try:
    import pymupdf
except ImportError:
    pymupdf = None

SCRIPT = Path(__file__).resolve().parents[1] / "skills/journal-submission-adapter/scripts/extract_pdf.py"
spec = importlib.util.spec_from_file_location("extract_pdf", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


@unittest.skipIf(pymupdf is None, "Optional PyMuPDF is not installed")
class ExtractionTests(unittest.TestCase):
    def make_pdf(self, folder, blank=False):
        path = Path(folder) / "source.pdf"
        with pymupdf.open() as doc:
            first = doc.new_page()
            first.insert_text((72, 72), "Synthetic research article. Methods and results use actual source data.")
            second = doc.new_page()
            if not blank:
                second.insert_text((72, 72), "Discussion: these observations describe an association rather than a tested cause.")
            doc.save(path)
        return path

    def test_real_pdf_page_anchors_and_no_false_reading_claim(self):
        with tempfile.TemporaryDirectory() as folder:
            source = self.make_pdf(folder)
            out = Path(folder) / "reading.txt"
            result = module.extract(source, out)
            self.assertEqual(result["pages"], 2)
            self.assertEqual(result["status"], "text_extracted_not_read")
            self.assertIn("## PDF Page 2", out.read_text(encoding="utf-8"))

    def test_blank_page_requires_inspection(self):
        with tempfile.TemporaryDirectory() as folder:
            result = module.extract(self.make_pdf(folder, blank=True), Path(folder) / "reading.txt")
            self.assertEqual(result["low_text_pages"], [2])
            self.assertEqual(result["status"], "needs_page_inspection_or_ocr")

    def test_existing_text_and_pdf_source_not_overwritten(self):
        with tempfile.TemporaryDirectory() as folder:
            source = self.make_pdf(folder)
            with self.assertRaises(ValueError):
                module.extract(source, source)
            out = Path(folder) / "reading.txt"
            out.write_text("original", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                module.extract(source, out)
            self.assertEqual(out.read_text(encoding="utf-8"), "original")

    def test_not_a_real_pdf_rejected_without_text_output(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "invalid.pdf"
            source.write_bytes(b"<html>Sign in</html>")
            out = Path(folder) / "reading.txt"
            with self.assertRaises(Exception):
                module.extract(source, out)
            self.assertFalse(out.exists())


if __name__ == "__main__":
    unittest.main()
