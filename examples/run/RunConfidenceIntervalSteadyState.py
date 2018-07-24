from examples.entitycreator import EntityCreator
from examples.entityserver import EntityServer
from simkit.stats import SimpleStatsTally, TruncatingSimpleStatsTally, TruncatingSimpleStatsTimeVarying
from simkit.stats import CollectionSizeTimeVarying
from simkit.rand import RandomVariate
from simkit.simkit import EventList
from time import time

interarrival_time_generator = RandomVariate.instance('Uniform', min=1.1, max=3.2)
entity_creator = EntityCreator(interarrival_time_generator)
print(entity_creator.describe())

total_number_servers=2
service_time_generator = RandomVariate.instance('Gamma', alpha=1.7, beta=1.8)
entity_server = EntityServer(total_number_servers, service_time_generator)
print(entity_server.describe())

entity_creator.add_sim_event_listener(entity_server)

truncation_point = 100000
steady_state_observations = 10000

inner_delay_in_queue_stat = TruncatingSimpleStatsTally('delay_in_queue', truncation_point)
entity_server.add_state_change_listener(inner_delay_in_queue_stat)

inner_number_in_queue_stat = CollectionSizeTimeVarying('queue')
entity_server.add_state_change_listener(inner_number_in_queue_stat)

outer_number_in_queue_stat = SimpleStatsTally('outer_number_in_queue')

outer_delay_in_queue_stat = SimpleStatsTally('mean_delay_in_queue')

p = 0.975
numberReps = 50

EventList.stop_on_event(truncation_point + steady_state_observations, 'start_service')

print('\nRunning {reps:d} replications with truncation at {tp:,d} observations and {ss:,d} observations in steady-state '.\
      format(reps=numberReps,tp=truncation_point, ss=steady_state_observations))
start = time()
for rep in range(1,numberReps+1):
    if rep % 10 == 0:
        print('rep {rep:d} halfwidth {hw:,.4f}'.format(rep=rep, hw=outer_delay_in_queue_stat.halfwidth(p)))
    EventList.reset()
    inner_delay_in_queue_stat.reset()
    inner_number_in_queue_stat.reset()
    EventList.start_simulation()
    outer_delay_in_queue_stat.new_observation(inner_delay_in_queue_stat.mean)
    outer_number_in_queue_stat.new_observation(inner_number_in_queue_stat.mean)
end = time()
elapsed = end-start

print('\nSimulation took {elapsed:,.4f} sec'.format(elapsed=elapsed))
print('95% CI for number in queue: {mean:,.4f} \u00B1 {halfwidth:,.4f}'.format(mean=outer_number_in_queue_stat.mean, halfwidth=outer_number_in_queue_stat.halfwidth(p)))
print('95% CI for delay in queue: {mean:,.4f} \u00B1 {halfwidth:,.4f}'.format(mean=outer_delay_in_queue_stat.mean, halfwidth=outer_delay_in_queue_stat.halfwidth(p)))
