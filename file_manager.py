import glob
import os
import shutil
from config import convert_month_str, DirectoryManager

"""
Description: 
    wrapper for file move and rename processes
    checks if data and serial number are valid
    if valid
        calls move_file_success 
    if not valid
        calls move_file_warning
Args:
    file: file to be moved
    serial_number: None if not found || Valid serial number
    date: None if not found || Valid date
    brand: 'Inventory_Pages', 'Kyocera', 'HP', only ones implemented so far
"""


def file_manager_wrapper(file, serial_number, date, brand):
    path_manager = DirectoryManager()
    logbook_path = path_manager.get_logbook_dir()
    inventory_page_path = path_manager.get_inventory_dir()

    if serial_number is not None and date is not None:
        destination_folder = rf"{logbook_path}\{brand}\{date.year}\{convert_month_str(date.month)}"
        os.makedirs(destination_folder, exist_ok=True)

        new_filename = f"{date.month}-{date.day}-{date.year}_{serial_number}"
        move_file_success(file, new_filename, destination_folder)

    elif serial_number is None and brand == "Inventory_Pages" and date is not None:
        destination_folder = rf"{inventory_page_path}\{date.year}\{convert_month_str(date.month)}"
        os.makedirs(destination_folder, exist_ok=True)

        new_filename = f"{date.month}-{date.day}-{date.year}_Inventory"
        move_file_success(file, new_filename, destination_folder)

    elif date is None or serial_number is None:

        move_file_warning(file)


"""
Description: 
    transfers all files to the 'temp_path'
Args:
    files: list of files that need moved
"""


def transfer_files_to_temp(files):
    path_manager = DirectoryManager()
    temp_path = path_manager.get_temp_dir()

    for file in files:
        filename = file.split("\\")[-1]
        shutil.copy(file, f"{temp_path}\\{filename}")


"""
Description: 
    gets all files within the given folder that is passed
Args:
    path: path of folder that houses files that need processed
Returns:
    list of files
"""


def populate_files(path):
    files = []
    for file in glob.glob(f"{path}\\*.pdf"):
        files.append(file)

    return files


"""
Description: 
    moves and renames a file into a specific destination
    multiple is set to DEFAULT value
    will check if file_name already exists and renames to file_name_x (x=1,2,3,etc) and rechecks
    logs operation of move to destination and deletion of file in 'temp_path' and 'unsorted_path'
    if operation fails, calls move_file_warning
Args:
    source: original file location
    filename: strict name of file so some_pdf.pdf would be passed as some_pdf
    destination: intended location for file
    extension: defaulted to .pdf but can be changed if something else is passed
    multiple: defaulted to True, not recommended to be changed    
"""


def move_file_success(source, filename, destination, extension='pdf', multiple=True):
    path_manager = DirectoryManager()
    unsorted_path = path_manager.get_unsorted_dir()
    temp_path = path_manager.get_temp_dir()
    logger = path_manager.get_logger()

    try:
        if multiple:
            if not os.path.exists(os.path.join(destination, f"{filename}.{extension}")):
                shutil.move(source, os.path.join(destination, f"{filename}.{extension}"))

                message = f"""RENAMED {source.split("\\")[-1]} to {filename}.{extension}
                        \t MOVED {filename}.{extension} to {destination}
                        \t DELETED {source.split("\\")[-1]} in {temp_path}
                        \t DELETED {source.split("\\")[-1]} in {unsorted_path}"""

                logger.info(message)
            else:
                count = 1
                while True:
                    if not os.path.exists(os.path.join(destination, f"{filename}_{count}.{extension}")):
                        shutil.move(source, os.path.join(destination, f"{filename}_{count}.{extension}"))

                        message = f"""RENAMED {source.split("\\")[-1]} to {filename}_{count}.{extension}
                                            \t MOVED {filename}.{extension}_{count} to {destination}
                                            \t DELETED {source.split("\\")[-1]} in {temp_path}
                                            \t DELETED {source.split("\\")[-1]} in {unsorted_path}"""

                        logger.info(message)
                        break
                    count += 1
        if not multiple:
            if not os.path.exists(os.path.join(destination, f"{filename}.{extension}")):
                shutil.move(source, os.path.join(destination, f"{filename}.{extension}"))

                message = f"""RENAMED {source.split("\\")[-1]} to {filename}.{extension}
                        \t MOVED {filename}.{extension} to {destination}
                        \t DELETED {source.split("\\")[-1]} in {temp_path}
                        \t DELETED {source.split("\\")[-1]} in {unsorted_path}"""

                logger.info(message)
        path_manager.update_successes()
    except Exception as e:
        logger.warning(e)
        move_file_warning(source)


"""
Description: 
    moves and renames a file into a specific destination
    multiple is set to DEFAULT value
    will check if file_name already exists and renames to file_name_x (x=1,2,3,etc) and rechecks
    logs operation of move to destination and deletion of file in 'temp_path' and 'unsorted_path'
Args:
    source: original file location
    filename: strict name of file so some_pdf.pdf would be passed as some_pdf
    destination: intended location for file
    extension: defaulted to .pdf but can be changed if something else is passed
    multiple: defaulted to True, not recommended to be changed    
"""


def move_file_warning(source, extension='pdf', multiple=True):
    path_manager = DirectoryManager()
    unsorted_path = path_manager.get_unsorted_dir()
    manual_sort_path = path_manager.get_manual_sort_dir()
    temp_path = path_manager.get_temp_dir()
    logger = path_manager.get_logger()

    path_manager.updated_fails()

    original_filename = source.split("\\")[-1][:-4]
    if multiple:
        if not os.path.exists(os.path.join(manual_sort_path, f"{original_filename}.{extension}")):
            shutil.move(source, os.path.join(manual_sort_path, f"{original_filename}.{extension}"))

            message = f"""UNABLE to parse DATE in document
                        \t MOVED {original_filename}.{extension} to {manual_sort_path}
                        \t DELETED {source.split("\\")[-1]} in {temp_path}
                        \t KEPT {source.split("\\")[-1]} in {unsorted_path}"""
            logger.error(message)
        else:
            count = 1
            while True:
                if not os.path.exists(os.path.join(manual_sort_path, f"{original_filename}_{count}.{extension}")):
                    shutil.move(source, os.path.join(manual_sort_path, f"{original_filename}_{count}.{extension}"))

                    message = f"""UNABLE to parse DATE in document
                                \t MOVED {original_filename}.{extension} to {manual_sort_path}
                                \t DELETED {source.split("\\")[-1]} in {temp_path}
                                \t KEPT {source.split("\\")[-1]} in {unsorted_path}"""

                    logger.error(message)
                    break
                count += 1
    if not multiple:
        if not os.path.exists(os.path.join(manual_sort_path, f"{original_filename}.{extension}")):
            shutil.move(source, os.path.join(manual_sort_path, f"{original_filename}.{extension}"))

            message = f"""UNABLE to parse DATE in document
                        \t MOVED {original_filename}.{extension} to {manual_sort_path}
                        \t DELETED {source.split("\\")[-1]} in {temp_path}
                        \t KEPT {source.split("\\")[-1]} in {unsorted_path}"""

            logger.error(message)
