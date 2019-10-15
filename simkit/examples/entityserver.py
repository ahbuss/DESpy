from simkit.base import SimEntityBase
from simkit.base import Priority
from math import nan
from heapq import heappush
from heapq import heappop

class EntityServer(SimEntityBase):

    def __init__(self, number_servers, service_time_generator):
        SimEntityBase.__init__(self)
        self.number_servers = number_servers
        self.service_time_generator = service_time_generator
        self.number_available_servers = nan
        self.queue = []
        self.delay_in_queue = nan
        self.time_in_system = nan

    @property
    def number_servers(self):
        return self.__number_servers

    @number_servers.setter
    def number_servers(self, numberServers):
        if numberServers <= 0:
            raise ValueError('number_servers must be > 0: ' + str(numberServers))
        self.__number_servers = numberServers

    def reset(self):
        self.number_available_servers = self.number_servers
        self.queue.clear()
        self.delay_in_queue = nan
        self.time_in_system = nan

    def run(self):
        self.notify_state_change('number_available_servers', self.number_available_servers)
        self.notify_state_change('queue', self.queue)

    def arrival(self, entity):
        entity.stamp_time()
        heappush(self.queue, entity)
        self.notify_state_change('queue', self.queue)

        if (self.number_available_servers > 0):
            self.schedule('start_service', 0.0, priority=Priority.HIGH)

    def start_service(self):
        entity = heappop(self.queue)
        self.notify_state_change('queue', self.queue)

        self.delay_in_queue = entity.elapsed_time()
        self.notify_state_change('delay_in_queue', self.delay_in_queue)

        self.number_available_servers -= 1
        self.notify_state_change('number_available_servers', self.number_available_servers)

        self.schedule('end_service', self.service_time_generator.generate(), entity)

    def end_service(self, entity):
        self.number_available_servers += 1
        self.notify_state_change('number_available_servers', self.number_available_servers)

        self.time_in_system = entity.elapsed_time()
        self.notify_state_change('time_in_system', self.time_in_system)

        if self.queue.__len__() > 0:
            self.schedule('start_service', 0.0, priority=Priority.HIGH)