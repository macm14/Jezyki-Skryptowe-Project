import directory_manager
import report
import config_holder


class Controller:

    def __init__(self):
        self.config = config_holder.Config()
        self.dir_manager = directory_manager.DirectoryManager(self.config)
        self.report_creator = report.Report(self.config)
