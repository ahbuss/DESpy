from abc import ABC
from abc import abstractmethod
from random import Random
from math import log
from math import nan
from math import exp
from math import sqrt
from sys import modules

class RandomVariate(ABC):
    baseRNG = Random(12345)

    @staticmethod
    def getInstance(name, module='simkit.rand', **kwds):
        clazz = getattr(modules[module],name)
        instance = clazz()
        for keyword in kwds.keys():
            if hasattr(instance, keyword):
                setattr(instance, keyword, kwds[keyword])
        if hasattr(instance, 'normalize'):
            getattr(instance, 'normalize')()
        return instance

    def __init__(self):
        self.setRNG(RandomVariate.baseRNG)
        self.originalState = self.rng.getstate()

    @abstractmethod
    def generate(self):
        pass

    def setRNG(self, rng):
        self.rng = rng

    def setSeed(self, seed):
        self.rng.seed(seed)

    def resetState(self):
        self.rng.setstate(self.originalState)

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
        return 'Exponential ({mean:.3f})'.format(mean=self.mean)

class Gamma(RandomVariate):
    def __init__(self, alpha=nan, beta=nan):
        RandomVariate.__init__(self)
        self.alpha = alpha
        self.beta = beta

    def generate(self):
        return self.baseRNG.gammavariate(self.alpha, self.beta)

    def __repr__(self):
        return 'Gamma ({alpha:.3f}, {beta:.3f})'.format(alpha=self.alpha, beta=self.beta)

class Beta(RandomVariate):
    def __init__(self,alpha=nan, beta=nan):
        RandomVariate.__init__(self)
        self.alpha = alpha
        self.beta = beta

    def generate(self):
        return self.rng.betavariate(self.alpha, self.beta)

    def __repr__(self):
        return 'Beta ({alpha:.3f}, {beta:.3f})'.format(alpha=self.alpha, beta=self.beta)

class Uniform(RandomVariate):
    def __init__(self, min=nan, max=nan):
        RandomVariate.__init__(self)
        self.min = min
        self.max = max

    def generate(self):
        return self.min + (self.max - self.min) * self.rng.random()

    def __repr__(self):
        return 'Uniform ({min:.3f}, {max:.3f})'.format(min=self.min, max=self.max)

class Constant(RandomVariate):

    def __init__(self, value=nan):
        self.value = value

    def __repr__(self):
        return 'Constant ({value:.3f})'.format(value=self.value)

    def generate(self):
        return self.value

class Triangular(RandomVariate):

    def __init__(self, min=nan, mode=nan, max=nan):
        RandomVariate.__init__(self)
        self.min = min
        self.mode = mode
        self.max = max

    def generate(self):
        return self.rng.triangular(self.min, self.max, self.mode)

    def __repr__(self):
        return 'Triangular ({min:.3f}, {max:.3f}, {mode:.3f})'.format(min=self.min, max=self.max, mode=self.mode)

class Normal(RandomVariate):
    def __init__(self, mean=0.0, stdev=1.0):
        RandomVariate.__init__(self)
        self.mean = mean
        self.stdev = stdev

    def generate(self):
        return self.rng.gauss(self.mean, self.stdev)

    def __repr__(self):
        return 'Normal ({mean:.3f}, {stdev:.3f})'.format(mean=self.mean, stdev=self.stdev)

class DiscreteUniform(RandomVariate):

    def __init__(self, min=nan, max=nan):
        RandomVariate.__init__(self)
        self.min = min
        self.max = max

    def __repr__(self):
        return 'Discrete Uniform ({min:d}, {max:d})'.format(min=self.min, max=self.max)

    def generate(self):
        return self.rng.randint(self.min, self.max)

class Poisson(RandomVariate):
    def __init__(self, mean=nan):
        RandomVariate.__init__(self)
        self.mean = mean

    def normalize(self):
        self.a = exp(-self.mean)
        self.sqrtmean = sqrt(self.mean)

    def generate(self):
        if self.mean < 100.0:
            x = 0
            y = self.rng.random()
            while y >= self.a:
                x += 1
                y *= self.rng.random()
        else:
            x = self.rng.normalvariate(self.mean, self.sqrtmean) + 0.5
        return x

    def __repr__(self):
        return 'Poisson ({mean:.3f})'.format(mean=self.mean)

class Binomial(RandomVariate):
    def __init__(self, n=nan, p=nan):
        RandomVariate.__init__(self)
        self.n = n
        self.p = p

    def generate(self):
        x = 0
        for i in range(self.n):
            if self.rng.random() < self.p:
                x += 1
        return x

    def __repr__(self):
        return 'Binomial ({n:d}, {p:.3f})'.format(n=self.n,p=self.p)

class Geometric(RandomVariate):

    def __init__(self, p=nan):
        RandomVariate.__init__(self)
        self.p = p

    def normalize(self):
        self.multiplier = 1.0 / log(1.0 - self.p)

    def generate(self):
        return round(log(self.rng.random()) * self.multiplier)

    def __repr__(self):
        return 'Geormetric: {p:f}'.format(p=self.p)

class Discrete(RandomVariate):

    def __init__(self, values=[], frequencies=[]):
        RandomVariate.__init__(self)
        self.values = values
        self.frequencies = frequencies
        if len(values) != len(frequencies):
            raise ValueError('values and frequencies must have the same length: {v:d}  {f:d}'.\
                             format(v=len(values), f=len(frequencies)))

    def normalize(self):
        cumulative = 0.0
        for freq in self.frequencies:
            cumulative += freq
        self.probabilities = []
        for freq in self.frequencies:
            self.probabilities.append(freq / cumulative)
        self.cdf = []
        self.cdf.append(self.probabilities[0])
        for i in range(1,len(self.probabilities)):
            self.cdf.append(self.cdf[i - 1] + self.probabilities[i])

    def generate(self):
        u = self.rng.random()
        index = 0
        while u > self.cdf[index] and index < len(self.probabilities) - 1:
            index += 1
        return self.values[index]

    def __repr__(self):
        return 'Discrete (' + str(self.values) + '=>' +str(self.probabilities) + ')'



