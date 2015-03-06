from abc import ABCMeta, abstractmethod
import numpy as np
import sys
from configuration import Configuration

class FitnessEvaluatorFactory:
    DEFAULT = "default"

    @staticmethod
    def make_fitness_evaluator(evaluator=DEFAULT):
        selected = Configuration.get()["fitness"][evaluator]
        config = selected["parameters"]
        return getattr(sys.modules[__name__], selected["class_name"])(**config)


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

    def __init__(self, z=4):
        self.z = z

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


class SurprisingFitnessEvaluator(AbstractFitnessEvaluator):
    #For LOLZ prefix problem

    def __init__(self, s=4, locally=False):
        #Checkbox or something to indicate global or local
        self.s = s
        self.locally = locally

    def evaluate(self, individual):
        #Locally implementation first, since its easier
        p = individual.phenotype_container.phenotype
        total = None
        iteration = None
        if self.locally:
            total = len(p)-1
            iteration = 2
        else:
            iteration =len(p)
            total = ((len(p)-1)*(len(p))/2)

        #Penality for nr of not surprising errors
        errors = 0
        for k in range(1, iteration):
            found_sequences = {}
            for i in range(len(p)-k):
                #print("i: ", i, " j ", i+k)
                seq = str(p[i]) + "," + str(p[i+k])
                if seq in found_sequences:
                    errors += 1
                else:
                    found_sequences[seq] = (i, i+k)

        score = 1 - errors/total
        return score
