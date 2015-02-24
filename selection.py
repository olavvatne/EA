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

    def select(self, adults, children):
        '''
        All Adults from the previous generation are removed from the pool eligible for
        reproduction.
        '''
        return children

class OverProductionAdultSelection(AbstractAdultSelection):

    def select(self, adults, children):
        pass


class MixingAdultSelection(AbstractAdultSelection):

    def select(self, adults, children):
        pass


