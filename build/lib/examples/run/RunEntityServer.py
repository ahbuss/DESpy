from simkit.examples import EntityServer
from simkit.rand import RandomVariate
from simkit.examples import EntityCreator
from simkit.simkit import EventList
from simkit.simutil import SimpleStateChangeDumper
from simkit.stats import SimpleStatsTally
from simkit.stats import CollectionSizeTimeVarying
from time import time

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

EventList.stop_at_time(100000.0)
EventList.verbose = False

start = time()
EventList.reset()
EventList.start_simulation()
end = time()

print('\nSimulation took {time:,.3f} sec'.format(time=(end-start)))
print('Simulation ended at simtime {time:,.0f}\n'.format(time=EventList.simtime))

print('Avg time in system = {avg:,.4f}'.format(avg=time_in_system_stat.mean))
print('Avg delay in queue = {avg:,.4f}'.format(avg=delay_in_queue_stat.mean))
print('Avg number in queue = {avg:,.4f}'.format(avg=number_in_queue_stat.mean))