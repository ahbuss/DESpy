from simkit.examples.arrivalprocess import StoppedArrivalProcess
from simkit.rand import RandomVariate
from simkit.base import EventList

interarrival_time_generator = RandomVariate.instance('Gamma', alpha=2.1, beta=1.8)
stop_time = 30.0
stopped_arrival_process = StoppedArrivalProcess(interarrival_time_generator, stop_time)
print(stopped_arrival_process.describe())

EventList.verbose = True

EventList.reset()
EventList.start_simulation()
