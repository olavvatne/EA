from abc import ABCMeta, abstractmethod
import sys
from config.configuration import Configuration
class AdultSelectionFactory:
    FULL = "full"

    @staticmethod
    def make_adult_selector(selector=FULL):
        selections = Configuration.get()["adult_selection"]
        return  getattr(sys.modules[__name__], selections[selector]["class_name"])()


class AbstractAdultSelection(metaclass=ABCMeta):

    @abstractmethod
    def select(self, adults, children):
        pass


class FullReplacementAdultSelection(AbstractAdultSelection):
    '''
        All Adults from the previous generation are removed from the pool eligible for
        reproduction.
    '''
    def select(self, adults, children, m):

        return children

class OverProductionAdultSelection(AbstractAdultSelection):
    '''
    Over-production create selection pressure by letting the n children compete for
    the m spots in the adult_pool. This require that more n > m.
    '''
    def select(self, adults, children, m):
        #TODO: Here a heap would be good?
        adult_pool = sorted(children, key=lambda child:child.fitness, reverse=True)
        return adult_pool[:m]


class MixingAdultSelection(AbstractAdultSelection):

    def select(self, adults, children, m):
        #TODO. Maybe heap impl for lists?
        mix = adults + children
        adult_pool = sorted(mix, key=lambda individual:individual.fitness, reverse=True)
        return adult_pool[:m]


