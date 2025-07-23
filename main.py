import os
import ctypes

import customtkinter as ct

from gc import collect
from help_menu import HelpMenu
from about_menu import AboutMenu
from config import DirectoryManager
from process_menu import ProcessMenu
from reports_menu import ReportsMenu
from settings_menu import SettingsMenu
from directory_menu import DirectoryMenu
from inventory_menu import InventoryMenu
from manual_review_menu import PDFViewer

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception as e:
    #print(e)
    pass

def get_window_scaling():
    try:
        hdc = ctypes.windll.user32.GetDC(0)
        dpi_x = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)
        ctypes.windll.user32.ReleaseDC(0, hdc)
        return dpi_x / 96
    except Exception as e:
        #print(e)
        return 1

class Log_Book_GUI(ct.CTk):
    def __init__(self):
        super().__init__()

        self.manager = DirectoryManager()

        if not self.manager.is_setup():
            self.setup_project()

        self.title("Digital Log Book")
        self.geometry(f"{1000}x{500}")
        self.minsize(1000, 500)
        self.maxsize(1000, 500)

        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar_frame = ct.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10, weight=1)

        self.separator = ct.CTkFrame(self, fg_color="black", width=5)
        self.separator.grid(row=0, column=1, rowspan=4, sticky="ns")

        self.user_menu_frame = ct.CTkFrame(self, corner_radius=0)
        self.user_menu_frame.grid(row=0, column=2, rowspan=4, sticky="nsew")
        #self.user_menu_frame.grid_rowconfigure(1, weight=1)

        self.logo_label = ct.CTkLabel(self.sidebar_frame, text="Menu",
                                      font=ct.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.Process_button = ct.CTkButton(self.sidebar_frame, text="Process",
                                           command=self.show_process_menu)
        self.Process_button.grid(row=1, column=0, padx=20, pady=10)

        self.Reports_button = ct.CTkButton(self.sidebar_frame, text="Reports",
                                            command=self.show_reports_menu)
        self.Reports_button.grid(row=2, column=0, padx=20, pady=10)

        self.Manual_button = ct.CTkButton(self.sidebar_frame, text="Manual Review",
                                          command=self.show_manual_menu)
        self.Manual_button.grid(row=3, column=0, padx=20, pady=10)

        self.Directories_button = ct.CTkButton(self.sidebar_frame, text="Directories",
                                               command=self.show_directories_menu)
        self.Directories_button.grid(row=4, column=0, padx=20, pady=10)

        self.Inventory_button = ct.CTkButton(self.sidebar_frame, text="Inventory",
                                             command=self.show_inventory_menu)
        self.Inventory_button.grid(row=5, column=0, padx=20, pady=10)

        self.Settings_button = ct.CTkButton(self.sidebar_frame, text="Settings",
                                            command=self.show_settings_menu)
        self.Settings_button.grid(row=6, column=0, padx=20, pady=10)

        self.Help_button = ct.CTkButton(self.sidebar_frame, text="Help",
                                        command=self.show_help_menu)
        self.Help_button.grid(row=7, column=0, padx=20, pady=10)

        self.About_button = ct.CTkButton(self.sidebar_frame, text="About",
                                         command=self.show_about_menu)
        self.About_button.grid(row=8, column=0, padx=20, pady=10)

        self.tool_tips_button = ct.CTkButton(self.sidebar_frame, text="?",
                                         command=self.toggle_menu_tips, width=25)
        self.tool_tips_button.grid(row=9, column=0, padx=(20, 0), pady=10, sticky='w')

        self.tool_tips_text = ct.CTkLabel(self.sidebar_frame, text="<<<   Menu Tips", width=75)
        self.tool_tips_text.grid(row=9, column=0, padx=(55, 0), pady=10, sticky='w')

        self.current_view = None

        self._switch_view(ProcessMenu)

    def toggle_menu_tips(self):

        #print("fg_color", self.tool_tips_button.cget('fg_color'))
        #print("hover_color", self.tool_tips_button.cget('hover_color'))

        self.manager.menu_tips = not self.manager.menu_tips
        self.manager.write_settings()
        try:
            self.current_view.update_fields()
        except AttributeError:
            pass

    # Switches Frame to the selected one
    def _switch_view(self, view_class):

        if self.manager.is_running():
            return

        menus = {
            "ProcessMenu": self.Process_button,
            "ReportsMenu": self.Reports_button,
            "PDFViewer": self.Manual_button,
            "DirectoryMenu": self.Directories_button,
            "InventoryMenu": self.Inventory_button,
            "SettingsMenu": self.Settings_button,
            "HelpMenu": self.Help_button,
            "AboutMenu": self.About_button
        }

        for menu in menus.values():
            #print(menu)
            menu.configure(fg_color=['#3B8ED0', '#1F6AA5'])

        if self.current_view:
            if 'directory' in str(self.current_view):
                self.current_view.save_directories_locations()
            self.current_view.destroy()
            collect()

        menu = menus.get(view_class.__name__, None)
        if menu is not None:
            menu.configure(fg_color=['#36719F', '#144870'])

        self.current_view = view_class(self.user_menu_frame)
        self.current_view.pack(fill="both", expand=True)

    def show_process_menu(self):
        self._switch_view(ProcessMenu)

    def show_reports_menu(self):
        self._switch_view(ReportsMenu)

    def show_manual_menu(self):
        self._switch_view(PDFViewer)

    def show_directories_menu(self):
        self._switch_view(DirectoryMenu)

    def show_inventory_menu(self):
        self._switch_view(InventoryMenu)

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

        json_dict = {
            'unsorted_dir': ready_sort,
            'runlog_dir': runtime_logs,
            'manual_sort_dir': manual_sort,
            'logbook_dir': used_parts,
            'inventory_dir': inventory_pages,
            'reports_dir': reports,
            'multi_cores': 0,
            'restock_days': 3,
            'last_inventory': None,
            'appearance': 'System'
        }

        self.manager.write_config_file(json_dict)


if __name__ == "__main__":
    app = Log_Book_GUI()
    app.mainloop()
