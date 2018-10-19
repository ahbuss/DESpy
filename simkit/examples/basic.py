from simkit.base import SimEntityBase
from simkit.base import EventList
from simkit.base import Priority
from math import nan
from random import Random

rng = Random(12345)

class SingleResourceModel(SimEntityBase):

    def __init__(self, interarrival_time_generator, service_time_generator):
        SimEntityBase.__init__(self)
        self.interarrival_time_generator = interarrival_time_generator
        self.service_time_generator = service_time_generator
        self.number_in_queue = nan
        self.number_available_resources = nan

    def reset(self):
        SimEntityBase.reset(self)
        self.number_in_queue = 0
        self.number_available_resources = 1

    def run(self):
        self.notify_state_change('number_in_queue', self.number_in_queue)
        self.notify_state_change('number_available_resources', self.number_available_resources)

        self.schedule('enter', 0.0)

    def enter(self):
        self.number_in_queue += 1
        self.notify_state_change('number_in_queue', self.number_in_queue)

        if (self.number_available_resources > 0):
            self.schedule('start', 0.0)

        self.schedule('enter', self.interarrival_time_generator.generate())

    def start(self):
        self.number_in_queue -= 1
        self.notify_state_change('number_in_queue', self.number_in_queue)

        self.number_available_resources -= 1
        self.notify_state_change('number_available_resources', self.number_available_resources)

        self.schedule('leave', self.service_time_generator.generate())

    def leave(self):
        self.number_available_resources += 1
        self.notify_state_change('number_available_resources', self.number_available_resources)

        if self.number_in_queue > 0:
            self.schedule('start', 0.0)

class ClosingTimes(SimEntityBase):
    def __init(self,interarrival_time_generator, service_time_generator, closing_time):
        SimEntityBase.__init__(self)
        self.interarrival_time_generator = interarrival_time_generator
        self.service_time_generator = service_time_generator
        self.closing_time = closing_time

    def reset(self):
        SimEntityBase.reset(self)
        self.number_in_queue = 0
        self.number_available_resources = 1

    def run(self):
        self.notify_state_change('number_in_queue', self.number_in_queue)
        self.notify_state_change('number_available_resources', self.number_available_resources)

        self.schedule('arrive', 0.0)

    def arrive(self):

        if EventList.simtime < self.closing_time:
            self.schedule('enter', 0.0)

        self.schedule('arrive', self.interarrival_time_generator.generate())

    def enter(self):
        self.number_in_queue += 1
        self.notify_state_change('number_in_queue', self.number_in_queue)

        if (self.number_available_resources == 1):
            self.schedule('start', 0.0)


    def start(self):
        self.number_in_queue -= 1
        self.notify_state_change('number_in_queue', self.number_in_queue)

        self.number_available_resources -= 1
        self.notify_state_change('number_available_resources', self.number_available_resources)

        self.schedule('leave', self.service_time_generator.generate())

    def leave(self):
        self.number_available_resources += 1
        self.notify_state_change('number_available_resources', self.number_available_resources)

        if self.number_in_queue > 0:
            self.schedule('start', 0.0)

class MultipleResourceModel(SimEntityBase):

    def __init__(self, interarrival_time_generator, service_time_generator, number_resources):
        SimEntityBase.__init__(self)
        self.interarrival_time_generator = interarrival_time_generator
        self.service_time_generator = service_time_generator
        self.number_resources = number_resources
        self.number_in_queue = nan
        self.number_available_resources = nan

    def reset(self):
        SimEntityBase.reset(self)
        self.number_in_queue = 0
        self.number_available_resources = self.number_resources

    def run(self):
        self.notify_state_change('number_in_queue', self.number_in_queue)
        self.notify_state_change('number_available_resources', self.number_available_resources)

        self.schedule('enter', 0.0)

    def enter(self):
        self.number_in_queue += 1
        self.notify_state_change('number_in_queue', self.number_in_queue)

        if self.number_available_resources > 0:
            self.schedule('start', 0.0)

        self.schedule('enter', self.interarrival_time_generator.generate())

    def start(self):
        self.number_in_queue -= 1
        self.notify_state_change('number_in_queue', self.number_in_queue)

        self.number_available_resources -= 1
        self.notify_state_change('number_available_resources', self.number_available_resources)

        self.schedule('leave', self.service_time_generator.generate())

    def leave(self):
        self.number_available_resources += 1
        self.notify_state_change('number_available_resources', self.number_available_resources)

        if self.number_in_queue > 0:
            self.schedule('start', 0.0)

