from simkit.simkit import EventList
from simkit.rand import RandomVariate
from simkit.simkit import Adapter
from simkit.stats import IndexedSimpleStatsTimeVarying
from simkit.stats import IndexedSimpleStatsTally
from simkit.stats import IndexedCollectionSizeTimeVaryingStat
from examples.transferline import TransferLine
from examples.transferline import JobCreator
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

number_in_queue_stat = IndexedCollectionSizeTimeVaryingStat('queue')
transfer_line.add_state_change_listener(number_in_queue_stat)

EventList.stop_at_time(100000.0)

start = time()
EventList.verbose = False
EventList.reset()
EventList.start_simulation()
end = time()

print('\nSimulation run took {sec:.4f} sec'.format(sec=(end-start)))
print('Simulation ended at simtime {time:,.0f}'.format(time=EventList.simtime))

print('Station\tAvg Util\tAvg # in Q\tAvg Delay\tAvg time at station')
for station in range(transfer_line.number_stations):
    utilization = 1.0 - number_available_machines_stat.mean(station) / transfer_line.number_machines[station]
    print('   {station:d}\t{util:.3f}\t\t  {numinq:.3f}\t\t  {delay:.3f}\t\t\t{timeas:.3f}'.\
          format(station=station, numinq=number_in_queue_stat.mean(station), util=utilization, delay=delay_in_queue_stat.mean(station),\
                 timeas=time_at_station_stat.mean(station)))
# print(number_available_machines_stat)