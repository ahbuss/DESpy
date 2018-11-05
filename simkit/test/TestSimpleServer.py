from simkit.examples.arrivalprocess import ArrivalProcess
from simkit.examples.simpleserver import SimpleServer
from simkit.rand import RandomVariate
from simkit.stats import SimpleStatsTimeVarying
from simkit.base import EventList

interarrival_time_generator = RandomVariate.instance('Uniform', min=0.9, max=2.2)
arrival_process = ArrivalProcess(interarrival_time_generator)
print(arrival_process.describe())

number_servers = 3
service_time_generator = RandomVariate.instance('Gamma', alpha=2, beta=2.2)
simple_server = SimpleServer(number_servers, service_time_generator)
print(simple_server.describe())

arrival_process.add_sim_event_listener(simple_server)

number_in_queue_stat = SimpleStatsTimeVarying('number_in_queue')
number_available_servers_stat = SimpleStatsTimeVarying('number_available_servers')

simple_server.add_state_change_listener(number_in_queue_stat)
simple_server.add_state_change_listener(number_available_servers_stat)

# simple_server.add_state_change_listener(SimpleStateChangeDumper())

service_mean = simple_server.service_time_generator.alpha * simple_server.service_time_generator.beta
arrival_mean = (arrival_process.interarrival_time_generator.min + arrival_process.interarrival_time_generator.max) * 0.5
intensity = service_mean / (simple_server.total_number_servers * arrival_mean)

print('traffic intensity = {rho:.4f}'.format(rho = intensity))

stopTime = 100000
# stopTime = 50
# EventList.verbose = True

EventList.stop_at_time(stopTime)
EventList.reset()
EventList.start_simulation()

print('\nSimulation ended at simtime {time:,.2f}'.format(time=EventList.simtime))

# print(number_in_queue_stat)
# print(number_available_servers_stat)

print('{num:,d} customers arrived'.format(num=arrival_process.number_arrivals))
print('{num:,d} customers served'.format(num=simple_server.number_served))

print('Avg number in queue = {avg:.4f}'.format(avg=number_in_queue_stat.mean))
utilization = 1.0 - number_available_servers_stat.mean / simple_server.total_number_servers
print("Avg utilization = {avg:.4f}".format(avg=utilization))