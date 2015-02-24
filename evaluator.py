from abc import ABCMeta, abstractmethod
import numpy as np

class FitnessEvaluatorFactory:
    DEFAULT = "default"

    @staticmethod
    def make_fitness_evaluator(evaluator=DEFAULT):
        evaluators = {FitnessEvaluatorFactory.DEFAULT:DefaultFitnessEvaluator}
        return evaluators[evaluator]()


class AbstractFitnessEvaluator(metaclass=ABCMeta):

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

    def evaluate(self, individual):
        p = individual.phenotype_container.phenotype
        return np.sum(p) / p.size
