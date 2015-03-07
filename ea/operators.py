import random
import math
#TODO: Make suitable for extensions
#TODO: Individual should have specific type of crossover and mutation.
#Should be a objectified

class GeneticOperators(object):

    @staticmethod
    def crossover(genotype1, genotype2):
        #TODO: Same length genome?
        crossover_rate = 0.65
        crossoverpoint = math.floor(random.uniform(0, genotype1.genotype.size))
        #print(crossoverpoint)
        cg1 = genotype1.copy()
        cg2 = genotype2.copy()
        if random.random() < crossover_rate:
            cg1.genotype[:crossoverpoint] = genotype2.genotype[:crossoverpoint]
        if random.random() < crossover_rate:
            cg2.genotype[:crossoverpoint] = genotype1.genotype[:crossoverpoint]
        return cg1, cg2

    @staticmethod
    def muatation(genotype):
        #Single bit mutation
        mutation_rate = 0.5
        if random.random() < mutation_rate:
            #print("MUTATE")
            mutation_point = math.floor(random.uniform(0, genotype.genotype.size))
            genotype.genotype[mutation_point] = not genotype.genotype[mutation_point]
        return genotype