from simkit.base import SimEntityBase
from simkit.base import Priority
from math import nan

class GGkQueue (SimEntityBase):
    def __init__(self, interarrival_time_generator, number_servers, service_time_generator):
        SimEntityBase.__init__(self)
        self.interarrival_time_generator = interarrival_time_generator
        self.number_servers = number_servers
        self.service_time_generator = service_time_generator
        self.number_in_queue = nan
        self.number_available_servers = nan

    def reset(self):
        SimEntityBase.reset(self)
        self.number_available_servers = self.number_servers
        self.number_in_queue = 0

    def run(self):
        self.notify_state_change('number_in_queue', self.number_in_queue)
        self.notify_state_change('number_available_servers', self.number_available_servers)

        self.schedule('arrival', self.service_time_generator.generate())

    def arrival(self):
        self.number_in_queue += 1
        self.notify_state_change('number_in_queue', self.number_in_queue)

        self.schedule('arrival', self.interarrival_time_generator.generate())

        if self.number_available_servers > 0:
            self.schedule('start_service', 0.0, priority=Priority.HIGH )

    def start_service(self):
        self.number_in_queue -= 1
        self.notify_state_change('number_in_queue', self.number_in_queue)

        self.number_available_servers -= 1
        self.notify_state_change('number_available_servers', self.number_available_servers)

        self.schedule('end_service', self.service_time_generator.generate())

    def end_service(self):
        self.number_available_servers += 1
        self.notify_state_change('number_available_servers', self.number_available_servers)

        if self.number_in_queue > 0:
            self.schedule('start_service', 0.0, priority=Priority.HIGH)
