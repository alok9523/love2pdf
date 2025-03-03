# utils/image_utils.py

from PIL import Image
import os

def convert_image_to_pdf(image_path, output_pdf):
    """Convert an image to a PDF."""
    image = Image.open(image_path)
    image.convert("RGB").save(output_pdf, "PDF")

def compress_image(image_path, output_path, quality=50):
    """Compress an image to reduce size."""
    image = Image.open(image_path)
    image.save(output_path, "JPEG", quality=quality)