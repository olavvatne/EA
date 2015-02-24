from abc import ABCMeta, abstractmethod
import numpy as np


class GenotypeFactory:
    DEFAULT = "default"

    @staticmethod
    def make_fitness_genotype(genotype=DEFAULT):
        genotypes = {GenotypeFactory.DEFAULT:BitVectorGenotype}
        return genotypes[genotype]()


class AbstractGenotype(metaclass=ABCMeta):

    def __init__(self):
        #TODO: Should genotype be initialized to zeroes, or parameter decide what to do.
        #Random init or copying operation
        self.genotype = None

    @abstractmethod
    def init_random_genotype(self, n):
        pass

    @abstractmethod
    def create_instance(self):
        pass

    @abstractmethod
    def copy(self):
        pass

    def __repr__(self):
        return str(self.genotype)


class BitVectorGenotype(AbstractGenotype):
    #Default genotype, for testing purposes.

    def init_random_genotype(self, n):
        self.genotype = np.random.randint(2, size=n)

    def copy(self):
        g = BitVectorGenotype()
        g.genotype = self.genotype.copy()
        return g

    def create_instance(self):
        #TODO: IS THIS NEEDED. FACTORY METHOD
        pass