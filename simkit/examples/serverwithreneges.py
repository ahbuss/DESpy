from simkit.base import SimEntityBase
from simkit.base import Entity
from simkit.base import Priority
from math import nan
from heapq import heappush
from heapq import  heappop

class RenegingCustomer(Entity):

    def __init__(self, renegeTime):
        Entity.__init__(self, 'RenegingCustomer')
        self.renegeTime = renegeTime

    def __repr__(self):
        return Entity.__repr__(self) + ' (' + str(round(self.renegeTime,4)) + ')'

class CustomerCreator(SimEntityBase):

    def __init__(self, interarrival_time_generator, renege_time_generator):
        SimEntityBase.__init__(self)
        self.interarrival_time_generator = interarrival_time_generator
        self.renege_time_generator = renege_time_generator
        self.number_arrivals = nan

    def reset(self):
        SimEntityBase.reset(self)
        self.number_arrivals = 0

    def run(self):
        self.schedule('create', self.interarrival_time_generator.generate())

    def create(self):
        self.number_arrivals += 1
        self.notify_state_change('number_arrivals', self.number_arrivals)
        customer = RenegingCustomer(self.renege_time_generator.generate())
        self.schedule('arrival', 0.0, customer)
        self.schedule('create', self.interarrival_time_generator.generate())

    def __repr__(self):
        return SimEntityBase.__repr__(self) + ' (' + str(self.interarrival_time_generator) + ', ' + str(self.renege_time_generator) + ')'

class ServerWithReneges(SimEntityBase):

    def __init__(self, total_number_servers, service_time_generator):
        SimEntityBase.__init__(self)
        self.total_number_servers = total_number_servers
        self.service_time_generator = service_time_generator
        self.queue = []
        self.number_available_servers = nan
        self.number_reneges = nan
        self.number_served = nan

    def reset(self):
        self.queue.clear()
        self.number_available_servers = self.total_number_servers
        self.number_reneges = 0
        self.number_served = 0

    def run(self):
        self.notify_state_change('number_available_servers', self.number_available_servers)
        self.notify_state_change('queue', self.queue)
        self.notify_state_change('number_reneges', self.number_reneges)
        self.notify_state_change('number_served', self.number_served)

    def arrival(self, customer):
        customer.stamp_time()
        heappush(self.queue, customer)
        self.notify_state_change('queue', self.queue)

        if self.number_available_servers > 0:
            self.schedule('start_service', 0.0, priority=Priority.HIGH)

        self.schedule('renege', customer.renegeTime, customer)

    def start_service(self):

        customer = heappop(self.queue)
        self.cancel('renege', customer)

        self.notify_state_change('delay_in_queue', customer.elapsed_time())
        self.notify_state_change('queue', self.queue)

        self.number_available_servers -= 1
        self.notify_state_change('number_available_servers', self.number_available_servers)

        self.schedule('end_service', self.service_time_generator.generate(), customer)

    def renege(self, customer):
        self.number_reneges += 1;
        self.notify_state_change('number_reneges', self.number_reneges)

        self.notify_state_change('delay_in_queue_reneged', customer.elapsed_time())

        self.queue.remove(customer)
        self.notify_state_change('queue', self.queue)

    def end_service(self, customer):
        self.notify_state_change('time_in_system', customer.elapsed_time())

        self.number_available_servers += 1
        self.notify_state_change('number_available_servers', self.number_available_servers)

        if self.queue.__len__() > 0:
            self.schedule('start_service', 0.0, priority=Priority.HIGH)

    @property
    def total_number_servers(self):
        return self.__totalNumberServers

    @total_number_servers.setter
    def total_number_servers(self, totalNumberServers):
        if totalNumberServers <= 0:
            raise ValueError('total_number_servers must be > 0: ' + str(totalNumberServers))
        self.__totalNumberServers = totalNumberServers


