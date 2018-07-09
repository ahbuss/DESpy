from heapq import heappush
from heapq import heappop
from enum import IntEnum
from enum import unique
from abc import ABC
from abc import abstractmethod
from math import nan
from math import inf
from decimal import Decimal
from itertools import count, product
from sched import Event

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

    def __init__(self, source, eventName, scheduledTime,  priority=Priority.DEFAULT, *arguments):
        self.source = source
        self.eventName = eventName
        self.scheduledTime = scheduledTime
        self.arguments = arguments
        self.priority = priority
        self.id = SimEvent.nextID
        self.cancelled = False
        SimEvent.nextID += 1

    def copy(self):
        return SimEvent(self.source, self.eventName, self.scheduledTime, self.priority, *self.arguments)

    def __repr__(self):
        if self.arguments == ():
            argstr = ""
        elif self.arguments.__len__() == 1:
            argstr = '(' + str(self.arguments[0]) + ')'
        else:
            argstr =  str(self.arguments)
        return '{0:,.4f}'.format(self.scheduledTime) + ' ' + self.eventName + ' ' + argstr + \
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
    currentEvent = None
    eventCounts = {}
    stopper = None
    stopOnEvent = False
    stopEventName = None
    stopEventNumber = inf
    stopEventCount = nan

    @staticmethod
    def stopAtTime(time):
        EventList.stopTime = time
        EventList.stopper = Stopper()

    @staticmethod
    def stopOnEvent(stopEventNumber, stopEventName, *args):
        EventList.stopOnEvent = True
        EventList.stopEventNumber = stopEventNumber
        EventList.stopEventName = stopEventName
        if EventList.simEntities.__contains__(EventList.stopper):
            EventList.simEntities.remove(EventList.stopper)

    @staticmethod
    def reset():
        EventList.simTime = 0.0
        EventList.eventList.clear()
        for simEntity in EventList.simEntities:
            if simEntity.persistent:
                simEntity.reset()
                if hasattr(simEntity, 'doRun'):
                    simEntity.waitDelay('Run', 0.0, Priority.HIGHEST)
            else:
                EventList.simEntities.remove(simEntity)
        if EventList.stopOnEvent:
            EventList.stopEventCount = 0
            EventList.eventCounts.clear()
            EventList.eventCounts[EventList.stopEventName] = 0

    @staticmethod
    def scheduleEvent(simEvent):
        heappush(EventList.eventList, simEvent)

    @staticmethod
    def cancelEvent(eventName, *args):
        for simEvent in EventList.eventList:
            if  eventName == simEvent.eventName and args == simEvent.arguments:
                simEvent.cancelled = True
                break

    @staticmethod
    def dump():
        dumpString = ""
        dumpString += '*** Event List ***\n'
        queueCopy = EventList.eventList.copy()
        queueCopy.sort()
        if not queueCopy:
            dumpString += '    <Empty>\n'
        for event in queueCopy:
            if not event.cancelled:
                dumpString += str(event) + '\n'
        return dumpString

    @staticmethod
    def startSimulation():
        EventList.running = True
        if EventList.verbose:
            print('Starting Simulation...')
            print(EventList.dump())
        while EventList.running and EventList.eventList:
            EventList.currentEvent = heappop(EventList.eventList)
            if EventList.currentEvent.cancelled:
                continue
            EventList.simTime = EventList.currentEvent.scheduledTime
            EventList.currentEvent.source.processSimEvent(EventList.currentEvent)
            if not EventList.eventCounts.keys().__contains__(EventList.currentEvent.eventName):
                EventList.eventCounts[EventList.currentEvent.eventName] = 1
            else:
                EventList.eventCounts[EventList.currentEvent.eventName] +=  1
            if EventList.verbose:
                print('CurrentEvent: ' + str(EventList.currentEvent) + ' [' + str(EventList.eventCounts[EventList.currentEvent.eventName]) + ']')
                print(EventList.dump())
            if EventList.stopOnEvent:
                if EventList.eventCounts[EventList.stopEventName] == EventList.stopEventNumber:
                    EventList.stopSimulation()

    @staticmethod
    def stopSimulation():
        EventList.running = False

    @staticmethod
    def coldReset():
        EventList.reset()
        EventList.simEntities.clear()
        SimEntityBase.nextID = 1
        if not EventList.stopOnEvent:
            EventList.stopAtTime(EventList.stopTime)

