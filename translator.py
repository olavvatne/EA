from abc import ABCMeta, abstractmethod
import numpy as np
from phenotype import IntegerPhenotype
import sys
from configuration import Configuration

class TranslatorFactory:
    DEFAULT = "default"

    @staticmethod
    def make_fitness_translator(translator=DEFAULT, **kwargs):
        translators = Configuration.get()["translator"]
        return getattr(sys.modules[__name__], translators[translator]["class_name"])(**kwargs)


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

    def develop(self, individual):
        p = individual.genotype_container.genotype
        #TODO set symbol size s in config
        s = 4
        #TODO: find better way to encode bin to symbol set
        symbol_list = [sum(p[i:i + s]) for i in range(0, len(p), s)]
        return IntegerPhenotype(np.array(symbol_list))

    def _gray2bin(self, bits):
        b = [bits[0]]
        for nextb in bits[1:]: b.append(b[-1] ^ nextb)
        return b

    def _bin2int(self, bits):
        'From binary bits, msb at index 0 to integer'
        i = 0
        for bit in bits:
            i = i * 2 + bit
        return i