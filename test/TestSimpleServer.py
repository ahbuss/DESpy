from examples.arrivalprocess import ArrivalProcess
from examples.simpleserver import SimpleServer
from simkit.rand import RandomVariate

interarrivalTimeGenerator = RandomVariate.getInstance('Exponential', mean=1.7)
arrivalProcess = ArrivalProcess(interarrivalTimeGenerator)
print(arrivalProcess.describe())

numberServers = 2
serviceTimeGenerator = RandomVariate.getInstance('Gamma', alpha=1.7, beta=1.8)
simpleServer = SimpleServer(numberServers, serviceTimeGenerator)
print(simpleServer.describe())