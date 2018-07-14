from time import time

from simkit.simkit import SimEntityBase
from simkit.simkit import EventList
from math import sqrt
from math import pow
from math import nan

class Point:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def distance(self, other):
        delta_x = other.x - self.x
        delta_y = other.y - self.y
        return sqrt(delta_x * delta_x + delta_y * delta_y)

    def set_coord(self, x, y):
        self.x = x
        self.y = y

    def add(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def subtract(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def norm_sq(self):
        return self.x * self.x + self.y * self.y

    def norm(self):
        return sqrt(self.norm_sq())

    def inner_product(self, other):
        return self.x * other.x + self.y + other.y

    def scalar_mult(self, a):
        self.x *= a
        self.y *= a

    def __repr__(self):
        return 'p({x:.3f}, {y:.3f})'.format(x=self.x, y= self.y)


class SimpleMover(SimEntityBase):
    def __init__(self, initial_loc, max_speed):
        SimEntityBase.__init__(self)
        self.initial_loc = initial_loc
        self.max_speed = max_speed
        self.last_stop_loc = None
        self.velocity = None
        self.start_move_time = nan
        self.destination = None

    def reset(self):
        self.start_move_time = EventList.simtime
        self.last_stop_loc = self.initial_loc
        self.velocity = Point(0.0, 0.0)
        self.destination = Point(nan, nan)

    def run(self):
        self.notify_state_change('start_move_time', self.start_move_time)
        self.notify_state_change('last_stop_loc', self.last_stop_loc)
        self.notify_state_change('velocity', self.velocity)
        self.notify_state_change('destination', self.destination)

    def move_to(self, destination):
        self.destination = destination
        self.notify_state_change('destination', self.destination)

        self.schedule('start_move', 0.0, self)

    def start_move(self, me):
        diff = self.destination.subtract(self.last_stop_loc)
        distance = diff.norm()
        self.velocity.set_coord(self.max_speed * diff.x / distance, self.max_speed * diff.y / distance)
        self.notify_state_change('velocity', self.velocity)

        self.start_move_time = EventList.simtime
        self.notify_state_change('start_move_time', self.start_move_time)

        time_to_destination = distance / self.max_speed
        self.schedule('end_move', time_to_destination, me)

    def end_move(self, me):
        self.last_stop_loc.set_coord(self.destination.x, self.destination.y)
        self.notify_state_change('last_stop_loc', self.last_stop_loc)

        self.velocity.set_coord(0.0, 0.0)
        self.notify_state_change('velocity', self.velocity)

        self.destination.set_coord(nan, nan)

    def order_stop(self):
        self.schedule('stop', 0.0, self)

    def stop(self, me):
        self.last_stop_loc = self.current_loc()
        self.notify_state_change('last_stop_loc', self.last_stop_loc)

        self.start_move_time = EventList.simtime
        self.notify_state_change('start_move_time', self.start_move_time)

        self.velocity.set_coord(0.0, 0.0)
        self.notify_state_change('velocity', self.velocity)

    def current_loc(self):
        current_loc = self.last_stop_loc
        if  not self.velocity is None:
            if self.velocity.norm() > 0:
                current_loc = Point(self.last_stop_loc.x + self.velocity.x * (EventList.simtime - self.start_move_time), \
                            self.last_stop_loc.y + self.velocity.y * (EventList.simtime - self.start_move_time))
        return current_loc

    def __repr__(self):
        return '{name} {loc} {velocity}'.format(name=self.name, loc=self.current_loc(), velocity=self.velocity)

class SimplePathMoverManager(SimEntityBase):
    def __init__(self, mover, path, start_on_run):
        SimEntityBase.__init__(self)
        self.mover = mover
        self.path = path
        self.start_on_run = start_on_run

        self.next = nan

        self.add_sim_event_listener(self.mover)
        self.mover.add_sim_event_listener(self)

    def reset(self):
        SimEntityBase.reset(self)
        self.next = 0

    def run(self):
        if self.start_on_run and len(self.path) > 0:
            self.schedule('move_to', 0.0, self.path[self.next])

    def move_to(self, destination):
        pass

    def end_move(self, mover):
        if mover == self.mover:
            self.next += 1;
            if self.next < (len(self.path) - 1):
                self.schedule('move_to', 0.0, self.path[self.next])

            else:
                self.schedule('order_stop', 0.0)


