from abc import ABCMeta, abstractmethod


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

    def evaluateAll(self, population):
        #TODO: Should evaluation be done for already adult individuals. Maybe not. Operation can
        #Be expensive. 
        for individual in population:
            individual.fitness = self.evaluate(individual)


class DefaultFitnessEvaluator(AbstractFitnessEvaluator):
    #For the simple problem. Put this here so the EA works without extension classes
    NUMBER_ONE = 1

    def evaluate(self, individual):
        return individual.phenotype.count(DefaultFitnessEvaluator.NUMBER_ONE)/len(individual.phenotype)
