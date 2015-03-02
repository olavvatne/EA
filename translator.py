from abc import ABCMeta, abstractmethod
import numpy as np
from phenotype import IntegerPhenotype
import sys

class TranslatorFactory:
    DEFAULT = "default"
    INTEGER = "integer"

    @staticmethod
    def make_fitness_translator(translator=DEFAULT):
        translators = {TranslatorFactory.DEFAULT: "DefaultTranslator",
                       TranslatorFactory.INTEGER: "BinToIntTranslator"}
        return getattr(sys.modules[__name__], translators[translator])()


class AbstractTranslator(metaclass=ABCMeta):

    @abstractmethod
    def develop(self, individual):
        pass


class DefaultTranslator(AbstractTranslator):

    def develop(self, individual):
        #For the first problem, no development is necessary
        return IntegerPhenotype(np.copy(individual.genotype_container.genotype))


class BinToIntTranslator(AbstractTranslator):

    def develop(self, individual):
        p = individual.genotype_container.genotype
        #TODO: Parameter k set
        #TODO: More efficient way?
        k = 8
        integer_list = [self._tobin(p[i:i + k]) for i in range(0, len(p), k)]
        return IntegerPhenotype(np.array(integer_list))


    def _tobin(self, x):
        s = ""
        for n in x:
            s += str(n)
        return int(s, 2)
