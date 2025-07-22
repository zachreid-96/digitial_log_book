# Digital Logbook
A smart, OCR-powered alternative to the traditional paper logbook — built for copier technicians who want to self-manage their inventory and usage tracking efficiently. This tool replaces the physical logbook with a digital, automated, and searchable system designed for modern techs who want independence, speed, and data-backed decision making.

## Key Features
- Full OCR Pipeline using Tesseract to scan usage pages and extract metadata (brand, serial number, date)
- Strict PDF Renaming and folder placement for tidy storage and traceability
- Barcode Data Extraction (part numbers and quantities used) post-OCR
- SQLite Database Integration for centralized part usage tracking
- Built-in Report Generation for 1/3/6/9/12-month windows or since last inventory — exported to CSV
- Modern GUI using CustomTkinter
- Multiprocessing support to significantly speed up OCR and barcode processing
- Folder Structure Auto-Setup — no manual prep needed
- Manual Review System with PDF Viewer to inspect/edit OCR-failed documents
- Persistent Settings stored in a user-facing JSON config file

# Menu Breakdown
### Process Menu

- Scans Ready to Sort folder
- OCRs all pages using multiprocessing
- Flags and logs files missing key metadata (serial number, brand, or date)
- Renames + relocates successful pages
- Rebuilds a fresh file list from the Parts Used folder (if not already added to DB)
- Extracts barcode data (also multiprocessed) for part/quantity
- Inputs structured data into the central database
- Flags pages with missing barcode data for Manual Review

### Manual Review Menu

- Simple PDF viewer for flagged documents
- Auto-fills known data into fields
- Allows manual entry of missing info (serial number, date, etc.)
- On completion, feeds updated data into the main pipeline and clears it from the review list

### Settings Menu

- Change directory paths for:
  - Folders for storing folder (Ready to Sort, Manual Review, Parts Log, Inventory, etc)
  - Database
- Save updated settings to a persistent config.json

Reports Menu

- Generate CSV reports for:
  - 1 / 3 / 6 / 9 / 12-month spans
  - Since last inventory date (not yet implemented fully)
- Output includes:
  - Serial number
  - Date
  - Part(s) used and quantity
  - File path for reference

### File Sorting & Organization
- Files are categorized into brand-specific folders (Kyocera, HP, Inventory, Canon) or flagged for manual review if essential data is missing.
- Customizable folder structure includes:
  - Unsorted: Files pending OCR processing
  - runLogs: Runtime logs
  - Manual_Sort: Files requiring manual review
  - Logs: Meter pages with stickers
  - Inventory Restock: Pages related to inventory management


# Stretch Goals
📈 Advanced Reporting

- Usage Summary Reports (Implemented)
  - Show total quantity of each part used, sorted by highest usage
  - Includes daily/weekly usage averages and suggested car stock values per item

- Stock Comparison Tool (Implemented)
  - Compare parts used during report timeframe to user-inputted car stock
  - Highlights overstock, understock, and dead inventory (never used)

- Inventory Management Menu (Implemented)
  - Add/import car stock (CSV or manual entry)
  - Save and update inventory levels per tech
  - Integrate with usage reports for live insights

## Requirements
- Software: Python 3.12+
- Libraries: tkinter, webbrowser, os, json, pathlib, re, datetime, rapidfuzz, logging, shutil, glob, PIL, fitz, pytesseract
- Dependencies: Tesseract-OCR
- Tesseract-OCR: Put in PATH via System Environment Variables

## License
This project is licensed under the MIT License, allowing for open use and modification.
