from examples.arrivalprocess import ArrivalProcess
from simkit.rand import RandomVariate
from simkit.simkit import EventList

arrivalProcess = ArrivalProcess(RandomVariate.getInstance('Constant', value=3.4))
print(arrivalProcess.describe())

print(EventList.simEntities)
arrivalProcess.persistent = False
EventList.reset()
print(EventList.simEntities)

