import re
import cv2
import fitz
import pytesseract

import numpy as np

from PIL import Image

"""
Description: 
    Applies image preprocessing to a PDF and performs OCR using Tesseract.
Args:
    file: the file that needs OCR
Returns:
    filtered_text: a list of the OCR data in string format, excludes empty strings and strings with len(1)
"""

def ocr_file(file):

    pages = fitz.open(file)
    page = pages[0]

    # Sets DPI of image
    pix = page.get_pixmap(dpi=300)
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # Attempts to get OSD of image and rotate if needed
    try:
        rotation_detection = pytesseract.image_to_osd(image)
        rotation = int(re.search('(?<=Rotate: )\\d+', rotation_detection).group())
        if rotation:
            image = image.rotate(-rotation, expand=True)
    except pytesseract.pytesseract.TesseractError:
        pass

    # Convert to grayscale to simplify the image and reduce noise
    cv_image = np.array(image)
    gray = cv2.cvtColor(cv_image, cv2.COLOR_RGB2GRAY)

    # Resizes image and applies slight GaussianBlur for letter definition
    gray = cv2.resize(gray, None, fx=1.75, fy=1.75, interpolation=cv2.INTER_LINEAR)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # Apply OTSU thresholding to binarize the image (helps separate text from background)
    _, otsu = cv2.threshold(gray, 0, 220, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    preprocessed_image = Image.fromarray(gray)

    # Uses Tesseract-OCR and returns filtered text list
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    custom_config = r'--oem 3 --psm 11 -c preserve_interword_spaces=1'
    text = pytesseract.image_to_data(preprocessed_image, lang="eng",
                                     config=custom_config, output_type=pytesseract.Output.DICT)

    filtered_text = []

    for word, conf in zip(text['text'], text['conf']):
        if int(conf) > 0 and len(word) > 2:
            filtered_text.append(word)


    #filtered_text = [
    #    word for word, conf in zip(text['text'], text['conf'])
    #    if word.strip() and int(conf) > 0 and len(word) > 2
    #]

    return filtered_text
