from examples.serverwithreneges import CustomerCreator
from examples.serverwithreneges import ServerWithReneges
from simkit.rand import RandomVariate
from simkit.simkit import EventList
from simkit.stats import SimpleStatsTally
from simkit.stats import CollectionSizeTimeVarying
from simkit.simutil import SimpleStateChangeDumper

interarrival_generator = RandomVariate.instance('Exponential', mean=1.5)
renege_generator = RandomVariate.instance('Uniform', min=2.0, max=6.0)
creator = CustomerCreator(interarrival_generator, renege_generator)
print(creator.describe())

total_number_servers = 2
service_time_generator = RandomVariate.instance('Gamma', alpha=2.5, beta=1.2)
server = ServerWithReneges(total_number_servers, service_time_generator)
print (server.describe())

creator.add_sim_event_listener(server)

# server.add_state_change_listener(SimpleStateChangeDumper())

delay_in_queue_stat = SimpleStatsTally('delay_in_queue')
server.add_state_change_listener(delay_in_queue_stat)

number_in_queue_stat = CollectionSizeTimeVarying('queue')
server.add_state_change_listener(number_in_queue_stat)

EventList.verbose = False
EventList.stop_at_time(100000.0)
# EventList.stopOnEvent(10000, 'Renege')
EventList.reset()
EventList.start_simulation()

print('\nSimulation ended at simtime {time:,.3f}'.format(time=EventList.simtime))
print('Avg delay in queue = {avg:,.4f}'.format(avg=(delay_in_queue_stat.mean)))
print('Avg number in queue = {avg:.4f}'.format(avg=number_in_queue_stat.mean))
print('There have been {num:,d} reneges'.format(num=server.number_reneges))
print('There have been {num:,d} served'.format(num=delay_in_queue_stat.count))
print('{percent:.2f}% reneged'.format(percent=(100 * server.number_reneges / (server.number_reneges + delay_in_queue_stat.count))))
