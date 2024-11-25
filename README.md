## Digital Log Book

This project serves as a personal log book sorting project. I work on copiers and printers, when using parts on a machine I like to keep a log of some information. Each part has a 'sticker' that contains part number and some other non-important bits (at least in the scope for this project). I place these stickers on a meter page for the machine I used it on. Information used in this scope is Brand name, Date of service, Serial number of machine.

This project needs some setup in order for it to work as programmed.</br>
These meter pages will need scanned to .pdf format.</br>
PDF24 will need installed on local device for the OCR'ing of files. This also doubles as a viable .pdf viewer.</br>
Python3.11+ will need installed on local device.</br>
Libraries used in project include: glob2, win32api, os, shutil, time, datetime, re, pdfminer.high_level (pdfminer.six), logging</br>
&emsp;install instructions can be found in setup() in main.py if not already installed.


The folder structure should be as follows:</br>
&emsp;?:\.\Digital Log Book\Unsorted&emsp;&emsp;&emsp;&ensp;Used to house files that need sorted</br>
&emsp;?:\.\Digital Log Book\runLogs&emsp;&emsp;&emsp;&emsp;Used to house the run logs for each runtime</br>
&emsp;?:\.\Digital Log Book\Manual_Sort&emsp;&emsp;Used to house the files marked for manual review</br>
&emsp;?:\.\Digital Log Book\Logs&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;Used to house the meter pages (with stickers) for manufacturers</br>
&emsp;?:\.\Digital Log Book&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Used to house the Inventory Restock pages</br>
&emsp;C:\.\temp&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;Used only if ?\. is not C:\</br>

?\.\ is included here as my setup exists on an external USB Drive but can be setup anywhere.</br>
If setup on C:\ the .\temp is not needed as PDF24-Ocr.exe can process files already located on C:\ but cannot process files not on C:\.

The basic idea of this project is this:
1) Process files in C:\.\temp
2) Apply OCR to all files
3) Read Data for each file and look for Date, Serial Number, and Brand ('Kyocera', 'HP', 'Inventory')
4) Move file to brand destination if Date and Serial Number where found and are valid
5) Move file to ?:\Digital Log Book\Manual_Sort if Date or Serial Number where not found or are not valid
6) Move all files from ?:\Digital Log Book\Unsorted to C:\.\temp
7) repeat steps 1-5


This project will only be updated as needed.
