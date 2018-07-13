from examples.arrivalprocess import EntityCreator
from examples.entityserver import EntityServer
from simkit.simkit import EventList
from simkit.rand import RandomVariate
from simkit.simkit import Adapter
from simkit.simkit import Priority
from simkit.simkit import Entity

entityCreator = EntityCreator(RandomVariate.getInstance('Constant', value=2.3))
entityServer = EntityServer(1, RandomVariate.getInstance('Constant', value=2.2))
adapter = Adapter("entityArrival", "arrival")
adapter.connect(entityCreator, entityServer)


# simEvent = entityCreator.waitDelay('Foo', 1.2, Priority.HIGH, Entity())
# print(simEvent)
# print(simEvent.id)
# copy = simEvent.copy()
# print(copy)
# print(copy.id)

EventList.stop_on_event(5, 'startService')
EventList.verbose = True

EventList.reset()
EventList.startSimulation()