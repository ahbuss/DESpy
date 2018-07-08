from pip._vendor.pyparsing import infixNotation

from examples.entitycreator import EntityCreator
from examples.entityserver import EntityServer
from simkit.stats import SimpleStatsTally
from simkit.stats import CollectionSizeTimeVarying
from simkit.rand import RandomVariate
from simkit.simkit import EventList, SimEntityBase
from time import time

interarrivalTimeGenerator = RandomVariate.getInstance('Uniform',min=0.9, max=2.2)
entityCreator = EntityCreator(interarrivalTimeGenerator)
print(entityCreator.describe())

totalNumberServers=2
serviceTimeGenerator = RandomVariate.getInstance('Gamma', alpha=1.7, beta=1.8)
entityServer = EntityServer(totalNumberServers, serviceTimeGenerator)
print(entityServer.describe())

entityCreator.addSimEventListener(entityServer)

innerDelayInQueueStat = SimpleStatsTally("delayInQueue")
entityServer.addStateChangeListener(innerDelayInQueueStat)

innerNumberInQueueStat = CollectionSizeTimeVarying('queue')
entityServer.addStateChangeListener(innerNumberInQueueStat)

outerNumberInQueueStat = SimpleStatsTally('outerNumberInQueue')

outerDelayInQueueStat = SimpleStatsTally('meanDelayInQueue')

# print(getattr(entityServer, 'numberServers'))

runtime = 800.0
p = 0.975
numberReps = 100

EventList.stopAtTime(runtime)

start = time()
for rep in range(numberReps):
    EventList.reset()
    innerDelayInQueueStat.reset()
    innerNumberInQueueStat.reset()
    EventList.startSimulation()
    outerDelayInQueueStat.newObservation(innerDelayInQueueStat.mean)
    outerNumberInQueueStat.newObservation(innerNumberInQueueStat.mean)
end = time()
elapsed = end-start
print('{reps:d} replications of length {runtime:,.1f} took {time:,.4f} sec'.format(reps=numberReps,runtime=runtime, time=elapsed))
print('95% CI for number in queue: {mean:,.4f} \u00B1 {halfwidth:,.4f}'.format(mean=outerNumberInQueueStat.mean, halfwidth=outerNumberInQueueStat.halfwidth(p)))
print('95% CI for delay in queue: {mean:,.4f} \u00B1 {halfwidth:,.4f}'.format(mean=outerDelayInQueueStat.mean, halfwidth=outerDelayInQueueStat.halfwidth(p)))


