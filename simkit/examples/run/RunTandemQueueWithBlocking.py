from simkit.rand import RandomVariate
from simkit.base import EventList
from simkit.simutil import SimpleStateChangeDumper
from simkit.examples.basic import TandemQueueWithBlocking
from simkit.stats import SimpleStatsTimeVarying
from simkit.rand import RandomVariate
from random import Random

# Uncomment to seed with computer clock time
# RandomVariate.baseRNG = Random()
interarrval_time_generator = RandomVariate.instance('Exponential', mean=1.8)
service_time_generator = [RandomVariate.instance('Gamma', alpha=2.5, beta=1.6), RandomVariate.instance('Uniform', min=2.2, max=4.4)]
number_servers = [3, 2]
buffer_size = 1

print(interarrval_time_generator)
print(service_time_generator)

tandem_queue_with_blocking = TandemQueueWithBlocking(interarrval_time_generator, number_servers[0], number_servers[1],
                                                    service_time_generator[0],
                                                     service_time_generator[1],
                                                     buffer_size)
print(tandem_queue_with_blocking.describe())

simple_state_change_dumper = SimpleStateChangeDumper()
# tandem_queue_with_blocking.add_state_change_listener(simple_state_change_dumper)

number_in_queue1_stat = SimpleStatsTimeVarying('number_in_queue1')
number_in_queue2_stat = SimpleStatsTimeVarying('number_in_queue2')
number_available_server1_stat = SimpleStatsTimeVarying('number_available_server1')
number_available_server2_stat = SimpleStatsTimeVarying('number_available_server2')
tandem_queue_with_blocking.add_state_change_listener(number_in_queue1_stat)
tandem_queue_with_blocking.add_state_change_listener(number_in_queue2_stat)
tandem_queue_with_blocking.add_state_change_listener(number_available_server1_stat)
tandem_queue_with_blocking.add_state_change_listener(number_available_server2_stat)

stop_time = 24 * 8 * 365.0
# stop_time = 1000
# EventList.verbose = True
# EventList.stop_at_time(stop_time)

number_leaves = 100000
EventList.stop_on_event(number_leaves, 'leave2')
# print('Simulation will run for {time:,.2f} time units'.format(time=EventList.stop_time))
print('Simulation will run for {num:,d} leave2 events'.format(num=number_leaves))

for buffer_size in range(1, 21):
    tandem_queue_with_blocking.buffer_size = buffer_size

    EventList.reset()

    number_in_queue1_stat.reset()
    number_in_queue2_stat.reset()
    number_available_server1_stat.reset()
    number_available_server2_stat.reset()

    EventList.start_simulation()

    print('buffer size: {buffer:d} avg # in queue1: {avg:,.4f}'.format(buffer=buffer_size, avg=number_in_queue1_stat.time_varying_mean()))
    # print(number_in_queue1_stat)
    # print(number_in_queue2_stat)
    # print(number_available_server1_stat)
    # print(number_available_server2_stat)