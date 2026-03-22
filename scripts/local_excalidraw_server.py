from __future__ import annotations

import hashlib
import json
import mimetypes
import ssl
import threading
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ESM_BASE_URL = "https://esm.sh"


class LocalExcalidrawServer:
    def __init__(self, pages: dict[str, tuple[str, str]] | None = None) -> None:
        self.pages = pages or {}
        # Persistent cache across all runs — avoids re-downloading the excalidraw
        # bundle (~3 MB from esm.sh) on every render invocation.
        self._cache_dir = Path.home() / ".cache" / "hand-drawn-diagrams" / "esm-cache"
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        self._server: ThreadingHTTPServer | None = None
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        server = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, format: str, *args: object) -> None:
                return

            def do_GET(self) -> None:  # noqa: N802
                parsed = urllib.parse.urlsplit(self.path)
                route = parsed.path or "/"

                if route in server.pages:
                    body_text, content_type = server.pages[route]
                    body = body_text.encode("utf-8")
                    self.send_response(200)
                    self.send_header("Content-Type", content_type)
                    self.send_header("Content-Length", str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)
                    return

                try:
                    body, content_type = server._get_esm_asset(self.path)
                except Exception as exc:
                    message = f"Proxy fetch failed: {exc}\n"
                    body = message.encode("utf-8", "replace")
                    self.send_response(502)
                    self.send_header("Content-Type", "text/plain; charset=utf-8")
                    self.send_header("Content-Length", str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)
                    return

                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

        httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self._server = httpd
        self._thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        self._thread.start()

    @property
    def base_url(self) -> str:
        if self._server is None:
            raise RuntimeError("Server not started")
        host, port = self._server.server_address
        return f"http://{host}:{port}"

    def url_for(self, path: str) -> str:
        if not path.startswith("/"):
            path = "/" + path
        return f"{self.base_url}{path}"

    def close(self) -> None:
        if self._server is not None:
            self._server.shutdown()
            self._server.server_close()
            self._server = None
        if self._thread is not None:
            self._thread.join(timeout=2)
            self._thread = None

    def _get_esm_asset(self, request_target: str) -> tuple[bytes, str]:
        cache_key = hashlib.sha256(request_target.encode("utf-8")).hexdigest()
        body_path = self._cache_dir / f"{cache_key}.bin"
        meta_path = self._cache_dir / f"{cache_key}.json"

        if body_path.exists() and meta_path.exists():
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            return body_path.read_bytes(), meta["content_type"]

        remote_url = f"{ESM_BASE_URL}{request_target}"
        request = urllib.request.Request(
            remote_url,
            headers={"User-Agent": "hand-drawn-diagrams/1.0"},
        )

        try:
            with urllib.request.urlopen(
                request,
                timeout=30,
                context=ssl._create_unverified_context(),
            ) as response:
                body = response.read()
                content_type = response.headers.get_content_type()
        except urllib.error.HTTPError as exc:
            raise RuntimeError(f"{remote_url} returned HTTP {exc.code}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"{remote_url} failed: {exc.reason}") from exc

        if content_type == "application/octet-stream":
            guessed = mimetypes.guess_type(
                urllib.parse.urlsplit(request_target).path,
            )[0]
            content_type = guessed or "application/octet-stream"

        body_path.write_bytes(body)
        meta_path.write_text(
            json.dumps({"content_type": content_type}),
            encoding="utf-8",
        )
        return body, content_type
