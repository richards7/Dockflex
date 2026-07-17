import os


def convert_pdf(path):
    """A PDF is already in the requested format; return it unchanged."""
    if not os.path.isfile(path):
        raise FileNotFoundError("Uploaded PDF was not saved")
    return path
