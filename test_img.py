from PIL import Image
import os, time
print("Creating image...")
img = Image.new('RGB', (4000, 3000), color = 'red')
img.save('test.jpg')
print("Converting image...")
start = time.time()
image = Image.open('test.jpg')
if image.mode in ("RGBA", "P"):
    image = image.convert("RGB")
pdf_path = "test.pdf"
image.save(pdf_path, "PDF", resolution=100.0)
print(f"Done in {time.time() - start} seconds")
