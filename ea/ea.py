import numpy as np

from ea.genotype import GenotypeFactory
from ea.translator import TranslatorFactory
from ea.evaluator import FitnessEvaluatorFactory
from ea.individual import Individual
from ea.selection import AdultSelectionFactory
from ea.reproduction import ParentSelectionFactory


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
        print("-------------------------")

        if not self.is_legal():
            raise RuntimeError("Cannot run EA. Lack neccessary objects")

        children = self.create_population(population_size)  #Inital population
        self.adult_pool = []

        for c in range(cycles):

            self.geno_to_pheno_development(children)
            self.fitness_evaluator.evaluate_all(children)
            self.adult_pool = self.adult_selector.select(self.adult_pool, children, population_size)
            mating_adults = self.parent_selector.select_mating_pool(self.adult_pool, population_size, t=1-(c/cycles))
            children = self.reproduce(mating_adults)

            #Check stopping condition, and gui update below
            best_individual = self.best_individual(self.adult_pool)
            if self.is_stopping or fitness_threshold <= best_individual.fitness:
                self.is_stopping = False
                break

            if self.listener and c%EA.EVENT_RATE == 0:
                #Sends an update every 10th cycle. Fraction multiplied by 100 and 10 (10th cyle)
                #send to indicate evolution loop progression.
                self.send_update(c, cycles, best_individual)

        #Final update
        best_individual = self.best_individual(self.adult_pool)
        self.send_update(c+1, cycles, best_individual)
        print("-------------------------")

    def stop(self):
        self.is_stopping = True

    def send_update(self, c, cycles, best):
        #TODO: MESSY
        avg_fitness = self.avg_fitness(self.adult_pool)
        std = np.std(list(a.fitness for a in self.adult_pool))
        print("C: ", c, "B_f: ", best.fitness, " A_f: ", avg_fitness, " std: ", std, "P: ", best.phenotype_container)
        self.listener.update(c, 1/cycles * 100 * EA.EVENT_RATE, avg_fitness, best.fitness, std)

    def best_individual(self, adults):
        return max(adults, key=lambda a: a.fitness)

    def avg_fitness(self, population):
        tot_fitness = sum(individual.fitness for individual in population)
        return tot_fitness/len(population)

    def create_population(self, n):
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

    def reproduce(self, mating_adults):
        children = []
        for a1, a2 in mating_adults:
            children.extend(a1.mate(a2))
        return children

    def setup(self, geno_to_pheno, evaluator, geno, adult, parent, genome_length):
        self.translator = TranslatorFactory.make_fitness_translator(geno_to_pheno)
        self.fitness_evaluator = FitnessEvaluatorFactory.make_fitness_evaluator(evaluator)
        self.genotype = geno
        self.genome_length = genome_length
        self.adult_selector = AdultSelectionFactory.make_adult_selector(adult)
        self.parent_selector = ParentSelectionFactory.make_parent_selector(parent)

    def is_legal(self):
        return self.translator and self.fitness_evaluator and self.adult_selector and self.parent_selector
