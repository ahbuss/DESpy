from simkit.examples.ggkqueue import GGkQueue
from simkit.rand import Uniform, Gamma
from simkit.base import EventList
from simkit.simutil import SimpleStateChangeDumper
from simkit.stats import SimpleStatsTimeVarying
from time import time

interarrival_time_generator = Uniform( min=0.5, max=1.5)
number_servers = 7
service_time_generator = Gamma(alpha=3.0, beta=2.0)

ggk_queue = GGkQueue(interarrival_time_generator, number_servers, service_time_generator)
simple_state_change_dumper = SimpleStateChangeDumper()
# ggk_queue.add_state_change_listener(simple_state_change_dumper)

print(ggk_queue.describe())



stop_time = 100000.0
EventList.stop_at_time(stop_time)
# EventList.verbose = True

number_in_queue_stat = SimpleStatsTimeVarying('number_in_queue')
number_available_servers_stat = SimpleStatsTimeVarying('number_available_servers')

ggk_queue.add_state_change_listener(number_in_queue_stat)
ggk_queue.add_state_change_listener(number_available_servers_stat)

start = time()
EventList.reset()
EventList.start_simulation()
end = time()

elapsed = end - start


print('avg # in queue: {avg:,.4f}'.format(avg=number_in_queue_stat.time_varying_mean()))
print('avg # avail servers: {avg:,.4f}'.format(avg=number_available_servers_stat.time_varying_mean()))

utilization = 1.0 - number_available_servers_stat.mean / ggk_queue.number_servers
print('avg utilization: {avg:,.4f}'.format(avg=utilization))
