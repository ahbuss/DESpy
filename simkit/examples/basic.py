from math import nan
from random import Random
from heapq import heappush
from heapq import heappop

from simkit.base import SimEntityBase
from simkit.base import EventList
from simkit.base import Priority
from simkit.base import Entity


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

class TandemQueueWithBlocking(SimEntityBase):

    def __init__(self, interarrival_time_generator, number_server1, number_server2, \
                 service_time1_generator, service_time2_generator, buffer_size):
        SimEntityBase.__init__(self)
        # Parameters
        self.interarrival_time_generator = interarrival_time_generator
        self.number_server1 = number_server1
        self.number_server2 = number_server2
        self.service_time1_generator = service_time1_generator
        self.service_time2_generator = service_time2_generator
        self.buffer_size = buffer_size
         # State variables
        self.number_in_queue1 = nan
        self.number_in_queue2 = nan
        self.number_available_server1 = nan
        self.number_available_server2 = nan
        self.number_blocked = nan

    def reset(self):
        SimEntityBase.reset(self)
        self.number_in_queue1 = 0
        self.number_in_queue2 = 0
        self.number_available_server1 = self.number_server1
        self.number_available_server2 = self.number_server2
        self.number_blocked = 0

    def run(self):
        self.notify_state_change('number_in_queue1', self.number_in_queue1)
        self.notify_state_change('number_in_queue2', self.number_in_queue2)
        self.notify_state_change('number_available_server1', self.number_available_server1)
        self.notify_state_change('number_available_server2', self.number_available_server2)
        self.notify_state_change('number_blocked', self.number_blocked)

        self.schedule('enter1', 0.0)

    def enter1(self):
        self.number_in_queue1 += 1
        self.notify_state_change('number_in_queue1', self.number_in_queue1)

        if self.number_available_server1 > 0:
            self.schedule('start1', 0.0)

        self.schedule('enter1', self.interarrival_time_generator.generate())

    def start1(self):
        self.number_in_queue1 -= 1
        self.notify_state_change('number_in_queue1', self.number_in_queue1)

        self.number_available_server1 -= 1
        self.notify_state_change('number_available_server1', self.number_available_server1)

        self.schedule('leave1', self.service_time1_generator.generate())

    def leave1(self):
        self.number_blocked += 1
        self.notify_state_change('number_blocked', self.number_blocked)

        if self.number_in_queue2 < self.buffer_size:
            self.schedule('enter2', 0.0)

    def enter2(self):
        self.number_available_server1 += 1
        self.notify_state_change('number_available_server1', self.number_available_server1)

        self.number_blocked -= 1
        self.notify_state_change('number_blocked', self.number_blocked)

        self.number_in_queue2 += 1;
        self.notify_state_change('number_in_queue2', self.number_in_queue2)

        if self.number_available_server2 > 0:
            self.schedule('start2', 0.0)

        if self.number_in_queue1 > 0:
            self.schedule('start1', 0.0)

    def start2(self):
        self.number_in_queue2 -= 1;
        self.notify_state_change('number_in_queue2', self.number_in_queue2)

        self.number_available_server2 -= 1
        self.notify_state_change('number_available_server2', self.number_available_server2)

        self.schedule('leave2', self.service_time2_generator.generate())

        if self.number_blocked > 0:
            self.schedule('enter2', 0.0)

    def leave2(self):
        self.number_available_server2 += 1
        self.notify_state_change('number_available_server2', self.number_available_server2)

        if self.number_in_queue2 > 0:
            self.schedule('start2', 0.0)

class MultipleServerQueue(SimEntityBase):

    def __init__(self, interarrival_time_generator, number_servers, service_time_generator):
        SimEntityBase.__init__(self)
        self.interarrival_time_generator = interarrival_time_generator
        self.number_servers = number_servers
        self.service_time_generator = service_time_generator
        self.number_arrivals = nan
        self.number_available_servers = nan
        self.queue = []
        self.number_in_queue = nan
        self.delay_in_queue = nan
        self.time_in_system = nan

    def reset(self):
        SimEntityBase.reset(self)
        self.number_arrivals = 0
        self.number_available_servers = self.number_servers
        self.queue = []
        self.number_in_queue = 0

    def run(self):
        self.notify_state_change('number_arrivals', self.number_arrivals)
        self.notify_state_change('number_available_servers', self.number_available_servers)
        self.notify_state_change('queue', self.queue)
        self.notify_state_change('number_in_queue', self.number_in_queue)

        self.schedule('enter', 0.0)

    def enter(self):
        customer = Entity()
        customer.stamp_time()
        heappush(self.queue, customer);
        self.notify_state_change('queue', self.queue)

        self.number_in_queue = len(self.queue)
        self.notify_state_change('number_in_queue', self.number_in_queue)

        self.number_arrivals += 1;
        self.notify_state_change('number_arrivals', self.number_arrivals)

        if self.number_available_servers > 0:
            self.schedule('start', 0.0)

        self.schedule('enter', self.interarrival_time_generator.generate())

    def start(self):
        customer = heappop(self.queue)
        self.notify_state_change('queue', self.queue)

        self.number_in_queue = len(self.queue)
        self.notify_state_change('number_in_queue', self.number_in_queue)

        self.delay_in_queue = customer.elapsed_time()
        self.notify_state_change('delay_in_queue', self.delay_in_queue)

        self.number_available_servers -= 1
        self.notify_state_change('number_available_servers', self.number_available_servers)

        self.schedule('leave', self.service_time_generator.generate(), customer)

    def leave(self, customer):
        self.time_in_system = customer.elapsed_time()
        self.notify_state_change('time_in_system', self.time_in_system)

        self.number_available_servers += 1
        self.notify_state_change('number_available_servers', self.number_available_servers)

        if len(self.queue) > 0:
            self.schedule('start', 0.0)