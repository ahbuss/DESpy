from pydoc import describe

from simkit.examples import twocranesberth
from simkit.rand import RandomVariate
from simkit.simkit import EventList
from simkit.simutil import SimpleStateChangeDumper
from simkit.examples.twocranesberth import ShipArrivalProcess
from simkit.examples.twocranesberth import TwoCranesBerth
from simkit.stats import SimpleStatsTally

interarrival_genarator = RandomVariate.instance('Exponential', mean=0.7)
unload_time_generator = RandomVariate.instance('Uniform', min=0.5, max=1.5)
ship_arrival_process = ShipArrivalProcess(interarrival_genarator, unload_time_generator)

two_cranes_berth = TwoCranesBerth();
ship_arrival_process.add_sim_event_listener(two_cranes_berth)

simple_state_dumper = SimpleStateChangeDumper()
ship_arrival_process.add_state_change_listener(simple_state_dumper)
two_cranes_berth.add_state_change_listener(simple_state_dumper)

print (ship_arrival_process)
print(two_cranes_berth)

delay_in_queue_stat = SimpleStatsTally('delay_in_queue')
time_in_system_stat = SimpleStatsTally('time_in_system')

two_cranes_berth.add_state_change_listener(delay_in_queue_stat)
two_cranes_berth.add_state_change_listener(time_in_system_stat)

EventList.verbose = True

stop_time = 3650.0
EventList.stop_at_time(stop_time)

EventList.reset()
EventList.start_simulation()

print('Simulation ended at time {time:,.1f}'.format(time=EventList.simtime))
print('# arriving ships: {arrive:,d}'.format(arrive=ship_arrival_process.number_arrivals))

