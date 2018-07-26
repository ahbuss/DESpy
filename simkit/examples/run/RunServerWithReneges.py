from simkit.examples.serverwithreneges import CustomerCreator
from simkit.examples.serverwithreneges import ServerWithReneges
from simkit.rand import RandomVariate
from simkit.simkit import EventList
from simkit.stats import SimpleStatsTally
from simkit.stats import CollectionSizeTimeVarying
from time import time

interarrival_generator = RandomVariate.instance('Exponential', mean=1.5)
renege_generator = RandomVariate.instance('Uniform', min=2.0, max=6.0)
creator = CustomerCreator(interarrival_generator, renege_generator)
print(creator.describe())

total_number_servers = 2
service_time_generator = RandomVariate.instance('Gamma', alpha=2.5, beta=1.2)
server = ServerWithReneges(total_number_servers, service_time_generator)
print (server.describe())

creator.add_sim_event_listener(server)

delay_in_queue_stat = SimpleStatsTally('delay_in_queue')
server.add_state_change_listener(delay_in_queue_stat)

numberInQueueStat = CollectionSizeTimeVarying('queue')
server.add_state_change_listener(numberInQueueStat)

start = time()
EventList.stop_at_time(100000.0)
EventList.reset()
EventList.start_simulation()
end = time()

print('\nSimulation took {time:.4f} sec'.format(time = end - start))
print('Simulation ended at simtime {time:,.0f}\n'.format(time=EventList.simtime))
print('Avg delay in queue = {avg:,.4f}'.format(avg=(delay_in_queue_stat.mean)))
print('Avg number in queue = {avg:.4f}'.format(avg=numberInQueueStat.mean))
print('There have been {num:,d} reneges'.format(num=server.number_reneges))
print('There have been {num:,d} served'.format(num=delay_in_queue_stat.count))
print('% of potential customers reneging = {percent:.2f}% '. \
      format(percent=(100 * server.number_reneges / (server.number_reneges + delay_in_queue_stat.count))))