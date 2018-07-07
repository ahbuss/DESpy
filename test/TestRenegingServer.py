from examples.serverwithreneges import CustomerCreator
from examples.serverwithreneges import ServerWithReneges
from simkit.rand import RandomVariate
from simkit.simkit import EventList
from simkit.stats import SimpleStatsTally
from simkit.stats import CollectionSizeTimeVarying
from simkit.simutil import SimpleStateChangeDumper

interarrivalGenerator = RandomVariate.getInstance('Exponential', mean=1.5)
renegeGenerator = RandomVariate.getInstance('Uniform', min=2.0, max=6.0)
creator = CustomerCreator(interarrivalGenerator, renegeGenerator)
print(creator.describe())

totalNumberServers = 2
serviceTimeGenerator = RandomVariate.getInstance('Gamma', alpha=2.5, beta=1.2)
server = ServerWithReneges(totalNumberServers, serviceTimeGenerator)
print (server.describe())

creator.addSimEventListener(server)

# server.addStateChangeListener(SimpleStateChangeDumper())

delayInQueueStat = SimpleStatsTally('delayInQueue')
server.addStateChangeListener(delayInQueueStat)

numberInQueueStat = CollectionSizeTimeVarying('queue')
server.addStateChangeListener(numberInQueueStat)

EventList.verbose = False
EventList.stopAtTime(100000.0)
EventList.stopOnEvent(10000, 'Renege')
EventList.reset()
EventList.startSimulation()

print('Simulation ended at time ' + str(EventList.simTime))
print('Avg delay in queue = ' + str(delayInQueueStat.mean))
print('Avg number in queue = ' + str(numberInQueueStat.mean))
print('There have been ' + str(server.numberReneges) + ' reneges')
print('There have been ' + str(delayInQueueStat.count) + ' served')
print('% reneges = ' + str(100 * server.numberReneges/ (server.numberReneges + delayInQueueStat.count)))