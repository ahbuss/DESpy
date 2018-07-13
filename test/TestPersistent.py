from examples.arrivalprocess import ArrivalProcess
from simkit.rand import RandomVariate
from simkit.simkit import EventList
from inspect import getmembers
arrivalProcess = ArrivalProcess(RandomVariate.getInstance('Constant', value=3.4))
print(arrivalProcess.describe())

print(EventList.sim_entities)
arrivalProcess.persistent = False
EventList.reset()
print(EventList.sim_entities)

print(getmembers(arrivalProcess))