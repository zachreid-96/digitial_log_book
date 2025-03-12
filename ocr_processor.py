import os
import pytesseract
import fitz
from PIL import Image

OCR_MAX = 2


def ocr_file(file):
    pages = fitz.open(file)
    page = pages[0]
    pix = page.get_pixmap(dpi=300)
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    text = pytesseract.image_to_string(image, lang="eng")

    return text

"""
Description: 
    Used PDF24-Ocr to apply OCR to the files
    will apply ocr OCR_MAX times {currently set to 2}
Args:
    file: the passed file that needs ocr applied
"""


def ocr_file_old(file):
    for _ in range(OCR_MAX):
        os.system(
            f'pdf24-Ocr.exe -outputFile "{file}" -language eng -dpi 300 -autoRotatePages -deskew -removeBackground "{file}" >nul 2>&1')
