from examples.serverwithreneges import CustomerCreator
from examples.serverwithreneges import ServerWithReneges
from simkit.rand import RandomVariate
from simkit.simkit import EventList
from simkit.stats import SimpleStatsTally
from simkit.stats import CollectionSizeTimeVarying
from time import time

interarrivalGenerator = RandomVariate.getInstance('Exponential', mean=1.5)
renegeGenerator = RandomVariate.getInstance('Uniform', min=2.0, max=6.0)
creator = CustomerCreator(interarrivalGenerator, renegeGenerator)
print(creator.describe())

totalNumberServers = 2
serviceTimeGenerator = RandomVariate.getInstance('Gamma', alpha=2.5, beta=1.2)
server = ServerWithReneges(totalNumberServers, serviceTimeGenerator)
print (server.describe())

creator.addSimEventListener(server)

delayInQueueStat = SimpleStatsTally('delayInQueue')
server.addStateChangeListener(delayInQueueStat)

numberInQueueStat = CollectionSizeTimeVarying('queue')
server.addStateChangeListener(numberInQueueStat)

start = time()
EventList.stopAtTime(100000.0)
EventList.reset()
EventList.startSimulation()
end = time()

print('\nSimulation took {time:.4f} sec'.format(time = end - start))
print('Simulation ended at simTime {time:,.0f}\n'.format(time=EventList.simTime))
print('Avg delay in queue = {avg:,.4f}'.format(avg=(delayInQueueStat.mean)))
print('Avg number in queue = {avg:.4f}'.format(avg=numberInQueueStat.mean))
print('There have been {num:,d} reneges'.format(num=server.numberReneges))
print('There have been {num:,d} served'.format(num=delayInQueueStat.count))
print('% of potential customers reneging = {percent:.2f}% '.\
      format(percent=(100 * server.numberReneges/ (server.numberReneges + delayInQueueStat.count))))