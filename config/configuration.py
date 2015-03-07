import json

class Configuration:

    config = None

    @staticmethod
    def init():
        #TODO: try catch and exception handling
        json_data = open('config.json')
        Configuration.config = json.load(json_data)
        json_data.close()

    @staticmethod
    def get():
        if not Configuration.config:
            Configuration.init()
        return Configuration.config

    @staticmethod
    def reload():
        Configuration.init()

    @staticmethod
    def store(config):
        json_data = open('config.json', 'w')
        data = Configuration.config
        p = "parameters"
        for module in data.keys():
            for element in data[module].keys():
                if p in data[module][element]:
                    for a in data[module][element][p].keys():
                        data[module][element][p][a] = config[module][element][p][a]
        json_data.seek(0)
        json.dump(data, json_data, indent=4)
        json_data.close()