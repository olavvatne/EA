from abc import ABCMeta, abstractmethod
import random
import statistics

import numpy as np

#Tournament selection
#Sigma scaling
#fitness proportionate
#...Maybe bolztmann as fourth


class ParentSelectionFactory:
    PROPORTIONATE = "proportionate"
    SIGMA = "sigma"
    TOURNAMENT = "tournament"

    @staticmethod
    def make_parent_selector(selector=PROPORTIONATE):
        selectors = {ParentSelectionFactory.PROPORTIONATE: ParentFitnessProportionateSelection,
                     ParentSelectionFactory.SIGMA: ParentSigmaScalingSelection,
                     ParentSelectionFactory: ParentTournamentSelection}
        return selectors[selector]()


class AbstractParentSelection(metaclass=ABCMeta):

    @abstractmethod
    def select_mating_pool(self, adults, m):
        pass

    def _weighted_parent_choice(self, pop, prob):
        return np.random.choice(pop, p=prob), np.random.choice(pop, p=prob)

    def _global_weighted_select(self, population, probs,  m):
        mate_pool = []
        for i in range(int(m/2)):
            mate_pool.append(self._weighted_parent_choice(population, probs))
        return mate_pool

class ParentFitnessProportionateSelection(AbstractParentSelection):

     def select_mating_pool(self, population, m):
        fitness = list(adult.fitness for adult in population)
        total = sum(fitness)
        probs = list(f/total for f in fitness)

        return self._global_weighted_select(population, probs, m)

class ParentSigmaScalingSelection(AbstractParentSelection):

    def select_mating_pool(self, population, m):
        fitness = list(a.fitness for a in population)
        avg = sum(fitness)/len(population)
        std = statistics.pstdev(fitness)
        exp_values = list((1+((f - avg)/2*std)) for f in fitness)
        probs = list(e/len(population) for e in exp_values)

        return self._global_weighted_select(population, probs, m)


class ParentTournamentSelection(AbstractParentSelection):

     def select_mating_pool(self, adults, m):
        return adults