from converters.libreoffice import convert_to_pdf


def convert_excel(path):
    """Convert an XLSX workbook to PDF with LibreOffice."""
    return convert_to_pdf(path)
