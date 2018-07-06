from heapq import heappush
from heapq import heappop
from enum import IntEnum
from enum import unique
from abc import ABC
from abc import abstractmethod
from math import nan
from decimal import Decimal
from itertools import count

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

    def __repr__(self):
        if self.arguments == None:
            argstr = ""
        else:
            argstr = '(' + str(self.arguments) + ')'
        return str(round(self.scheduledTime, 4)) + ' ' + self.eventName + ' ' + argstr + \
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

    @staticmethod
    def stopAtTime(time):
        EventList.stopTime = time
        Stopper()

    @staticmethod
    def reset():
        EventList.simTime = 0.0
        EventList.eventList.clear()
        for simEntity in EventList.simEntities:
            simEntity.reset()
            if hasattr(simEntity, 'doRun'):
                simEntity.waitDelay('Run', 0.0, Priority.HIGHEST)

    @staticmethod
    def scheduleEvent(simEvent):
        heappush(EventList.eventList, simEvent)

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
            if EventList.verbose:
                print('CurrentEvent: ' + str(EventList.currentEvent))
                print(EventList.dump())

class SimEntityBase:

    nextID = 1

    def __init__(self, name="SimEntity"):
        self.eventListeners = []
        self.stateChangeListeners = []
        self.name = type(self).__name__
        EventList.simEntities.append(self)
        self.id = SimEntityBase.nextID
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
            # if simEvent.arguments != None:
            #     method(simEvent.arguments)
            # else:
            #     method()
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
        event = SimEvent(self, eventName, EventList.simTime + delay, priority, *arguments)
        EventList.scheduleEvent(event)
        return event;

class Stopper(SimEntityBase):
    def __init__(self):
        SimEntityBase.__init__(self,'Stopper')

    def doRun(self):
        self.waitDelay('Stop', EventList.stopTime, Priority.LOWEST)

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
        return self.name + '.' + str(self.id) + '[' + str(round(self.creationTime,4)) +', ' + str(round(self.timeStamp,4)) + ']'
