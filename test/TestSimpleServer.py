from examples.arrivalprocess import ArrivalProcess
from examples.simpleserver import SimpleServer
from simkit.rand import RandomVariate
from simkit.stats import SimpleStatsTimeVarying
from simkit.simkit import EventList
from simkit.simutil import SimpleStateChangeDumper

interarrivalTimeGenerator = RandomVariate.getInstance('Uniform', min=0.9, max=2.2)
arrivalProcess = ArrivalProcess(interarrivalTimeGenerator)
print(arrivalProcess.describe())

numberServers = 3
serviceTimeGenerator = RandomVariate.getInstance('Gamma', alpha=2, beta=2.2)
simpleServer = SimpleServer(numberServers, serviceTimeGenerator)
print(simpleServer.describe())

arrivalProcess.addSimEventListener(simpleServer)

numberInQueueStat = SimpleStatsTimeVarying('numberInQueue')
numberAvailableServersStat = SimpleStatsTimeVarying('numberAvailableServers')

simpleServer.addStateChangeListener(numberInQueueStat)
simpleServer.addStateChangeListener(numberAvailableServersStat)

# simpleServer.addStateChangeListener(SimpleStateChangeDumper())

serviceMean = simpleServer.serviceTimeGenerator.alpha * simpleServer.serviceTimeGenerator.beta
arrivalMean = (arrivalProcess.generator.min + arrivalProcess.generator.max) * 0.5
intensity = serviceMean / (simpleServer.totalNumberServers * arrivalMean)

print('traffic intensity = {rho:.4f}'.format(rho = intensity))

stopTime = 100000
# stopTime = 50
# EventList.verbose = True

EventList.stopAtTime(stopTime)
EventList.reset()
EventList.startSimulation()

print('Simulation ended at time {time:,.2f}'.format(time=EventList.simtime))

# print(numberInQueueStat)
# print(numberAvailableServersStat)

print('{num:,d} customers arrived'.format(num=arrivalProcess.number_arrivals))
print('{num:,d} customers served'.format(num=simpleServer.numberServed))

print('Avg number in queue = {avg:.4f}'.format(avg=numberInQueueStat.mean))
utilization = 1.0 - numberAvailableServersStat.mean / simpleServer.totalNumberServers
print("Avg utilization = {avg:.4f}".format(avg=utilization))