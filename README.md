# cpdf_compress
The script is made to compress JPG and PDF files.
Pillow is used to compress JPG and cpdf utility to compress PDF.
Script walks over directory and all subdirectories extracting archives (7z, rar, zip) deleting them and
checks if the file is in log.csv and compresses and replaces PDF and JPG files if they're not in log.csv.

Usage
cpdf_compress.py, unrar.exe and cpdf.exe should be in the same folder.
os.chdir("your_start_folder") - select your start folder


Output
log.csv with some statistics such as: size of the file before, size after, and size decreased in percent.
