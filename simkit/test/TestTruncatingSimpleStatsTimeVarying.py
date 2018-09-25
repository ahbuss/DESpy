from simkit.examples.arrivalprocess import ArrivalProcess
from simkit.examples.simpleserver import SimpleServer
from simkit.rand import RandomVariate
from simkit.stats import TruncatingSimpleStatsTimeVarying
from simkit.base import EventList

interarrival_time_generator = RandomVariate.instance('Uniform', min=0.9, max=2.2)
arrival_process = ArrivalProcess(interarrival_time_generator)
print(arrival_process.describe())

number_servers = 3
service_time_generator = RandomVariate.instance('Gamma', alpha=2, beta=2.2)
simple_server = SimpleServer(number_servers, service_time_generator)
print(simple_server.describe())

arrival_process.add_sim_event_listener(simple_server)

truncation_time = 50000
number_in_queue_stat = TruncatingSimpleStatsTimeVarying(truncation_time, 'number_in_queue')
number_available_servers_stat = TruncatingSimpleStatsTimeVarying(truncation_time, 'number_available_servers')

simple_server.add_state_change_listener(number_in_queue_stat)
simple_server.add_state_change_listener(number_available_servers_stat)

# simple_server.add_state_change_listener(SimpleStateChangeDumper())

service_mean = simple_server.service_time_generator.alpha * simple_server.service_time_generator.beta
arrival_mean = (arrival_process.generator.min + arrival_process.generator.max) * 0.5
intensity = service_mean / (simple_server.total_number_servers * arrival_mean)

print('\ntraffic intensity = {rho:.4f}'.format(rho = intensity))

stop_time = 150000
# stopTime = 50

# arrival_process_stat = TruncatingSimpleStatsTimeVarying(truncation_time, 'number_arrivals')
# arrival_process.add_state_change_listener(arrival_process_stat)

# EventList.verbose = True

EventList.stop_at_time(stop_time + truncation_time)
EventList.reset()
EventList.start_simulation()

print('\nSimulation ended at simtime {time:,.2f}'.format(time=EventList.simtime))

# print(arrival_process_stat)
# print(number_in_queue_stat)
# print(number_available_servers_stat)

# print('{num:,d} customers arrived'.format(num=arrival_process.number_arrivals))
# print('{num:,d} customers served'.format(num=simple_server.number_served))

print('Avg number in queue = {avg:.4f}'.format(avg=number_in_queue_stat.mean))
utilization = 1.0 - number_available_servers_stat.mean / simple_server.total_number_servers
print("Avg utilization = {avg:.4f}".format(avg=utilization))