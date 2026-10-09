from __future__ import annotations

import importlib.util
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from unittest.mock import patch

try:
    import pymupdf
except ImportError:
    pymupdf = None

try:
    import requests
except ImportError:
    requests = None

ROOT = Path(__file__).resolve().parents[1] / "skills/journal-submission-adapter/scripts"


def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


acquisition = load("acquire_fulltext")
extraction = load("extract_pdf")


@unittest.skipIf(pymupdf is None, "Optional PyMuPDF is not installed")
class HttpPipelineTests(unittest.TestCase):
    def test_real_http_download_to_parseable_pdf_and_page_text(self):
        with pymupdf.open() as document:
            page = document.new_page()
            page.insert_text((72, 72), "Synthetic article: a biological question precedes its methods and findings.")
            data = document.tobytes()

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/redirect':
                    self.send_response(302)
                    self.send_header('Location', '/paper.pdf')
                    self.send_header('Content-Length', '4096')
                    self.end_headers()
                    try:
                        self.wfile.write(b'x' * 4096)
                    except (BrokenPipeError, ConnectionResetError):
                        pass
                    return
                self.send_response(200)
                self.send_header("Content-Type", "application/pdf")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)

            def log_message(self, *_):
                pass

        server = HTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            url = f"http://127.0.0.1:{server.server_port}/paper.pdf"
            article = {"id": "P01", "title": "A synthetic article", "journal": "Synthetic Journal",
                       "published_online": "2026-10-01", "landing_url": url, "full_text_url": url,
                       "format": "pdf", "access": "user_authorized"}
            for transport in (["urllib", "requests"] if requests else ["urllib"]):
                with self.subTest(transport=transport), tempfile.TemporaryDirectory() as folder, patch.dict("os.environ", {"NO_PROXY": "127.0.0.1"}):
                    redirected, _, _ = acquisition.fetch(
                        url.replace('/paper.pdf', '/redirect'), 'pdf', 3, len(data)+1, transport)
                    self.assertEqual(redirected, data)
                    result = acquisition.acquire([article], Path(folder), pause=0, timeout=3, transport=transport)[0]
                    self.assertEqual(result["status"], "downloaded")
                    pdf = Path(folder) / "P01.pdf"
                    self.assertEqual(pdf.read_bytes(), data)
                    text = Path(folder) / "P01.txt"
                    parsed = extraction.extract(pdf, text)
                    self.assertEqual(parsed["status"], "text_extracted_not_read")
                    self.assertIn("biological question", text.read_text(encoding="utf-8"))
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=3)


if __name__ == "__main__":
    unittest.main()
