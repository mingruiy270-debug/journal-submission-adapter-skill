#!/usr/bin/env python3
"""Save a small, agent-selected full-text list; do not search or rank papers."""

from __future__ import annotations

import argparse
import http.client
import json
import re
import socket
import ssl
import time
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit, urlunsplit
from urllib.request import Request, urlopen


class DownloadError(Exception):
    def __init__(self, reason: str, *, error_type: str | None = None, category: str | None = None):
        super().__init__(reason)
        self.error_type = error_type
        self.category = category


def transport_diagnostic(exc: Exception) -> dict:
    cause = exc.reason if isinstance(exc, URLError) else exc
    error_type = type(cause).__name__ if isinstance(cause, BaseException) else type(exc).__name__
    if isinstance(cause, ssl.SSLError):
        category = "tls_error"
    elif isinstance(cause, socket.gaierror):
        category = "dns_error"
    elif isinstance(cause, TimeoutError):
        category = "timeout"
    elif isinstance(cause, ConnectionError):
        category = "connection_error"
    elif isinstance(cause, http.client.HTTPException):
        category = "protocol_error"
    elif isinstance(cause, OSError):
        category = "os_error"
    else:
        category = "transport_error"
    return {"error_type": error_type, "category": category}


def valid_url(value: str) -> str:
    try:
        parsed = urlsplit(value)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            raise ValueError("A full-text URL must use http or https.")
        if parsed.username or parsed.password:
            raise ValueError("Credentials must not be embedded in URLs.")
        _ = parsed.port
    except (ValueError, TypeError) as exc:
        raise ValueError("Invalid or credential-bearing URL.") from exc
    return value


def public_url(value: str) -> str:
    """Do not persist signed query strings or fragments in download reports."""
    parsed = urlsplit(value)
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", ""))


def read_manifest(path: Path) -> list[dict]:
    manifest = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(manifest, dict) or not isinstance(manifest.get("articles"), list):
        raise ValueError("Manifest must contain an articles list.")
    articles = manifest["articles"]
    if not 1 <= len(articles) <= 20:
        raise ValueError("Use an explicit list of 1-20 selected papers.")
    seen = set()
    for item in articles:
        if not isinstance(item, dict):
            raise ValueError("Each article must be an object.")
        identifier = item.get("id", "")
        if not isinstance(identifier, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", identifier):
            raise ValueError("Article IDs must be safe, unique filename stems.")
        folded = identifier.casefold()
        reserved = {"con", "prn", "aux", "nul"} | {f"com{i}" for i in range(1, 10)} | {f"lpt{i}" for i in range(1, 10)}
        if folded in reserved:
            raise ValueError("Article ID is a reserved Windows filename.")
        if folded in seen:
            raise ValueError("Duplicate article ID.")
        seen.add(folded)
        for field in ("title", "journal", "published_online"):
            value = item.get(field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"Missing article field: {field}.")
            if value.startswith("Replace with"):
                raise ValueError("Replace example metadata before downloading.")
        date.fromisoformat(item["published_online"])
        if item.get("format") not in {"pdf", "html"}:
            raise ValueError("Article format must be pdf or html.")
        if item.get("access") not in {"open_access", "user_authorized"}:
            raise ValueError("Record open_access or user_authorized access.")
        valid_url(item.get("landing_url", ""))
        if item.get("full_text_url"):
            valid_url(item["full_text_url"])
    return articles


def fetch(url: str, expected_format: str, timeout: float, max_bytes: int) -> tuple[bytes, str, str]:
    request = Request(valid_url(url), headers={
        "User-Agent": "journal-submission-adapter/1.0 (selected academic full-text retrieval)",
        "Accept": "application/pdf,text/html;q=0.9,application/xhtml+xml;q=0.8",
    })
    try:
        with urlopen(request, timeout=timeout) as response:
            final_url = valid_url(response.geturl())
            mime = response.headers.get_content_type()
            declared = response.headers.get("Content-Length")
            if declared and declared.isdigit() and int(declared) > max_bytes:
                raise DownloadError("size_limit")
            data = response.read(max_bytes + 1)
            if len(data) > max_bytes:
                raise DownloadError("size_limit")
    except HTTPError as exc:
        raise DownloadError(f"http_{exc.code}") from exc
    except (URLError, TimeoutError, OSError, http.client.HTTPException) as exc:
        raise DownloadError("network_error", **transport_diagnostic(exc)) from exc
    if not data:
        raise DownloadError("empty_response")
    if expected_format == "pdf":
        if b"%PDF-" not in data[:1024]:
            raise DownloadError("not_a_pdf")
    else:
        prefix = data[:1024].lstrip().lower()
        if mime not in {"text/html", "application/xhtml+xml"} or not (
            b"<html" in prefix or b"<!doctype html" in prefix
        ):
            raise DownloadError("not_html")
    return data, mime, public_url(final_url)


def acquire(articles: list[dict], out: Path, *, timeout: float = 30, max_bytes: int = 50 * 1024**2,
            pause: float = 1) -> list[dict]:
    if timeout <= 0 or max_bytes <= 0 or pause < 0:
        raise ValueError("Timeout/size must be positive and pause nonnegative.")
    out.mkdir(parents=True, exist_ok=True)
    results = []
    for index, item in enumerate(articles):
        destination = out / f"{item['id']}.{item['format']}"
        row = {
            "id": item["id"], "title": item["title"], "doi": item.get("doi", ""),
            "journal": item["journal"], "published_online": item["published_online"],
            "landing_url": public_url(item["landing_url"]), "access": item["access"],
            "format": item["format"], "local_path": str(destination.resolve()),
            "identity_verified": False, "reading_status": "not_read",
        }
        url = item.get("full_text_url", "")
        if not url:
            row.update(status="manual_required", reason="no_verified_full_text_url")
        elif destination.exists():
            row.update(status="existing_not_checked", reason="original_not_overwritten")
        else:
            try:
                data, mime, final_url = fetch(url, item["format"], timeout, max_bytes)
                with destination.open("xb") as handle:
                    handle.write(data)
                row.update(status="downloaded", bytes=len(data), mime=mime, final_url=final_url)
            except DownloadError as exc:
                row.update(status="manual_required", reason=str(exc))
                if exc.error_type:
                    row["error_type"] = exc.error_type
                if exc.category:
                    row["transport_category"] = exc.category
            except FileExistsError:
                row.update(status="existing_not_checked", reason="original_not_overwritten")
        results.append(row)
        if index + 1 < len(articles) and pause:
            time.sleep(pause)
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--timeout", type=float, default=30)
    parser.add_argument("--max-mb", type=int, choices=range(1, 101), default=50)
    parser.add_argument("--pause", type=float, default=1)
    args = parser.parse_args()
    try:
        articles = read_manifest(args.manifest)
        if args.report.exists():
            raise ValueError("Report already exists; choose a new report path.")
        results = acquire(articles, args.out, timeout=args.timeout,
                          max_bytes=args.max_mb * 1024**2, pause=args.pause)
        report = {"checked_at_utc": datetime.now(timezone.utc).isoformat(), "results": results}
        args.report.parent.mkdir(parents=True, exist_ok=True)
        with args.report.open("x", encoding="utf-8") as handle:
            json.dump(report, handle, ensure_ascii=False, indent=2)
        for row in results:
            print(f"{row['id']}: {row['status']} {row.get('reason', '')}")
        return 0 if all(row["status"] == "downloaded" for row in results) else 2
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
