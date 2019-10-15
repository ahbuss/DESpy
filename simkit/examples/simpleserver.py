from simkit.base import SimEntityBase
from simkit.base import Priority
from math import nan

class SimpleServer(SimEntityBase):

    def __init__(self, total_number_servers, service_time_generator):
        SimEntityBase.__init__(self)
        self.total_number_servers = total_number_servers
        self.service_time_generator = service_time_generator
        self.number_in_queue = nan
        self.number_available_servers = nan
        self.number_served = nan

    def reset(self):
        self.number_available_servers = self.total_number_servers
        self.number_in_queue = 0
        self.number_served = 0

    def run(self):
        self.notify_state_change('number_available_servers', self.number_available_servers)
        self.notify_state_change('number_in_queue', self.number_in_queue)
        self.notify_state_change('number_served', self.number_served)

    def arrival(self):
        self.number_in_queue += 1
        self.notify_state_change('number_in_queue', self.number_in_queue)

        if (self.number_available_servers > 0):
            self.schedule('start_service', 0.0, priority=Priority.HIGH)

    def start_service(self):
        self.number_in_queue -= 1
        self.notify_state_change('number_in_queue', self.number_in_queue)

        self.number_available_servers -= 1
        self.notify_state_change('number_available_servers', self.number_available_servers)

        self.schedule('end_service', self.service_time_generator.generate())

    def end_service(self):
        self.number_available_servers += 1
        self.notify_state_change('number_available_servers', self.number_available_servers)

        self.number_served += 1
        self.notify_state_change('number_served', self.number_served)

        if self.number_in_queue > 0:
            self.schedule('start_service', 0.0, priority=Priority.HIGH)
