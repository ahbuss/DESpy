from abc import ABC
from abc import abstractmethod
from random import Random
from math import log


class RandomVariate(ABC):
    baseRNG = Random(12345)

    # How to use reflection for this??
    @staticmethod
    def getInstance(name, *args):
        if name == 'Exponential':
            return ExponentialVariate(args[0])

    def __init__(self):
        self.setRNG(RandomVariate.baseRNG)

    @abstractmethod
    def generate(self):
        pass

    def setRNG(self, rng):
        self.rng = rng

    def setSeed(self, seed):
        self.rng.seed(seed)

class ExponentialVariate(RandomVariate):

    def __init__(self, mean):
        RandomVariate.__init__(self)
        self.mean = mean

    def generate(self):
        return -self.mean * log(self.rng.random())

    def __repr__(self):
        return 'Exponential (' + str(self.mean) + ')'