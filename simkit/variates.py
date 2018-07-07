from simkit.rand import RandomVariate
from math import nan

class Constant(RandomVariate):

    def __init__(self):
        RandomVariate.__init__(self)
        self.value = nan

    @property
    def value(self):
        return self.value

    @value.setter
    def value(self, x):
        self.value = x

    def __repr__(self):
        return 'Constant (' + str(self.value) + ')'

    def generate(self):
        return self.value