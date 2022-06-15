import re
import os
import time
import zipfile
import openpyxl
import config_holder


class DirectoryManager:

    def __init__(self, c: config_holder):
        self.config = c.read_file()

    def clean_start_folder(self):
        # przenosze sie do folderu startowego
        os.chdir(self.config['start'])

        # w liscie zapisuje pliki ktore sa w folderze start
        start_folder_files = list(os.listdir())

        for file_name in start_folder_files:
            regex = re.split("[.]", file_name)
            name = regex[0]
            extension = regex[1]
            for folder_name in self.config['important_folders']:
                if folder_name.lower() in name.lower():
                    os.replace(self.config['start'] + '/' + file_name, self.config[folder_name] + '/' + file_name)
                    break

            # jezeli plik nie ma w nazwie nazwy folderu
            if os.path.isfile(self.config['start'] + '/' + file_name):
                if extension in self.config['extensions']:
                    os.replace(self.config['start'] + '/' + file_name, self.config[extension] + '/' + file_name)
                    self.control_number_of_files(config[extension])
                    self.control_file_size(config[extension], file_name)
                else:
                    os.replace(self.config['start'] + '/' + file_name, self.config['others'] + '/' + file_name)
                    self.control_number_of_files(config['others'])

    def control_number_of_files(self, path):
        os.chdir(path)
        folder_files = list(os.listdir())
        if len(folder_files) > self.config['max_number_of_files']:
            min_date = time.ctime(os.path.getctime(folder_files[0]))
            file_to_remove = folder_files[0]
            for file_name in folder_files:
                if min_date > time.ctime(os.path.getctime(file_name)):
                    min_date = time.ctime(os.path.getctime(file_name))
                    file_to_remove = file_name
            os.remove(file_to_remove)

    def control_file_size(self, path, file_name):
        os.chdir(path)
        if os.path.getsize(file_name) > self.config['max_size_of_file']:
            self.file_compress(path, [file_name], file_name.split('.')[0] + '.zip')
            os.remove(file_name)

    def print_folder_names(self):
        for name in self.config['folder_names']:
            print(name)

    def print_folder_content(self, path):
        os.chdir(path)
        folder_content = list(os.listdir())

        for file_name in folder_content:
            print(file_name)

    def print_file_content(self, path, file_name):
        if file_name.split('.')[1] == 'xlsx':
            self.print_xlsx_file(path, file_name)
            return
        os.chdir(path)
        with open(file_name, "r") as f:
            for line in f:
                print(line)

    def print_xlsx_file(self, path, file_name):
        xlsx_file = path + '/' + file_name
        wb_obj = openpyxl.load_workbook(xlsx_file)

        sheet = wb_obj.active

        for row in sheet.iter_rows(max_row=sheet.max_row):
            for cell in row:
                if cell.value is None:
                    print(end="\t")
                else:
                    print(cell.value, end="\t")
            print()

    def file_compress(self, path, inp_file_names, out_zip_file):
        os.chdir(path)
        # Select the compression mode ZIP_DEFLATED for compression
        # or zipfile.ZIP_STORED to just store the file
        compression = zipfile.ZIP_DEFLATED

        zf = zipfile.ZipFile(out_zip_file, mode="w")

        try:
            for file_to_write in inp_file_names:
                # Add file to the zip file
                # first parameter file to zip, second filename in zip
                # print(f' *** Processing file {file_to_write}')
                zf.write(file_to_write, file_to_write, compress_type=compression)

        except FileNotFoundError as e:
            print(f' *** Exception occurred during zip process - {e}')
        finally:
            zf.close()