from simkit.examples import EntityCreator
from simkit.examples import EntityServer
from simkit.stats import SimpleStatsTally
from simkit.stats import CollectionSizeTimeVarying
from simkit.rand import RandomVariate
from simkit.base import EventList
from time import time

interarrival_time_generator = RandomVariate.instance('Uniform', min=0.9, max=2.2)
entity_creator = EntityCreator(interarrival_time_generator)
print(entity_creator.describe())

total_number_servers=2
service_time_generator = RandomVariate.instance('Gamma', alpha=1.7, beta=1.8)
entity_server = EntityServer(total_number_servers, service_time_generator)
print(entity_server.describe())

entity_creator.add_sim_event_listener(entity_server)

inner_delay_in_queue_stat = SimpleStatsTally("delay_in_queue")
entity_server.add_state_change_listener(inner_delay_in_queue_stat)

inner_number_in_queue_stat = CollectionSizeTimeVarying('queue')
entity_server.add_state_change_listener(inner_number_in_queue_stat)

outer_number_in_queue_stat = SimpleStatsTally('outer_number_in_queue')

outer_delay_in_queue_stat = SimpleStatsTally('mean_delay_in_queue')

# print(getattr(entity_server, 'number_servers'))

runtime = 800.0
p = 0.975
numberReps = 100

EventList.stop_at_time(runtime)

start = time()
for rep in range(numberReps):
    EventList.reset()
    inner_delay_in_queue_stat.reset()
    inner_number_in_queue_stat.reset()
    EventList.start_simulation()
    outer_delay_in_queue_stat.new_observation(inner_delay_in_queue_stat.mean)
    outer_number_in_queue_stat.new_observation(inner_number_in_queue_stat.mean)
end = time()
elapsed = end-start
print('\n{reps:d} replications of length {runtime:,.1f} took {time:,.4f} sec'.format(reps=numberReps,runtime=runtime, time=elapsed))
print('95% CI for number in queue: {mean:,.4f} \u00B1 {halfwidth:,.4f}'.format(mean=outer_number_in_queue_stat.mean, halfwidth=outer_number_in_queue_stat.halfwidth(p)))
print('95% CI for delay in queue: {mean:,.4f} \u00B1 {halfwidth:,.4f}'.format(mean=outer_delay_in_queue_stat.mean, halfwidth=outer_delay_in_queue_stat.halfwidth(p)))


