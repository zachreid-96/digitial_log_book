import os
import hashlib
import cv2
from pyzbar.pyzbar import decode
from PIL import Image, ImageFilter
import fitz
import numpy as np
from config import DirectoryManager
from pathlib import Path
from collections import Counter, defaultdict


def resize_image(image, scale_factor=1.5):
    width, height = image.size
    if width == 0 or height == 0:
        return image
    image = image.resize((int(width * scale_factor), int(height * scale_factor)), Image.LANCZOS)
    image = image.filter(ImageFilter.MedianFilter(size=3))
    return image


def extract_barcode_cv2(file):
    dpi = 300
    pages = fitz.open(file)
    page = pages[0]
    pix = page.get_pixmap(dpi=dpi)
    image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    """Detects barcode regions using Canny edge detection & contour filtering."""

    # Convert image to grayscale
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)

    # Use Canny edge detection to highlight barcode edges
    edges = cv2.Canny(gray, 50, 200)

    # Apply morphological closing to fill gaps in barcode lines
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))  # 9, 9
    closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    # Find contours
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize barcode region list
    barcode_regions = []
    debug_image = np.array(image).copy()
    barcode_data = []

    for contour in contours:
        # Get the rotated bounding box
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.intp(box)  # Convert to int

        # Get width, height, and angle
        (x, y), (w, h), angle = rect
        try:
            aspect_ratio = max(w, h) / min(w, h)
        except ZeroDivisionError:
            continue

        area = w * h

        # Filter based on aspect ratio and area
        if 2.25 < aspect_ratio < 7 and area > 35000:
            padding = 200  # Add padding to ensure the full barcode is captured
            x_min = int(x - w / 2 - padding)
            y_min = int(y - h / 2)
            x_max = int(x + w / 2 + padding)
            y_max = int(y + h / 2)

            # Ensure the bounding box stays within image bounds
            x_min = max(x_min, 0)
            x_max = min(x_max, image.width)

            barcode_regions.append((x_min, y_min, x_max, y_max, angle))
            cv2.rectangle(debug_image, (x_min, y_min), (x_max, y_max), (0, 0, 255), 2)

            cropped = np.array(image)[y_min:y_max, x_min:x_max]

            cropped_image = Image.fromarray(cropped)

            width, height = image.size
            if width != 0 or height != 0:
                try:
                    cropped_image = resize_image(cropped_image)
                    decoded_object = decode(cropped_image)
                    cropped_image.show()
                    if len(decoded_object) == 1:
                        for obj in decoded_object:
                            data = obj.data.decode('utf-8')
                            barcode_data.append(data)
                except Exception as e:
                    continue

    parts_tuple = [(part, count) for part, count in Counter(barcode_data).items()]
    return parts_tuple


def generate_hash(file):
    sha256 = hashlib.sha256()
    filename = os.path.basename(file)
    sha256.update(filename.encode('utf-8'))
    return sha256.hexdigest()


def check_hash_exists(file_hash):
    path_manager = DirectoryManager()
    cursor, connection = path_manager.get_database()

    cursor.execute('SELECT FILE_PATH FROM FILE_HASH WHERE HASH = ?', (file_hash,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()
    return result


def write_to_database(file, file_hash):
    path_manager = DirectoryManager()
    cursor, connection = path_manager.get_database()

    # Sort Data into Entry
    file_name_parts = Path(file).stem.split('_')

    serial_number = file_name_parts[1]
    date = file_name_parts[0]
    brand = Path(file).parts[-4]

    barcode_data = extract_barcode_cv2(file)

    if len(file_name_parts) == 2:

        if barcode_data:

            cursor.execute('INSERT INTO MACHINES (BRAND, SERIAL_NUM, DATE) VALUES (?, ?, ?)',
                           (brand, serial_number, date))

            machine_id = cursor.lastrowid
            for part_num, quantity in barcode_data:
                cursor.execute('INSERT INTO PARTS_USED (ENTRY_ID, PART_USED, QUANTITY) VALUES (?, ?, ?)',
                               (machine_id, part_num, quantity))

            cursor.execute('INSERT INTO FILE_HASH (HASH, FILE_PATH, ENTRY_ID) VALUES (?, ?, ?)',
                           (file_hash, file, machine_id))

            connection.commit()
            cursor.close()
            connection.close()

        else:
            print("failed to get barcode data vvv")
            print(file)

    if len(file_name_parts) == 3:

        if barcode_data:

            cursor.execute('SELECT ENTRY_ID FROM MACHINES WHERE SERIAL_NUM = ? AND DATE = ?',
                           (serial_number, date))
            entry_id = cursor.fetchone()

            if entry_id is not None:

                cursor.execute('SELECT PART_USED, QUANTITY FROM PARTS_USED WHERE ENTRY_ID = ?', (entry_id[0],))
                existing_parts = cursor.fetchall()

                combined_parts = defaultdict(int)
                for part, quantity in existing_parts:
                    combined_parts[part] += quantity

                for part, quantity in barcode_data:
                    combined_parts[part] += quantity

                new_parts = tuple((part, quantity) for part, quantity in combined_parts.items())

                if set(existing_parts) != set(new_parts):
                    cursor.execute('DELETE FROM PARTS_USED WHERE ENTRY_ID = ?', (entry_id[0],))

                    for part, quantity in new_parts:
                        cursor.execute('''INSERT INTO PARTS_USED (ENTRY_ID, PART_USED, QUANTITY)
                            VALUES (?, ?, ?)''', (entry_id[0], part, quantity))

                cursor.execute('INSERT INTO FILE_HASH (HASH, FILE_PATH, ENTRY_ID) VALUES (?, ?, ?)',
                               (file_hash, file, entry_id[0]))

            if entry_id is None:
                cursor.execute('INSERT INTO MACHINES (BRAND, SERIAL_NUM, DATE) VALUES (?, ?, ?)',
                               (brand, serial_number, date))

                machine_id = cursor.lastrowid
                for part_num, quantity in barcode_data:
                    cursor.execute('INSERT INTO PARTS_USED (ENTRY_ID, PART_USED, QUANTITY) VALUES (?, ?, ?)',
                                   (machine_id, part_num, quantity))

                cursor.execute('INSERT INTO FILE_HASH (HASH, FILE_PATH, ENTRY_ID) VALUES (?, ?, ?)',
                               (file_hash, file, machine_id))

            connection.commit()
            cursor.close()
            connection.close()


def database_add_files(file):
    file_name = Path(file).stem
    file_hash = generate_hash(file_name)

    # Write Data to Database
    if not check_hash_exists(file_hash):
        write_to_database(file, file_hash)

