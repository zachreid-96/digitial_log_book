from config import logger
import json
import os


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
            cls._instance.load_directories_from_file()
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
            except json.JSONDecodeError:
                logger.error("Failed to populate Singleton")

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
