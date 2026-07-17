"""Shared, defensive LibreOffice conversion helper."""

import os
import subprocess
import tempfile

from config import CONVERTED_FOLDER


class ConversionError(RuntimeError):
    """Raised when LibreOffice cannot create the requested PDF."""


def convert_to_pdf(path):
    """Convert *path* to PDF and return its absolute output path."""
    # An isolated profile prevents concurrent web requests from locking the
    # user's regular LibreOffice profile.
    with tempfile.TemporaryDirectory(prefix="docflex-lo-") as profile:
        result = subprocess.run(
            [
                "soffice",
                "--headless",
                "--nologo",
                "--nolockcheck",
                f"-env:UserInstallation=file://{profile}",
                "--convert-to",
                "pdf",
                "--outdir",
                CONVERTED_FOLDER,
                path,
            ],
            capture_output=True,
            text=True,
            timeout=90,
            check=False,
        )

    pdf_path = os.path.join(
        CONVERTED_FOLDER, os.path.splitext(os.path.basename(path))[0] + ".pdf"
    )
    if result.returncode != 0 or not os.path.isfile(pdf_path):
        detail = (result.stderr or result.stdout or "LibreOffice returned no output").strip()
        raise ConversionError(f"LibreOffice could not convert this file: {detail}")

    return pdf_path
