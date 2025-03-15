import webbrowser
from config import DirectoryManager
from ocr_processor import ocr_file
from manufacturer_handler import manufacturer_wrapper
from file_manager import populate_files
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
from pathlib import Path


class Log_Book_GUI:
    def __init__(self, gui_root):

        self.root = gui_root
        self.root.title("Log Book Automate Tool")
        self.root.geometry("600x325")

        self.last_menu_visited = ""

        self.manager = DirectoryManager()

        self.file_list = []

        self.unsorted_button = None
        self.unsorted_directory = None
        self.unsorted_label = None

        self.log_button = None
        self.log_directory = None
        self.log_label = None

        self.manual_sort_button = None
        self.manual_sort_directory = None
        self.manual_sort_label = None

        self.logbook_label = None
        self.logbook_directory = None
        self.logbook_button = None

        self.inventory_page_label = None
        self.inventory_page_directory = None
        self.inventory_page_button = None

        self.readme_button = None
        self.save_directories = None
        self.start_button = None
        self.verify_button = None

        self.custom_topbar = tk.Frame(self.root)
        self.custom_topbar.pack(side="top", fill="x")

        self.process_logs_button = tk.Button(
            self.custom_topbar, text="Process Logs",
            relief="flat", padx=10, pady=0,
            command=self.process_menu_load
        )
        self.database_button = tk.Button(
            self.custom_topbar, text="Database",
            relief="flat", padx=10, pady=0,
            command=self.database_menu_load
        )
        self.settings_button = tk.Button(
            self.custom_topbar, text="Settings",
            relief="flat", padx=10, pady=0,
            command=self.settings_menu_load
        )
        self.help_button = tk.Button(
            self.custom_topbar, text="Help",
            relief="flat", padx=10, pady=0,
            command=self.help_menu_load
        )

        self.process_logs_button.pack(side=tk.LEFT)
        self.database_button.pack(side=tk.LEFT)
        self.settings_button.pack(side=tk.LEFT)
        self.help_button.pack(side=tk.LEFT)

        self.settings_menu_frame = tk.Frame(self.root)
        self.process_menu_frame = tk.Frame(self.root)
        self.database_menu_frame = tk.Frame(self.root)
        self.help_menu_frame = tk.Frame(self.root)

        self.verified_var = None
        self.progress = None
        self.discovery_var = None
        self.process_var = None
        self.success_var = None
        self.fail_var = None

        self.verified_label = None
        self.progress_start_label = None
        self.discovery_label = None
        self.process_label = None
        self.success_label = None
        self.fail_label = None

        self.process_menu_load()

    def settings_menu_load(self):

        if self.last_menu_visited == "settings_menu":
            return

        if self.last_menu_visited == "process_menu":
            self.last_menu_visited = "settings_menu"
            for widget in self.process_menu_frame.winfo_children():
                widget.destroy()
            self.process_menu_frame.pack_forget()
            self.process_logs_button.config(bg="#F0F0F0")
        elif self.last_menu_visited == "database_menu":
            self.last_menu_visited = "settings_menu"
            for widget in self.database_menu_frame.winfo_children():
                widget.destroy()
            self.database_menu_frame.pack_forget()
            self.database_button.config(bg="#F0F0F0")
        elif self.last_menu_visited == "help_menu":
            self.last_menu_visited = "settings_menu"
            for widget in self.help_menu_frame.winfo_children():
                widget.destroy()
            self.help_menu_frame.pack_forget()
            self.help_button.config(bg="#F0F0F0")
        elif self.last_menu_visited == "":
            self.last_menu_visited = "settings_menu"

        self.settings_button.config(bg="#D9D9D9")
        self.settings_menu_frame.pack(fill="both", expand=True)

        directory_unsorted = ttk.Frame(self.settings_menu_frame)
        directory_unsorted.pack(pady=5, fill=tk.X, padx=10)

        self.unsorted_label = ttk.Label(directory_unsorted, text="Unsorted")
        self.unsorted_label.pack(side=tk.LEFT)
        self.unsorted_directory = ttk.Entry(directory_unsorted, width=50)
        self.unsorted_directory.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self.unsorted_button = ttk.Button(directory_unsorted, text="Browse",
                                          command=lambda: self.select_directory("unsorted"))
        self.unsorted_button.pack(side=tk.RIGHT)

        directory_logs = ttk.Frame(self.settings_menu_frame)
        directory_logs.pack(pady=5, fill=tk.X, padx=10)

        self.log_label = ttk.Label(directory_logs, text="Runtime Logs")
        self.log_label.pack(side=tk.LEFT)
        self.log_directory = ttk.Entry(directory_logs, width=50)
        self.log_directory.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self.log_button = ttk.Button(directory_logs, text="Browse", command=lambda: self.select_directory("log"))
        self.log_button.pack(side=tk.RIGHT)

        directory_manual = ttk.Frame(self.settings_menu_frame)
        directory_manual.pack(pady=5, fill=tk.X, padx=10)

        self.manual_sort_label = ttk.Label(directory_manual, text="Manual Sort")
        self.manual_sort_label.pack(side=tk.LEFT)
        self.manual_sort_directory = ttk.Entry(directory_manual, width=50)
        self.manual_sort_directory.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self.manual_sort_button = ttk.Button(directory_manual, text="Browse",
                                             command=lambda: self.select_directory("manual_sort"))
        self.manual_sort_button.pack(side=tk.RIGHT)

        directory_logbook = ttk.Frame(self.settings_menu_frame)
        directory_logbook.pack(pady=5, fill=tk.X, padx=10)

        self.logbook_label = ttk.Label(directory_logbook, text="Logbook")
        self.logbook_label.pack(side=tk.LEFT)
        self.logbook_directory = ttk.Entry(directory_logbook, width=50)
        self.logbook_directory.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self.logbook_button = ttk.Button(directory_logbook, text="Browse",
                                         command=lambda: self.select_directory("logbook"))
        self.logbook_button.pack(side=tk.RIGHT)

        directory_inventory = ttk.Frame(self.settings_menu_frame)
        directory_inventory.pack(pady=5, fill=tk.X, padx=10)

        self.inventory_page_label = ttk.Label(directory_inventory, text="Inventory Pages")
        self.inventory_page_label.pack(side=tk.LEFT)
        self.inventory_page_directory = ttk.Entry(directory_inventory, width=50)
        self.inventory_page_directory.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self.inventory_page_button = ttk.Button(directory_inventory, text="Browse",
                                                command=lambda: self.select_directory("inventory_page"))
        self.inventory_page_button.pack(side=tk.RIGHT)

        buttons_frame = ttk.Frame(self.settings_menu_frame)
        buttons_frame.pack(pady=5, fill=tk.X, padx=10)

        self.save_directories = ttk.Button(buttons_frame, text="Save Directories", command=self.save_directories)

        self.save_directories.pack(pady=5, fill=tk.X, padx=10)

        self.populate_directories()

    def process_menu_load(self):

        if self.last_menu_visited == "process_menu":
            return

        if self.last_menu_visited == "settings_menu":
            self.last_menu_visited = "process_menu"
            for widget in self.settings_menu_frame.winfo_children():
                widget.destroy()
            self.settings_menu_frame.pack_forget()
            self.settings_button.config(bg="#F0F0F0")
        elif self.last_menu_visited == "database_menu":
            self.last_menu_visited = "process_menu"
            for widget in self.database_menu_frame.winfo_children():
                widget.destroy()
            self.database_menu_frame.pack_forget()
            self.database_button.config(bg="#F0F0F0")
        elif self.last_menu_visited == "help_menu":
            self.last_menu_visited = "process_menu"
            for widget in self.help_menu_frame.winfo_children():
                widget.destroy()
            self.help_menu_frame.pack_forget()
            self.help_button.config(bg="#F0F0F0")
        elif self.last_menu_visited == "":
            self.last_menu_visited = "process_menu"

        self.process_logs_button.config(bg="#D9D9D9")
        self.process_menu_frame.pack(fill="both", expand=True)

        directory_unsorted = ttk.Frame(self.process_menu_frame)
        directory_unsorted.pack(pady=5, fill=tk.X, padx=10)
        self.unsorted_label = ttk.Label(directory_unsorted, text="Unsorted Directory:")
        self.unsorted_label.pack(side=tk.LEFT)
        self.unsorted_directory = ttk.Label(directory_unsorted, text=self.manager.get_unsorted_dir())
        self.unsorted_directory.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        directory_runtime = ttk.Frame(self.process_menu_frame)
        directory_runtime.pack(pady=5, fill=tk.X, padx=10)
        self.log_label = ttk.Label(directory_runtime, text="Runtime Log Directory:")
        self.log_label.pack(side=tk.LEFT)
        self.log_directory = ttk.Label(directory_runtime, text=self.manager.get_runlog_dir())
        self.log_directory.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        directory_manual_sort = ttk.Frame(self.process_menu_frame)
        directory_manual_sort.pack(pady=5, fill=tk.X, padx=10)
        self.manual_sort_label = ttk.Label(directory_manual_sort, text="Manual Sort Directory:")
        self.manual_sort_label.pack(side=tk.LEFT)
        self.manual_sort_directory = ttk.Label(directory_manual_sort, text=self.manager.get_manual_sort_dir())
        self.manual_sort_directory.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        directory_logbook = ttk.Frame(self.process_menu_frame)
        directory_logbook.pack(pady=5, fill=tk.X, padx=10)
        self.logbook_label = ttk.Label(directory_logbook, text="Logbook Directory:")
        self.logbook_label.pack(side=tk.LEFT)
        self.logbook_directory = ttk.Label(directory_logbook, text=self.manager.get_logbook_dir())
        self.logbook_directory.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        directory_inventory = ttk.Frame(self.process_menu_frame)
        directory_inventory.pack(pady=5, fill=tk.X, padx=10)
        self.inventory_page_label = ttk.Label(directory_inventory, text="Inventory Pages Directory:")
        self.inventory_page_label.pack(side=tk.LEFT)
        self.inventory_page_directory = ttk.Label(directory_inventory, text=self.manager.get_inventory_dir())
        self.inventory_page_directory.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        buttons_frame = ttk.Frame(self.process_menu_frame)
        buttons_frame.pack(pady=5, fill=tk.X, padx=10)

        self.verify_button = ttk.Button(buttons_frame, text="Verify Directories",
                                       command=lambda: self.verify_directories())
        self.verify_button.grid(row=0, column=1, sticky="w", padx=5, pady=2)

        self.start_button = ttk.Button(buttons_frame, text="Start Process",
                                       command=lambda: self.run_process_files(self.manager.unsorted_dir))
        self.start_button.grid(row=0, column=2, sticky="w", padx=5, pady=2)
        self.start_button.config(state="disabled")

        progress_frame = ttk.Frame(self.process_menu_frame)
        progress_frame.pack(pady=5, fill=tk.X, padx=5)

        self.verified_var = tk.StringVar(value="Verified...")
        self.progress = tk.StringVar(value="Running...")
        self.discovery_var = tk.StringVar(value="Discovering Files...")
        self.process_var = tk.StringVar(value="Processing Files...")
        self.success_var = tk.StringVar(value="Successful Files: ")
        self.fail_var = tk.StringVar(value="Failed Files: ")

        self.verified_label = tk.Label(progress_frame, textvariable=self.verified_var, anchor="w", width=35)
        self.progress_start_label = tk.Label(progress_frame, textvariable=self.progress, anchor="w", width=35)
        self.discovery_label = tk.Label(progress_frame, textvariable=self.discovery_var, anchor="w", width=35)
        self.process_label = tk.Label(progress_frame, textvariable=self.process_var, anchor="w", width=35)
        self.success_label = tk.Label(progress_frame, textvariable=self.success_var, anchor="w", width=35)
        self.fail_label = tk.Label(progress_frame, textvariable=self.fail_var, anchor="w", width=35)

        self.verified_label.grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.progress_start_label.grid(row=0, column=1, sticky="w", padx=5, pady=2)
        self.discovery_label.grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.process_label.grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.success_label.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        self.fail_label.grid(row=2, column=1, sticky="w", padx=5, pady=2)

        return

    def database_menu_load(self):

        if self.last_menu_visited == "database_menu":
            return

        if self.last_menu_visited == "settings_menu":
            self.last_menu_visited = "database_menu"
            for widget in self.settings_menu_frame.winfo_children():
                widget.destroy()
            self.settings_menu_frame.pack_forget()
            self.settings_button.config(bg="#F0F0F0")
        elif self.last_menu_visited == "process_menu":
            self.last_menu_visited = "database_menu"
            for widget in self.process_menu_frame.winfo_children():
                widget.destroy()
            self.process_menu_frame.pack_forget()
            self.process_logs_button.config(bg="#F0F0F0")
        elif self.last_menu_visited == "help_menu":
            self.last_menu_visited = "database_menu"
            for widget in self.help_menu_frame.winfo_children():
                widget.destroy()
            self.help_menu_frame.pack_forget()
            self.help_button.config(bg="#F0F0F0")
        elif self.last_menu_visited == "":
            self.last_menu_visited = "database_menu"

        self.database_button.config(bg="#D9D9D9")
        self.database_menu_frame.pack(fill="both", expand=True)

        database_text = """
        The Database Part of the Project has not yet been implemented.
        
        Please check again soon using the links found in Help.
        """

        database_label = ttk.Label(self.database_menu_frame, text=database_text, justify="center")
        database_label.pack(pady=5)

        return

    def help_menu_load(self):

        if self.last_menu_visited == "help_menu":
            return

        if self.last_menu_visited == "settings_menu":
            self.last_menu_visited = "help_menu"
            for widget in self.settings_menu_frame.winfo_children():
                widget.destroy()
            self.settings_menu_frame.pack_forget()
            self.settings_button.config(bg="#F0F0F0")
        elif self.last_menu_visited == "process_menu":
            self.last_menu_visited = "help_menu"
            for widget in self.process_menu_frame.winfo_children():
                widget.destroy()
            self.process_menu_frame.pack_forget()
            self.process_logs_button.config(bg="#F0F0F0")
        elif self.last_menu_visited == "database_menu":
            self.last_menu_visited = "help_menu"
            for widget in self.database_menu_frame.winfo_children():
                widget.destroy()
            self.database_menu_frame.pack_forget()
            self.database_button.config(bg="#F0F0F0")
        elif self.last_menu_visited == "":
            self.last_menu_visited = "help_menu"

        self.help_button.config(bg="#D9D9D9")
        self.help_menu_frame.pack(fill="both", expand=True)

        help_text = """This GUI/project is still a work in progress. Check often for updates.
        Gui version 1.2.0
        
        Feel free to submit feature requests and bug reports.
        See below for important links        
        """
        help_label = ttk.Label(self.help_menu_frame, text=help_text, justify="center")
        help_label.pack(pady=5)

        repo_button = ttk.Button(self.help_menu_frame, text="GitHub Releases", command=lambda: self.open_link("https://github.com/zachreid-96/digitial_log_book/releases"))
        readme_button = ttk.Button(self.help_menu_frame, text="README/Setup", command=lambda: self.open_link("https://github.com/zachreid-96/digitial_log_book"))
        issues_button = ttk.Button(self.help_menu_frame, text="Report Issue", command=lambda: self.open_link("https://github.com/zachreid-96/digitial_log_book/issues"))
        repo_button.pack(pady=5, fill=tk.X, padx=10)
        readme_button.pack(pady=5, fill=tk.X, padx=10)
        issues_button.pack(pady=5, fill=tk.X, padx=10)

        return

    def open_link(self, link):
        webbrowser.open(link)

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

    def save_directories(self):
        data = {
            "unsorted_dir": str(Path(self.unsorted_directory.get())),
            "runlog_dir": str(Path(self.log_directory.get())),
            "manual_sort_dir": str(Path(self.manual_sort_directory.get())),
            "logbook_dir": str(Path(self.logbook_directory.get())),
            "inventory_dir": str(Path(self.inventory_page_directory.get())),
        }
        with open("config.json", "w") as file:
            json.dump(data, file, indent=4)

    def select_directory(self, option):
        directory = filedialog.askdirectory()
        if directory:
            if option == "unsorted":
                self.unsorted_directory.delete(0, tk.END)
                self.unsorted_directory.insert(0, str(Path(directory)))
            elif option == "log":
                self.log_directory.delete(0, tk.END)
                self.log_directory.insert(0, str(Path(directory)))
            elif option == "manual_sort":
                self.manual_sort_directory.delete(0, tk.END)
                self.manual_sort_directory.insert(0, str(Path(directory)))
            elif option == "logbook":
                self.logbook_directory.delete(0, tk.END)
                self.logbook_directory.insert(0, str(Path(directory)))
            elif option == "inventory_page":
                self.inventory_page_directory.delete(0, tk.END)
                self.inventory_page_directory.insert(0, str(Path(directory)))
            else:
                pass

    def run_process_files(self, path):

        self.manager.create_logger()

        files = populate_files(path)
        self.discovery_var.set(f"Discovered {len(files)} Files.")
        self.progress.set("Running... Processing")
        processed = 0

        if files:
            for file in files:
                processed += 1
                self.process_var.set(f"Processing Files... {processed}/{len(files)}")
                data = ocr_file(file)
                manufacturer_wrapper(file, data)

        self.progress.set("Running... DONE")
        self.manager.logger.info("Done processing all copied files in 'Unsorted'...\n")

    def verify_directories(self):
        message = ""
        if not os.path.exists(self.manager.get_unsorted_dir()):
            message += "Please ensure Unsorted path is correct\n"
        if not os.path.exists(self.manager.get_runlog_dir()):
            message += "Please ensure Runtime Log path is correct\n"
        if not os.path.exists(self.manager.get_manual_sort_dir()):
            message += "Please ensure Manual Sort path is correct\n"
        if not os.path.exists(self.manager.get_logbook_dir()):
            message += "Please ensure Logbook path is correct\n"
        if not os.path.exists(self.manager.get_inventory_dir()):
            message += "Please ensure Inventory Page path is correct\n"

        if message != "":
            messagebox.showwarning(message)
            return

        self.verify_button.config(state="disabled")
        self.start_button.config(state="normal")

        self.verified_var.set("Verified... Success")


if __name__ == '__main__':

    root = tk.Tk()
    app = Log_Book_GUI(root)
    root.mainloop()
