import glob
from config import temp_path, unsorted_path, logger
from ocr_processor import ocr_file
from manufacturer_handler import manufacturer_wrapper
from file_manager import populate_files, transfer_files_to_temp
import time

"""
Description: 
    Here are the imports (either native or needed installed) used by this project
    It tries to import each module
        if fails provides instructions on how to install module
Returns:
    returns True if no imports failed
    returns False if at least 1 import failed
"""
def setup():

    import_error_count = 0

    try:
        import glob
    except ImportError:
        print("Please install glob 'pip install glob2'")
        import_error_count += 1

    try:
        import shutil
    except ImportError:
        print("Please install shutil 'pip install shutil'")
        import_error_count += 1

    try:
        from pathlib import Path
    except ImportError:
        print("Please install pathlib 'pip install pathlib'")
        import_error_count += 1

    try:
        from pdfminer.high_level import extract_text
    except ImportError:
        print("Please install pdfminer 'pip install pdfminer.six'")
        import_error_count += 1

    try:
        import datetime
    except ImportError:
        print("Please install datetime 'pip install datetime'")
        import_error_count += 1

    try:
        import re
    except ImportError:
        print("Please install re 'pip install regex'")
        import_error_count += 1

    return import_error_count == 0

"""
Description: 
    checks if all modules needed are installed and can be imported
    uses logger.info to create detailed logs
    
    populates files in the 'temp_path' first to clear out the folder
    applies ocr x2 to the file and then passes to manufacturer.py for processing
    
    once 'temp_path' is cleared it'll populate it once again with the 'unsorted_path' files
    applies ocr x2 to the files and then passes to manufacturer.py for processing
"""
if __name__ == '__main__':

    if not setup():
        print("Please install the above libraries and try again...")
        input("Exiting under LIBRARIES_NOT_INSTALLED. Press any key to exit...")
        exit()

    start_time = time.time()

    ## Process files in temp first

    logger.info("Getting all files in 'TEMP' and processing...\n")

    files = populate_files(temp_path)

    if files:
        for file in files:
            ocr_file(file)
            manufacturer_wrapper(file)

    logger.info("Done processing all files in 'TEMP'...\n")

    exit()

    ## Copy files from Unsorted_path to temp_path then process

    logger.info("Getting all files in 'Unsorted_Path', copying to 'TEMP' and processing...\n")

    files.clear()
    files = populate_files(unsorted_path)
    transfer_files_to_temp(files)

    files.clear()
    files = populate_files(temp_path)

    if files:
        for file in files:
            ocr_file(file)
            manufacturer_wrapper(file)

    logger.info("Done processing all copied files in 'TEMP'...\n")

    end_time = time.time()

    elapsed_time = end_time - start_time

    hours = int(elapsed_time // 3600)
    minutes = int((elapsed_time % 3600) // 60)
    seconds = int(elapsed_time % 60)

    print(f"Runtime took {hours:02} hrs {minutes:02} min {seconds:02} seconds")