class Adapter:

    def __init__(self, sourceEventName, targetEventName):
        self.sourceEventName = sourceEventName
        self.targetEventName = targetEventName
        self.source =None
        self.target = None

    def connect(self, source, target):
        self.source = source
        self.target = target
        self.source.addSimEventListener(self)

    def disconnect(self, source, target):
        self.source = None
        self.target = None

    def processSimEvent(self, simEvent):
        if simEvent.eventName == self.sourceEventName:
            newEvent = simEvent.copy()
            newEvent.eventName = self.targetEventName
            self.target.processSimEvent(newEvent)


class SimEntityBase:

    nextID = 1

    def __init__(self):
        self.eventListeners = []
        self.stateChangeListeners = []
        self.name = type(self).__name__
        self.id = SimEntityBase.nextID
        self.persistent = True
        EventList.simEntities.append(self)
        SimEntityBase.nextID += 1

    def __repr__(self):
        return self.name + '.' + str(self.id)

    def reset(self):
        pass

    def processSimEvent(self, simEvent):
        methodName = 'do' + simEvent.eventName
        if hasattr(self, methodName):
            method = getattr(self, methodName)
            if (simEvent.arguments.__len__() > 0):
                method(*simEvent.arguments)
            else:
                method()
        if simEvent.source == self:
            self.notifySimEventListeners(simEvent)

    def addSimEventListener(self, simEventListener):
        if not simEventListener in self.eventListeners:
            self.eventListeners.append(simEventListener)

    def removeSimEventListener(self, simEventListener):
        self.eventListeners.remove(simEventListener)

    def addStateChangeListener(self, stateChangeListener):
        if hasattr(stateChangeListener, 'stateChange'):
            if not stateChangeListener in self.stateChangeListeners:
                self.stateChangeListeners.append(stateChangeListener)

    def removeStateChangeListener(self, stateChangeListener):
        self.stateChangeListeners.remove(stateChangeListener)

    def notifyStateChange(self, stateName, stateValue):
        stateChangeEvent = StateChangeEvent(self, stateName, stateValue)
        for stateChangeListener in self.stateChangeListeners:
            if hasattr(stateChangeListener, 'stateChange'):
                stateChangeListener.stateChange(stateChangeEvent)

    def notifySimEventListeners(self, simEvent):
        if simEvent.eventName != 'Run':
            for listener in self.eventListeners:
                listener.processSimEvent(simEvent)

    def waitDelay(self, eventName, delay, priority=Priority.DEFAULT, *arguments):
        if delay < 0.0:
            raise ValueError('delay must be \u2265 0.0: {delay:.3f}'.format(delay=delay))
        event = SimEvent(self, eventName, EventList.simTime + delay, priority, *arguments)
        EventList.scheduleEvent(event)
        return event;

    def interrupt(self, eventName, *arguments):
        EventList.cancelEvent(eventName, *arguments)

    def describe(self):
        description = self.name
        for property in self.__dict__.keys():
            if not ['name', 'stateChangeListeners', 'eventListeners'].__contains__(property):
                value = self.__dict__.get(property)
                description += '\n\t' + property + " = " + str(value)
        return description

class Stopper(SimEntityBase):
    def __init__(self):
        SimEntityBase.__init__(self)
        self.stopEvent = None

    def doRun(self):
        self.stopEvent = self.waitDelay('Stop', EventList.stopTime, Priority.LOWEST)

    def doStop(self):
        EventList.eventList.clear()

class StateChangeEvent:
    def __init__(self, source, stateName, stateValue):
        self.source = source
        self.name = stateName
        self.value = stateValue

    def __repr__(self):
        return str(self.source) + '> ' + str(self.name) + ': ' + str(self.value)

class StateChangeListener(ABC):

    @abstractmethod
    def stateChange(self, stateChangeEvent):
        pass

class Entity:
    nextID = 1

    def __init__(self, name='Entity'):
        self.name=name
        self.id = Entity.nextID
        self.creationTime = EventList.simTime
        self.timeStamp = EventList.simTime
        self.stampTime()
        Entity.nextID += 1

    def stampTime(self):
        self.timeStamp = EventList.simTime

    def elapsedTime(self):
        return EventList.simTime - self.timeStamp

    def age(self):
        return EventList.simTime - self.creationTime

    def __eq__(self, other):
        if other == None:
            return False
        else:
            return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if self.timeStamp < other.timeStamp:
            return True
        elif self.timeStamp > other.timeStamp:
            return False
        else:
            return self.id < other.id

    def __gt__(self, other):
        return not self.lt(self, other)

    def __repr__(self):
        return self.name + '.' + str(self.id) + ' [' + str(round(self.creationTime,4)) +', ' + str(round(self.timeStamp,4)) + ']'
