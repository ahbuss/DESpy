from examples.serverwithreneges import CustomerCreator
from examples.serverwithreneges import ServerWithReneges
from simkit.rand import RandomVariate
from simkit.simkit import EventList
from simkit.stats import SimpleStatsTally
from simkit.stats import CollectionSizeTimeVarying

interarrivalGenerator = RandomVariate.getInstance('Exponential', mean=1.5)
renegeGenerator = RandomVariate.getInstance('Uniform', min=2.0, max=6.0)
creator = CustomerCreator(interarrivalGenerator, renegeGenerator)
print(creator)

totalNumberServers = 2
serviceTimeGenerator = RandomVariate.getInstance('Gamma', alpha=2.5, beta=1.2)
server = ServerWithReneges(totalNumberServers, serviceTimeGenerator)
print (server)

creator.addSimEventListener(server)

# server.addStateChangeListener(SimpleStateChangeDumper())

delayInQueueStat = SimpleStatsTally('delayInQueue')
server.addStateChangeListener(delayInQueueStat)

numberInQueueStat = CollectionSizeTimeVarying('queue')
server.addStateChangeListener(numberInQueueStat)

EventList.verbose = False
EventList.stopAtTime(100000.0)

EventList.reset()
EventList.startSimulation()

print(delayInQueueStat)
print(numberInQueueStat)