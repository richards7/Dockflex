from PIL import Image
import os
import img2pdf

from config import CONVERTED_FOLDER

def convert_image(path):

    name = os.path.splitext(os.path.basename(path))[0]
    pdf_path = os.path.join(CONVERTED_FOLDER, name + ".pdf")

    try:
        # Use img2pdf for extremely fast, lossless conversion
        with open(pdf_path, "wb") as f:
            f.write(img2pdf.convert(path))
    except Exception:
        # Fallback to Pillow for formats/modes img2pdf does not support
        image = Image.open(path)
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")
        image.save(pdf_path, "PDF", resolution=100.0)

    return pdf_path
