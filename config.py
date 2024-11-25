import logging
from win32api import GetVolumeInformation, GetLogicalDriveStrings
from datetime import datetime

"""
Description: 
    Creates a logger instance for the run duration
    will used a specified log output path to store the log file once completed
"""
def setup_logger():
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
    Utilizes win32api to get drive letters based on drive names
    used in this project due to project running on work computer and all files on external drive
Args:
    drive_name: name of the target drive that houses all the files
Returns:
    drive_letter: for example D:\\
"""
def find_drive_letter(drive_name):
    drive_letter = None
    for drive in GetLogicalDriveStrings().split('\000')[:-1]:
        try:
            if GetVolumeInformation(drive)[0] == drive_name:
                drive_letter = drive
                break
        except Exception as e:
            continue
    return drive_letter

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

manuals_drive = find_drive_letter("Manuals")

if manuals_drive is None:
    ## raise ValueError("External Drive 'Manuals' is not found...")
    print("Please ensure External Drive 'Manuals' is installed...")
    input("Exiting under DRIVE_NOT_FOUND. Press any key to exit...")
    exit()

unsorted_path = rf"{manuals_drive}\Digital Log Book\Unsorted"
log_path = rf"{manuals_drive}\Digital Log Book\runLogs"
manual_sort_path = rf"{manuals_drive}\Digital Log Book\Manual_Sort"
logbook_path = rf"{manuals_drive}\Digital Log Book\Logs"
# inventory_page_path = rf"{manuals_drive}\Digital Log Book\Inventory_Pages"
inventory_page_path = rf"{manuals_drive}\Digital Log Book"
temp_path = rf"C:\Users\********\DLB_testing\temp"

logger = setup_logger()
