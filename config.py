import logging
from datetime import datetime
import json
import os

"""
Description: 
    Creates a logger instance for the run duration
    will used a specified log output path to store the log file once completed
"""


def setup_logger():
    path_manager = DirectoryManager()
    log_path = path_manager.get_runlog_dir()

    log_filename = datetime.now().strftime(rf"{log_path}\%m-%d-%Y_runtime.log")

    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename)
        ]
    )
    return logging.getLogger()


"""
Description: 
    used to convert 2 in 2/15/2024 to 2-February while utilizing a dictionary
    used to name folders in the folder structure
Args:
    int_month: integer representation of the month
Returns:
    returns 2-February for 2 in 2/15/2024
"""


def convert_month_str(int_month):
    months = {1: "January",
              2: "February",
              3: "March",
              4: "April",
              5: "May",
              6: "June",
              7: "July",
              8: "August",
              9: "September",
              10: "October",
              11: "November",
              12: "December"}

    return f"{int_month}-{months.get(int_month)}"


"""
Description: 
    This is used to setup and store a lot of commonly used pathing vars
    
"""

#unsorted_path = rf"{manuals_drive}\Digital Log Book\Unsorted"
#log_path = rf"{manuals_drive}\Digital Log Book\runLogs"
#manual_sort_path = rf"{manuals_drive}\Digital Log Book\Manual_Sort"
#logbook_path = rf"{manuals_drive}\Digital Log Book\Logs"
# inventory_page_path = rf"{manuals_drive}\Digital Log Book\Inventory_Pages"
#inventory_page_path = rf"{manuals_drive}\Digital Log Book"
#temp_path = rf"C:\Users\********\DLB_testing\temp"

#logger = setup_logger()


class DirectoryManager:
    _instance = None
    CONFIG_FILE = "config.json"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.unsorted_dir = ""
            cls._instance.runlog_dir = ""
            cls._instance.manual_sort_dir = ""
            cls._instance.logbook_dir = ""
            cls._instance.inventory_dir = ""
            cls._instance.temp_dir = ""
            cls._instance.logger = None
            cls._instance.load_directories_from_file()
            cls._instance.fails = 0
            cls._instance.successes = 0
        return cls._instance

    def load_directories_from_file(self):
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, "r") as file:
                    data = json.load(file)
                    self.unsorted_dir = data.get("unsorted_dir")
                    self.runlog_dir = data.get("runlog_dir")
                    self.manual_sort_dir = data.get("manual_sort_dir")
                    self.logbook_dir = data.get("logbook_dir")
                    self.inventory_dir = data.get("inventory_dir")
                    self.temp_dir = data.get("temp_dir")
                self.logger = None
                self.fails = 0
                self.successes = 0
            except json.JSONDecodeError:
                if self.logger is not None:
                    self.logger.error("Failed to populate Singleton")
                else:
                    pass

    def updated_fails(self):
        self.fails += 1

    def update_successes(self):
        self.successes += 1

    def create_logger(self):
        self.logger = setup_logger()

    def get_unsorted_dir(self):
        return self.unsorted_dir

    def get_runlog_dir(self):
        return self.runlog_dir

    def get_manual_sort_dir(self):
        return self.manual_sort_dir

    def get_logbook_dir(self):
        return self.logbook_dir

    def get_inventory_dir(self):
        return self.inventory_dir

    def get_temp_dir(self):
        return self.temp_dir

    def get_logger(self):
        return self.logger
