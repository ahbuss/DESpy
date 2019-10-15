from simkit.base import SimEntityBase
from simkit.base import Entity
from simkit.base import Priority
from simkit.examples.arrivalprocess import ArrivalProcess
from math import nan
from heapq import heappush
from heapq import heappop

class Ship (Entity):
    def __init__(self, unloading_time_generator):
        Entity.__init__(self)
        self.remaining_unloading_time = unloading_time_generator
        self.name = 'Ship'

    def credit_work(self, rate):
        """
        Decrement remaining_unloading_time by the elapsed time * the rate
        :param rate: Rate at which credit_work was performed; must be > 0.0.
        """
        if rate <= 0.0:
            raise ValueError('rate must be > 0.0: {rate}'.format(rate=rate))
        self.remaining_unloading_time -= self.elapsed_time() * rate;

    def __repr__(self):
        return '{super} {remain:.4f}'.format(super=Entity.__repr__(self), remain=self.remaining_unloading_time)

class ShipArrivalProcess(ArrivalProcess):
    def __init__(self, interarrival_time_generator, unloading_time_generator):
        ArrivalProcess.__init__(self, interarrival_time_generator)
        self.unloading_time_generator = unloading_time_generator

    def arrival(self):
        ArrivalProcess.arrival(self)
        ship = Ship(self.unloading_time_generator.generate())
        self.schedule('ship_arrival', 0.0, ship)

class TwoCranesBerth(SimEntityBase):
    def __init__(self):
        SimEntityBase.__init__(self)
        self.queue = []
        self.berths = []
        self.delay_in_queue = nan
        self.time_in_System = nan

    def reset(self):
        SimEntityBase.reset(self)
        self.queue.clear()
        self.berths.clear()
        self.delay_in_queue = nan
        self.time_in_System = nan

    def run(self):
        self.notify_state_change('queue', self.queue)
        self.notify_state_change('berths', self.berths)

    def ship_arrival(self, ship):
        ship.stamp_time()
        heappush(self.queue, ship)
        self.notify_state_change('queue', self.queue)

        if len(self.berths)== 0:
            self.schedule('start_unloading_two_cranes', 0.0, priority=Priority.HIGH)

        if len(self.berths)== 1:
            self.schedule('switch_to_one_crane', 0.0)

    def start_unloading_two_cranes(self):
        ship = heappop(self.queue)
        self.notify_state_change('queue', self.queue)

        self.delay_in_queue = ship.elapsed_time()
        self.notify_state_change('delay_in_queue', self.delay_in_queue)

        ship.stamp_time()
        heappush(self.berths, ship)
        self.notify_state_change('berths', self.berths)

        self.schedule('end_unloading_two_cranes', ship.remaining_unloading_time / 2)

    def end_unloading_two_cranes(self):
        ship = heappop(self.berths)
        # ship = self.berths.pop()
        self.notify_state_change('berths', self.berths)

        self.time_in_System = ship.age()
        self.notify_state_change('time_in_system', self.time_in_System)

    def switch_to_one_crane(self):
        ship = heappop(self.berths)
        # ship = self.berths[0]
        ship.credit_work(2)
        ship.stamp_time()
        heappush(self.berths, ship)

        self.cancel('end_unloading_two_cranes')

        self.schedule('start_unloading_one_crane', 0.0, priority=Priority.HIGH)

        self.schedule('end_unloading_one_crane', ship.remaining_unloading_time, ship)

    def start_unloading_one_crane(self):
        ship = heappop(self.queue)
        self.notify_state_change('queue', self.queue)

        self.delay_in_queue = ship.elapsed_time()
        self.notify_state_change('delay_in_queue', self.delay_in_queue)

        ship.stamp_time()

        heappush(self.berths, ship)
        # self.berths.append(ship)
        self.notify_state_change('berths', self.berths)

        self.schedule('end_unloading_one_crane', ship.remaining_unloading_time, ship)

    def end_unloading_one_crane(self, ship):
        self.berths.remove(ship)
        self.notify_state_change('berths', self.berths)

        self.time_in_System = ship.age()
        self.notify_state_change('time_in_system', self.time_in_System)

        if len(self.queue) == 0:
            self.schedule('switch_to_two_cranes', 0.0)

        if len(self.queue) > 0:
            self.schedule('start_unloading_one_crane', 0.0, priority=Priority.HIGH)

    def switch_to_two_cranes(self):
        ship = heappop(self.berths)
        ship.credit_work(1)
        ship.stamp_time()
        heappush(self.berths, ship)

        self.notify_state_change('in_berth', ship)

        self.cancel('end_unloading_one_crane', ship)

        self.schedule('end_unloading_two_cranes', ship.remaining_unloading_time / 2, priority=Priority.HIGH)

