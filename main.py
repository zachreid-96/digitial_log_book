import glob
import os.path

from config import DirectoryManager
from ocr_processor import ocr_file
from manufacturer_handler import manufacturer_wrapper
from file_manager import populate_files
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
from pathlib import Path

class Log_Book_GUI:
    def __init__(self, gui_root):
        self.root = gui_root
        self.root.title("Log Book Automate Tool")
        self.root.geometry("600x300")

        self.manager = DirectoryManager()

        self.file_list = []

        directory_unsorted = ttk.Frame(gui_root)
        directory_unsorted.pack(pady=5, fill=tk.X, padx=10)

        self.unsorted_label = ttk.Label(directory_unsorted, text="Unsorted")
        self.unsorted_label.pack(side=tk.LEFT)
        self.unsorted_directory = ttk.Entry(directory_unsorted, width=50)
        self.unsorted_directory.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self.unsorted_button = ttk.Button(directory_unsorted, text="Browse",
                                          command=lambda: self.select_directory("unsorted"))
        self.unsorted_button.pack(side=tk.RIGHT)

        directory_logs = ttk.Frame(gui_root)
        directory_logs.pack(pady=5, fill=tk.X, padx=10)

        self.log_label = ttk.Label(directory_logs, text="Runtime Logs")
        self.log_label.pack(side=tk.LEFT)
        self.log_directory = ttk.Entry(directory_logs, width=50)
        self.log_directory.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self.log_button = ttk.Button(directory_logs, text="Browse", command=lambda: self.select_directory("log"))
        self.log_button.pack(side=tk.RIGHT)

        directory_manual = ttk.Frame(gui_root)
        directory_manual.pack(pady=5, fill=tk.X, padx=10)

        self.manual_sort_label = ttk.Label(directory_manual, text="Manual Sort")
        self.manual_sort_label.pack(side=tk.LEFT)
        self.manual_sort_directory = ttk.Entry(directory_manual, width=50)
        self.manual_sort_directory.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self.manual_sort_button = ttk.Button(directory_manual, text="Browse",
                                             command=lambda: self.select_directory("manual_sort"))
        self.manual_sort_button.pack(side=tk.RIGHT)

        directory_logbook = ttk.Frame(gui_root)
        directory_logbook.pack(pady=5, fill=tk.X, padx=10)

        self.logbook_label = ttk.Label(directory_logbook, text="Logbook")
        self.logbook_label.pack(side=tk.LEFT)
        self.logbook_directory = ttk.Entry(directory_logbook, width=50)
        self.logbook_directory.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self.logbook_button = ttk.Button(directory_logbook, text="Browse",
                                         command=lambda: self.select_directory("logbook"))
        self.logbook_button.pack(side=tk.RIGHT)

        directory_inventory = ttk.Frame(gui_root)
        directory_inventory.pack(pady=5, fill=tk.X, padx=10)

        self.inventory_page_label = ttk.Label(directory_inventory, text="Inventory Pages")
        self.inventory_page_label.pack(side=tk.LEFT)
        self.inventory_page_directory = ttk.Entry(directory_inventory, width=50)
        self.inventory_page_directory.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self.inventory_page_button = ttk.Button(directory_inventory, text="Browse",
                                                command=lambda: self.select_directory("inventory_page"))
        self.inventory_page_button.pack(side=tk.RIGHT)

        directory_temp = ttk.Frame(gui_root)
        directory_temp.pack(pady=5, fill=tk.X, padx=10)

        self.temp_label = ttk.Label(directory_temp, text="Temp")
        self.temp_label.pack(side=tk.LEFT)
        self.temp_directory = ttk.Entry(directory_temp, width=50)
        self.temp_directory.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self.temp_button = ttk.Button(directory_temp, text="Browse", command=lambda: self.select_directory("temp"))
        self.temp_button.pack(side=tk.RIGHT)

        buttons_frame = ttk.Frame(gui_root)
        buttons_frame.pack(pady=5, fill=tk.X, padx=10)

        self.start_button = ttk.Button(buttons_frame, text="Start Process",
                                       command=lambda: self.thread_process(self.manager.unsorted_dir))
        self.readme_button = ttk.Button(buttons_frame, text="README/Instructions")
        self.save_directories = ttk.Button(buttons_frame, text="Save Directories", command=self.save_directories)

        self.start_button.grid(row=0, column=3, sticky="w", padx=5, pady=2)
        self.readme_button.grid(row=0, column=1, sticky="w", padx=5, pady=2)
        self.save_directories.grid(row=0, column=2, sticky="w", padx=5, pady=2)

        self.populate_directories()

    def populate_directories(self):
        self.unsorted_directory.delete(0, tk.END)
        self.unsorted_directory.insert(0, self.manager.unsorted_dir)

        self.log_directory.delete(0, tk.END)
        self.log_directory.insert(0, self.manager.runlog_dir)

        self.manual_sort_directory.delete(0, tk.END)
        self.manual_sort_directory.insert(0, self.manager.manual_sort_dir)

        self.logbook_directory.delete(0, tk.END)
        self.logbook_directory.insert(0, self.manager.logbook_dir)

        self.inventory_page_directory.delete(0, tk.END)
        self.inventory_page_directory.insert(0, self.manager.inventory_dir)

        self.temp_directory.delete(0, tk.END)
        self.temp_directory.insert(0, self.manager.temp_dir)

    def save_directories(self):
        data = {
            "unsorted_dir": str(Path(self.unsorted_directory.get())),
            "runlog_dir": str(Path(self.log_directory.get())),
            "manual_sort_dir": str(Path(self.manual_sort_directory.get())),
            "logbook_dir": str(Path(self.logbook_directory.get())),
            "inventory_dir": str(Path(self.inventory_page_directory.get())),
            "temp_dir": str(Path(self.temp_directory.get()))
        }
        print(data)
        with open("config.json", "w") as file:
            json.dump(data, file, indent=4)

    def select_directory(self, option):
        directory = filedialog.askdirectory()
        if directory:
            if option == "unsorted":
                self.unsorted_directory.delete(0, tk.END)
                self.unsorted_directory.insert(0, directory)
            elif option == "log":
                self.log_directory.delete(0, tk.END)
                self.log_directory.insert(0, directory)
            elif option == "manual_sort":
                self.manual_sort_directory.delete(0, tk.END)
                self.manual_sort_directory.insert(0, directory)
            elif option == "logbook":
                self.logbook_directory.delete(0, tk.END)
                self.logbook_directory.insert(0, directory)
            elif option == "inventory_page":
                self.inventory_page_directory.delete(0, tk.END)
                self.inventory_page_directory.insert(0, directory)
            elif option == "temp":
                self.temp_directory.delete(0, tk.END)
                self.temp_directory.insert(0, directory)
            else:
                pass

    def thread_process(self, path):

        files = populate_files(path)

        if files:
            for file in files:
                print(file)
                data = ocr_file(file)
                manufacturer_wrapper(file, data)

        self.manager.logger.info("Done processing all copied files in 'Unsorted'...\n")

    def run(self, path):
        files = populate_files(path)

        if files:
            for file in files:
                print(file)
                data = ocr_file(file)
                manufacturer_wrapper(file, data)

        self.manager.logger.info("Done processing all copied files in 'Unsorted'...\n")


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

    try:
        import win32api
    except ImportError:
        print("Please install re 'pip install pywin32'")
        import_error_count += 1

    return import_error_count == 0


'''def run(path):
    files = populate_files(path)

    if files:
        for file in files:
            data = ocr_file(file)
            manufacturer_wrapper(file, data)

    logger.info("Done processing all copied files in 'Unsorted'...\n")'''


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
    '''if not setup():
        print("Please install the above libraries and try again...")
        input("Exiting under LIBRARIES_NOT_INSTALLED. Press any key to exit...")
        exit()

    start_time = time.time()

    ## Process files in temp first

    logger.info("Getting all files in 'TEMP' and processing...\n")

    files = populate_files(temp_path)

    if files:
        for file in files:
            data = ocr_file(file)
            manufacturer_wrapper(file, data)

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

    print(f"Runtime took {hours:02} hrs {minutes:02} min {seconds:02} seconds")'''

    root = tk.Tk()
    app = Log_Book_GUI(root)
    root.mainloop()
