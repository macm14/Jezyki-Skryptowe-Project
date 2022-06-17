import controller


if __name__ == '__main__':

    controller = controller.Controller()
    config_file = controller.config.file
    print(config_file)

    controller.dir_manager.clean_start_folder()
    user_input = input('Program do zarządzania folderami.\n'
                       'Zrobiłem już porządek w folderach. Co chcesz zrobić następne?\n'
                       '1. Spis folderów.\n'
                       '2. Stwórz własny plik tekstowy.\n'
                       '3. Działania na folderach.\n'
                       '4. Raport dla wszyskitch folderow.\n'
                       '5. Raport dla wybranego folderu\n'
                       '6. Nowy folder\n')
    match user_input:
        case '1':
            controller.dir_manager.print_folder_names()

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
            chosen_path = ''
            if user_input == '1':
                chosen_path = config_file['text']
            elif user_input == '2':
                chosen_path = config_file['data']

            if chosen_path != '':
                controller.dir_manager.print_folder_content(chosen_path)
                user_input = input("Co chcesz zrobic:\n "
                                   "1. Wyswietl zawartosc pliku\n 2. Kompresja plikow\n")
                match user_input:
                    case '1':
                        user_input = input("Który plik chcesz wyswietlić?\n")
                        controller.dir_manager.print_file_content(chosen_path, user_input)

                    case '2':
                        user_input = input("Które pliki chcesz przenieść do zip? (z rozszerzeniem)\n")
                        files_to_zip = user_input.split(' ')
                        user_input = input("Podaj nazwę pliku zip (bez rozszerzenia)\n")
                        controller.dir_manager.file_compress(chosen_path, files_to_zip, user_input + '.zip')

        case '4':
            controller.report_creator.all_folders_report()

        case '5':
            # user_input = input(  + list(config['folder_names']))
            # print("Dla którego folderu chcesz zrobić raport: ", config['folder_names'])
            print("Dla którego folderu chcesz zrobić raport: ")
            for name in config_file['folder_names']:
                print(name)

            user_input = input()
            controller.report_creator.files_report(config_file[user_input])

        case '6':
            user_input = input('Jaki folder chcesz stworzyć:\n'
                               '1. Sortowanie po nazwie\n'
                               '2. Sortowanie po rozszerzeniu\n')
            if user_input == '1':
                user_input = input('Podaj nazwę folderu:\n')
                if user_input not in config_file['by_names']:
                    # config_file['by_names'].append(user_input)
                    controller.dir_manager.createFolder(user_input)
                    controller.config.edit_file('by_names', user_input)
                else:
                    print('Program już obsługuje ten folder')
            elif user_input == '2':
                user_input = input('Podaj rozszerzenie:\n')
                if user_input not in config_file['extensions']:
                    user_input = input('Podaj nazwę folderu:\n')
                    # config_file['extensions'].append(user_input)
                    controller.dir_manager.createFolder(user_input)
                else:
                    print('Program już obsługuje to rozszerzenie')
