import os

from flask import Flask, render_template
from flask_cors import CORS

from routes.convert import convert_bp
from config import (
    UPLOAD_FOLDER,
    CONVERTED_FOLDER,
    MAX_CONTENT_LENGTH
)

# -------------------------------------------------
# Flask App Configuration
# -------------------------------------------------

app = Flask(__name__)

CORS(app)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["CONVERTED_FOLDER"] = CONVERTED_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

# -------------------------------------------------
# Create Required Folders
# -------------------------------------------------

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

# -------------------------------------------------
# Register Routes
# -------------------------------------------------

app.register_blueprint(convert_bp)


@app.errorhandler(413)
def upload_too_large(_error):
    return {"error": "Files must be 50 MB or smaller."}, 413

# -------------------------------------------------
# Home Route
# -------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.get("/health")
def health():
    """Lightweight health endpoint used by Docker Compose."""
    return {"status": "ok"}

# -------------------------------------------------
# Run Application
# -------------------------------------------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=7000,
        debug=True
    )
