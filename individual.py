from operators import GeneticOperators
class Individual(object):

    def __init__(self, genotype, translator):
        self.genotype_container = genotype
        self.translator = translator
        self.phenotype_container = None
        self.fitness = 0 #TODO: 0 here?
        self.adult = False
        #TODO: Counter to seperate old and young adults?

    def devlop(self):
        #TODO: What if already adult and developed?
        self.phenotype_container = self.translator.develop(self)

    def mate(self, partner):
        genome = GeneticOperators.crossover(self.genotype_container, partner.genotype_container)
        genome = GeneticOperators.muatation(genome)
        return Individual(genome, self.translator)#, Individual(genome[1], self.translator)

    def copy(self):
        return Individual(self.genotype_container, self.translator)

    def __repr__(self):
        return "F: " +str(self.fitness) +" G:" + str(self.genotype_container)