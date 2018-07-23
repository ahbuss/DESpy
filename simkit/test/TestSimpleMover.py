from examples.mover.simplemover import SimpleMover
from examples.mover.simplemover import Point
from examples.mover.simplemover import SimplePathMoverManager
from simkit.simkit import EventList
from simkit.simutil import SimpleStateChangeDumper

start_loc = Point(20.0, 30.0)
max_speed = 30.0
simple_mover = SimpleMover(start_loc, max_speed)

simple_mover.add_state_change_listener(SimpleStateChangeDumper())

print(simple_mover.describe())

path = []
path.append(Point(25.0, -20.0))
path.append(Point(50.0, 10.0))
path.append(Point(-100.0, -30.0))

simple_path_mover_manager = SimplePathMoverManager(simple_mover, path, True)
print(simple_path_mover_manager.describe())

EventList.verbose = True
EventList.reset()
EventList.start_simulation()