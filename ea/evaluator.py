from abc import ABCMeta, abstractmethod
import numpy as np
import sys
from config.configuration import Configuration

class FitnessEvaluatorFactory:
    DEFAULT = "default"

    @staticmethod
    def make_fitness_evaluator(genome_length, evaluator=DEFAULT):
        selected = Configuration.get()["fitness"][evaluator]
        config = selected["parameters"]
        return getattr(sys.modules[__name__], selected["class_name"])(genome_length, **config)


class AbstractFitnessEvaluator(metaclass=ABCMeta):

    def __init__(self, genome_length, **kwargs):
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

    def __init__(self, genome_length, random_target=False):
        if random_target:
            self.target = np.random.randint(2, size=genome_length)
            print("RANDOM TARGET: ", self.target)
        else:
            self.target = np.ones(genome_length, dtype=np.int)

    def evaluate(self, individual):
        p = individual.phenotype_container.phenotype
        d = sum(p[i] == self.target[i] for i in range(p.size))
        return (d / p.size)


class LeadingFitnessEvaluator(AbstractFitnessEvaluator):
    #For LOLZ prefix problem

    def __init__(self, genome_length, z=4):
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
    #For Surprising sequence problem

    def __init__(self, genome_length, locally=False):
        #Checkbox or something to indicate global or local
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

                seq = str(p[i]) + "," + str(p[i+k])
                if seq in found_sequences:
                    errors += 1
                else:
                    found_sequences[seq] = (i, i+k)


        score = 1 - errors/total
        #score = 1/(1.+errors)
        return score
