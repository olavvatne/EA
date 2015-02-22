from abc import ABCMeta, abstractmethod
import numpy as np

class GenotypeFactory:
    DEFAULT = "default"

    @staticmethod
    def make_fitness_genotype(genotype=DEFAULT):
        genotypes = {GenotypeFactory.DEFAULT:GenotypeFactory}
        return genotypes[genotype]()

class AbstractGenotype(metaclass=ABCMeta):

    @abstractmethod
    def init_random_genotype(self, n):
        pass

    @abstractmethod
    def create_instance(self):
        pass

class BitVectorGenotype(AbstractGenotype):
    #Default genotype, for testing purposes.

    def __init__(self, length):
        #TODO: Should genotype be initialized to zeroes, or parameter decide what to do.
        #Random init or copying operation
        self.genotype = np.zeroes(length)

    def init_random_genotype(self, n):
        self.genotype = np.random.randInt(2, size=(n,))

    def create_instance(self):
        #TODO: IS THIS NEEDED. FACTORY METHOD
        pass