class BatchedServiceModel(SimEntityBase):

    def __init__(self, interarrival_time_generator, service_time_generator, number_resources, batch_size):
        SimEntityBase.__init__(self)
        self.interarrival_time_generator = interarrival_time_generator
        self.service_time_generator = service_time_generator
        self.number_resources = number_resources
        self.batch_size = batch_size
        self.number_in_queue = nan
        self.number_available_resources = nan

    def reset(self):
        SimEntityBase.reset(self)
        self.number_in_queue = 0
        self.number_available_resources = self.number_resources

    def run(self):
        self.notify_state_change('number_in_queue', self.number_in_queue)
        self.notify_state_change('number_available_resources', self.number_available_resources)

        self.schedule('enter', 0.0)

    def enter(self):
        self.number_in_queue += 1
        self.notify_state_change('number_in_queue', self.number_in_queue)

        if self.number_available_resources > 0 & self.number_in_queue >= self.batch_size:
            self.schedule('start', 0.0)

        self.schedule('enter', self.interarrival_time_generator.generate())

    def start(self):
        self.number_in_queue -= 1
        self.notify_state_change('number_in_queue', self.number_in_queue)

        self.number_available_resources -= 1
        self.notify_state_change('number_available_resources', self.number_available_resources)

        self.schedule('leave', self.service_time_generator.generate())

    def leave(self):
        self.number_available_resources += 1
        self.notify_state_change('number_available_resources', self.number_available_resources)

        if self.number_in_queue > self.batch_size:
            self.schedule('start', 0.0)

class ReworkModel(SimEntityBase):

    def __init__(self, interarrival_time_generator, service_time_generator, prob_needs_rework):
        SimEntityBase.__init__(self)
        self.interarrival_time_generator = interarrival_time_generator
        self.service_time_generator = service_time_generator
        self.prob_needs_rework = prob_needs_rework
        self.number_in_queue = nan
        self.number_available_resources = nan

    def reset(self):
        SimEntityBase.reset(self)
        self.number_in_queue = 0
        self.number_available_resources = 1

    def run(self):
        self.notify_state_change('number_in_queue', self.number_in_queue)
        self.notify_state_change('number_available_resources', self.number_available_resources)

        self.schedule('enter', 0.0)

    def enter(self):
        self.number_in_queue += 1
        self.notify_state_change('number_in_queue', self.number_in_queue)

        if self.number_available_resources > 0:
            self.schedule('start', 0.0)

        self.schedule('enter', self.interarrival_time_generator.generate())

    def start(self):
        self.number_in_queue -= 1
        self.notify_state_change('number_in_queue', self.number_in_queue)

        self.number_available_resources -= 1
        self.notify_state_change('number_available_resources', self.number_available_resources)

        self.schedule('leave', self.service_time_generator.generate())

    def leave(self):
        self.number_available_resources += 1
        self.notify_state_change('number_available_resources', self.number_available_resources)

        rw = rng.random()

        if self.number_in_queue > 0 & rw > self.prob_needs_rework:
            self.schedule('start', 0.0)

        if rw <= self.prob_needs_rework:
            self.schedule('rework', 0.0)

    def rework(self):
        self.number_in_queue += 1;
        self.notify_state_change('number_in_queue', self.number_in_queue)

        if self.number_available_resources > 0:
            self.schedule('start', 0.0)