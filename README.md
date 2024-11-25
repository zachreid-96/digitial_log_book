# Digital Logbook

The **Digital Logbook** project is designed to help track copier and printer service information, particularly related to parts used during repairs. The system organizes data from scanned meter pages, each containing stickers with part numbers, and stores relevant details like the machine’s brand, date of service, and serial number.

## Key Features:
- **OCR Processing**: Scanned meter pages (PDF format) are processed using OCR (via PDF24) to extract relevant information.
- **File Sorting**: Based on the extracted data, files are categorized into brand-specific folders (Kyocera, HP, Inventory) or flagged for manual review if key data is missing or invalid.
- **Customizable Folder Structure**: Organizes files into:
    - `Unsorted`: Files pending OCR processing
    - `runLogs`: Logs for each runtime
    - `Manual_Sort`: Files for manual review
    - `Logs`: Meter pages with stickers
    - `Inventory Restock`: Pages related to inventory management
    - `temp`: Temporary folder for processing files (if setup is on the C: drive)
    
## Requirements:
- **Software**: 
    - PDF24 (for OCR and PDF viewing)
    - Python 3.11+ 
- **Libraries**: `glob2`, `win32api`, `os`, `shutil`, `time`, `datetime`, `re`, `pdfminer.high_level`, `logging`
    - Install instructions are available in the `setup()` function in `main.py` if libraries are not already installed.

## Workflow:
1. Process files from `C:.\temp`
2. Apply OCR to all files
3. Extract and validate key data: Date, Serial Number, Brand
4. Sort files into appropriate folders based on extracted data
5. Flag invalid files for manual review
6. Move remaining files from `Unsorted` to `temp` for next processing cycle
7. Repeat

This project is intended for personal use and will be updated as needed.
