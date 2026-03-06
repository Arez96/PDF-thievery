import threading
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path

import pandas as pd
import importlib.util
import pathlib

# Importér programmet via sti
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = PROJECT_ROOT / "pdf_downloader_snake.py"

spec = importlib.util.spec_from_file_location("pdf_downloader_snake", MODULE_PATH)
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)


class PdfHandler(BaseHTTPRequestHandler):
    # Denne server giver PRÆCIS Content-Type: application/pdf (som din kollegas kode kræver)
    def do_GET(self):
        if self.path == "/ok.pdf":
            content = b"%PDF-1.4\nFAKE\n%%EOF"
            self.send_response(200)
            self.send_header("Content-Type", "application/pdf")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return

        if self.path == "/notpdf.html":
            content = b"<html>not a pdf</html>"
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return

        self.send_response(404)
        self.send_header("Content-Type", "text/html")
        self.end_headers()

    def log_message(self, format, *args):
        return


def start_server():
    server = ThreadingHTTPServer(("127.0.0.1", 0), PdfHandler)
    host, port = server.server_address
    base_url = f"http://{host}:{port}"

    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    return server, base_url


def test_integration_excel_to_downloaded_pdf(tmp_path: Path):
    # 1) Start lokal server
    server, base_url = start_server()

    try:
        # 2) Lav en rigtig Excel-fil + output-mappe
        excel_path = tmp_path / "input.xlsx"
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        df = pd.DataFrame({
            "BRnum": ["A1", "A2", "A3"],
            "Pdf_URL": [
                f"{base_url}/ok.pdf",        # skal gemmes
                f"{base_url}/notpdf.html",   # må ikke gemmes
                f"{base_url}/missing.pdf",   # 404 -> må ikke gemmes
            ],
        })
        df.to_excel(excel_path, index=False)

        # 3) Peg programmet på vores test-filer
        app.input_path = str(excel_path)
        app.output_path = str(output_dir)

        # 4) Kør programmet
        app.main()

        # 5) Tjek resultater
        assert (output_dir / "A1.pdf").exists()
        assert not (output_dir / "A2.pdf").exists()
        assert not (output_dir / "A3.pdf").exists()

    finally:
        server.shutdown()