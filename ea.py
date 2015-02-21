from genotype import BitVectorGenotype

class EA(object):
    #Highly parameterized, should be able to change all parameters, through gui
    #Create python file with methods that return object, with the right mix of fitness eval, phenotype etc, can be used
    #a setup type of method that configure the EA before running. Drop down with alternatives in gui, pop size etc d
    #decided by other gui elements
    pass

    def __init__(self):
        self.translator = None
        self.fitness_evaluator = None
        self.genotype = None
        self.phenotype = None

    def run(self, population_size, cycles, fitness_threshold):
        initial_population = self.create_population(population_size)

        #TODO: stop if provided threshold is reached
        for c in range(cycles):
            pass

    def create_population(self, n):
        pass

    def setup(self, translator, fitness_evaluator, genotype, selector):
        #TODO: is geno to pheno translator be sufficent. No need for phenotype as parameter?
        pass


ea = EA()
#@classmethod
#@staticmethod