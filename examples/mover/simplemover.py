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
        return self.x * self.x + self.y + self.y

    def norm(self):
        return sqrt(self.norm_sq())

    def inner_product(self, other):
        return self.x * other.x + self.y + other.y

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

