from genotype import GenotypeFactory
from translator import TranslatorFactory
from evaluator import FitnessEvaluatorFactory
from individual import Individual

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
        self.selector = None

    def run(self, population_size, cycles, fitness_threshold):
        population = self.create_population(population_size)  #Inital population
        #TODO: stop if provided threshold is reached
        for c in range(cycles):
            self.geno_to_pheno_development(population)
            self.fitness_evaluator.evaluteAll(population)

    def create_population(self, n):
        population = []
        for i in range(n):
            genotype = GenotypeFactory.make_fitness_genotype("default")  #TODO: Better way. Maybe costly
            genotype.init_random_genotype(20) #TODO: Where should length be specified
            individual = Individual(genotype, self.translator)
            population.append(individual)
        return population

    def geno_to_pheno_development(self, population):
        for individual in population:
            individual.devlop()

    def setup(self, translator, fitness_evaluator, genotype, selector):
        #TODO: is geno to pheno translator be sufficent. No need for phenotype as parameter?
        self.translator = translator
        self.fitness_evaluator = fitness_evaluator
        self.genotype = genotype
        self.selector = selector


ea = EA()
config = "default"
g = GenotypeFactory.make_fitness_genotype(config)
g_to_p_translator = TranslatorFactory.make_fitness_translator(config)
f = FitnessEvaluatorFactory.make_fitness_evaluator(config)
ea.setup(g_to_p_translator, f, g, None)
ea.run(10,10,1)
#@classmethod
#@staticmethod