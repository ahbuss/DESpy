from simkit.simkit import EventList
from simkit.rand import RandomVariate
from simkit.simutil import SimpleStateChangeDumper
from simkit.simkit import Adapter
from examples.transferline import TransferLine
from examples.transferline import JobCreator
from examples.transferline import JobCreator

jobCreator = JobCreator(RandomVariate.getInstance('Exponential', mean=1.7))
print(jobCreator.describe())

numberStations = 3
numberMachines = [5, 4, 2]
serviceTimes = [RandomVariate.getInstance('Gamma', alpha=3.2, beta=2.3),\
                RandomVariate.getInstance('Uniform', min=4.5, max=6.7),
                RandomVariate.getInstance('Exponential', mean=3.0)]
transferLine = TransferLine(numberStations, numberMachines, serviceTimes)
print(transferLine.describe())

adapter = Adapter('jobArrival', 'arrival')
adapter.connect(jobCreator, transferLine)

transferLine.addStateChangeListener(SimpleStateChangeDumper())

# EventList.stopAtTime(20.0)

EventList.stopOnEvent(10, 'jobComplete')

EventList.verbose = True
EventList.reset()
EventList.startSimulation()