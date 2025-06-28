import logging
from datetime import datetime
import json
import os
import sqlite3

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
            cls._instance.database_dir = ""
            cls._instance.reports_dir = ""
            cls._instance.logger = None
            cls._instance.fails = 0
            cls._instance.successes = 0
            cls._instance.cursor = None
            cls._instance.connection = None
            cls._instance.database_total = 0
            cls._instance.database_processed = 0
            cls._instance.setup = 0
            cls._instance.longest_dir_pixel = 0
            cls._instance.load_directories_from_file()
        return cls._instance

    def load_directories_from_file(self, recursive=False):
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, "r") as file:
                    data = json.load(file)
                    self.unsorted_dir = data.get("unsorted_dir")
                    self.runlog_dir = data.get("runlog_dir")
                    self.manual_sort_dir = data.get("manual_sort_dir")
                    self.logbook_dir = data.get("logbook_dir")
                    self.inventory_dir = data.get("inventory_dir")
                    self.database_dir = data.get("database_dir")
                    self.reports_dir = data.get("reports_dir")

                    print(self.reports_dir)

                if any(filepath == "" for filepath in [self.unsorted_dir, self.runlog_dir, self.manual_sort_dir,
                                                       self.logbook_dir, self.inventory_dir, self.database_dir,
                                                       self.reports_dir]):
                    self.setup = 1

                self.logger = self.get_logger()
                self.fails = 0
                self.successes = 0
                self.cursor = None
                self.connection = None

                for temp_str in [self.unsorted_dir, self.runlog_dir, self.manual_sort_dir, self.logbook_dir,
                                 self.inventory_dir, self.database_dir]:
                    if len(temp_str) * 8 > self.longest_dir_pixel:
                        self.longest_dir_pixel = len(temp_str) * 8

            except json.JSONDecodeError:
                if self.logger is not None:
                    self.logger.error("Failed to populate Singleton")
                else:
                    pass
        else:
            if not recursive:
                with open(self.CONFIG_FILE, "w") as file:
                    self.load_directories_from_file(True)

    def setup_database(self):
        database_name = self.database_dir
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()

        machines = """CREATE TABLE MACHINES(
                            ENTRY_ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                            BRAND TEXT, 
                            SERIAL_NUM TEXT, 
                            DATE TEXT);"""

        parts_used = """CREATE TABLE PARTS_USED(
                            ENTRY_ID INTEGER,
                            PART_USED TEXT, 
                            QUANTITY INTEGER,
                            FOREIGN KEY (ENTRY_ID) REFERENCES MACHINES(ENTRY_ID));"""

        file_hash = """CREATE TABLE FILE_HASH(
                            HASH TEXT PRIMARY KEY,
                            FILE_PATH TEXT,
                            ENTRY_ID INTEGER,
                            FOREIGN KEY (ENTRY_ID) REFERENCES MACHINES(ENTRY_ID));"""

        try:
            cursor.execute(machines)
        except Exception as e:
            self.logger.warning(e)

        try:
            cursor.execute(parts_used)
        except Exception as e:
            self.logger.warning(e)

        try:
            cursor.execute(file_hash)
        except Exception as e:
            self.logger.warning(e)

        connection.commit()
        connection.close()

    def get_database(self):
        database_name = self.database_dir
        if self.logger is None:
            # print('logger is setup')
            self.create_logger()

        self.setup_database()
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()
        return self.cursor, self.connection

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

    def get_database_dir(self):
        return self.database_dir

    def get_reports_dir(self):
        return self.reports_dir

    def get_logger(self):
        return self.logger

    def update_database_total(self, total):
        self.database_total = total

    def update_database_process(self):
        self.database_processed += 1

    def is_setup(self):
        if self.setup == 0:
            return True
        return False

    def write_config_file(self, path_dict):

        if not os.path.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, 'w') as f:
                pass

        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(path_dict, f, indent=4, sort_keys=True)

        return
