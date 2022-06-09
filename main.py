import os
import shutil
import re
import time
import zipfile
import io
import yaml


def clean_start_folder():
    # przenosze sie do folderu startowego
    os.chdir(config['start_path'])

    # w liscie zapisuje pliki ktore sa w folderze start
    start_folder_files = list(os.listdir())

    for file_name in start_folder_files:
        regex = re.split("[.]", file_name)
        if regex[1] == 'txt' or regex[1] == 'pdf' or regex[1] == 'docx':
            shutil.move(config['start_path'] + '/' + file_name,
                        config['text_path'])
            control_number_of_files(config['text_path'])
        elif regex[1] == 'csv':
            shutil.move(config['start_path'] + '/' + file_name,
                        config['data_path'])
            control_number_of_files(config['data_path'])
        else:
            shutil.move(config['start_path'] + '/' + file_name,
                        config['others_path'])
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
                # print(time.ctime(os.path.getctime(file_name)))
        os.remove(file_to_remove)


def print_folder_content(path):
    os.chdir(path)
    folder_content = list(os.listdir())

    for file_name in folder_content:
        print(file_name)


def print_file_content(path, file_name):
    os.chdir(path)
    with open(file_name, "r") as f:
        for line in f:
            print(line)


def file_compress(inp_file_names, out_zip_file):
    os.chdir("C:/Users/Dell/Desktop/Jezyki Skryptowe lab/Projekt/start")
    # Select the compression mode ZIP_DEFLATED for compression
    # or zipfile.ZIP_STORED to just store the file
    compression = zipfile.ZIP_DEFLATED
    print(f" *** Input File name passed for zipping - {inp_file_names}")

    # create the zip file first parameter path/name, second mode
    print(f' *** out_zip_file is - {out_zip_file}')
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
        # Don't forget to close the file!
        zf.close()


if __name__ == '__main__':

    with open('config.yaml', 'r') as fp:
        config = yaml.safe_load(fp)

    # file_compress(['rpe.xlsx'], 'test_zip.zip')
    clean_start_folder()
    user_input = input('Program do zarządzania folderami.\n'
                       'Zrobiłem już porządek w folderach. Co chcesz zrobić następne?\n'
                       '1. Stwórz własny plik tekstowy.\n'
                       '2. Wyswietl wybrany plik\n')
    match user_input:
        case '1':
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

        case '2':
            user_input = input("Ktory folder chcesz wyswietlic:\n 1. text\n 2. data\n")
            match user_input:
                case '1':
                    print_folder_content(config['text_path'])
                    user_input = input("Który plik chcesz wyswietlić?\n")
                    print_file_content(config['test_path'], user_input)
                case '2':
                    print_folder_content(config['data_path'])
                    user_input = input("Który plik chcesz wyswietlić?\n")
                    print_file_content(config['data_path'], user_input)


