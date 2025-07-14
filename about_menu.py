import webbrowser

import customtkinter as ct

from config import DirectoryManager

class AboutMenu(ct.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.manager = DirectoryManager()

        self.kyocera_scanning_label = ct.CTkLabel(self, text="Scanning Reports on Kyocera",
                                              font=ct.CTkFont(size=15, weight="bold"))
        self.kyocera_scanning_label.grid(row=0, column=0, padx=20, pady=(20, 5), columnspan=4, sticky='news')

        self.kyocera_scanning_resolution = ct.CTkLabel(self, text="Scan Resolution > 300x300 DPI")
        self.kyocera_scanning_resolution.grid(row=1, column=0, padx=40, pady=0, columnspan=4, sticky='nws')
        self.kyocera_scanning_image_type = ct.CTkLabel(self, text="Image Type > Text")
        self.kyocera_scanning_image_type.grid(row=2, column=0, padx=40, pady=0, columnspan=4, sticky='nws')
        self.kyocera_scanning_file_type = ct.CTkLabel(self, text="File Type > PDF Compression 4 or 5")
        self.kyocera_scanning_file_type.grid(row=3, column=0, padx=40, pady=0, columnspan=4, sticky='nws')

        self.canon_scanning_label = ct.CTkLabel(self, text="Scanning Reports on Canon",
                                                  font=ct.CTkFont(size=15, weight="bold"))
        self.canon_scanning_label.grid(row=4, column=0, padx=20, pady=(20, 5), columnspan=4, sticky='news')

        self.canon_scanning_resolution = ct.CTkLabel(self, text="Scan Resolution > 300x300 DPI")
        self.canon_scanning_resolution.grid(row=5, column=0, padx=40, pady=0, columnspan=4, sticky='nws')
        self.canon_scanning_image_type = ct.CTkLabel(self, text="Image Type > Text")
        self.canon_scanning_image_type.grid(row=6, column=0, padx=40, pady=0, columnspan=4, sticky='nws')
        self.canon_scanning_file_type = ct.CTkLabel(self, text="File Type > PDF Uncompressed")
        self.canon_scanning_file_type.grid(row=7, column=0, padx=40, pady=0, columnspan=4, sticky='nws')

        self.how_to_use_label = ct.CTkLabel(self, text="How to Use Program",
                                            font=ct.CTkFont(size=15, weight='bold'))

        self.usage_load_files = ct.CTkLabel(self, text="Load Scanned Documents into 'Ready to Sort' folder.")
        self.usage_load_files.grid(row=5, column=0, padx=40, pady=0, columnspan=4, sticky='nws')
        self.usage_load_files_1 = ct.CTkLabel(self, text="In 'Process' Menu, hit 'Start'.")
        self.usage_load_files_1.grid(row=5, column=0, padx=40, pady=0, columnspan=4, sticky='nws')
        self.usage_review_files = ct.CTkLabel(self, text="Image Type > Text")
        self.usage_review_files.grid(row=6, column=0, padx=40, pady=0, columnspan=4, sticky='nws')
        self.usage_run_reports = ct.CTkLabel(self, text="File Type > PDF Uncompressed")
        self.usage_run_reports.grid(row=7, column=0, padx=40, pady=0, columnspan=4, sticky='nws')
