import pytesseract
import fitz
from PIL import Image


def ocr_file(file):
    pages = fitz.open(file)
    page = pages[0]
    pix = page.get_pixmap(dpi=300)
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    custom_config = r'--oem 3 --psm 4 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890/ :;*'
    text = pytesseract.image_to_string(image, lang="eng", config=custom_config)

    return text
