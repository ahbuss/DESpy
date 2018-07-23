from examples.arrivalprocess import EntityCreator
from examples.entityserver import EntityServer
from simkit.simkit import EventList
from simkit.rand import RandomVariate
from simkit.simkit import Adapter
from simkit.simkit import Priority
from simkit.simkit import Entity

entity_creator = EntityCreator(RandomVariate.instance('Constant', value=2.3))
entity_server = EntityServer(1, RandomVariate.instance('Constant', value=2.2))
adapter = Adapter("entity_arrival", "arrival")
adapter.connect(entity_creator, entity_server)


# simEvent = entity_creator.waitDelay('Foo', 1.2, Priority.HIGH, Entity())
# print(simEvent)
# print(simEvent.id)
# copy = simEvent.copy()
# print(copy)
# print(copy.id)

EventList.stop_on_event(5, 'start_service')
EventList.verbose = True

EventList.reset()
EventList.start_simulation()