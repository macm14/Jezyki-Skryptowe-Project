import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import config_holder


class Report:

    def __init__(self, c: config_holder):
        self.config = c.read_file()

    def get_file_size(self, file_name):
        """
        :param file_name: File name
        :return: File's size
        """
        return round(os.path.getsize(file_name) / 1000, 2)

    def get_folder_size(self, path):
        """
        :param path: Directory path
        :return: Sum of files' sizes in directory
        """
        size = 0
        os.chdir(path)
        for file_name in list(os.listdir()):
            size += self.get_file_size(file_name)

        return size

    def all_folders_report(self):
        """
        Creates lists with data about folders sizes. Gives them to create_plot method
        :return: None
        """
        folders_list = []
        folders_size = []

        for name in self.config['folder_names']:
            folders_list.append(name)
            folders_size.append(self.get_folder_size(self.config[name]))

        self.create_plot('Folder name', 'Folder size [KB]', folders_list, folders_size)

    def files_report(self, path):
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

    def create_plot(self, x_name, y_name, names_list, sizes_list):
        """
        Creates a bar chart.
        :param x_name: X-axis data
        :param y_name: Y-axis data
        :param names_list: List with folder or files names
        :param sizes_list: List with folder or files sizes
        :return: None
        """
        d = {'Name': names_list,
             'Size': sizes_list}
        df = pd.DataFrame(data=d)

        print(df)
        fig, ax = plt.subplots()
        x = np.arange(len(names_list))
        x_bar = ax.bar(x, sizes_list, label='Size')
        ax.set_xticks(x, names_list, rotation=45, fontsize=8)
        ax.set_xlabel(x_name)
        ax.set_ylabel(y_name)
        ax.legend()
        ax.bar_label(x_bar)
        plt.show()
