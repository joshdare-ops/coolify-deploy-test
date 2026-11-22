"""Small standard-library server for the Coolify deploy/rollback test."""

import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

VERSION = "1"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/index.html"):
            status, body = 200, f"VERSION={VERSION}\n"
        elif self.path in ("/health", "/health/"):
            status, body = 200, "ok\n"
        else:
            status, body = 404, "not found\n"

        payload = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_request(self, code="-", size="-"):
        # Log the method and status only; paths may contain sensitive input.
        self.log_message("%s %s", self.command, code)

    def log_message(self, format, *args):
        print(format % args, flush=True)

    def log_error(self, format, *args):
        # Do not echo malformed request input into logs.
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    with ThreadingHTTPServer(("0.0.0.0", port), Handler) as server:
        server.serve_forever()
