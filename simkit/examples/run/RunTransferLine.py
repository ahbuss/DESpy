from simkit.simkit import EventList
from simkit.rand import RandomVariate
from simkit.simkit import Adapter
from simkit.stats import IndexedSimpleStatsTimeVarying
from simkit.stats import IndexedSimpleStatsTally
from simkit.stats import SimpleStatsTally
from simkit.stats import IndexedCollectionSizeTimeVaryingStat
from simkit.examples.transferline import TransferLine
from simkit.examples.transferline import JobCreator
from time import time

job_creator = JobCreator(RandomVariate.instance('Exponential', mean=1.7))
print(job_creator.describe())

number_stations = 3
number_machines = [5, 4, 2]
service_times = [RandomVariate.instance('Gamma', alpha=3.2, beta=2.3), \
                 RandomVariate.instance('Uniform', min=4.5, max=6.7),
                 RandomVariate.instance('Exponential', mean=3.0)]
transfer_line = TransferLine(number_stations, number_machines, service_times)
print(transfer_line.describe())

adapter = Adapter('job_arrival', 'arrival')
adapter.connect(job_creator, transfer_line)

number_available_machines_stat = IndexedSimpleStatsTimeVarying('number_available_machines')
transfer_line.add_state_change_listener(number_available_machines_stat)

delay_in_queue_stat = IndexedSimpleStatsTally('delay_in_queue')
transfer_line.add_state_change_listener(delay_in_queue_stat)

time_at_station_stat = IndexedSimpleStatsTally('time_at_station')
transfer_line.add_state_change_listener(time_at_station_stat)

time_in_system_stat = SimpleStatsTally('time_in_system')
transfer_line.add_state_change_listener(time_in_system_stat)

number_in_queue_stat = IndexedCollectionSizeTimeVaryingStat('queue')
transfer_line.add_state_change_listener(number_in_queue_stat)

total_delay_in_queue_stat = SimpleStatsTally('total_delay_in_queue')
transfer_line.add_state_change_listener(total_delay_in_queue_stat)

time_in_system_stat = SimpleStatsTally('time_in_system')
transfer_line.add_state_change_listener(time_in_system_stat)

EventList.stop_at_time(100000.0)

start = time()
EventList.verbose = False
EventList.reset()
EventList.start_simulation()
end = time()

print('\nSimulation run took {sec:.4f} sec'.format(sec=(end-start)))
print('Simulation ended at simtime {time:,.0f}'.format(time=EventList.simtime))

print('Number of Arrivals:\t{num:,d}'.format(num=job_creator.number_arrivals))
print('Number completed:  \t{num:,d}'.format(num=time_in_system_stat.count))

print('\nUsing Direct Estimation:')
print('Station\tAvg Util\tAvg # in Q\tAvg Delay in Q\tAvg time at station')
for station in range(transfer_line.number_stations):
    utilization = 1.0 - number_available_machines_stat.mean(station) / transfer_line.number_machines[station]
    print('   {station:d}\t{util:.3f}\t\t  {numinq:.3f}\t\t  {delay:.3f}\t\t\t{timeas:.3f}'.\
          format(station=station, numinq=number_in_queue_stat.mean(station), util=utilization, delay=delay_in_queue_stat.mean(station),\
                 timeas=time_at_station_stat.mean(station)))

arrival_rate = job_creator.number_arrivals / EventList.simtime

print('\nUsing Little\'s Formula:')
print('Station\tAvg Delay\tAvg Time at station')
for station in range(transfer_line.number_stations):
    number_arrivals_to_station = delay_in_queue_stat.count(station) + len(transfer_line.queue[station]) + \
            transfer_line.number_machines[station] - transfer_line.number_available_machines[station]
    arrival_rate_to_station = number_arrivals_to_station / EventList.simtime
    print('   {station:d}\t   {delay:,.3f}\t   {time:,.3f}'.format(station=station,\
                        delay=(number_in_queue_stat.mean(station)/arrival_rate),\
                        time = ((number_in_queue_stat.mean(station) + transfer_line.number_machines[station] - \
                                number_available_machines_stat.mean(station))/arrival_rate)))

print('\nAvg total delay in queue\t{delay:,.3f}'.format(delay=total_delay_in_queue_stat.mean))
print('Avg total time in system\t{time:,.3f}'.format(time=time_in_system_stat.mean))