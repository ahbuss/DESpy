"""
This example executes the Simple Server component for one replication, estimating the expected average number in
queue and utilization of servers. Arrivals are using the ArrivalProcess component

Parameters Used:
    ArrivalProcess: Exponential(1.7) interarrival times
    SimpleServer: 2 servers, Gamma(1.7, 1.8) service times
    Run length: 100,000 time units
"""
from examples.arrivalprocess import ArrivalProcess
from examples.simpleserver import SimpleServer
from simkit.rand import RandomVariate
from simkit.simkit import EventList
from simkit.stats import SimpleStatsTimeVarying
from simkit.simutil import SimpleStateChangeDumper
from time import time

interarrivalTimeGenerator = RandomVariate.getInstance('Exponential', mean=1.7)
arrivalProcess = ArrivalProcess(interarrivalTimeGenerator)

numberServers = 2;
serviceTimeGenerator = RandomVariate.getInstance('Gamma', alpha=1.7, beta=1.8)
simpleServer = SimpleServer(numberServers, serviceTimeGenerator)

arrivalProcess.addSimEventListener(simpleServer)

numberInQueueStat = SimpleStatsTimeVarying('numberInQueue')
numberAvailableServersStat = SimpleStatsTimeVarying('numberAvailableServers')

simpleServer.addStateChangeListener(numberInQueueStat)
simpleServer.addStateChangeListener(numberAvailableServersStat)

print(arrivalProcess.describe())
print(simpleServer.describe())
print()


stopTime = 100000;
EventList.stopAtTime(stopTime)

start = time()
EventList.reset()
EventList.startSimulation()
end = time()

elapsed = end - start
print('Simulation took {time:.3f} sec'.format(time=elapsed))
print('Simulation ended at simTime {time:,.0f}'.format(time=EventList.simtime))
utilization = 1.0 - numberAvailableServersStat.mean / simpleServer.totalNumberServers
print('Avg # in queue = \t{avg:.4f}'.format(avg=numberInQueueStat.mean))
print('Avg # utilization = {avg:.4f}'.format(avg=utilization))