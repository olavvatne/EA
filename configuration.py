import json

class Configuration:

    #Maybe use as backup
    #options = {
    #        "genotype": ["default"],
    #        "translator": ["default", "integer"],
    #        "parent_selection": ["proportionate", "sigma", "boltzmann", "tournament"],
    #        "adult_selection": ["full", "over", "mixing"],
    #        "fitness": ["default", "leading"]
    #    }

    config = None

    @staticmethod
    def init():
        #TODO: try catch and exception handling
        json_data = open('config.json')
        Configuration.config = json.load(json_data)
        json_data.close()

    @staticmethod
    def get():
        return Configuration.config