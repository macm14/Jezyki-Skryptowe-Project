import os
import yaml


class Config:

    def __init__(self):
        self.config_name = 'config.yaml'
        self.file = self.read_file()

    def read_file(self) -> dict:
        """
        Takes no parameters\n
        Returns dictionary with config file contents
        """
        with open(self.config_name, 'r') as fp:
            config = yaml.safe_load(fp)

        return config

    def edit_file(self, module, folder_name) -> None:
        """
        :param module: Key from dictionary for extension folder or by-name folders
        :param folder_name: New folder name
        :return: None
        """
        os.chdir(self.file['parent_directory'][0])
        self.file[module].append(folder_name)
        self.file[folder_name] = [self.file['parent_directory'][0] + '/' + folder_name]
        self.file['folder_names'].append(folder_name)

        try:
            file = open(self.config_name, 'w')
            for key, list in self.file.items():
                file.write(key)
                file.write(':\n')
                for element in list:
                    file.write('   - ')
                    file.write(str(element))
                    file.write('\n')

                file.write('\n')
        except FileExistsError:
            print("Ten plik już istnieje")
        finally:
            file.close()

        self.file = self.read_file()
