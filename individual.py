
class Individual(object):

    def __init__(self, genotype, translator):
        self.genotype = genotype
        self.translator = translator
        self.phenotype = None
        self.fitness = 0 #TODO: 0 here?

    def devlop(self):
        #TODO: What if already adult and developed?
        self.phenotype = self.translator.develop(self)

    def __repr__(self):
        return "G:" + str(self.genotype)