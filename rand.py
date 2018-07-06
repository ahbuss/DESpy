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
        return clazz()

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