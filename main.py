import os
import shutil
import re
import time
import zipfile
import io
import yaml
import openpyxl


def clean_start_folder():
    # przenosze sie do folderu startowego
    os.chdir(config['start_path'])

    # w liscie zapisuje pliki ktore sa w folderze start
    start_folder_files = list(os.listdir())

    for file_name in start_folder_files:
        regex = re.split("[.]", file_name)
        extension = regex[1]
        if extension in config['extensions']:
            os.replace(config['start_path'] + '/' + file_name, config[extension] + '/' + file_name)
            control_number_of_files(config[extension])
            control_file_size(config[extension], file_name)
        else:
            os.replace(config['start_path'] + '/' + file_name, config['others_path'] + '/' + file_name)
            control_number_of_files(config['others_path'])


def control_number_of_files(path):
    os.chdir(path)
    folder_files = list(os.listdir())
    if len(folder_files) > config['max_number_of_files']:
        min_date = time.ctime(os.path.getctime(folder_files[0]))
        file_to_remove = folder_files[0]
        for file_name in folder_files:
            if min_date > time.ctime(os.path.getctime(file_name)):
                min_date = time.ctime(os.path.getctime(file_name))
                file_to_remove = file_name
        os.remove(file_to_remove)


def control_file_size(path, file_name):
    os.chdir(path)
    print(os.path.getsize(file_name))
    if os.path.getsize(file_name) > config['max_size_of_file']:
        file_compress(path, [file_name], file_name.split('.')[0] + '.zip')
        os.remove(file_name)


def print_folder_names():
    for name in config['folder_names'].split(' '):
        print(name)


def print_folder_content(path):
    os.chdir(path)
    folder_content = list(os.listdir())

    for file_name in folder_content:
        print(file_name)


def print_file_content(path, file_name):
    if file_name.split('.')[1] == 'xlsx':
        print_xlsx_file(path, file_name)
        return
    os.chdir(path)
    with open(file_name, "r") as f:
        for line in f:
            print(line)


def print_xlsx_file(path, file_name):
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


def file_compress(path, inp_file_names, out_zip_file):
    os.chdir(path)
    # Select the compression mode ZIP_DEFLATED for compression
    # or zipfile.ZIP_STORED to just store the file
    compression = zipfile.ZIP_DEFLATED

    zf = zipfile.ZipFile(out_zip_file, mode="w")

    try:
        for file_to_write in inp_file_names:
            # Add file to the zip file
            # first parameter file to zip, second filename in zip
            print(f' *** Processing file {file_to_write}')
            zf.write(file_to_write, file_to_write, compress_type=compression)

    except FileNotFoundError as e:
        print(f' *** Exception occurred during zip process - {e}')
    finally:
        zf.close()


if __name__ == '__main__':

    with open('config.yaml', 'r') as fp:
        config = yaml.safe_load(fp)

    clean_start_folder()
    user_input = input('Program do zarządzania folderami.\n'
                       'Zrobiłem już porządek w folderach. Co chcesz zrobić następne?\n'
                       '1. Spis folderów.\n'
                       '2. Stwórz własny plik tekstowy.\n'
                       '3. Działania na folderach.\n')
    match user_input:
        case '1':
            print_folder_names()

        case '2':
            user_input = input('Podaj nazwe pliku: ')
            try:
                file = open(user_input, 'x')
                user_input = input('Co chcesz mieć w pliku: ')
                while user_input != '':
                    file.write(user_input)
                    user_input = input()
                    file.write('\n')
                file.close()
            except FileExistsError:
                print("Ten plik już istnieje")

        case '3':
            user_input = input("Na ktorym folderze chcesz operowac:\n 1. text\n 2. data\n")
            path = ''
            if user_input == '1':
                path = config['text_path']
            elif user_input == '2':
                path = config['data_path']

            if path != '':
                print_folder_content(path)
                user_input = input("Co chcesz zrobic:\n "
                                   "1. Wyswietl zawartosc pliku\n 2. Kompresja plikow\n 3. Raport dla tego folderu.\n")
                match user_input:
                    case '1':
                        user_input = input("Który plik chcesz wyswietlić?\n")
                        print_file_content(path, user_input)

                    case '2':
                        user_input = input("Które pliki chcesz przenieść do zip?\n")
                        files_to_zip = user_input.split(' ')
                        user_input = input("Podaj nazwę pliku zip\n")
                        file_compress(path, files_to_zip, user_input + '.zip')


