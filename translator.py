from abc import ABCMeta, abstractmethod
import numpy as np

class TranslatorFactory:
    DEFAULT = "default"
    INTEGER = "integer"

    @staticmethod
    def make_fitness_translator(translator=DEFAULT):
        translators = {TranslatorFactory.DEFAULT: DefaultTranslator,
                       TranslatorFactory.INTEGER: BinToIntTranslator}
        return translators[translator]()


class AbstractTranslator(metaclass=ABCMeta):

    @abstractmethod
    def develop(self, individual):
        pass

class DefaultTranslator(AbstractTranslator):

    def develop(self, individual):
        #For the first problem, no development is necessary
        individual.phenotype = np.copy(individual.genotype)

class BinToIntTranslator(AbstractTranslator):

    def develop(self, individual):
        pass
        #TODO: conversion from binary to integer values