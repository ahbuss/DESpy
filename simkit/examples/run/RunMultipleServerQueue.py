from simkit.examples.basic import MultipleServerQueue
from simkit.rand import RandomVariate
from simkit.base import EventList
from simkit.simutil import SimpleStateChangeDumper
from simkit.stats import *

interarrival_time_generator = RandomVariate.instance('Uniform', min=0.9, max=2.3)
number_servers = 2
service_time_generator = RandomVariate.instance('Gamma', alpha=1.7, beta=1.8)

multiple_server_queue = MultipleServerQueue(interarrival_time_generator, number_servers, service_time_generator)
print(multiple_server_queue.describe())

simple_state_change_dumper = SimpleStateChangeDumper()
# multiple_server_queue.add_state_change_listener(simple_state_change_dumper)

number_in_queue_stat = SimpleStatsTimeVarying('number_in_queue')
multiple_server_queue.add_state_change_listener(number_in_queue_stat)

delay_in_queue_stat = SimpleStatsTally('delay_in_queue')
multiple_server_queue.add_state_change_listener(delay_in_queue_stat)

time_in_system_stat = SimpleStatsTally('time_in_system')
multiple_server_queue.add_state_change_listener(time_in_system_stat)

collection_stat = CollectionSizeTimeVarying('queue')
multiple_server_queue.add_state_change_listener(collection_stat)

number_available_servers_stat = SimpleStatsTimeVarying('number_available_servers')
multiple_server_queue.add_state_change_listener(number_available_servers_stat)

EventList.verbose = False
# EventList.stop_on_event(5, 'arrival')
EventList.stop_at_time(10000)

EventList.reset()
EventList.start_simulation()

print('Simulation ended at time {time:,.2f}'.format(time=EventList.simtime))
print('There have been {arrivals:,d} arrivals'.format(arrivals=multiple_server_queue.number_arrivals))
print('Avg # in queue: {avg:.4f}'.format(avg=number_in_queue_stat.time_varying_mean()))
print('Avg delay in queue: {time:.4f}'.format(time=delay_in_queue_stat.mean))
print('Avg time in system: {time:.4f}'.format(time=time_in_system_stat.mean))

avg_number_in_queue = number_in_queue_stat.time_varying_mean()
avg_arrival_rate = multiple_server_queue.number_arrivals / EventList.simtime

little_delay_in_queue = avg_number_in_queue / avg_arrival_rate
print("Avg delay in queue via Little's formula: {avg:.4f}".format(avg=little_delay_in_queue))

avg_number_in_system = number_in_queue_stat.time_varying_mean() + multiple_server_queue.number_servers - number_available_servers_stat.time_varying_mean()
little_time_in_system = avg_number_in_system / avg_arrival_rate

print("Avg time in system via Little's formula: {avg:.4f}".format(avg=little_time_in_system))
