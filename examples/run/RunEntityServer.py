from examples.entityserver import EntityServer
from simkit.rand import RandomVariate
from examples.entitycreator import EntityCreator
from simkit.simkit import EventList
from simkit.simutil import SimpleStateChangeDumper
from simkit.stats import SimpleStatsTally
from simkit.stats import SimpleStatsTimeVarying
from time import time

interarrivalMean = 1.7
interarrival = RandomVariate.instance('Exponential', mean=interarrivalMean)
entityCreator = EntityCreator(interarrival)
print (entityCreator.describe())

alpha = 1.7
beta = 1.8
numberServers = 2
generator = RandomVariate.instance('Gamma', alpha=alpha, beta=beta)
entityServer = EntityServer(numberServers, generator)

print(entityServer.describe())

entityCreator.addSimEventListener(entityServer)

dumper = SimpleStateChangeDumper()

delayInQueueStat = SimpleStatsTally("delayInQueue")
entityServer.addStateChangeListener(delayInQueueStat)

timeInSystemStat = SimpleStatsTally('timeInSystem')
entityServer.addStateChangeListener(timeInSystemStat)

numberInQueueStat = SimpleStatsTimeVarying("numberInQueue")
entityServer.addStateChangeListener(numberInQueueStat)
serviceMean = alpha * beta

EventList.stopAtTime(100000.0)
EventList.verbose = False

start = time()
EventList.reset()
EventList.startSimulation()
end = time()

print('\nSimulation took {time:,.3f} sec'.format(time=(end-start)))
print('Simulation ended at simTime {time:,.0f}\n'.format(time=EventList.simtime))

print('Avg time in system = {avg:,.4f}'.format(avg=timeInSystemStat.mean))
print('Avg delay in queue = {avg:,.4f}'.format(avg=delayInQueueStat.mean))
print('Avg number in queue = {avg:,.4f}'.format(avg=numberInQueueStat.mean))