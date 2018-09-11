from simkit.simkit import SimEntityBase
from simkit.simkit import Priority
from math import nan

class TandmQueueWithBlocking(SimEntityBase):
    def __init__(self, interarrival_time_generator, number_servers, service_time_generator, buffer_size):
        SimEntityBase.__init__(self)
        self.interarrival_time_generator = interarrival_time_generator
        self.number_servers = number_servers
        self.service_time_generator = service_time_generator
        self.buffer_size = buffer_size
        self.number_in_queue=[nan, nan]
        self.number_available_servers = [nan,nan]
        self.number_blocked = nan

    def reset(self):
        SimEntityBase.reset(self)
        self.number_in_queue[0] = 0
        self.number_in_queue[1] = 0
        self.number_available_servers[0] = self.number_servers[0]
        self.number_available_servers[1] = self.number_servers[1]
        self.number_blocked = 0

    def run(self):
        self.notify_indexed_state_change(0, 'number_in_queue', self.number_in_queue[0])
        self.notify_indexed_state_change(1, 'number_in_queue', self.number_in_queue[1])
        self.notify_indexed_state_change(0, 'number_available_servers', self.number_available_servers[0])
        self.notify_indexed_state_change(1, 'number_available_servers', self.number_available_servers[1])
        self.notify_state_change('number_blocked', self.number_blocked)

        self.schedule('enter0', 0.0)

    def enter0(self):
        self.number_in_queue[0] += 1
        self.notify_indexed_state_change(0, 'number_in_queue', self.number_in_queue[0])

        if self.number_available_servers[0] > 0:
            self.schedule('start0', 0.0, priority=Priority.HIGH)

        self.schedule('enter0', self.interarrival_time_generator.generate())

    def start0(self):
        self.number_in_queue[0] -= 1
        self.notify_indexed_state_change(0, 'number_in_queue', self.number_in_queue[0])

        self.number_available_servers[0] -= 1
        self.notify_indexed_state_change(0, 'number_available_servers', self.number_available_servers[0])

        self.schedule('leave0', self.service_time_generator[0].generate())

    def leave0(self):
        self.number_blocked += 1
        self.notify_state_change('number_blocked', self.number_blocked)

        if self.number_in_queue[1] < self.buffer_size:
            self.schedule('enter1', 0.0)

    def enter1(self):
        self.number_blocked -= 1
        self.notify_state_change('number_blocked', self.number_blocked)

        self.number_available_servers[0] += 1;
        self.notify_indexed_state_change(0, 'number_available_servers', self.number_available_servers[0])

        self.number_in_queue[1] += 1
        self.notify_indexed_state_change(1, 'number_in_queue', self.number_in_queue[1])

        if self.number_available_servers[1] > 0:
            self.schedule('start1', 0.0, priority=Priority.HIGH)

        if self.number_in_queue[0] > 0:
            self.schedule('start0', 0.0, priority=Priority.HIGH)

    def start1(self):
        self.number_in_queue[1] -= 1
        self.notify_indexed_state_change(1, 'number_in_queue', self.number_in_queue[1])

        self.number_available_servers[1] -= 1
        self.notify_indexed_state_change(1, 'number_available_servers', self.number_available_servers[1])

        self.schedule('leave1', self.service_time_generator[1].generate())

        if self.number_blocked > 0:
            self.schedule('enter1', 0.0)

    def leave1(self):
        self.number_available_servers[1] += 1;
        self.notify_indexed_state_change(1, 'number_available_servers', self.number_available_servers[1])

        if self.number_in_queue[1] > 0:
            self.schedule('start1', 0.0, priority=Priority.HIGH)
