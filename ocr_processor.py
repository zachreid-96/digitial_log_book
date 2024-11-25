import os

OCR_MAX = 2

"""
Description: 
    Used PDF24-Ocr to apply OCR to the files
    will apply ocr OCR_MAX times {currently set to 2}
Args:
    file: the passed file that needs ocr applied
"""
def ocr_file(file):
    for _ in range(OCR_MAX):
        os.system(
            f'pdf24-Ocr.exe -outputFile "{file}" -language eng -dpi 300 -autoRotatePages -deskew -removeBackground "{file}" >nul 2>&1')
