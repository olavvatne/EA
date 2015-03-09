from abc import ABCMeta, abstractmethod
import numpy as np
import sys, random, math
from config.configuration import Configuration

class GenotypeFactory:
    DEFAULT = "default"

    @staticmethod
    def make_fitness_genotype(genotype=DEFAULT):
        selected = Configuration.get()["genotype"][genotype]
        config = selected["parameters"]
        return getattr(sys.modules[__name__], selected["class_name"])(**config)


class AbstractGenotype(metaclass=ABCMeta):

    def __init__(self, crossover_rate=1.0, mutation_rate=0.01):
        #TODO: Should genotype be initialized to zeroes, or parameter decide what to do.
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        #Random init or copying operation
        self.genotype = None

    @abstractmethod
    def init_random_genotype(self, n):
        pass

    @abstractmethod
    def copy(self):
        pass

    def crossover(self, partner):
        crossover = math.floor(random.uniform(0, self.genotype.size))
        cg1 = self.copy()
        if random.random() < self.crossover_rate:
            cg1.genotype[:crossover] = partner.genotype[:crossover]
        return cg1

    @abstractmethod
    def mutation(self):
        pass

    def __repr__(self):
        return "G:" + str(self.genotype)


class BitVectorGenotype(AbstractGenotype):
    #Default genotype, for testing purposes.


    def init_random_genotype(self, n):
        self.genotype = np.random.randint(2, size=n)

    def copy(self):
        g = BitVectorGenotype(crossover_rate=self.crossover_rate, mutation_rate=self.mutation_rate)
        g.genotype = self.genotype.copy()
        return g

    def mutation(self):
        #Single bit mutation
        for i in range(self.genotype.size):
            if random.random() < self.mutation_rate:
                #mutation_point = math.floor(random.uniform(0, self.genotype.size))
                self.genotype[i] = not self.genotype[i]

    def crossover(self, partner):
        crossover = math.floor(random.uniform(0, self.genotype.size))
        cg1 = self.copy()
        if random.random() < self.crossover_rate:
            cg1.genotype[:crossover] = partner.genotype[:crossover]
        return cg1

class SymbolGenotype(AbstractGenotype):

    def init_random_genotype(self, n):
        self.genotype = np.random.randint(10, size=n)

    def copy(self):
        g = SymbolGenotype(crossover_rate=self.crossover_rate, mutation_rate=self.mutation_rate)
        g.genotype = self.genotype.copy()
        return g

    def mutation(self):
        for i in range(self.genotype.size):
            if random.random() < self.mutation_rate:
                self.genotype[i] = random.randint(0, 9)