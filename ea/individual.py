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
        #g1, g2 = GeneticOperators.crossover(self.genotype_container, partner.genotype_container)
        #g1 = GeneticOperators.muatation(g1)
        #g2 = GeneticOperators.muatation(g2)
        g1 = self.genotype_container.crossover(partner.genotype_container)
        g2 = partner.genotype_container.crossover(self.genotype_container)
        g1.mutation()
        g2.mutation()
        return Individual(g1, self.translator), Individual(g2, self.translator)

    def copy(self):
        return Individual(self.genotype_container, self.translator)

    def __repr__(self):
        return "F: " +str(self.fitness) +" G:" + str(self.genotype_container)