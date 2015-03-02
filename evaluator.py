from abc import ABCMeta, abstractmethod
import numpy as np
import sys
from configuration import Configuration

class FitnessEvaluatorFactory:
    DEFAULT = "default"

    @staticmethod
    def make_fitness_evaluator(evaluator=DEFAULT, **kwargs):
        evaluators = Configuration.get()["fitness"]
        return getattr(sys.modules[__name__], evaluators[evaluator]["class_name"])(**kwargs)


class AbstractFitnessEvaluator(metaclass=ABCMeta):

    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def evaluate(self, individual):
        pass

    def evaluate_all(self, population):
        #TODO: Should evaluation be done for already adult individuals. Maybe not. Operation can
        #Be expensive.
        for individual in population:
            individual.fitness = self.evaluate(individual)


class DefaultFitnessEvaluator(AbstractFitnessEvaluator):
    #For the simple problem. Put this here so the EA works without extension classes
    NUMBER_ONE = 1

    def __init__(self, **kwargs):
        pass

    def evaluate(self, individual):
        p = individual.phenotype_container.phenotype
        return (np.sum(p) / p.size)

class LeadingFitnessEvaluator(AbstractFitnessEvaluator):
    #For LOLZ prefix problem

    def __init__(self, **kwargs):
        if "z" in kwargs:
            self.z = kwargs["z"]
        else:
            self.z = 4

    def evaluate(self, individual):
        p = individual.phenotype_container.phenotype
        leading = p[0]
        score = 0
        for n in p:
            if n == leading:
                score += 1
            else:
                break
        if leading == 1:
            return score
        else:
            if score > self.z:
                return self.z
            return score
