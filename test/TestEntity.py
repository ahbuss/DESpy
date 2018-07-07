from examples.entityserver import EntityServer
from simkit.rand import Exponential
from examples.entitycreator import EntityCreator
from simkit.simkit import EventList
from simkit.simutil import SimpleStateChangeDumper
from simkit.stats import SimpleStatsTally
from simkit.stats import SimpleStatsTimeVarying

serviceMean = 1.3
numberServers = 1
generator = Exponential(serviceMean)
entityServer = EntityServer(numberServers, generator)

print(entityServer)

interarrivalMean = 1.7
interarrival = Exponential(interarrivalMean)
entityCreator = EntityCreator(interarrival)
print (entityCreator)
print (entityCreator.generator)

entityCreator.addSimEventListener(entityServer)

dumper = SimpleStateChangeDumper()
# entityServer.addStateChangeListener(dumper)

delayInQueueStat = SimpleStatsTally("delayInQueue")
entityServer.addStateChangeListener(delayInQueueStat)

timeInSystemStat = SimpleStatsTally('timeInSystem')
entityServer.addStateChangeListener(timeInSystemStat)

numberInQueueStat = SimpleStatsTimeVarying("numberInQueue")
entityServer.addStateChangeListener(numberInQueueStat)
# queue = []
# heappush(queue, Entity() )
# heappush(queue, Entity() )
# print(queue)

expected = (serviceMean * interarrivalMean) / (interarrivalMean -serviceMean)
print('expected avg delayInQueue: ' + str(expected * serviceMean / interarrivalMean))
print('expected avg timeInSystem: ' + str(expected))

EventList.stopAtTime(1000000.0)
EventList.verbose = False

EventList.reset()
print(entityServer.numberAvailableServers)
EventList.startSimulation()

print('Simulation ended at time ' + str(EventList.simTime))

print(timeInSystemStat)
print(delayInQueueStat)
print(numberInQueueStat)