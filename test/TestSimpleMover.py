from examples.mover.simplemover import SimpleMover
from examples.mover.simplemover import Point
from simkit.simkit import EventList
from simkit.simutil import SimpleStateChangeDumper

start_loc = Point(20.0, 30.0)
max_speed = 30.0
simple_mover = SimpleMover(start_loc, max_speed)

simple_mover.add_state_change_listener(SimpleStateChangeDumper())

print(simple_mover.describe())

EventList.verbose = True
EventList.reset()
simple_mover.schedule('move_to', 0.0, Point(40.0, 50.0))
EventList.start_simulation()