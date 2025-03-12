import os
import re
from datetime import datetime
from pdfminer.high_level import extract_text
from file_manager import file_manager_wrapper

"""
Description: 
    extracts data from the passed file and splits it by " "
Args:
    file: passed from anywhere where file data is needed
Returns:
    returns string array of data
"""


def get_data(file):
    try:
        data_raw = extract_text(file).upper()
        data = data_raw.split(" ")
    except Exception as e:
        data = None
    return data


"""
Description: 
    a wrapper function for the currently programmed manufacturers
    Currently handles Kyocera pages, HP pages, and Inventory Re-Stock pages
Args:
    file: passed file that is ready to be processed and renamed
"""


def manufacturer_wrapper(file, data):
    inventory_subset = {"SERVICE", "INVENTORY", "PICKING", "LIST"}
    kyocera_subset = {"KYOCERA", "STATUS", "PAGE"}
    hp_subset_1 = {"HP", "USAGE", "PAGE"}
    hp_subset_2 = {"HP", "USAGE", "TOTALS"}

    #data = get_data(file)
    data = " ".join(data).split(" ")

    if data is None:
        file_manager_wrapper(file, None, None, None)

    if inventory_subset.issubset(data):
        parse_inventory(file, data)
    elif kyocera_subset.issubset(data):
        parse_kyocera(file, data)
    elif hp_subset_1.issubset(data) or hp_subset_2.issubset(data):
        parse_hp(file, data)
    else:
        file_manager_wrapper(file, None, None, None)


"""
Description: 
    called from manufacturer_wrapper for every inventory restock page found
    finds date in file and checks if it is a valid date
    then calls file_manager_wrapper to rename and move the file to destination
Args:
    file: inventory restock page
    data: data from file (saves an additional I/O operation to read data)
"""


def parse_inventory(file, data):
    date = None

    # data_raw = extract_text(file)
    # data = data_raw.split(" ")

    for entry in data:
        if date is not None:
            break
        elif 8 <= len(entry.strip()) <= 10 and date is None:
            try:
                date = datetime.strptime(entry.strip(), '%m/%d/%Y')
            except ValueError:
                continue

    file_manager_wrapper(file, None, date, "Inventory_Pages")


"""
Description: 
    called from manufacturer_wrapper for every kyocera page found
    finds date in file and checks if it is a valid date
    finds serial number and checks if it matches a specific set of requirements
    then calls file_manager_wrapper to rename and move the file to destination
Args:
    file: inventory restock page
    data: data from file (saves an additional I/O operation to read data)
"""


def parse_kyocera(file, data):
    date = None
    serial_number = None

    excluded_chars = "-_[].;:()"
    excluded_phrase = ("dpi", "dpl", "dp1")

    # data = get_data(file)

    for entry in data:
        temp = entry.strip()
        if (any(char.isdigit() for char in temp)
                and any(char.isalpha() for char in temp)
                and not any(char in excluded_chars for char in temp)
                and len(temp) == 10 and not temp.endswith(excluded_phrase)):
            if not temp[:3].isnumeric() and serial_number is None:
                serial_number = temp
        elif len(temp) == 10 and date is None:
            try:
                date = datetime.strptime(temp, '%m/%d/%Y')
            except ValueError:
                continue

    file_manager_wrapper(file, serial_number, date, 'Kyocera')


"""
Description: 
    called from manufacturer_wrapper for every hp page found
    finds date in file and checks if it is a valid date
    finds serial number based on specific regex pattern
    then calls file_manager_wrapper to rename and move the file to destination
Args:
    file: inventory restock page
    data: data from file (saves an additional I/O operation to read data)
"""


def parse_hp(file, data):
    date = None
    serial_number = None
    serial_number_pattern = re.compile(r'\b[a-z0-9]{10}\b', re.IGNORECASE)

    # data = get_data(file)

    for entry in data:
        temp = entry.strip()
        if len(temp) == 10 and serial_number is None:
            serial_number = serial_number_pattern.search(temp)
        if len(temp) == 10 and date is None:
            try:
                date = datetime.strptime(temp, '%m/%d/%Y')
            except ValueError:
                continue

    file_manager_wrapper(file, serial_number, date, 'HP')
