from abc import abstractmethod
from math import inf
from math import nan
from math import sqrt

from simkit.base import StateChangeListener, SimEntityBase
from simkit.base import EventList
from simkit.base import IndexedStateChangeEvent
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
    def new_observation(self, x):
        self.count += 1
        if x < self.min:
            self.min = x
        if x > self.max:
            self.max = x

    def mean(self):
        return self.mean()

    def __repr__(self):
        return '{name}: {count:,d} {min:,.4f} {max:,.4f} {mean:,.4f} {var:,.4f} {stdev:,.4f}'.\
            format(name=self.name, count=self.count, min=self.min, max=self.max, mean=self.mean,var=self.variance, stdev=self.stdev)

    def state_change(self, state_change_event):
        if state_change_event.name == self.name:
            self.new_observation(state_change_event.value)

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

    def new_observation(self, x):
        SimpleStatsBase.new_observation(self, x)
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
        self.last_value = nan

    def new_observation(self, x):
        SimpleStatsBase.new_observation(self, x)
        if self.count == 1:
            self.mean = self.diff
            self.variance = 0.0
        elif EventList.simtime > self.last_time:
            factor = 1.0 - (self.last_time - self.startTime) / (EventList.simtime - self.startTime)
            self.mean += self.diff * factor
            self.variance += factor * ((1.0 - factor) * self.diff * self.diff -self.variance)
        self.diff = x - self.mean
        self.last_time = EventList.simtime
        self.stdev = sqrt(self.variance)

    def reset(self):
        SimpleStatsBase.reset(self)
        self.diff = 0.0
        self.last_time = 0.0
        self.last_value = nan

    def time_varying_mean(self):
        self.new_observation(self.last_value)
        return self.mean

    def time_varying_variance(self):
        self.new_observation(self.last_value)
        return self.variance

    def time_varying_stdev(self):
        return sqrt(self.time_varying_variance())

    def __repr__(self):
        self.new_observation(self.last_value)
        return '{name}: {count:,d} {min:,.4f} {max:,.4f} {mean:,.4f} {var:,.4f} {stdev:,.4f}'.\
            format(name=self.name, count=self.count, min=self.min, max=self.max, mean=self.mean,var=self.variance, stdev=self.stdev)

class CollectionSizeTimeVarying(SimpleStatsTimeVarying):

    def __init__(self, name='default'):
        SimpleStatsTimeVarying.__init__(self, name)
        self.last_value = []

    def reset(self):
        SimpleStatsTimeVarying.reset(self)
        self.last_value = []

    def new_observation(self, q):
        SimpleStatsTimeVarying.new_observation(self, q.__len__())

class IndexedSimpleStats():

    def __init__(self, name='default'):
        self.stats = {}
        self.name = name

    def reset(self):
        self.stats = {}

    def state_change(self, stateChangeEvent):
        if isinstance(stateChangeEvent, IndexedStateChangeEvent) and stateChangeEvent.name == self.name:
            self.new_observation(stateChangeEvent.index, stateChangeEvent.value)


    @abstractmethod
    def new_observation(self, index, x):
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

    def new_observation(self, index, x):
        if not index in self.stats:
            self.stats[index] = SimpleStatsTally('{name}[{index:d}]'.format(name=self.name, index=index))
        self.stats[index].new_observation(x)

class IndexedSimpleStatsTimeVarying(IndexedSimpleStats):

    def __init__(self, name='default'):
        IndexedSimpleStats.__init__(self, name)

    def new_observation(self, index, x):
        if not index in self.stats:
            self.stats[index] = SimpleStatsTimeVarying('{name}[{index:d}]'.format(name=self.name, index=index))
        self.stats[index].new_observation(x)

    def time_varying_mean(self, index):
        if index in self.stats:
            return self.stats[index].time_varying_mean()
        else:
            return nan

class IndexedCollectionSizeTimeVaryingStat(IndexedSimpleStats):

    def __int__(self,name='default'):
        IndexedSimpleStatsTally.__init__(self)

    def new_observation(self, index, x):
        if not index in self.stats:
            self.stats[index] = CollectionSizeTimeVarying('{name}[{index:d}]'.format(name=self.name, index=index))
        self.stats[index].new_observation(x)

    def time_varying_mean(self, index):
        if index in self.stats:
            return self.stats[index].time_varying_mean()
        else:
            return nan

class TruncatingSimpleStatsTally(SimpleStatsTally):

    def __init__(self, name='default', truncation_point=0):
        SimpleStatsTally.__init__(self, name)
        self.truncated = None
        if truncation_point < 0:
            raise ValueError('truncation_point must be \u2265 0: {tp:d}'.format(tp=truncation_point))
        self.truncation_point = truncation_point

    def reset(self):
        SimpleStatsTally.reset(self)
        self.truncated = False

    def new_observation(self, x):
        SimpleStatsTally.new_observation(self, x)
        if not self.truncated and self.count >= self.truncation_point:
            self.reset()
            self.truncated = True

    def __repr__(self):
        return SimpleStatsTally.__repr__(self) + " [{tp:,d}]".format(tp=self.truncation_point)

class TruncatingSimpleStatsTimeVarying(SimpleStatsTimeVarying):

    def __init__(self, truncation_point, name='default'):
        SimpleStatsTimeVarying.__init__(self, name)
        self.truncation_point = truncation_point
        if truncation_point < 0.0:
            raise ValueError('truncation_point must be \u2265 0: {tp:,.f}'.format(tp=truncation_point))
        self.truncated = None
        self.reset()
        self.truncate = TruncatingSimpleStatsTimeVarying.Truncate()
        self.truncate.truncation_point = self.truncation_point
        self.truncate.outer = self

    def truncation_reset(self):
        last_value = self.last_value
        SimpleStatsTimeVarying.reset(self)
        self.lastTime = EventList.simtime
        self.truncated = False
        self.last_value = last_value

    def new_observation(self, x):
        SimpleStatsTimeVarying.new_observation(self, x)

    class Truncate(SimEntityBase):

        def __int__(self):
            SimEntityBase.__init__(self)
            self.outer = None
            self.truncation_point = nan

        def run(self):
            self.schedule('truncate', self.outer.truncation_point)

        def truncate(self):
            self.outer.truncation_reset()




