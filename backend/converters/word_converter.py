from converters.libreoffice import convert_to_pdf


def convert_word(path):
    """Convert a DOCX document to PDF with LibreOffice."""
    return convert_to_pdf(path)
