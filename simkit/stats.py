from abc import abstractmethod
from math import inf
from math import nan
from math import sqrt
from simkit.simkit import StateChangeListener
from simkit.simkit import EventList
from simkit.quantiles import studentT

class SimpleStatsBase(StateChangeListener):

    def __init__(self, name="default"):
        self.min = inf
        self.max = -inf
        self.count = 0
        self.mean = 0.0
        self.diff = 0.0
        self.variance = 0.0
        self.stdev = 0.0
        self.name = name

    def reset(self):
        self.min = inf
        self.max = -inf
        self.count = 0
        self.mean = 0.0
        self.diff = 0.0
        self.variance = 0.0
        self.stdev = 0.0

    @abstractmethod
    def newObservation(self, x):
        self.count += 1
        if x < self.min:
            self.min = x
        if x > self.max:
            self.max = x

    def __repr__(self):
        return '{name}: {count:,d} {min:,.4f} {max:,.4f} {mean:,.4f} {var:,.4f} {stdev:,.4f}'.\
            format(name=self.name, count=self.count, min=self.min, max=self.max, mean=self.mean,var=self.variance, stdev=self.stdev)

    def stateChange(self, stateChangeEvent):
        if stateChangeEvent.name == self.name:
            self.newObservation(stateChangeEvent.value)

    def halfwidth(self, p):
        if self.count > 1:
            quantile = studentT(p, self.count - 1)
        else:
            quantile = inf
        return self.stdev / self.count * quantile

class SimpleStatsTally(SimpleStatsBase):

    def __init__(self, name='default'):
        SimpleStatsBase.__init__(self, name)
        self.reset()

    def newObservation(self, x):
        SimpleStatsBase.newObservation(self,x)
        self.diff = x - self.mean
        self.mean += self.diff / self.count
        if self.count == 1:
            self.variance += 0.0
        else:
            self.variance += self.diff * self.diff / self.count - 1.0 / (self.count - 1) * self.variance
        self.stdev = sqrt(self.variance)

    def reset(self):
        SimpleStatsBase.reset(self)
        self.diff = 0.0

class SimpleStatsTimeVarying(SimpleStatsBase):

    def __init__(self, name='default'):
        SimpleStatsBase.__init__(self, name)
        self.startTime = EventList.simTime
        self.reset()

    def newObservation(self, x):
        SimpleStatsBase.newObservation(self,x)
        if self.count == 1:
            self.mean = self.diff
            self.variance = 0.0
        elif EventList.simTime > self.lastTime:
            factor = 1.0 - (self.lastTime - self.startTime) /(EventList.simTime - self.startTime)
            self.mean += self.diff * factor
            self.variance += factor * ((1.0 - factor) * self.diff * self.diff -self.variance)
        self.diff = x - self.mean
        self.lastTime = EventList.simTime
        self.stdev = sqrt(self.variance)

    def reset(self):
        SimpleStatsBase.reset(self)
        self.diff = 0.0
        self.lastTime = 0.0
        self.lastValue = nan

class CollectionSizeTimeVarying(SimpleStatsTimeVarying):

    def __init__(self, name='default'):
        SimpleStatsTimeVarying.__init__(self, name)

    def newObservation(self, q):
        SimpleStatsTimeVarying.newObservation(self, q.__len__())
