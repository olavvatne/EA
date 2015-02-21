from abc import ABCMeta, abstractmethod
import numpy as np

class AbstractGenotype(metaclass=ABCMeta):

    @abstractmethod
    def init_random_genotype(self):
        pass

class BitVectorGenotype(AbstractGenotype):
    #Default genotype, for testing purposes.

    def __init__(self, length):
        #TODO: Should genotype be initialized to zeroes, or parameter decide what to do.
        #Random init or copying operation
        self.genotype = np.zeroes(length)

    def init_random(self):
        self.genotype = np.random.randInt(2, size=(n,))