from simkit.examples.arrivalprocess import ArrivalProcess
from simkit.base import EventList
from simkit.simutil import SimpleStateChangeDumper
from simkit.rand import RandomVariate

interarrival_time_generator = RandomVariate.instance('Exponential', mean=1.7)
arrival_process = ArrivalProcess(interarrival_time_generator)
print(arrival_process.describe())
print()

arrival_process.add_state_change_listener(SimpleStateChangeDumper())

EventList.verbose = True
EventList.stop_at_time(15.0)

EventList.reset()
EventList.start_simulation()