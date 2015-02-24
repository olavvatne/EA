from abc import ABCMeta, abstractmethod
import random

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
    def select_mating_pool(self, adults):
        pass


class ParentFitnessProportionateSelection(AbstractParentSelection):

     def select_mating_pool(self, population):
        #TODO:Should method return mating pairs or children directy.
        #TODO: Semantically it is best to return pairs and let another method combine them
        max = sum(adult.fitness for adult in population)
        mate_pool = []
        for i in range(len(population)):
            a1 = self.pick_adult(population, random.uniform(0, max))
            a2 = self.pick_adult(population, random.uniform(0, max))
            mate_pool.append((a1, a2))

        return mate_pool

     def pick_adult(self, population, pick):
        current = 0
        for adult in population:
            current += adult.fitness
            if current > pick:
                return adult

class ParentSigmaScalingSelection(AbstractParentSelection):

     def select_mating_pool(self, adults):
        return adults


class ParentTournamentSelection(AbstractParentSelection):

     def select_mating_pool(self, adults):
        return adults