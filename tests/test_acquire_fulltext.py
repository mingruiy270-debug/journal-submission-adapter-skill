from __future__ import annotations

import importlib.util
import io
import json
import socket
import ssl
import tempfile
import unittest
from email.message import Message
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError, URLError


SCRIPT = Path(__file__).resolve().parents[1] / "skills/journal-submission-adapter/scripts/acquire_fulltext.py"
spec = importlib.util.spec_from_file_location("acquire_fulltext", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def article(**changes):
    item = {"id": "P01", "title": "A synthetic study", "doi": "10.example/test",
            "journal": "Synthetic Journal", "published_online": "2026-10-01",
            "landing_url": "https://example.org/article", "full_text_url": "https://example.org/paper.pdf",
            "format": "pdf", "access": "open_access"}
    item.update(changes)
    return item


class Response(io.BytesIO):
    def __init__(self, body, mime="application/pdf", url="https://example.org/paper.pdf", length=None):
        super().__init__(body)
        self.headers = Message()
        self.headers["Content-Type"] = mime
        if length is not None:
            self.headers["Content-Length"] = str(length)
        self.url = url

    def geturl(self):
        return self.url


class AcquisitionTests(unittest.TestCase):
    def test_save_pdf_without_hash_or_false_reading_status(self):
        with tempfile.TemporaryDirectory() as folder:
            data = b"%PDF-1.7\ntransport fixture, not a structural PDF"
            with patch.object(module, "urlopen", return_value=Response(data)):
                result = module.acquire([article()], Path(folder), pause=0)[0]
            self.assertEqual((Path(folder) / "P01.pdf").read_bytes(), data)
            self.assertEqual(result["status"], "downloaded")
            self.assertEqual(result["reading_status"], "not_read")
            self.assertFalse(result["identity_verified"])
            self.assertEqual(set(result).intersection({"sha256", "md5", "hash"}), set())

    def test_login_html_is_not_saved_as_pdf(self):
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(module, "urlopen", return_value=Response(b"<html>Sign in</html>", "text/html")):
                result = module.acquire([article()], Path(folder), pause=0)[0]
            self.assertEqual(result["reason"], "not_a_pdf")
            self.assertEqual(list(Path(folder).iterdir()), [])

    def test_preserve_html_extension(self):
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(module, "urlopen", return_value=Response(b"<!doctype html><html>Full article</html>", "text/html")):
                result = module.acquire([article(format="html")], Path(folder), pause=0)[0]
            self.assertEqual(result["status"], "downloaded")
            self.assertTrue((Path(folder) / "P01.html").exists())

    def test_missing_url_and_existing_file_require_review(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "P01.pdf"
            path.write_bytes(b"original")
            with patch.object(module, "urlopen") as network:
                results = module.acquire([article(), article(id="P02", full_text_url="")], Path(folder), pause=0)
            self.assertEqual(path.read_bytes(), b"original")
            self.assertEqual([row["status"] for row in results], ["existing_not_checked", "manual_required"])
            network.assert_not_called()

    def test_http_error_is_bounded_and_does_not_expose_url_token(self):
        url = "https://example.org/paper.pdf?token=SECRET"
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(module, "urlopen", side_effect=HTTPError(url, 403, "SECRET", {}, None)) as network:
                result = module.acquire([article(full_text_url=url)], Path(folder), pause=0)[0]
            self.assertEqual(result["reason"], "http_403")
            self.assertNotIn("SECRET", json.dumps(result))
            self.assertEqual(network.call_count, 1)

    def test_redirect_query_is_not_persisted(self):
        with patch.object(module, "urlopen", return_value=Response(b"%PDF-1.7", url="https://example.org/p.pdf?key=SECRET")):
            _, _, url = module.fetch("https://example.org/p.pdf", "pdf", 1, 100)
        self.assertEqual(url, "https://example.org/p.pdf")

    def test_transport_categories_without_secret_exception_details(self):
        cases = [(socket.gaierror(-2, "SECRET host"), "dns_error"),
                 (ssl.SSLError("SECRET certificate URL"), "tls_error"),
                 (TimeoutError("SECRET timeout URL"), "timeout")]
        for cause, category in cases:
            with tempfile.TemporaryDirectory() as folder:
                with patch.object(module, "urlopen", side_effect=URLError(cause)):
                    result = module.acquire([article()], Path(folder), pause=0)[0]
                self.assertEqual(result["reason"], "network_error")
                self.assertEqual(result["transport_category"], category)
                self.assertNotIn("SECRET", json.dumps(result))

    def test_size_limit_declared_and_actual(self):
        for response in (Response(b"%PDF-1.7", length=200), Response(b"%PDF-1.7" + b"x" * 200)):
            with patch.object(module, "urlopen", return_value=response):
                with self.assertRaisesRegex(module.DownloadError, "size_limit"):
                    module.fetch("https://example.org/p.pdf", "pdf", 1, 100)

    def test_manifest_rejects_path_escape_duplicate_and_placeholder(self):
        for items in ([article(id="../escape")], [article(), article()],
                      [article(title="Replace with a title")], [article(access="unknown")]):
            with tempfile.TemporaryDirectory() as folder:
                path = Path(folder) / "input.json"
                path.write_text(json.dumps({"articles": items}), encoding="utf-8")
                with self.assertRaises(ValueError):
                    module.read_manifest(path)

    def test_urls_reject_file_scheme_and_embedded_credentials(self):
        for url in ("file:///private/document.pdf", "https://user:pass@example.org/p.pdf", "https://"):
            with self.assertRaises(ValueError):
                module.valid_url(url)

    def test_portable_filename_collision_and_reserved_names(self):
        for items in ([article(), article(id="p01")], [article(id="CON")], [article(id="lpt9")]):
            with tempfile.TemporaryDirectory() as folder:
                path = Path(folder) / "input.json"
                path.write_text(json.dumps({"articles": items}), encoding="utf-8")
                with self.assertRaises(ValueError):
                    module.read_manifest(path)

    def test_utf8_bom_manifest_and_chinese_title(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "input.json"
            path.write_text(json.dumps({"articles": [article(title="示例论文")]}, ensure_ascii=False), encoding="utf-8-sig")
            self.assertEqual(module.read_manifest(path)[0]["title"], "示例论文")


if __name__ == "__main__":
    unittest.main()
