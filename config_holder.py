import yaml


class Config:

    def __init__(self):
        self.config_name = 'config.yaml'
        self.file = self.read_file()

    def read_file(self):
        with open(self.config_name, 'r') as fp:
            config = yaml.safe_load(fp)

        return config
