

class AbstractPhenotype(object):

    def __init__(self):
        pass

class IntegerPhenotype(AbstractPhenotype):

    def __init__(self, phenotype):
        self.phenotype = phenotype

    def __repr__(self):
        return str(self.phenotype)