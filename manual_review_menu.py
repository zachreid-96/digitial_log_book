import os
import fitz
import json

import customtkinter as ct

from PIL import Image
from config import DirectoryManager
from file_manager import move_file_manual_sort
from database_handler import database_add_files

class PDFViewer(ct.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.bind("<Button-1>", self.remove_focus)
        self.entries = []

        self.manager = DirectoryManager()

        self.pages = self.read_pages()
        self.current_page = 0
        self.tk_image = None

        self.zoom_factor = 1.75

        self.viewer_frame = ct.CTkScrollableFrame(self, corner_radius=0)
        self.viewer_frame.grid(row=1, column=0, columnspan=8, rowspan=9, sticky='news')

        self.image_label = ct.CTkLabel(self.viewer_frame, text="")
        self.image_label.grid(row=1, column=0, columnspan=9, rowspan=9, sticky='news')

        self.brand_entry = ct.CTkEntry(self, placeholder_text="Brand")
        self.brand_entry.grid(row=0, column=0, columnspan=2, padx=10)
        self.entries.append(self.brand_entry)

        self.serial_num_entry = ct.CTkEntry(self, placeholder_text="Serial Number")
        self.serial_num_entry.grid(row=0, column=2, columnspan=2, padx=10)
        self.entries.append(self.serial_num_entry)

        self.date_entry = ct.CTkEntry(self, placeholder_text="Date")
        self.date_entry.grid(row=0, column=4, columnspan=2, padx=10)
        self.entries.append(self.date_entry)

        self.delete_checkbox = ct.CTkCheckBox(self, text="Delete File")
        self.delete_checkbox.grid(row=0, column=6, columnspan=2, padx=10)

        self.previous_button = ct.CTkButton(self, text="<", command=self.previous_log, width=50)
        self.previous_button.grid(row=0, column=8, columnspan=1, padx=10, pady=10)

        self.next_button = ct.CTkButton(self, text=">", command=self.next_log, width=50)
        self.next_button.grid(row=0, column=9, columnspan=1, padx=10, pady=10)

        self.part_entry = ct.CTkEntry(self, placeholder_text="Part Number", width=100)
        self.part_entry.grid(row=1, column=8, padx=5, pady=5)
        self.entries.append(self.part_entry)

        self.quantity_entry = ct.CTkEntry(self, placeholder_text="QTY", width=50)
        self.quantity_entry.grid(row=1, column=9, padx=5, pady=5)
        self.entries.append(self.quantity_entry)

        self.add_part_button = ct.CTkButton(self, text="Add Part", command=self.add_part)
        self.add_part_button.grid(row=2, column=8, columnspan=2, padx=5)

        self.parts_list = ct.CTkTextbox(self, width=150)
        self.parts_list.grid(row=3, column=8, columnspan=2, padx=5, pady=5, rowspan=6)
        self.parts_list.configure(state="disabled")
        self.part_line = 0

        self.submit_button = ct.CTkButton(self, text="Submit Logs", command=self.submit_logs)
        self.submit_button.grid(row=9, column=8, columnspan=2, padx=5, pady=5)

        self.display_page()

    def add_part(self):

        if self.part_entry.get() and self.quantity_entry.get():
            self.parts_list.configure(state="normal")
            self.parts_list.insert(f'{self.part_line}.0',
                                   f'{self.part_entry.get()} x {self.quantity_entry.get()}\n')
            self.parts_list.configure(state="disabled")
            self.part_line += 1

            self.part_entry.delete(0, 'end')
            self.quantity_entry.delete(0, 'end')
            self.part_entry.configure(placeholder_text="Part Number")
            self.quantity_entry.configure(placeholder_text="QTY")

    def read_pages(self):

        pages_json = self.manager.get_manual_json()
        try:
            with open(pages_json) as f:
                data = json.load(f)
        except json.decoder.JSONDecodeError:
            return []

        return data

    def display_page(self):

        self.master.update_idletasks()
        frame_width = self.master.winfo_width() - 200
        frame_height = self.master.winfo_height() - 50

        self.serial_num_entry.delete(0, 25)
        self.date_entry.delete(0, 25)
        self.delete_checkbox.deselect()

        self.part_entry.delete(0, 25)
        self.quantity_entry.delete(0, 3)

        self.parts_list.configure(state='normal')
        self.parts_list.delete('0.0', 'end')
        self.parts_list.configure(state='disabled')

        self.viewer_frame.configure(width=frame_width, height=frame_height)

        if len(self.pages) == 0:
            self.image_label.configure(text="No PDF's need reviewing!")

        else:

            dpi = int(300 * self.zoom_factor)
            page = fitz.open(self.pages[self.current_page]['file'])[0]

            page_size = page.rect
            page_width = page_size.width
            page_height = page_size.height

            zoom_x = (frame_width / page_width * self.zoom_factor)
            zoom_y = (frame_height / page_height * self.zoom_factor)
            zoom = min(zoom_x, zoom_y)
            zoom_matrix = fitz.Matrix(zoom, zoom)
            
            #print(page_width, page_height)
            #print(frame_width, frame_height)

            pix = page.get_pixmap(matrix=zoom_matrix)
            image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            #image.thumbnail(((frame_width-340),(frame_height-50)))
            #self.image_label.configure(width=(page_width-200), height=(page_height-50))
            #image = ImageOps.contain(image, (1000, 900))

            extracted_brand = self.pages[self.current_page]['brand']
            extracted_serial = self.pages[self.current_page]['serial_num']
            extracted_date = self.pages[self.current_page]['date']
            extracted_parts = self.pages[self.current_page].get('parts', '')

            if extracted_serial:
                self.brand_entry.insert(0, extracted_brand)
            else:
                self.brand_entry.configure(placeholder_text='Brand')

            if extracted_serial:
                self.serial_num_entry.insert(0, extracted_serial)
            else:
                self.serial_num_entry.configure(placeholder_text='Serial Number')

            if extracted_date:
                self.date_entry.insert(0, extracted_date)
            else:
                self.date_entry.configure(placeholder_text='Date')

            if extracted_parts:
                self.parts_list.configure(state='normal')
                self.parts_list.insert('0.0', f"{'\n'.join(extracted_parts)}\n")
                self.parts_list.configure(state='disabled')
                self.part_line = len(extracted_parts) + 1

            #print(self.pages[index]['serial_num'], self.pages[index]['date'])
            self.part_entry.configure(placeholder_text="Part Number")
            self.quantity_entry.configure(placeholder_text="QTY")

            self.tk_image = ct.CTkImage(light_image=image, size=image.size)
            self.image_label.configure(image=self.tk_image)

            self.image_label.image = self.tk_image

    def previous_log(self):

        self.data_capture_edits()
        self.part_line = 0

        if self.current_page > 0:
            self.current_page -= 1
            self.display_page()

    def next_log(self):

        self.data_capture_edits()
        self.part_line = 0

        if self.current_page < (len(self.pages) - 1):
            self.current_page += 1
            self.display_page()

    def data_capture_edits(self):

        filtered_parts = [
            part_qty for part_qty in self.parts_list.get('0.0', 'end').split('\n')
            if part_qty != ''
        ]

        self.pages[self.current_page]['serial_num'] = self.serial_num_entry.get()
        self.pages[self.current_page]['date'] = self.date_entry.get()
        self.pages[self.current_page]['parts'] = filtered_parts
        self.pages[self.current_page]['deletion'] = True if self.delete_checkbox.get() == 1 else False


    def submit_logs(self):

        self.data_capture_edits()
        removable_pages = []

        for file in self.pages:
            if any(item for item in
                   [file['serial_num'], file['date'], file['brand'], file['parts']]
                   ) is not None:
                move_file_manual_sort(file)
            break

        for file in self.pages:
            if file.get('new_file', None) is not None and file['brand'] != 'Inventory':
                database_add_files(file['new_file'], file['parts'])

            if file.get('new_file', None) is not None:
                removable_pages.append(file)
            if file.get('deletion', False) is True:
                removable_pages.append(file)
                os.remove(file)

        still_needs_review = [file for file in self.pages
                              if file not in removable_pages]

        pages_json = self.manager.get_manual_json()

        with open(pages_json, 'w') as local_manual_json:
            data = json.load(local_manual_json)
            data.append(entry for entry in list(still_needs_review))
            json.dump(list(data), local_manual_json, indent=4)

    def remove_focus(self, event):
        for entry in self.entries:
            if not entry.winfo_containing(event.x_root, event.y_root) == entry:
                self.focus()

