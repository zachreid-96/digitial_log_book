import os
import csv
import glob
import json
import time
import threading
import webbrowser

import tkinter as tk
import customtkinter as ct

from pdf_viewer import PDFViewer
from config import DirectoryManager
from file_manager import populate_files
from manufacturer_handler import manufacturer_multi
from database_handler import database_add_files, barcode_wrapper

from pathlib import Path
from datetime import datetime
from tkinter import filedialog
from dateutil.relativedelta import relativedelta
from multiprocessing import Pool, Manager, set_start_method

class Log_Book_GUI(ct.CTk):
    def __init__(self):
        super().__init__()

        self.manager = DirectoryManager()

        if self.manager.is_setup():
            self.setup_project()

        self.title("Digital Log Book")
        self.geometry(f"{1000}x{450}")
        self.minsize(750, 450)

        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar_frame = ct.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)

        self.separator = ct.CTkFrame(self, fg_color="black", width=5)
        self.separator.grid(row=0, column=1, rowspan=4, sticky="ns")

        self.user_menu_frame = ct.CTkFrame(self, corner_radius=0)
        self.user_menu_frame.grid(row=0, column=2, rowspan=4, sticky="nsew")
        self.user_menu_frame.grid_rowconfigure(1, weight=1)

        self.logo_label = ct.CTkLabel(self.sidebar_frame, text="Menu",
                                      font=ct.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.Process_button = ct.CTkButton(self.sidebar_frame, text="Process",
                                           command=self.show_process_menu)
        self.Process_button.grid(row=1, column=0, padx=20, pady=10)

        self.Database_button = ct.CTkButton(self.sidebar_frame, text="Database",
                                            command=self.show_database_menu)
        self.Database_button.grid(row=2, column=0, padx=20, pady=10)

        self.Manual_button = ct.CTkButton(self.sidebar_frame, text="Manual Sort",
                                            command=self.show_manual_menu)
        self.Manual_button.grid(row=3, column=0, padx=20, pady=10)

        self.Settings_button = ct.CTkButton(self.sidebar_frame, text="Settings",
                                            command=self.show_settings_menu)
        self.Settings_button.grid(row=4, column=0, padx=20, pady=10)

        self.Help_button = ct.CTkButton(self.sidebar_frame, text="Help",
                                        command=self.show_help_menu)
        self.Help_button.grid(row=5, column=0, padx=20, pady=10)

        self.About_button = ct.CTkButton(self.sidebar_frame, text="About",
                                         command=self.show_about_menu)
        self.About_button.grid(row=6, column=0, padx=20, pady=10)

        self.current_view = None

        self._switch_view(ProcessMenu)

    def open_input_dialog_event(self):
        dialog = ct.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ct.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ct.set_widget_scaling(new_scaling_float)

    # Switches Frame to the selected one
    def _switch_view(self, view_class):
        if self.current_view:
            self.current_view.destroy()

        self.current_view = view_class(self.user_menu_frame)
        self.current_view.pack(fill="both", expand=True)

    def show_process_menu(self):
        self._switch_view(ProcessMenu)

    def show_database_menu(self):
        self._switch_view(DatabaseMenu)

    def show_manual_menu(self):
        self._switch_view(PDFViewer)

    def show_settings_menu(self):
        self._switch_view(SettingsMenu)

    def show_help_menu(self):
        self._switch_view(HelpMenu)

    def show_about_menu(self):
        self._switch_view(AboutMenu)

    """
    Description: 
        Sets up the designated folder structure without user input or worry about what is needed
    """
    def setup_project(self):

        pathing = os.path.join(os.environ['USERPROFILE'], 'Parts_Log')

        if not os.path.exists(pathing):
            os.mkdir(pathing)

        manual_sort = os.path.join(pathing, 'Manual Sorting Required')
        runtime_logs = os.path.join(pathing, 'Runtime Logs')
        ready_sort = os.path.join(pathing, 'Ready to Sort Pages')
        inventory_pages = os.path.join(pathing, 'Inventory Pages')
        used_parts = os.path.join(pathing, 'Used Parts Logs')
        reports = os.path.join(pathing, 'Reports')

        # Cretes all needed folders if not already created
        for folder in [manual_sort, runtime_logs, ready_sort, inventory_pages, used_parts, reports]:
            if not os.path.exists(folder):
                os.mkdir(folder)

        database_file = os.path.join(pathing, 'Used Parts Database.db')
        manual_json = os.path.join(pathing, 'manual_sort.json')

        # Creates all needed files, if not already created
        for file in [database_file, manual_json]:
            if not os.path.exists(file):
                with open(file, 'w') as f:
                    pass

        json_dict = {
            'unsorted_dir': ready_sort,
            'runlog_dir': runtime_logs,
            'manual_sort_dir': manual_sort,
            'logbook_dir': used_parts,
            'inventory_dir': inventory_pages,
            'database_dir': database_file,
            'reports_dir': reports,
            'manual_json': manual_json
        }

        self.manager.write_config_file(json_dict)


class ProcessMenu(ct.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.manager = DirectoryManager()

        self.unsorted_label = ct.CTkLabel(self, text="Pages Ready to Sort:")
        self.unsorted_label.grid(row=0, column=0, columnspan=3, sticky="e", pady=(40, 10))
        self.unsorted_directory = ct.CTkLabel(self, text=self.manager.get_unsorted_dir())
        self.unsorted_directory.grid(row=0, column=3, columnspan=4, sticky="w", padx=25, pady=(40, 10))

        self.log_label = ct.CTkLabel(self, text="Runtime Logs:")
        self.log_label.grid(row=1, column=0, columnspan=3, sticky="e", pady=10)
        self.log_directory = ct.CTkLabel(self, text=self.manager.get_runlog_dir())
        self.log_directory.grid(row=1, column=3, columnspan=4, sticky="w", padx=25, pady=10)

        self.manual_sort_label = ct.CTkLabel(self, text="Manual Sorting Required:")
        self.manual_sort_label.grid(row=2, column=0, columnspan=3, sticky="e", pady=10)
        self.manual_sort_directory = ct.CTkLabel(self, text=self.manager.get_manual_sort_dir())
        self.manual_sort_directory.grid(row=2, column=3, columnspan=4, sticky="w", padx=25, pady=10)

        self.logbook_label = ct.CTkLabel(self, text="Used Parts:")
        self.logbook_label.grid(row=3, column=0, columnspan=3, sticky="e", pady=10)
        self.logbook_directory = ct.CTkLabel(self, text=self.manager.get_logbook_dir())
        self.logbook_directory.grid(row=3, column=3, columnspan=4, sticky="w", padx=25, pady=10)

        self.inventory_page_label = ct.CTkLabel(self, text="Inventory Pages:")
        self.inventory_page_label.grid(row=4, column=0, columnspan=3, sticky="e", pady=10)
        self.inventory_page_directory = ct.CTkLabel(self, text=self.manager.get_inventory_dir())
        self.inventory_page_directory.grid(row=4, column=3, columnspan=4, sticky="w", padx=25, pady=10)

        self.start_button = ct.CTkButton(self, text="Start Process",
                                         command=self.run_process_multi)
        self.start_button.grid(row=5, column=0, sticky="w", padx=25, pady=10, columnspan=3)
        self.start_button.configure(state="normal")

        self.progress = tk.StringVar(value="Status...")
        self.success_var = tk.StringVar(value="Files Sorted: ")
        self.fail_var = tk.StringVar(value="Files Needing Manual Sorting: ")

        self.progress_start_label = ct.CTkLabel(self, textvariable=self.progress, anchor="w", width=35)
        self.success_label = ct.CTkLabel(self, textvariable=self.success_var, anchor="w", width=35)
        self.fail_label = ct.CTkLabel(self, textvariable=self.fail_var, anchor="w", width=35)

        self.progress_start_label.grid(row=5, column=3, columnspan=2, sticky="w", padx=25, pady=10)
        self.success_label.grid(row=6, column=0, columnspan=3, sticky="w", padx=25, pady=10)
        self.fail_label.grid(row=6, column=2, columnspan=3, sticky="w", padx=25, pady=10)

    def run_process_multi(self):

        thread = threading.Thread(target=self.thread_multi)
        thread.start()

    def thread_multi(self):

        start = time.perf_counter()
        print(f"Start: {start}")

        self.manager.create_logger()

        path = self.manager.unsorted_dir

        files = populate_files(path)
        self.progress.set("Status... EXTRACTING DATA FROM LOGS")

        try:
            set_start_method('spawn', force=True)
        except RuntimeError:
            pass

        cpu_count = max(1, os.cpu_count() // 2)

        process_chunks = [files[i::cpu_count] for i in range(cpu_count)]
        with Manager() as manager:
            manual_sort_list = manager.list()
            process_args = [(chunk, manual_sort_list) for chunk in process_chunks]
            with Pool(processes=cpu_count) as pool:
               pool.starmap(manufacturer_multi, process_args)

            self.progress.set("Status... ADDING DATA TO DATABASE")
            self.manager.logger.info("Done processing all copied files in 'Unsorted'...\n")

            # Get files
            cursor, connection = self.manager.get_database()
            cursor.execute('SELECT STEM FROM FILE_HASH')
            processed_stems = cursor.fetchall()

            files = []
            for file in glob.glob(str(Path(self.manager.get_logbook_dir()).resolve() / '**' / '*.pdf'), recursive=True):
                stem = Path(file).stem
                if stem not in processed_stems:
                    files.append(file)

            files_sorted = sorted(files, key=self.sort_key)
            barcode_list = manager.list()
            barcode_chunks = [files_sorted[i::cpu_count] for i in range(cpu_count)]
            barcode_args = [(chunk, barcode_list) for chunk in barcode_chunks]

            with Pool(processes=cpu_count) as pool:
                pool.starmap(barcode_wrapper, barcode_args)

            for entry in barcode_list:

                if not entry['parts_data']:
                    file_name_parts = Path(entry).stem.split('_')

                    brand = None
                    if 'Kyocera' in entry['file']:
                        brand = 'Kyocera'
                    elif 'HP' in entry['file']:
                        brand = 'HP'
                    elif 'Canon' in entry['file']:
                        brand = 'Canon'
                    elif 'Konica' in entry['file']:
                        brand = 'Konica'

                    manual_sort_list.append({
                        'file': entry['file'],
                        'serial_num': file_name_parts[1],
                        'date': file_name_parts[0],
                        'brand': brand,
                        'parts': None
                    })
                else:
                    database_add_files(entry['file'], entry['parts_data'])

            with open(self.manager.get_manual_json(), 'w') as manual_json:
                json.dump(list(manual_sort_list), manual_json, indent=4)

        end = time.perf_counter()
        self.progress.set("Status... DONE")

        print(f"End: {end}\n")
        print(f"Execution on {len(files)} files took {end - start:.2f} seconds.")

    def sort_key(self, file):
        name = Path(file).stem.split('_')

        if len(name) == 3:
            return 1, name
        elif len(name) == 2:
            return 0, name


class DatabaseMenu(ct.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.manager = DirectoryManager()

        self.report_label = ct.CTkLabel(self, text="Generate Pre-determined Reports",
                                        font=ct.CTkFont(size=15, weight="bold"))
        self.report_label.grid(row=0, column=0, padx=20, pady=(20, 10), columnspan=4, sticky='news')

        self.open_reports = ct.CTkButton(self, text="Open Reports",
                                         command=self.open_report_folder)
        self.open_reports.grid(row=3, column=0, padx=20, pady=10, columnspan=2, sticky='news')

        self.report_month_1 = ct.CTkButton(self, text="1 Month Report",
                                           command=lambda: self.generate_report(1))
        self.report_month_1.grid(row=1, column=0, padx=20, pady=10, columnspan=2, sticky='news')

        self.report_month_3 = ct.CTkButton(self, text="3 Month Report",
                                           command=lambda: self.generate_report(3))
        self.report_month_3.grid(row=1, column=2, padx=20, pady=10, columnspan=2, sticky='news')

        self.report_month_6 = ct.CTkButton(self, text="6 Month Report",
                                           command=lambda: self.generate_report(6))
        self.report_month_6.grid(row=1, column=4, padx=20, pady=10, columnspan=2, sticky='news')

        self.report_month_9 = ct.CTkButton(self, text="9 Month Report",
                                           command=lambda: self.generate_report(9))
        self.report_month_9.grid(row=2, column=0, padx=20, pady=10, columnspan=2, sticky='news')

        self.report_month_12 = ct.CTkButton(self, text="12 Month Report",
                                            command=lambda: self.generate_report(12))
        self.report_month_12.grid(row=2, column=2, padx=20, pady=10, columnspan=2, sticky='news')

        self.report_last_inventory = ct.CTkButton(self, text="Last Inventory",
                                                  command=lambda: self.generate_report("last_inventory"))
        self.report_last_inventory.grid(row=2, column=4, padx=20, pady=10, columnspan=2, sticky='news')

    def open_report_folder(self):

        os.startfile(self.manager.get_reports_dir())

    def generate_report(self, time_frame):

        cursor, connection = self.manager.get_database()

        current_date = datetime.now()
        report_time = None
        report_name = None

        if time_frame == 1:
            report_name = f"1_month_report_{current_date.month}-{current_date.day}-{current_date.year}.csv"
            format_date = datetime.now() - relativedelta(months=1)
            report_time = format_date.strftime('%Y-%m-%d')
        elif time_frame == 3:
            report_name = f"3_month_report_{current_date.month}-{current_date.day}-{current_date.year}.csv"
            format_date = datetime.now() - relativedelta(months=3)
            report_time = format_date.strftime('%Y-%m-%d')
        elif time_frame == 6:
            report_name = f"6_month_report_{current_date.month}-{current_date.day}-{current_date.year}.csv"
            format_date = datetime.now() - relativedelta(months=6)
            report_time = format_date.strftime('%Y-%m-%d')
        elif time_frame == 9:
            report_name = f"9_month_report_{current_date.month}-{current_date.day}-{current_date.year}.csv"
            format_date = datetime.now() - relativedelta(months=9)
            report_time = format_date.strftime('%Y-%m-%d')
        elif time_frame == 12:
            report_name = f"12_month_report_{current_date.month}-{current_date.day}-{current_date.year}.csv"
            format_date = datetime.now() - relativedelta(months=12)
            report_time = format_date.strftime('%Y-%m-%d')
        elif time_frame == "last_inventory":
            report_name = f"last_inventory_report_{current_date.month}-{current_date.day}-{current_date.year}.csv"
            report_time = self.manager.get_last_inventory_date()

        if report_time and report_name:
            command = f"""SELECT 
                                m.DATE,
                                m.SERIAL_NUM,
                                GROUP_CONCAT(p.PART_USED || ' x' || p.QUANTITY, ',') AS Parts_List,
                                f.FILE_PATH
                            FROM MACHINES m
                            LEFT JOIN PARTS_USED p ON m.ENTRY_ID = p.ENTRY_ID
                            LEFT JOIN FILE_HASH f ON m.ENTRY_ID = f.ENTRY_ID
                            WHERE m.DATE >= '{report_time}'
                            GROUP BY m.ENTRY_ID
                            ORDER BY m.DATE DESC;"""

            cursor.execute(command)
            rows = cursor.fetchall()

            headers = [description[0] for description in cursor.description]

            report_path = os.path.join(self.manager.get_reports_dir(), report_name)

            with open(report_path, 'w', newline='', encoding='utf-8') as report_csv:
                writer = csv.writer(report_csv)
                writer.writerow(headers)
                writer.writerows(rows)

        return


class SettingsMenu(ct.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.manager = DirectoryManager()

        magic_width = self.manager.longest_dir_pixel

        self.unsorted_label = ct.CTkLabel(self, text="Pages Ready to Sort:")
        self.unsorted_label.grid(row=0, column=0, columnspan=3, sticky="e", pady=10)
        self.unsorted_directory = ct.CTkEntry(self, width=magic_width)
        self.unsorted_directory.grid(row=0, column=3, columnspan=8, sticky="w", padx=25, pady=10)
        self.unsorted_button = ct.CTkButton(self, text="Browse",
                                            command=lambda: self.select_directory("unsorted"))
        self.unsorted_button.grid(row=0, column=8, columnspan=1, sticky="w", padx=25, pady=10)

        self.log_label = ct.CTkLabel(self, text="Runtime Logs:")
        self.log_label.grid(row=1, column=0, columnspan=3, sticky="e", pady=10)
        self.log_directory = ct.CTkEntry(self, width=magic_width)
        self.log_directory.grid(row=1, column=3, columnspan=4, sticky="w", padx=25, pady=10)
        self.log_button = ct.CTkButton(self, text="Browse", command=lambda: self.select_directory("log"))
        self.log_button.grid(row=1, column=8, columnspan=1, sticky="w", padx=25, pady=10)

        self.manual_sort_label = ct.CTkLabel(self, text="Manual Sorting Required:")
        self.manual_sort_label.grid(row=2, column=0, columnspan=3, sticky="e", pady=10)
        self.manual_sort_directory = ct.CTkEntry(self, width=magic_width)
        self.manual_sort_directory.grid(row=2, column=3, columnspan=4, sticky="w", padx=25, pady=10)
        self.manual_sort_button = ct.CTkButton(self, text="Browse",
                                               command=lambda: self.select_directory("manual_sort"))
        self.manual_sort_button.grid(row=2, column=8, columnspan=1, sticky="w", padx=25, pady=10)

        self.logbook_label = ct.CTkLabel(self, text="Used Parts:")
        self.logbook_label.grid(row=3, column=0, columnspan=3, sticky="e", pady=10)
        self.logbook_directory = ct.CTkEntry(self, width=magic_width)
        self.logbook_directory.grid(row=3, column=3, columnspan=4, sticky="w", padx=25, pady=10)
        self.logbook_button = ct.CTkButton(self, text="Browse",
                                           command=lambda: self.select_directory("logbook"))
        self.logbook_button.grid(row=3, column=8, columnspan=1, sticky="w", padx=25, pady=10)

        self.inventory_page_label = ct.CTkLabel(self, text="Inventory Pages:")
        self.inventory_page_label.grid(row=4, column=0, columnspan=3, sticky="e", pady=10)
        self.inventory_page_directory = ct.CTkEntry(self, width=magic_width)
        self.inventory_page_directory.grid(row=4, column=3, columnspan=4, sticky="w", padx=25, pady=10)
        self.inventory_page_button = ct.CTkButton(self, text="Browse",
                                                  command=lambda: self.select_directory("inventory_page"))
        self.inventory_page_button.grid(row=4, column=8, columnspan=1, sticky="w", padx=25, pady=10)

        self.database_label = ct.CTkLabel(self, text="Used Parts Database:")
        self.database_label.grid(row=5, column=0, columnspan=3, sticky="e", pady=10)
        self.database_directory = ct.CTkEntry(self, width=magic_width)
        self.database_directory.grid(row=5, column=3, columnspan=4, sticky="w", padx=25, pady=10)
        self.database_button = ct.CTkButton(self, text="Browse",
                                            command=lambda: self.select_file("database"))
        self.database_button.grid(row=5, column=8, columnspan=1, sticky="w", padx=25, pady=10)

        self.save_directories = ct.CTkButton(self, text="Save Directories",
                                             command=self.save_directories_locations)

        self.save_directories.grid(row=6, column=2, columnspan=2, sticky="w", padx=25, pady=10)

        self.appearance_mode_label = ct.CTkLabel(self, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=7, column=1, padx=20, pady=(10, 0), columnspan=2)
        self.appearance_mode_optionemenu = ct.CTkOptionMenu(self,
                                                            values=["Light", "Dark", "System"],
                                                            command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=8, column=1, padx=20, pady=(10, 10), columnspan=2)
        self.appearance_mode_optionemenu.set("System")

        self.scaling_label = ct.CTkLabel(self, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=3, padx=20, pady=(10, 0), columnspan=2)
        self.scaling_optionemenu = ct.CTkOptionMenu(self,
                                                    values=["80%", "90%", "100%", "110%", "120%"],
                                                    command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=3, padx=20, pady=(10, 20), columnspan=2)
        self.scaling_optionemenu.set("100%")

        self.populate_directories()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ct.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ct.set_widget_scaling(new_scaling_float)

    def populate_directories(self):
        self.unsorted_directory.delete(0, len(self.manager.unsorted_dir))
        self.unsorted_directory.insert(0, self.manager.unsorted_dir)

        self.log_directory.delete(0, len(self.manager.runlog_dir))
        self.log_directory.insert(0, self.manager.runlog_dir)

        self.manual_sort_directory.delete(0, len(self.manager.manual_sort_dir))
        self.manual_sort_directory.insert(0, self.manager.manual_sort_dir)

        self.logbook_directory.delete(0, len(self.manager.logbook_dir))
        self.logbook_directory.insert(0, self.manager.logbook_dir)

        self.inventory_page_directory.delete(0, len(self.manager.inventory_dir))
        self.inventory_page_directory.insert(0, self.manager.inventory_dir)

        self.database_directory.delete(0, len(self.manager.database_dir))
        self.database_directory.insert(0, self.manager.database_dir)

    def select_file(self, option):
        file = filedialog.askopenfilename(title="Select Database File")
        if file:
            if option == "database":
                self.database_directory.delete(0, len(self.manager.database_dir))
                self.database_directory.insert(0, str(Path(file)))

    def select_directory(self, option):
        directory = filedialog.askdirectory()
        if directory:
            if option == "unsorted":
                self.unsorted_directory.delete(0, len(self.manager.unsorted_dir))
                self.unsorted_directory.insert(0, str(Path(directory)))
            elif option == "log":
                self.log_directory.delete(0, len(self.manager.runlog_dir))
                self.log_directory.insert(0, str(Path(directory)))
            elif option == "manual_sort":
                self.manual_sort_directory.delete(0, len(self.manager.manual_sort_dir))
                self.manual_sort_directory.insert(0, str(Path(directory)))
            elif option == "logbook":
                self.logbook_directory.delete(0, len(self.manager.logbook_dir))
                self.logbook_directory.insert(0, str(Path(directory)))
            elif option == "inventory_page":
                self.inventory_page_directory.delete(0, len(self.manager.inventory_dir))
                self.inventory_page_directory.insert(0, str(Path(directory)))
            else:
                pass

    def save_directories_locations(self):
        data = {
            "unsorted_dir": str(Path(self.unsorted_directory.get())),
            "runlog_dir": str(Path(self.log_directory.get())),
            "manual_sort_dir": str(Path(self.manual_sort_directory.get())),
            "logbook_dir": str(Path(self.logbook_directory.get())),
            "inventory_dir": str(Path(self.inventory_page_directory.get())),
            "database_dir": str(Path(self.database_directory.get()))
        }
        with open("config.json", "w") as file:
            json.dump(data, file, indent=4)


class AboutMenu(ct.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.manager = DirectoryManager()

        help_text = """
                This GUI/project is still a work in progress. Check often for updates.
                Gui version 1.2.0

                Feel free to submit feature requests and bug reports.
                See below for important links"""

        help_label = ct.CTkLabel(self, text=help_text, justify="center")
        help_label.grid(row=0, column=1, columnspan=4, sticky='news')

        repo_button = ct.CTkButton(self, text="GitHub Releases", command=lambda: self.open_link(
            "https://github.com/zachreid-96/digitial_log_book/releases"))
        readme_button = ct.CTkButton(self, text="README/Setup",
                                     command=lambda: self.open_link("https://github.com/zachreid-96/digitial_log_book"))
        issues_button = ct.CTkButton(self, text="Report Issue", command=lambda: self.open_link(
            "https://github.com/zachreid-96/digitial_log_book/issues"))
        repo_button.grid(row=1, column=0, columnspan=2)
        readme_button.grid(row=1, column=2, columnspan=2)
        issues_button.grid(row=1, column=4, columnspan=2)

    def open_link(self, link):
        webbrowser.open(link)


"""
Description: 
    Houses
Args:

Returns:

"""


class HelpMenu(ct.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.manager = DirectoryManager()

        self.unsorted_label = ct.CTkLabel(self, text="Pages Ready to Sort:")
        self.unsorted_label.grid(row=0, column=0, columnspan=3, sticky="e", pady=10)

        self.log_label = ct.CTkLabel(self, text="Runtime Logs:")
        self.log_label.grid(row=1, column=0, columnspan=3, sticky="e", pady=10)

        self.manual_sort_label = ct.CTkLabel(self, text="Manual Sorting Required:")
        self.manual_sort_label.grid(row=2, column=0, columnspan=3, sticky="e", pady=10)

        self.logbook_label = ct.CTkLabel(self, text="Used Parts:")
        self.logbook_label.grid(row=3, column=0, columnspan=3, sticky="e", pady=10)

        self.inventory_page_label = ct.CTkLabel(self, text="Inventory Pages:")
        self.inventory_page_label.grid(row=4, column=0, columnspan=3, sticky="e", pady=10)

        self.reports_label = ct.CTkLabel(self, text="Reports:")
        self.reports_label.grid(row=5, column=0, columnspan=3, sticky="e", pady=10)

        self.database_label = ct.CTkLabel(self, text="Database.db:")
        self.database_label.grid(row=6, column=0, columnspan=3, sticky="e", pady=10)


if __name__ == "__main__":
    app = Log_Book_GUI()
    app.mainloop()
