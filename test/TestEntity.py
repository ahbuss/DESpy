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

interarrivalMean = 2.0
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
print('expected avg timeInSystem: {avg:.4f}'.format(avg=expected))
print('expected avg delayInQueue: {avg:.4f}'.format( avg=(expected * serviceMean / interarrivalMean)))

EventList.stopAtTime(100000.0)
EventList.verbose = False

EventList.reset()
EventList.startSimulation()

print('Simulation ended at time ' + str(EventList.simTime))

print(timeInSystemStat)
print(delayInQueueStat)
print(numberInQueueStat)