import os, zipfile, time
from PIL import Image
import py7zr
import rarfile

start_time = time.time()
rarfile.UNRAR_TOOL = r"'.\UnRAR.exe"
os.chdir("C:/input/02072020")  # начальная папка
count_pdf = 0
count_jpg = 0
total_compressed_files = 0
total_files = 0


def get_size(start_path='.'):
    total_size = 0
    for path, names, files in os.walk(start_path):
        for f in files:
            fp = os.path.join(path, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size


total_size_before = round(get_size('.') / 1024 ** 2, 2)

for path, subdir, files in os.walk('.'):
    for file in files:
        my_name, file_extension = os.path.splitext(file)
        path_to_file = os.path.join(path, file)
        path = os.path.dirname(path_to_file)
        if file_extension in ('.zip'):  # Dealing with ZIP right here
            with zipfile.ZipFile(path_to_file, 'r') as my_zip:
                for name in my_zip.namelist():
                    if os.path.exists(os.path.join(path, name)):
                        print(path_to_file, 'already exists')
                    else:
                        my_zip.extractall(path)
                        print(file, 'extracted')
            os.remove(path_to_file)
        if file_extension == '.7z':
            with py7zr.SevenZipFile(path_to_file, 'r') as my_zip:  # Dealing with 7z here
                for name in my_zip.getnames():
                    if os.path.exists(os.path.join(path, name)):
                        print(path_to_file, 'already exists')
                    else:
                        my_zip.extractall(path)
                        print(file, 'extracted')
            os.remove(path_to_file)
        elif file_extension == '.rar':  # Dealing with RAR right here
            with rarfile.RarFile(path_to_file, 'r') as my_zip:
                for name in my_zip.namelist():
                    if os.path.exists(os.path.join(path, name)):
                        print(path_to_file, 'already exists')
                    else:
                        my_zip.extractall(path)
                        print(file, 'extracted')
            os.remove(path_to_file)

for path, subdir, files in os.walk('.'):
    for file in files:
        path_to_file = os.path.join(path, file)
        absolute_path_to_file = os.path.abspath(path_to_file)
        path = os.path.dirname(path_to_file)
        absolute_path = os.path.abspath(path)
        my_name, file_extension = os.path.splitext(file)
        if file_extension in ('.pdf', '.PDF'):
            count_pdf += 1
            size_pdf_before = os.path.getsize(absolute_path_to_file)
            os.system(f'''C:\input\cpdf.exe -squeeze "{absolute_path_to_file}" -o "{absolute_path_to_file}"''')
            total_size_jpg_after = os.path.getsize(absolute_path_to_file)  # size PDF after

        elif file_extension in ('.jpg', '.jpeg', '.JPEG', '.JPG'):
            count_jpg += 1
            print(path_to_file, 'executing')
            size_jpg_before = os.path.getsize(absolute_path_to_file)
            img = Image.open(path_to_file)
            img.save(path_to_file, format='JPEG', optimize=True, quality=20)
            size_jpg_after = os.path.getsize(path_to_file)
            total_size_jpg_after += size_jpg_after

total_compressed_files = count_jpg + count_pdf
total_size_after = round(get_size('.') / 1024 ** 2, 2)
size_diff = total_size_before - total_size_after
size_diff_percent = 100 - total_size_after * (100 / total_size_before)
size_diff_percent = round(size_diff_percent, 2)
print(f'Time spent {time.time() - start_time} seconds')
print(f'Total of {total_compressed_files} files processed. PDF files - {count_pdf}, JPG files - {count_jpg}.')
print(
    f'Total size before was {total_size_before} MB. Total size now is {total_size_after} MB. Saved {size_diff_percent}'
    f'% of space. Equals {size_diff} MB')

# Remove compressed* files
# count_matched = 0
# for path, subdir, files in os.walk('.'):
#     for name in files:
#         if fnmatch(name, 'compressed*.jpg'):
#             count_matched += 1
#             file = os.path.join(path, name)
#             os.remove(file)
#             print(f'{file} removed')
# print(count_matched)
