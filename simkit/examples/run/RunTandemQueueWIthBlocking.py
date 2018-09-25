from simkit.examples.tandem_queue_with_blocking import TandmQueueWithBlocking
from simkit.base import EventList
from simkit.rand import RandomVariate
from simkit.simutil import SimpleStateChangeDumper
from simkit.stats import IndexedSimpleStatsTimeVarying
from simkit.stats import SimpleStatsTimeVarying

interarrival_time_generator = RandomVariate.instance('Exponential', mean=2.7)
service_time_generator = [RandomVariate.instance('Uniform', min=1.2, max=2.4),
                          RandomVariate.instance('Gamma', alpha=2.1, beta=2.2)]
number_servers = [4, 2]
buffer_size = 2

queue = TandmQueueWithBlocking(interarrival_time_generator, number_servers, service_time_generator, buffer_size)
print(queue.describe())

number_in_queue_stat = IndexedSimpleStatsTimeVarying('number_in_queue')
queue.add_state_change_listener(number_in_queue_stat)

number_blocked_stat = SimpleStatsTimeVarying('number_blocked')
queue.add_state_change_listener(number_blocked_stat)

simple_state_change_dumper = SimpleStateChangeDumper()
# queue.add_state_change_listener(simple_state_change_dumper)

stop_time = 100000.0;
EventList.stop_at_time(stop_time)
EventList.verbose = False

EventList.reset()
EventList.start_simulation()


print('Simulation ended at time {time:,.2f}'.format(time=EventList.simtime))

print('Avg. # in Queue0: {queue:,.4f}'.format(queue=number_in_queue_stat.mean(0)))
print('Avg. # in Queue1: {queue:,.4f}'.format(queue=number_in_queue_stat.mean(1)))
print('Avg, # blocked:   {blocked:,.4f}'.format(blocked=number_blocked_stat.mean))