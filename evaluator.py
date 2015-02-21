from abc import ABCMeta, abstractmethod

def AbstractFitnessEvaluator(metaclass=ABCMeta):

    @abstractmethod
    def evaluate(self, population):
        pass
