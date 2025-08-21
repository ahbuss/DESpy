from simkit.base import SimEntityBase
from simkit.base import Priority
from math import nan

class FiniteCapacityQueue(SimEntityBase):

    def __init__(self, total_number_servers, service_time_generator, queue_capacity):
        SimEntityBase.__init__(self)
        self.total_number_servers = total_number_servers
        self.service_time_generator = service_time_generator
        self.queue_capacity = queue_capacity
        # self.number_in_queue = nan
        # self.number_available_servers = nan
        # self.number_balks = nan
        # self.number_potential_customers = nan

        if (self.queue_capacity < 0):
            raise ValueError('queue_capacity must be \u2265 0: {cap:%d}'.format(cap=self.queue_capacity))

    @property
    def number_balks(self):
        return self._number_balks

    @property
    def number_available_servers(self):
        return self._number_available_servers

    @property
    def number_potential_customers(self):
        return self._number_potential_customers

    @property
    def number_in_queue(self):
        return self._number_in_queue

    def reset(self):
        SimEntityBase.reset(self)
        self._number_in_queue = 0
        self._number_available_servers = self.total_number_servers
        self._number_balks = 0
        self._number_potential_customers = 0

    def run(self):
        self.notify_state_change('number_in_queue', self.number_in_queue)
        self.notify_state_change('number_available_servers', self.number_available_servers)
        self.notify_state_change('number_balks', self.number_balks)
        self.notify_state_change('number_potential_customers', self.number_potential_customers)

    def arrival(self):
        self._number_potential_customers += 1
        self.notify_state_change('number_potential_customers', self.number_potential_customers)

        if self.number_in_queue < self.queue_capacity or self.number_available_servers > 0:
            self.schedule('join_queue', 0.0)

        if self.number_in_queue == self.queue_capacity and self.number_available_servers == 0:
            self.schedule('balk', 0.0)

    def balk(self):
        self._number_balks += 1
        self.notify_state_change('number_balks', self.number_balks)

    def join_queue(self):
        self._number_in_queue += 1

        if self.number_available_servers > 0:
            self.schedule('start_service', 0.0, priority=Priority.HIGH)

    def start_service(self):
        self._number_in_queue -= 1
        self.notify_state_change('number_in_queue', self.number_in_queue)

        self._number_available_servers -= 1
        self.notify_state_change('number_available_servers', self.number_available_servers)

        self.schedule('end_service', self.service_time_generator.generate())

    def end_service(self):
        self._number_available_servers += 1
        self.notify_state_change('number_available_servers', self.number_available_servers)

        if self.number_in_queue > 0:
            self.schedule('start_service', 0.0, priority=Priority.HIGH)
