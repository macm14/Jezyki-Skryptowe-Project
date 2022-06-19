import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import config_holder


class Report:

    def __init__(self, c: config_holder):
        self.config = c.read_file()

    def get_file_size(self, file_name: str) -> float:
        """
        :param file_name: File name
        :return: File's size
        """
        return round(os.path.getsize(file_name) / 1000, 2)

    def get_folder_size(self, path: str) -> float:
        """
        :param path: Directory path
        :return: Sum of files' sizes in directory
        """
        size = 0
        os.chdir(path)
        for file_name in list(os.listdir()):
            size += self.get_file_size(file_name)

        return size

    def all_folders_report(self) -> None:
        """
        Creates lists with data about folders sizes. Gives them to create_plot method
        :return: None
        """
        folders_list = []
        folders_size = []

        for name in self.config['folder_names']:
            folders_list.append(name)
            folders_size.append(self.get_folder_size(self.config[name][0]))

        self.create_plot('Folder name', 'Folder size [KB]', folders_list, folders_size)

    def files_report(self, path: str) -> None:
        """
        Creates lists with data about files sizes. Gives them to create_plot method
        :param path: Directory path
        :return: None
        """
        os.chdir(path)
        files_list = list(os.listdir())
        files_size = []
        for file_name in files_list:
            files_size.append(self.get_file_size(file_name))

        self.create_plot('File name', 'File size [KB]', files_list, files_size)

    def create_plot(self, x_name: str, y_name: str, x_list: list[str], y_list: list[float]):
        """
        Creates a bar chart.
        :param x_name: X-axis label
        :param y_name: Y-axis label
        :param x_list: X-axis data
        :param y_list: Y-axis data
        :return: None
        """
        d = {'Name': x_list,
             'Size': y_list}
        df = pd.DataFrame(data=d)

        print(df)
        fig, ax = plt.subplots()
        x = np.arange(len(x_list))
        x_bar = ax.bar(x, y_list, label='Size')
        ax.set_xticks(x, x_list, rotation=45, fontsize=8)
        ax.set_xlabel(x_name)
        ax.set_ylabel(y_name)
        ax.legend()
        ax.bar_label(x_bar)
        plt.show()
