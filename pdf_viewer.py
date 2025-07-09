import fitz
import json

import customtkinter as ct

from PIL import Image
from config import DirectoryManager

class PDFViewer(ct.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.manager = DirectoryManager()

        self.pages = self.read_pages()
        self.current_page = 0
        self.tk_image = None

        self.zoom_factor = 1.75

        self.viewer_frame = ct.CTkScrollableFrame(self, corner_radius=0)
        self.viewer_frame.grid(row=1, column=0, columnspan=10, rowspan=11)

        self.image_label = ct.CTkLabel(self.viewer_frame, text="")
        self.image_label.grid(row=1, column=0, columnspan=10, rowspan=11)

        self.serial_num_entry = ct.CTkEntry(self, placeholder_text="Serial Number")
        self.serial_num_entry.grid(row=0, column=0, columnspan=2, padx=20)

        self.date_entry = ct.CTkEntry(self, placeholder_text="Date")
        self.date_entry.grid(row=0, column=2, columnspan=2, padx=20)

        self.delete_checkbox = ct.CTkCheckBox(self, text="Delete File")
        self.delete_checkbox.grid(row=0, column=4, columnspan=2, padx=20)

        self.previous_button = ct.CTkButton(self, text="<", command=self.previous_log, width=50)
        self.previous_button.grid(row=0, column=6, columnspan=1, padx=20, pady=10)

        self.next_button = ct.CTkButton(self, text=">", command=self.next_log, width=50)
        self.next_button.grid(row=0, column=7, columnspan=1, padx=10, pady=10)

        self.part_entry_1 = ct.CTkEntry(self, placeholder_text="Part Number", width=100)
        self.part_entry_1.grid(row=2, column=11)
        self.quantity_entry_1 = ct.CTkEntry(self, placeholder_text="QTY", width=50)
        self.quantity_entry_1.grid(row=2, column=12)

        self.part_entry_2 = ct.CTkEntry(self, placeholder_text="Part Number", width=100)
        self.part_entry_2.grid(row=3, column=11)
        self.quantity_entry_2 = ct.CTkEntry(self, placeholder_text="QTY", width=50)
        self.quantity_entry_2.grid(row=3, column=12)

        self.part_entry_3 = ct.CTkEntry(self, placeholder_text="Part Number", width=100)
        self.part_entry_3.grid(row=4, column=11)
        self.quantity_entry_3 = ct.CTkEntry(self, placeholder_text="QTY", width=50)
        self.quantity_entry_3.grid(row=4, column=12)

        self.part_entry_4 = ct.CTkEntry(self, placeholder_text="Part Number", width=100)
        self.part_entry_4.grid(row=5, column=11)
        self.quantity_entry_4 = ct.CTkEntry(self, placeholder_text="QTY", width=50)
        self.quantity_entry_4.grid(row=5, column=12)

        self.part_entry_5 = ct.CTkEntry(self, placeholder_text="Part Number", width=100)
        self.part_entry_5.grid(row=6, column=11)
        self.quantity_entry_5 = ct.CTkEntry(self, placeholder_text="QTY", width=50)
        self.quantity_entry_5.grid(row=6, column=12)

        self.part_entry_6 = ct.CTkEntry(self, placeholder_text="Part Number", width=100)
        self.part_entry_6.grid(row=7, column=11)
        self.quantity_entry_6 = ct.CTkEntry(self, placeholder_text="QTY", width=50)
        self.quantity_entry_6.grid(row=7, column=12)

        self.part_entry_7 = ct.CTkEntry(self, placeholder_text="Part Number", width=100)
        self.part_entry_7.grid(row=8, column=11)
        self.quantity_entry_7 = ct.CTkEntry(self, placeholder_text="QTY", width=50)
        self.quantity_entry_7.grid(row=8, column=12)

        self.part_entry_8 = ct.CTkEntry(self, placeholder_text="Part Number", width=100)
        self.part_entry_8.grid(row=9, column=11)
        self.quantity_entry_8 = ct.CTkEntry(self, placeholder_text="QTY", width=50)
        self.quantity_entry_8.grid(row=9, column=12)

        self.part_entry_9 = ct.CTkEntry(self, placeholder_text="Part Number", width=100)
        self.part_entry_9.grid(row=10, column=11)
        self.quantity_entry_9 = ct.CTkEntry(self, placeholder_text="QTY", width=50)
        self.quantity_entry_9.grid(row=10, column=12)

        self.parts = [
            (self.part_entry_1, self.quantity_entry_1),
            (self.part_entry_2, self.quantity_entry_2),
            (self.part_entry_3, self.quantity_entry_3),
            (self.part_entry_4, self.quantity_entry_4),
            (self.part_entry_5, self.quantity_entry_5),
            (self.part_entry_6, self.quantity_entry_6),
            (self.part_entry_7, self.quantity_entry_7),
            (self.part_entry_8, self.quantity_entry_8),
            (self.part_entry_9, self.quantity_entry_9)
        ]

        self.next_button = ct.CTkButton(self, text="Submit Logs", command=self.submit_logs, width=100)
        self.next_button.grid(row=0, column=11, columnspan=2, padx=10, pady=10)

        self.display_page()

    def read_pages(self):

        pages_json = self.manager.get_manual_json()

        with open(pages_json) as f:
            data = json.load(f)

        return data

    def display_page(self):

        self.master.update_idletasks()
        frame_width = self.master.winfo_width()
        frame_height = self.master.winfo_height()

        self.serial_num_entry.delete(0, 15)
        self.date_entry.delete(0, 15)
        self.delete_checkbox.deselect()

        for part, qty in self.parts:
            part.delete(0, 25)
            part.configure(placeholder_text="Part Number")

            qty.delete(0, 25)
            qty.configure(placeholder_text="QTY")

        self.viewer_frame.configure(width=(frame_width-200), height=(frame_height-50))

        dpi = int(300 * self.zoom_factor)
        page = fitz.open(self.pages[self.current_page]['file'])[0]

        page_size = page.rect
        page_width = page_size.width
        page_height = page_size.height

        zoom_x = (frame_width / page_width * self.zoom_factor)
        zoom_y = (frame_height / page_height * self.zoom_factor)
        zoom = min(zoom_x, zoom_y)
        zoom_matrix = fitz.Matrix(zoom, zoom)

        pix = page.get_pixmap(matrix=zoom_matrix)
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        #image.thumbnail((1000,900))
        #image = ImageOps.contain(image, (1000, 900))

        extracted_serial = self.pages[self.current_page]['serial_num']
        extracted_date = self.pages[self.current_page]['date']
        extracted_parts = self.pages[self.current_page].get('parts', '')

        if extracted_serial:
            self.serial_num_entry.insert(0, extracted_serial)
        else:
            self.serial_num_entry.configure(placeholder_text='Serial Number')

        if extracted_date:
            self.date_entry.insert(0, extracted_date)
        else:
            self.date_entry.configure(placeholder_text='Date')

        if extracted_parts:
            for part_used, entry in zip(extracted_parts, self.parts):
                part_entry, qty_entry = entry
                part = part_used.split('x')[0]
                qty = part_used.split('x')[1]
                part_entry.insert(0, part)
                qty_entry.insert(0, qty)

        #print(self.pages[index]['serial_num'], self.pages[index]['date'])

        self.tk_image = ct.CTkImage(light_image=image, size=image.size)
        self.image_label.configure(image=self.tk_image)

        self.image_label.image = self.tk_image

    def previous_log(self):

        self.data_capture_edits()

        if self.current_page > 0:
            self.current_page -= 1
            self.display_page()

    def next_log(self):

        self.data_capture_edits()

        if self.current_page < (len(self.pages) - 1):
            self.current_page += 1
            self.display_page()

    def data_capture_edits(self):

        self.pages[self.current_page]['serial_num'] = self.serial_num_entry.get()
        self.pages[self.current_page]['date'] = self.date_entry.get()
        self.pages[self.current_page]['parts'] = [
            f'{part.get()}x{qty.get()}' for part, qty in self.parts
            if f'{part.get()}x{qty.get()}' != 'x'
        ]
        self.pages[self.current_page]['deletion'] = True if self.delete_checkbox.get() == 1 else False

        #print(self.pages[self.current_page])

    def submit_logs(self):
        pass

