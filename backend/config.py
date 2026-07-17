import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
CONVERTED_FOLDER = os.path.join(BASE_DIR, "converted")

ALLOWED_EXTENSIONS = {
    "docx",
    "xlsx",
    "pdf",
    "jpg",
    "jpeg",
    "png"
}

MAX_CONTENT_LENGTH = 50 * 1024 * 1024
