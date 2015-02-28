from genotype import GenotypeFactory
from translator import TranslatorFactory
from evaluator import FitnessEvaluatorFactory
from individual import Individual
from selection import AdultSelectionFactory
from reproduction import ParentSelectionFactory

class EA(object):
    #Highly parameterized, should be able to change all parameters, through gui
    #Create python file with methods that return object, with the right mix of fitness eval, phenotype etc, can be used
    #a setup type of method that configure the EA before running. Drop down with alternatives in gui, pop size etc d
    #decided by other gui elements

    EVENT_RATE = 10

    def __init__(self):
        self.is_stopping = False
        self.translator = None
        self.fitness_evaluator = None
        self.genotype = None
        self.genome_length = 0
        self.phenotype = None
        self.adult_selector = None
        self.parent_selector = None
        self.listener = None
        self.adult_pool = []

    def add_listener(self, listener):
        self.listener = listener

    def run(self, population_size, cycles, fitness_threshold):
        #TODO: Make fitness threshold optional, and settable in GUI

        if not self.is_legal():
            raise RuntimeError("Cannot run EA. Lack neccessary objects")

        children = self.create_population(population_size)  #Inital population
        self.adult_pool = []

        for c in range(cycles):

            self.geno_to_pheno_development(children)
            self.fitness_evaluator.evaluate_all(children)
            self.adult_pool = self.adult_selector.select(self.adult_pool, children, population_size)
            mating_adults = self.parent_selector.select_mating_pool(self.adult_pool, population_size, t=1-(c/cycles))
            children = []
            for a1, a2 in mating_adults:
                children.extend(a1.mate(a2))

            best_fitness = self.best_fitness(self.adult_pool)
            if self.is_stopping or fitness_threshold <= best_fitness:
                self.is_stopping = False
                self.send_update(c, cycles, best_fitness)
                break

            if self.listener and c%EA.EVENT_RATE == 0:
                #Sends an update every 10th cycle. Fraction multiplied by 100 and 10 (10th cyle)
                #send to indicate evolution loop progression.
                self.send_update(c, cycles, best_fitness)

        print(self.adult_pool)
        print(self.best_fitness(self.adult_pool))

    def stop(self):
        self.is_stopping = True

    def send_update(self, c, cycles, best_fitness):
        #Send stuff to be displayed
        avg_fitness = self.avg_fitness(self.adult_pool)
        self.listener.update(c, 1/cycles * 100 * EA.EVENT_RATE, avg_fitness, best_fitness)

    def best_fitness(self, adults):
        return max(adult.fitness for adult in adults)

    def avg_fitness(self, population):
        tot_fitness = sum(individual.fitness for individual in population)
        return tot_fitness/len(population)

    def create_population(self, n):
        #TODO: consider using heap or more appropriate data structure. Currently use list to avoid clutter.
        population = []
        for i in range(n):
            genotype = GenotypeFactory.make_fitness_genotype(self.genotype)
            genotype.init_random_genotype(self.genome_length)
            individual = Individual(genotype, self.translator)
            population.append(individual)
        return population

    def geno_to_pheno_development(self, population):
        for individual in population:
            individual.devlop()

    def setup(self, translator, fitness_evaluator, genotype, adult_selector, parent_selector, genome_length):

        self.translator = TranslatorFactory.make_fitness_translator(translator)
        self.fitness_evaluator = FitnessEvaluatorFactory.make_fitness_evaluator(fitness_evaluator)
        self.genotype = genotype
        self.genome_length = genome_length
        self.adult_selector = AdultSelectionFactory.make_adult_selector(adult_selector)
        self.parent_selector = ParentSelectionFactory.make_parent_selector(parent_selector)

    def is_legal(self):
        return self.translator and self.fitness_evaluator and self.adult_selector and self.parent_selector

ea = EA()
config = "default"
g = config
g_to_p_translator = config
f = config
s = "full"
p = "proportionate"

#ea.setup(g_to_p_translator, f, g, s, p, 20)
#ea.run(20,100,1)
#@classmethod
#@staticmethod