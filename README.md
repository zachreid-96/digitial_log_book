# Digital Logbook
The **Digital Logbook** project is designed to streamline copier and printer service tracking, particularly focusing on logging part usage during repairs. The system processes scanned meter pages, extracts key details such as part numbers, machine brand, service date, and serial number, and organizes the data into a structured format.

## Key Features

## Graphical User Interface (GUI)
The project now includes a Tkinter-based GUI with four main tabs:
- **Process Logs**: Handles file processing, including OCR, data extraction, renaming, and file organization.
- **Database** (_Not yet implemented_): Will support adding processed logs to a database and searching through logged data.
- **Settings**: Allows users to define and save directory paths to a .json file for future use.
- **Help**: Provides basic project information, including a work-in-progress notice and useful GitHub links.

### Updated OCR Processing
- Uses pytesseract instead of PDF24 for OCR, reducing external dependencies and ensuring a minimal setup.
- Extracted data includes part numbers, serial numbers, service dates, and machine brands.

### File Sorting & Organization
- Files are categorized into brand-specific folders (Kyocera, HP, Inventory) or flagged for manual review if essential data is missing.
- Customizable folder structure includes:
  - Unsorted: Files pending OCR processing
  - runLogs: Runtime logs
  - Manual_Sort: Files requiring manual review
  - Logs: Meter pages with stickers
  - Inventory Restock: Pages related to inventory management


## Workflow
- Process scanned files from the user-defined directory.
- Apply OCR using pytesseract.
- Extract and validate key data: Date, Serial Number, Brand, and Part Number.
- Sort files into appropriate folders based on extracted data.
- Flag invalid files for manual review.
- Repeat for the next processing batch.

## Planned Features
- Database Integration: A structured database will store extracted log data, separate from the processing workflow.
- Barcode Scanner Support: For improved part number extraction accuracy.
- Enhanced Search & Filtering: To quickly find specific logs in the database.
- Create a setup.py to install all required libraries
- Create an .exe to allow more flexibility

## Requirements
- Software: Python 3.11+
- Libraries: tkinter, webbrowser, os, json, pathlib, re, datetime, rapidfuzz, logging, shutil, glob, PIL, fitz, pytesseract

## License
This project is licensed under the MIT License, allowing for open use and modification.