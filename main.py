import os

import controller

if __name__ == '__main__':

    controller = controller.Controller()
    config_file = controller.config.file
    # print(config_file)

    # controller.dir_manager.clean_start_folder()
    flag = True
    print('Program do zarządzania folderami.\n')
    while flag is True:
        os.chdir(config_file['parent_directory'][0])
        user_input = input('Menu\n'
                           '1. Posprzątaj folder startowy.\n'
                           '2. Spis folderów.\n'
                           '3. Stwórz własny plik tekstowy.\n'
                           '4. Działania na folderach.\n'
                           '5. Raport dla wszyskitch folderow.\n'
                           '6. Raport dla wybranego folderu\n'
                           '7. Nowy folder\n'
                           '8. Zakończ działanie\n')
        match user_input:
            case '1':
                controller.dir_manager.clean_start_folder()
            case '2':
                controller.dir_manager.print_folder_names()

            case '3':
                file_name = input('Podaj nazwe pliku (bez rozszerzenia):\n')
                file_name = file_name + '.txt'
                text = []
                user_input = input('Co chcesz mieć w pliku: ')
                while user_input != '':
                    text.append(user_input)
                    text.append('\n')
                    user_input = input()
                controller.dir_manager.create_file(file_name, text)

            case '4':
                user_input = input("Na ktorym folderze chcesz operowac:\n 1. text\n 2. data\n")
                chosen_path = ''
                if user_input == '1':
                    chosen_path = config_file['text'][0]
                elif user_input == '2':
                    chosen_path = config_file['data'][0]

                if chosen_path != '':
                    if controller.dir_manager.print_folder_content(chosen_path):
                        user_input = input("Co chcesz zrobic:\n "
                                           "1. Wyswietl zawartosc pliku\n 2. Kompresja plikow\n")
                        match user_input:
                            case '1':
                                user_input = input("Podaj nazwę pliku, który plik chcesz wyswietlić: (bez rozszerzenia)\n")
                                controller.dir_manager.print_file_content(chosen_path, user_input)

                            case '2':
                                user_input = input("Które pliki chcesz przenieść do zip? (z rozszerzeniem)\n")
                                files_to_zip = user_input.split(' ')
                                user_input = input("Podaj nazwę pliku zip (bez rozszerzenia)\n")
                                controller.dir_manager.file_compress(chosen_path, files_to_zip, user_input + '.zip')

            case '5':
                controller.report_creator.all_folders_report()

            case '6':
                # user_input = input(  + list(config['folder_names']))
                # print("Dla którego folderu chcesz zrobić raport: ", config['folder_names'])
                print("Dla którego folderu chcesz zrobić raport: ")
                for name in config_file['folder_names']:
                    print(name)

                user_input = input()
                controller.report_creator.files_report(config_file[user_input][0])

            case '7':
                user_input = input('Jaki folder chcesz stworzyć:\n'
                                   '1. Sortowanie po nazwie\n'
                                   '2. Sortowanie po rozszerzeniu\n')
                if user_input == '1':
                    user_input = input('Podaj nazwę folderu:\n')
                    if user_input not in config_file['by_names']:
                        controller.dir_manager.create_folder(user_input)
                        controller.config.edit_file('by_names', user_input)
                    else:
                        print('Program już obsługuje ten folder')
                elif user_input == '2':
                    user_input = input('Podaj rozszerzenie:\n')
                    if user_input not in config_file['extensions']:
                        user_input = input('Podaj nazwę folderu:\n')
                        controller.dir_manager.create_folder(user_input)
                    else:
                        print('Program już obsługuje to rozszerzenie')

            case '8':
                flag = False
