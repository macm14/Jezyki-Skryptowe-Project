import controller


if __name__ == '__main__':

    controller = controller.Controller()

    controller.dir_manager.clean_start_folder()
    user_input = input('Program do zarządzania folderami.\n'
                       'Zrobiłem już porządek w folderach. Co chcesz zrobić następne?\n'
                       '1. Spis folderów.\n'
                       '2. Stwórz własny plik tekstowy.\n'
                       '3. Działania na folderach.\n'
                       '4. Raport dla wszyskitch folderow.\n'
                       '5. Raport dla wybranego folderu\n')
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
                chosen_path = controller.config.file['text']
            elif user_input == '2':
                chosen_path = controller.config.file['data']

            if chosen_path != '':
                controller.dir_manager.print_folder_content(chosen_path)
                user_input = input("Co chcesz zrobic:\n "
                                   "1. Wyswietl zawartosc pliku\n 2. Kompresja plikow\n")
                match user_input:
                    case '1':
                        user_input = input("Który plik chcesz wyswietlić?\n")
                        controller.dir_manager.print_file_content(chosen_path, user_input)

                    case '2':
                        user_input = input("Które pliki chcesz przenieść do zip?\n")
                        files_to_zip = user_input.split(' ')
                        user_input = input("Podaj nazwę pliku zip\n")
                        controller.dir_manager.file_compress(chosen_path, files_to_zip, user_input + '.zip')

        case '4':
            controller.report_creator.all_folders_report()

        case '5':
            # user_input = input(  + list(config['folder_names']))
            # print("Dla którego folderu chcesz zrobić raport: ", config['folder_names'])
            print("Dla którego folderu chcesz zrobić raport: ")
            for name in controller.config.file['folder_names']:
                print(name)

            user_input = input()
            controller.report_creator.files_report(controller.config.file[user_input])
