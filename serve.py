#!/usr/bin/env python3
"""Dev server for the project page, with automatic browser reload.

Serves this directory and injects a small polling script into every HTML
response. Whenever any file under the directory changes on disk, the open
page reloads itself -- edit ``index.html`` in any editor and the browser
follows along, with no cache to fight.

Standard library only; nothing to install.

Usage
-----
    python3 serve.py            # serve on http://localhost:8000 and open it
    python3 serve.py 8080       # a different port
    python3 serve.py --no-open  # do not launch a browser
"""

from __future__ import annotations

import http.server
import sys
import threading
import webbrowser
from pathlib import Path

ROOT: Path = Path(__file__).resolve().parent
POLL_MS: int = 500
IGNORED: frozenset[str] = frozenset({".git", "__pycache__", ".DS_Store"})

_SNIPPET: str = f"""
<script>
/* injected by serve.py -- never present in the published page */
(function () {{
  let seen = null;
  setInterval(async function () {{
    try {{
      const stamp = await (await fetch("/__mtime", {{cache: "no-store"}})).text();
      if (seen !== null && stamp !== seen) location.reload();
      seen = stamp;
    }} catch (err) {{ /* server restarting; try again next tick */ }}
  }}, {POLL_MS});
}})();
</script>
"""


def latest_mtime() -> float:
    """Return the newest modification time of any file under :data:`ROOT`.

    Files inside :data:`IGNORED` directories are skipped so that git's own
    bookkeeping does not trigger a reload.

    Returns
    -------
    float
        The largest ``st_mtime`` found, or ``0.0`` if the tree is empty.
    """
    newest = 0.0
    for path in ROOT.rglob("*"):
        if IGNORED.intersection(path.parts):
            continue
        if path.is_file():
            newest = max(newest, path.stat().st_mtime)
    return newest


class ReloadHandler(http.server.SimpleHTTPRequestHandler):
    """Static handler that answers ``/__mtime`` and injects the reload script."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, directory=str(ROOT), **kwargs)  # type: ignore[arg-type]

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store, must-revalidate")
        super().end_headers()

    def _send_bytes(self, body: bytes, content_type: str) -> None:
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802 - name fixed by the base class
        if self.path.startswith("/__mtime"):
            self._send_bytes(f"{latest_mtime():.6f}".encode(), "text/plain")
            return

        target = Path(self.translate_path(self.path))
        if target.is_dir():
            target = target / "index.html"

        if target.suffix.lower() in {".html", ".htm"} and target.is_file():
            html = target.read_text(encoding="utf-8")
            html = (
                html.replace("</body>", _SNIPPET + "</body>", 1)
                if "</body>" in html
                else html + _SNIPPET
            )
            self._send_bytes(html.encode("utf-8"), "text/html; charset=utf-8")
            return

        super().do_GET()


def main(argv: list[str]) -> int:
    """Parse ``argv`` and run the server until interrupted."""
    port = 8000
    open_browser = True
    for arg in argv:
        if arg == "--no-open":
            open_browser = False
        elif arg.isdigit():
            port = int(arg)
        else:
            print(__doc__)
            return 2

    url = f"http://localhost:{port}"
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), ReloadHandler)
    print(f"serving {ROOT} at {url}  (live reload on, Ctrl-C to stop)")
    if open_browser:
        threading.Timer(0.5, webbrowser.open, args=(url,)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
