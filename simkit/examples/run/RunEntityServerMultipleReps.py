from simkit.examples.entityserver import EntityServer
from simkit.rand import RandomVariate
from simkit.examples.entitycreator import EntityCreator
from simkit.base import EventList
from simkit.simutil import SimpleStateChangeDumper
from simkit.stats import SimpleStatsTally
from simkit.stats import CollectionSizeTimeVarying
from simkit.quantiles import student_t
from math import sqrt

interarrivalMean = 1.7
interarrival = RandomVariate.instance('Exponential', mean=interarrivalMean)
entity_creator = EntityCreator(interarrival)
print (entity_creator.describe())

alpha = 1.7
beta = 1.8
number_servers = 2
generator = RandomVariate.instance('Gamma', alpha=alpha, beta=beta)
entity_server = EntityServer(number_servers, generator)

print(entity_server.describe())

entity_creator.add_sim_event_listener(entity_server)

dumper = SimpleStateChangeDumper()

delay_in_queue_stat = SimpleStatsTally("delay_in_queue")
entity_server.add_state_change_listener(delay_in_queue_stat)

time_in_system_stat = SimpleStatsTally('time_in_system')
entity_server.add_state_change_listener(time_in_system_stat)

number_in_queue_stat = CollectionSizeTimeVarying("queue")
entity_server.add_state_change_listener(number_in_queue_stat)
service_mean = alpha * beta

outer_number_in_queue_stat = SimpleStatsTally("outer_number_in_queue")
outer_delay_in_queue_stat = SimpleStatsTally("outer_delay_in_queue")

stop_time = 100000.0

EventList.stop_at_time(stop_time)
EventList.verbose = False

number_replications = 100

print('There will be {reps:,d} replications for {time:,.1f} time units each'.
      format(reps=number_replications, time=stop_time))

for replication in [1, number_replications + 1]:
    EventList.reset()
    delay_in_queue_stat.reset()
    number_in_queue_stat.reset()
    EventList.start_simulation()
    outer_delay_in_queue_stat.new_observation(delay_in_queue_stat.mean)
    outer_number_in_queue_stat.new_observation(number_in_queue_stat.time_varying_mean())

alpha = 0.05;
t_value = student_t(1-alpha/2, number_replications - 1)

delay_halfwidth = outer_delay_in_queue_stat.stdev * t_value / sqrt(number_replications)
number_in_queue_halfwidth = outer_number_in_queue_stat.stdev * t_value / sqrt(number_replications)

print('{conf:.0f}% CI for delay in queue: {avg:,.4f} ± {half:,.4f}'.format(\
     conf=100*(1-alpha),avg=outer_delay_in_queue_stat.mean, half = delay_halfwidth))
print('{conf:.0f}% CI for number in queue = {avg:,.4f} ± {half:,.4f}'.format(\
    conf=100*(1-alpha),avg=outer_number_in_queue_stat.mean, half=number_in_queue_halfwidth))