from abc import ABC
from abc import abstractmethod
from random import Random
from math import log
from math import nan
from sys import modules

class RandomVariate(ABC):
    baseRNG = Random(12345)

    @staticmethod
    def getInstance(name, module='rand', **kwds):
        clazz = getattr(modules[module],name)
        instance = clazz()
        for keyword in kwds.keys():
            if hasattr(instance, keyword):
                setattr(instance, keyword, kwds[keyword])
        return instance

    def __init__(self):
        self.setRNG(RandomVariate.baseRNG)

    @abstractmethod
    def generate(self):
        pass

    def setRNG(self, rng):
        self.rng = rng

    def setSeed(self, seed):
        self.rng.seed(seed)

class Exponential(RandomVariate):

    def __init__(self, mean=nan):
        RandomVariate.__init__(self)
        self.__mean = mean

    @property
    def mean(self):
        return self.__mean

    @mean.setter
    def mean(self, mean):
       if mean <= 0:
           raise ValueError('mean must be > 0:')

       self.__mean = mean


    def generate(self):
        return -self.mean * log(self.rng.random())

    def __repr__(self):
        return 'Exponential (' + str(self.mean) + ')'

class Gamma(RandomVariate):
    def __init__(self, alpha=nan, beta=nan):
        RandomVariate.__init__(self)
        self.alpha = alpha
        self.beta = beta

    def generate(self):
        return self.baseRNG.gammavariate(self.alpha, self.beta)

    def __repr__(self):
        return 'Gamma (' + str(self.alpha) +', ' + str(self.beta) + ')'

class Uniform(RandomVariate):
    def __init__(self, min=nan, max=nan):
        self.min = min
        self.max = max

    def generate(self):
        return self.baseRNG.uniform(self.min, self.max)

    def __repr__(self):
        return 'Uniform (' + str(self.min) + ',' + str(self.max) + ')'