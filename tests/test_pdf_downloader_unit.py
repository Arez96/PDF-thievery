"""
Enhedstest (Unit Tests) for PDF-downloaderen.

Formål:
At teste programmets kernefunktioner isoleret fra eksterne afhængigheder
såsom:
- Excel-filer
- Netværksforbindelse
- Filsystem

Mocking anvendes for at sikre, at testene ikke foretager rigtige
downloads eller skriver faktiske filer på disken.
"""

import builtins
from unittest.mock import patch, mock_open
import pandas as pd
import requests
import importlib.util
import pathlib

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = PROJECT_ROOT / "pdf_downloader_snake.py"

spec = importlib.util.spec_from_file_location("pdf_downloader_snake", MODULE_PATH)
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)


def test_springer_nan_url_over():
    """
    Tester at rækker med NaN som URL bliver sprunget over,
    og at der ikke foretages netværkskald.
    """

    # Opretter en falsk DataFrame som simulerer Excel-input
    df = pd.DataFrame({"BRnum": ["A1"], "Pdf_URL": [float("nan")]})

    with patch.object(app.pd, "read_excel", return_value=df), \
         patch.object(app.os.path, "exists", return_value=False), \
         patch.object(app.requests, "get") as fake_get:

        app.main()

        # Kontrollerer at download aldrig blev forsøgt
        fake_get.assert_not_called()


def test_springer_over_hvis_fil_eksisterer():
    """
    Tester at programmet ikke forsøger at downloade en PDF,
    hvis filen allerede findes i output-mappen.
    """

    df = pd.DataFrame({"BRnum": ["A1"], "Pdf_URL": ["https://example.com/a.pdf"]})

    with patch.object(app.pd, "read_excel", return_value=df), \
         patch.object(app.os.path, "exists", return_value=True), \
         patch.object(app.requests, "get") as fake_get:

        app.main()

        # Download må ikke blive kaldt
        fake_get.assert_not_called()


def test_downloader_og_gemmer_pdf_ved_status_200():
    """
    Tester succes-scenariet:
    - HTTP statuskode 200
    - Content-Type er application/pdf
    - Filen forsøges gemt
    """

    df = pd.DataFrame({"BRnum": ["A1"], "Pdf_URL": ["https://example.com/a.pdf"]})

    # Opretter et falsk HTTP-response objekt
    fake_response = type("Resp", (), {})()
    fake_response.status_code = 200
    fake_response.headers = {"Content-Type": "application/pdf"}
    fake_response.content = b"%PDF-FAKE"

    with patch.object(app.pd, "read_excel", return_value=df), \
         patch.object(app.os.path, "exists", return_value=False), \
         patch.object(app.requests, "get", return_value=fake_response), \
         patch.object(builtins, "open", mock_open()) as m:

        app.main()

        # Kontrollerer at der blev forsøgt at skrive fil
        m.assert_called()


def test_haandterer_404_korrekt():
    """
    Tester at HTTP 404-fejl håndteres korrekt,
    og at der ikke gemmes nogen fil.
    """

    df = pd.DataFrame({"BRnum": ["A1"], "Pdf_URL": ["https://example.com/missing.pdf"]})

    fake_response = type("Resp", (), {})()
    fake_response.status_code = 404
    fake_response.headers = {"Content-Type": "text/html"}
    fake_response.content = b"Not Found"

    with patch.object(app.pd, "read_excel", return_value=df), \
         patch.object(app.os.path, "exists", return_value=False), \
         patch.object(app.requests, "get", return_value=fake_response), \
         patch.object(builtins, "open", mock_open()) as m:

        app.main()

        # Der må ikke forsøges at skrive fil ved 404
        m.assert_not_called()


def test_haandterer_netvaerksfejl_timeout():
    """
    Tester at netværksfejl (f.eks. timeout) håndteres uden
    at programmet crasher eller forsøger at gemme fil.
    """

    df = pd.DataFrame({"BRnum": ["A1"], "Pdf_URL": ["https://example.com/a.pdf"]})

    with patch.object(app.pd, "read_excel", return_value=df), \
         patch.object(app.os.path, "exists", return_value=False), \
         patch.object(app.requests, "get", side_effect=requests.Timeout("timeout")), \
         patch.object(builtins, "open", mock_open()) as m:

        app.main()

        # Ingen fil må skrives hvis der opstår timeout
        m.assert_not_called()