from abc import ABCMeta, abstractmethod
import sys
import math

import numpy as np

from ea.phenotype import IntegerPhenotype
from config.configuration import Configuration


class TranslatorFactory:
    DEFAULT = "default"

    @staticmethod
    def make_fitness_translator(translator=DEFAULT):
        selected = Configuration.get()["translator"][translator]
        config = selected["parameters"]
        print(config)
        return getattr(sys.modules[__name__], selected["class_name"])(**config)


class AbstractTranslator(metaclass=ABCMeta):

    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def develop(self, individual):
        pass


class DefaultTranslator(AbstractTranslator):

    def develop(self, individual):
        #For the first problem, no development is necessary
        return IntegerPhenotype(np.copy(individual.genotype_container.genotype))


class BinToIntTranslator(AbstractTranslator):
    def __init__(self, k=8):
        self.k = k

    def develop(self, individual):
        p = individual.genotype_container.genotype
        integer_list = [self._tobin(p[i:i + self.k]) for i in range(0, len(p), self.k)]
        return IntegerPhenotype(np.array(integer_list))


    def _tobin(self, x):
        s = ""
        for n in x:
            s += str(n)
        return int(s, 2)

class BinToSymbolTranslator(AbstractTranslator):

    def __init__(self, s=4):
        self.nr_of_symbols = s
        self.b = math.ceil(math.log2(self.nr_of_symbols))#Gray bits to support nr of symbols

    def develop(self, individual):
        p = individual.genotype_container.genotype

        #Use gray encoding so that a bit change will not
        #Possibly better for integers, and not symbols that has no appearant relations
        #TODO: modulo a good idea???
        symbol_list = [(self._g2i(p[i:i + self.b]))%self.nr_of_symbols for i in range(0, len(p), self.b)]
        return IntegerPhenotype(np.array(symbol_list))

    def _g2i(self, l):
        return BinToSymbolTranslator._bin2int(BinToSymbolTranslator._gray2bin(l))

    @staticmethod
    def _gray2bin(bits):
        b = [bits[0]]
        for nextb in bits[1:]: b.append(b[-1] ^ nextb)
        return b

    @staticmethod
    def _bin2int(bits):
        'From binary bits, msb at index 0 to integer'
        i = 0
        for bit in bits:
            i = i * 2 + bit
        return i