from PIL import Image
import os

from config import CONVERTED_FOLDER

def convert_image(path):

    image = Image.open(path)

    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    name = os.path.splitext(os.path.basename(path))[0]

    pdf_path = os.path.join(CONVERTED_FOLDER, name + ".pdf")

    image.save(pdf_path, "PDF", resolution=100.0)

    return pdf_path
