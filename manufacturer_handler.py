import re
from datetime import datetime
from pdfminer.high_level import extract_text
from file_manager import file_manager_wrapper
from rapidfuzz import fuzz

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


def fuzzy_subset(subset, data, threshold=80):
    match_count = 0
    for item in subset:
        for data_item in data:
            if fuzz.ratio(item.lower(), data_item.lower()) >= threshold:
                match_count += 1
                break
    return match_count >= (len(subset) // 2)


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
    hp_subset = {"HP", "USAGE", "PAGE", "TOTALS"}
    canon_subset = {"CR", "SN", "CCD", "DID"}

    match_threshhold = 80

    data = data.split()

    if data is None:
        file_manager_wrapper(file, None, None, None)

    if fuzzy_subset(inventory_subset, data, match_threshhold):
        parse_inventory(file, data)
    elif fuzzy_subset(kyocera_subset, data, match_threshhold):
        parse_kyocera(file, data)
    elif fuzzy_subset(hp_subset, data, match_threshhold):
        parse_hp(file, data)
    elif fuzzy_subset(canon_subset, data, match_threshhold):
        parse_canon(file, data)
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

    excluded_chars = "-_[].,;:()#/?<>|\\\'\"“"
    excluded_phrase = ("dpi", "dpl", "dp1")

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


def parse_canon(file, data):
    date = None
    serial_number = None
    has_seen_sn_tag = False

    for entry in data:
        temp = entry.strip()
        if temp == "SN":
            has_seen_sn_tag = True
        if (serial_number is None and any(char.isdigit() for char in temp)
                and any(char.isalpha() for char in temp) and len(temp) == 8 and has_seen_sn_tag):
            serial_number = temp
        elif '/' in temp:
            try:
                date = datetime.strptime(temp[:10], '%m/%d/%Y')
            except ValueError:
                continue

    file_manager_wrapper(file, serial_number, date, 'Canon')
