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
    def instance(name, module='simkit.rand', **kwds):
        """

        :param name: The name of the random variate ('Exponential', 'Gamma', etc)
        :param module: The module it is in (default is 'simkit.rand'
        :param kwds: named parameters for the random variate class; specifics depend on the class
                    or a dictionary with the RandomVariate parameters as key=value pairs
        :return: The desired instance of the random variate class
        """
        clazz = getattr(modules[module],name)
        instance = clazz()
        if kwds.keys().__contains__('params'):
            params = kwds.get('params')
        else:
            params = kwds
        for keyword in params.keys():
            if hasattr(instance, keyword):
                setattr(instance, keyword, params[keyword])
        if hasattr(instance, 'normalize'):
            getattr(instance, 'normalize')()
        return instance

    def __init__(self):
        self.rng(RandomVariate.baseRNG)
        self.originalState = self.rng.getstate()

    @abstractmethod
    def generate(self):
        pass

    def rng(self, rng):
        self.rng = rng

    def seed(self, seed):
        self.rng.seed(seed)

    def reset(self):
        self.rng.setstate(self.originalState)

class Exponential(RandomVariate):

    def __init__(self, mean=nan):
        """

        :param mean: Mean of the Exponential random variates generated
        """
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
        """

        :param alpha: \u03B1 of the Gamma distribution (shape parameter)
        :param beta: \u0B32 of the Gamma distribution (scale parameter)
        """
        RandomVariate.__init__(self)
        self.alpha = alpha
        self.beta = beta

    def generate(self):
        return self.baseRNG.gammavariate(self.alpha, self.beta)

    def __repr__(self):
        return 'Gamma ({alpha:.3f}, {beta:.3f})'.format(alpha=self.alpha, beta=self.beta)

class Beta(RandomVariate):
    def __init__(self,alpha=nan, beta=nan, shift=0.0, scale=1.0):
        """

        :param alpha: \u03B1 of the Beta distribution (shape parameter)
        :param beta: \u0B32 of the Beta distribution (shape parameter)
        """
        RandomVariate.__init__(self)
        self.alpha = alpha
        self.beta = beta
        self.scale = scale
        self.shift = shift

    def generate(self):
        return self. shift + self.scale * self.rng.betavariate(self.alpha, self.beta)

    def __repr__(self):
        if self.scale == 1.0 and self.shift == 0.0:
            return 'Beta ({alpha:.3f}, {beta:.3f})'.format(alpha=self.alpha, beta=self.beta)
        else:
            return 'Beta ({alpha:.3f}, {beta:.3f}, {shift:.3f}, {scale:.3f})'.\
                format(alpha=self.alpha, beta=self.beta, shift=self.shift, scale=self.scale)

class Uniform(RandomVariate):
    def __init__(self, min=nan, max=nan):
        """

        :param min: Minimum value
        :param max: Maximum value
        """
        RandomVariate.__init__(self)
        self.min = min
        self.max = max

    def generate(self):
        return self.min + (self.max - self.min) * self.rng.random()

    def __repr__(self):
        return 'Uniform ({min:.3f}, {max:.3f})'.format(min=self.min, max=self.max)

class Constant(RandomVariate):

    def __init__(self, value=nan):
        """

        :param value: The one value that will always be generated
        """
        self.value = value

    def __repr__(self):
        return 'Constant ({value:.3f})'.format(value=self.value)

    def generate(self):
        return self.value

class Triangular(RandomVariate):

    def __init__(self, min=nan, mode=nan, max=nan):
        """

        :param min: Minimum value of triangle
        :param mode: Mode (point) of triangle
        :param max: Maximum value of triangle
        """
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
        """

        :param mean: \u03BC of Normal distribution (defaults to 0.0)
        :param stdev: \u03C3 of Normal distribution (defaults to 1.0)
        """
        RandomVariate.__init__(self)
        self.mean = mean
        self.stdev = stdev

    def generate(self):
        return self.rng.gauss(self.mean, self.stdev)

    def __repr__(self):
        return 'Normal ({mean:.3f}, {stdev:.3f})'.format(mean=self.mean, stdev=self.stdev)

class TruncatedNormal(Normal):
    def __init__(self, mean=0.0, stdev=1.0, trunc=0.0):
        Normal.__init__(self, mean, stdev)
        self.trunc = trunc

    def generate(self):
        x = Normal.generate(self)
        return max(x, self.trunc)

    def __repr__(self):
        return 'Truncated Normal ({mean:.3f}, {stdev:.3f} {trunc:.3f})'.format(mean=self.mean, stdev=self.stdev, trunc=self.trunc)

class ResampledNormal(Normal):
    def __init__(self, mean=0.0, stdev=1.0, trunc=0.0):
        Normal.__init__(self, mean, stdev)
        self.trunc = trunc

    def generate(self):
        x = Normal.generate(self)
        while x < self.trunc:
            x = Normal.generate(self)
        return x

    def __repr__(self):
        return 'Resampled Normal ({mean:.3f}, {stdev:.3f} {trunc:.3f})'.format(mean=self.mean, stdev=self.stdev, trunc=self.trunc)


class Weibull(RandomVariate):
    def __init__(self, shape=1, scale=1):
        RandomVariate.__init__(self)
        self.shape=shape
        self.scale = scale

    def generate(self):
        return self.scale * (-log(self.rng.random()))**(1.0 / self.shape)

    def __repr__(self):
        return "Weibull ({shape:.3f}, {scale:.3f})".format(shape=self.shape, scale=self.scale)

class DiscreteUniform(RandomVariate):

    def __init__(self, min=nan, max=nan):
        """

        :param min: Min value (should be int)
        :param max: Max value (should be int)
        """
        RandomVariate.__init__(self)
        self.min = min
        self.max = max

    def __repr__(self):
        return 'Discrete Uniform ({min:d}, {max:d})'.format(min=self.min, max=self.max)

    def generate(self):
        return self.rng.randint(self.min, self.max)

class Poisson(RandomVariate):
    def __init__(self, mean=nan):
        """

        :param mean: Mean of the Poisson distribution
        """
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
        """

        :param n: Maximum possible value of Binomial
        :param p: Probability of 'success'
        """
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
        """

        :param p: Probability if 'success' for Geometric distribution
        """
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
        """

        :param values: Possible values to be generated
        :param frequencies: Frequencies of respective values; must be non-negative, but need not sum to 1.0
        """
        RandomVariate.__init__(self)
        self.values = values
        self.frequencies = frequencies
        if len(values) != len(frequencies):
            raise ValueError('values and frequencies must have the same length: {v:d}  {f:d}'.\
                             format(v=len(values), f=len(frequencies)))

    def normalize(self):
        """
        Computes the probabilities and cumulative probabilities based on the passed-in frequencies
        """
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



