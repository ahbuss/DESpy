from abc import abstractmethod
from math import inf
from math import nan
from math import sqrt
from simkit.simkit import StateChangeListener
from simkit.simkit import EventList
from simkit.simkit import IndexedStateChangeEvent
from simkit.quantiles import student_t

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

    def state_change(self, state_change_event):
        if state_change_event.name == self.name:
            self.newObservation(state_change_event.value)

    def halfwidth(self, p):
        if self.count > 1:
            quantile = student_t(p, self.count - 1)
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
        self.startTime = EventList.simtime
        self.reset()

    def newObservation(self, x):
        SimpleStatsBase.newObservation(self,x)
        if self.count == 1:
            self.mean = self.diff
            self.variance = 0.0
        elif EventList.simtime > self.lastTime:
            factor = 1.0 - (self.lastTime - self.startTime) /(EventList.simtime - self.startTime)
            self.mean += self.diff * factor
            self.variance += factor * ((1.0 - factor) * self.diff * self.diff -self.variance)
        self.diff = x - self.mean
        self.lastTime = EventList.simtime
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

class IndexedSimpleStats():

    def __init__(self, name='default'):
        self.stats = {}
        self.name = name

    def reset(self):
        self.stats = {}

    def stateChange(self, stateChangeEvent):
        if isinstance(stateChangeEvent, IndexedStateChangeEvent) and stateChangeEvent.name == self.name:
            self.newObservation(stateChangeEvent.index, stateChangeEvent.value)


    @abstractmethod
    def newObservation(self, index, x):
        pass

    def mean(self, index):
        if index in self.stats:
            return self.stats[index].mean
        else:
            return nan

    def variance(self, index):
        if index in self.stats:
            return self.stats[index].variance
        else:
            return nan

    def stdev(self, index):
        if index in self.stats:
            return self.stats[index].stdev
        else:
            return nan

    def count(self, index):
        if index in self.stats:
            return self.stats[index].count
        else:
            return nan

    def min(self, index):
        if index in self.stats:
            return self.stats[index].min
        else:
            return nan

    def max(self, index):
        if index in self.stats:
            return self.stats[index].max
        else:
            return nan

    def __repr__(self):
        ret = self.name
        keys = sorted(self.stats.keys())
        for index in keys:
            ret += '\n{stat}'.format(stat=self.stats[index])
        return ret

class IndexedSimpleStatsTally(IndexedSimpleStats):

    def __init__(self, name='default'):
        IndexedSimpleStats.__init__(self, name)

    def newObservation(self, index, x):
        if index in self.stats:
            self.stats[index].newObservation(x)
        else:
            self.stats[index] = SimpleStatsTally('{name}[{index:d}]'.format(name=self.name, index=index))

class IndexedSimpleStatsTimeVarying(IndexedSimpleStats):

    def __init__(self, name='default'):
        IndexedSimpleStats.__init__(self, name)

    def newObservation(self, index, x):
        if index in self.stats:
            self.stats[index].newObservation(x)
        else:
            self.stats[index] = SimpleStatsTimeVarying('{name}[{index:d}]'.format(name=self.name, index=index))
