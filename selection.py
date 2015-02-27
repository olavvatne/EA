from abc import ABCMeta, abstractmethod


class AdultSelectionFactory:
    FULL = "full"
    OVER_PRODUCTION = "over"
    MIXING = "mixing"

    @staticmethod
    def make_adult_selector(selector=FULL):
        selections = {AdultSelectionFactory.FULL: FullReplacementAdultSelection,
                      AdultSelectionFactory.OVER_PRODUCTION: OverProductionAdultSelection,
                      AdultSelectionFactory.MIXING: MixingAdultSelection}
        return selections[selector]()


class AbstractAdultSelection(metaclass=ABCMeta):

    @abstractmethod
    def select(self, adults, children):
        pass


class FullReplacementAdultSelection(AbstractAdultSelection):
    '''
        All Adults from the previous generation are removed from the pool eligible for
        reproduction.
    '''
    def select(self, adults, children):

        return children

class OverProductionAdultSelection(AbstractAdultSelection):
    '''
    Over-production create selection pressure by letting the n children compete for
    the m spots in the adult_pool. This require that more n > m.
    '''
    def select(self, adults, children):
        m = len(adults) #TODO: parameter?
        #TODO: Here a heap would be good?
        return children


class MixingAdultSelection(AbstractAdultSelection):

    def select(self, adults, children):
        return children


