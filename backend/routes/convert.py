import os
import uuid

from flask import Blueprint, jsonify, request, send_file

from werkzeug.utils import secure_filename

from converters.image_converter import convert_image
from converters.word_converter import convert_word
from converters.excel_converter import convert_excel
from converters.pdf_converter import convert_pdf
from converters.libreoffice import ConversionError

from config import *

convert_bp = Blueprint("convert",__name__)

@convert_bp.route("/upload",methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "Choose a file before converting."}), 400

    file = request.files["file"]

    if not file.filename:
        return jsonify({"error": "Choose a file before converting."}), 400

    original_name = secure_filename(file.filename)
    if not original_name or "." not in original_name:
        return jsonify({"error": "The file must have a supported extension."}), 400

    extension = original_name.rsplit(".", 1)[1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        return jsonify({"error": "Supported files: DOCX, XLSX, PDF, JPG, JPEG, and PNG."}), 400

    # A generated stem avoids collisions between simultaneous uploads.
    filename = f"{uuid.uuid4().hex}_{original_name}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    try:
        if extension == "docx":
            pdf = convert_word(filepath)
        elif extension == "xlsx":
            pdf = convert_excel(filepath)
        elif extension == "pdf":
            pdf = convert_pdf(filepath)
        else:
            pdf = convert_image(filepath)
    except (ConversionError, OSError, ValueError) as error:
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({"error": str(error) or "Conversion failed. Please try another file."}), 422

    download_name = f"{os.path.splitext(original_name)[0]}.pdf"
    response = send_file(
        pdf, as_attachment=True, download_name=download_name, mimetype="application/pdf"
    )

    # Files are transient conversion artifacts. Flask calls this once the
    # response stream has been closed, i.e. after the browser receives it.
    def remove_artifacts():
        for artifact in {filepath, pdf}:
            try:
                os.remove(artifact)
            except FileNotFoundError:
                pass

    response.call_on_close(remove_artifacts)
    return response
