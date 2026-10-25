from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path

from database import get_all_jobs

WEB_DIR = Path(__file__).resolve().parent / "web"


class ScraperHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    def do_GET(self):
        if self.path == "/api/jobs":
            try:
                jobs = get_all_jobs()
                payload = json.dumps(jobs, ensure_ascii=False).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)
            except Exception as error:
                payload = json.dumps({"error": str(error)}).encode("utf-8")
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)
            return
        if self.path == "/":
            self.path = "/index.html"
        return super().do_GET()


if __name__ == "__main__":
    address = ("127.0.0.1", 8000)
    print(f"Job scraper interface: http://{address[0]}:{address[1]}")
    print("Stop the server with Ctrl+C.")
    ThreadingHTTPServer(address, ScraperHandler).serve_forever()
