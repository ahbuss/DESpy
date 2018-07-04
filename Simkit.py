from heapq import heappush, heappop
from enum import IntEnum, unique

__author__ = "Arnold Buss"

@unique
class Priority(IntEnum):
    LOWEST = 1E10
    LOWER = 1000
    LOW = 100
    DEFAULT = 0
    HIGH = -100
    HIGHER = -1000
    HIGHEST = -1E10

class SimEvent:
    nextID = 0

    def __init__(self, source, eventName, scheduledTime, arguments, priority=Priority.DEFAULT):
        self.source = source
        self.eventName = eventName
        self.scheduledTime = scheduledTime
        self.arguments = arguments
        self.priority = priority
        self.id = SimEvent.nextID
        self.cancelled = False
        SimEvent.nextID += 1

    def __repr__(self):
        return str(self.scheduledTime) + ' ' + self.eventName + ' ' + str(self.arguments) + \
               ' <' + str(self.source) + '>'

    def __eq__(self, other):
        return (self.scheduledTime, self.priority) == (other.scheduledTime, other.priority)

    def __ne__(self, other):
        return (self.scheduledTime, self.priority) != (other.scheduledTime, other.priority)

    def __lt__(self, other):
        return (self.scheduledTime, self.priority) < (other.scheduledTime, other.priority)

    def __gt__(self, other):
        return other.__lt__(self)

class EventList:
    eventList = []
    simEntities = []
    simTime = 0.0
    stopTime = 0.0
    verbose = False
    running = False

    @staticmethod
    def stopAtTime(time):
        EventList.stopTime = time

    @staticmethod
    def reset():
        EventList.simTime = 0.0
        EventList.eventList.clear()
        for simEntity in EventList.simEntities:
            if hasattr(simEntity, 'doRun'):
                simEntity.waitDelay('Run', 0.0, Priority.HIGHEST)

    @staticmethod
    def scheduleEvent(simEvent):
        heappush(EventList.eventList, simEvent)

    @staticmethod
    def dump():
        dump = '*** Event List ***\n'
        queueCopy = EventList.eventList.copy()
        queueCopy.sort()
        if not queueCopy:
            dump += '    <Empty>\n'
        for event in queueCopy:
            if not event.cancelled:
                dump += str(event) + '\n'
        return dump


class SimEntityBase:

    nextID = 0

    def __init__(self, name="SimEntity"):
        self.eventListsners = []
        self.propertyChangeListsners = []
        self.name = name
        EventList.simEntities.append(self)
        self.id = SimEntityBase.nextID
        SimEntityBase.nextID += 1

    def __repr__(self):
        return self.name + '.' + str(self.id)

    def processSimEvent(self, simEvent):
        methodName = 'do' + simEvent.eventName

    def waitDelay(self, eventName, delay, arguments=[], priority=0):
        event = SimEvent(self, eventName, EventList.simTime + delay, arguments, priority)
        EventList.scheduleEvent(event)
        return event;





