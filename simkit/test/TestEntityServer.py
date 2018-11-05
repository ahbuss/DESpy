from simkit.examples.entityserver import EntityServer
from simkit.rand import Exponential
from simkit.examples.entitycreator import EntityCreator
from simkit.base import EventList
from simkit.simutil import SimpleStateChangeDumper
from simkit.stats import SimpleStatsTally
from simkit.stats import SimpleStatsTimeVarying

serviceMean = 1.3
numberServers = 1
generator = Exponential(serviceMean)
entityServer = EntityServer(numberServers, generator)

print(entityServer)

interarrivalMean = 2.0
interarrival = Exponential(interarrivalMean)
entityCreator = EntityCreator(interarrival)
print (entityCreator)
print (entityCreator.interarrival_time_generator)

entityCreator.add_sim_event_listener(entityServer)

dumper = SimpleStateChangeDumper()
# entity_server.add_state_change_listener(dumper)

delayInQueueStat = SimpleStatsTally("delayInQueue")
entityServer.add_state_change_listener(delayInQueueStat)

timeInSystemStat = SimpleStatsTally('time_in_system')
entityServer.add_state_change_listener(timeInSystemStat)

numberInQueueStat = SimpleStatsTimeVarying("number_in_queue")
entityServer.add_state_change_listener(numberInQueueStat)
# queue = []
# heappush(queue, Entity() )
# heappush(queue, Entity() )
# print(queue)

expected = (serviceMean * interarrivalMean) / (interarrivalMean -serviceMean)
print('expected avg time_in_system: {avg:.4f}'.format(avg=expected))
print('expected avg delayInQueue: {avg:.4f}'.format( avg=(expected * serviceMean / interarrivalMean)))

EventList.stop_at_time(100000.0)
EventList.verbose = False

EventList.reset()
EventList.start_simulation()

print('Simulation ended at time ' + str(EventList.simtime))

print(timeInSystemStat)
print(delayInQueueStat)
print(numberInQueueStat)