from simkit.rand import RandomVariate
from simkit.simkit import EventList
from simkit.simkit import SimEntityBase
from simkit.simkit import Adapter
from simkit.simutil import SimpleStateChangeDumper
from examples.arrivalprocess import BatchArrivalProcess
from examples.simpleserver import SimpleServer

interarrivalTimeGenerator = RandomVariate.getInstance('Exponential', mean=2.5)
batchGenerator = RandomVariate.getInstance('Discrete', values=[1,2,3,4,5],\
                                           frequencies=[20, 30, 40, 50, 60])
batchArrivalProcess = BatchArrivalProcess(interarrivalTimeGenerator, batchGenerator)
print(batchArrivalProcess.describe())

numberServers = 1
serviceTimeGenerator = RandomVariate.getInstance('Gamma', alpha=1.2, beta = 2.3)
simpleServer = SimpleServer(numberServers, serviceTimeGenerator)
print(simpleServer.describe())

adapter = Adapter('arrival1', 'arrival')
adapter.connect(batchArrivalProcess, simpleServer)

batchArrivalProcess.addStateChangeListener(SimpleStateChangeDumper())
simpleServer.addStateChangeListener(SimpleStateChangeDumper())

stopTime = 20.0

EventList.verbose = True
EventList.stopAtTime(stopTime)
EventList.stopOnEvent(10, 'arrival')

EventList.reset()
EventList.startSimulation()