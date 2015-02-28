from abc import ABCMeta, abstractmethod
import math
import numpy as np

class ParentSelectionFactory:
    PROPORTIONATE = "proportionate"
    SIGMA = "sigma"
    BOLTZMANN = "boltzmann"
    TOURNAMENT = "tournament"

    @staticmethod
    def make_parent_selector(selector=PROPORTIONATE):
        selectors = {ParentSelectionFactory.PROPORTIONATE: ParentFitnessProportionateSelection,
                     ParentSelectionFactory.SIGMA: ParentSigmaScalingSelection,
                     ParentSelectionFactory.TOURNAMENT: ParentTournamentSelection,
                     ParentSelectionFactory.BOLTZMANN: ParentBoltzmannSelection}
        return selectors[selector]()


class AbstractParentSelection(metaclass=ABCMeta):

    #TODO: Let EA loop update variables here, so more modularity for subclasses
    #TODO: update parameters method
    
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

     def select_mating_pool(self, population, m, t=1):
        fitness = list(adult.fitness for adult in population)
        total = sum(fitness)
        probs = list(f/total for f in fitness)

        return self._global_weighted_select(population, probs, m)


class ParentSigmaScalingSelection(AbstractParentSelection):

    def select_mating_pool(self, population, m, t=1):
        fitness_list = list(a.fitness for a in population)
        avg = sum(fitness_list)/len(population)
        std = np.std(fitness_list)
        exp_values = list((1+((f -avg)/(2*std))) for f in fitness_list)
        for i, v in enumerate(exp_values):
            if v <= 0:
                exp_values[i] = 0.1 #If negative expected value, reset to small positive value so the individual has
                #of getting picked
        s = sum(exp_values)
        probs = list(e/s for e in exp_values)
        return self._global_weighted_select(population, probs, m)


class ParentBoltzmannSelection(AbstractParentSelection):

    def select_mating_pool(self, population, m, t=1):
        temp = list(math.exp(a.fitness/t) for a in population)
        avg = sum(temp)/len(population)
        exp_values = list(c/avg for c in temp)
        s = sum(exp_values)
        probs = list(e/s for e in exp_values)
        return self._global_weighted_select(population, probs, m)


class ParentTournamentSelection(AbstractParentSelection):

     def select_mating_pool(self, adults, m, t=1):
        return adults
