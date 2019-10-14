from heapq import heappush
from heapq import heappop
from enum import IntEnum
from enum import unique
from abc import ABC
from abc import abstractmethod
from math import nan
from math import inf


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
    NEXT_ID = 0

    def __init__(self, source, event_name, scheduled_time, *arguments, **kwds):
        """

        :param source: Object that scheduled this SimEvent
        :param event_name: Name of event method
        :param scheduled_time: Time this SimEvent is scheduled to occur; should be \u2265 EventList.simtime
        :param arguments: optional arguments to be passed to the scheduled event
        :param kwds: optional keywords - currently if a Priority other tha DEFAULT is desired use the priority value;
                     e.g. priority=Priority.HIGH
        """
        if kwds.keys().__contains__('priority'):
            self.priority = kwds.get('priority')
        else:
            self.priority = Priority.DEFAULT
        self.source = source
        self.event_name = event_name
        self.scheduled_time = scheduled_time
        self.arguments = arguments
        self.id = SimEvent.NEXT_ID
        self.cancelled = False
        SimEvent.NEXT_ID += 1

    def copy(self):
        """:return copy of this SimEvent"""
        return SimEvent(self.source, self.event_name, self.scheduled_time, *self.arguments, priority=self.priority)

    def __repr__(self):
        if self.arguments == ():
            argstr = ""
        elif self.arguments.__len__() == 1:
            argstr = '(' + str(self.arguments[0]) + ')'
        else:
            argstr =  str(self.arguments)
        return '{0:,.4f}'.format(self.scheduled_time) + ' ' + self.event_name + ' ' + argstr + \
               ' <' + str(self.source) + '>'

    def __eq__(self, other):
        return (self.scheduled_time, self.priority) == (other.scheduled_time, other.priority)

    def __ne__(self, other):
        return (self.scheduled_time, self.priority) != (other.scheduled_time, other.priority)

    def __lt__(self, other):
        return (self.scheduled_time, self.priority) < (other.scheduled_time, other.priority)

    def __gt__(self, other):
        return other.__lt__(self)

    def __hash__(self):
        return hash((self.event_name, self.scheduled_time, self.arguments, self.priority))

class EventList:
    event_list = []
    sim_entities = []
    ignore_on_dump = []
    simtime = 0.0
    stop_time = 0.0
    verbose = False
    running = False
    current_event = None
    event_counts = {}
    stopper = None
    is_stop_on_event = False
    stop_event_name = None
    stop_event_number = inf
    stop_event_count = nan

    @staticmethod
    def stop_at_time(time):
        """:param time: Given time to stop simulation and clear event list """
        EventList.stop_time = time
        if EventList.sim_entities.__contains__(EventList.stopper):
            EventList.sim_entities.remove(EventList.stopper)
        EventList.stopper = Stopper()

    @staticmethod
    def stop_on_event(number_events, stop_event_name, *args):
        """

        :param number_events: Stop after this many stop_event_name events have occurred
        :param stop_event_name: Given event to stop after
        :param args: unused
        """
        EventList.is_stop_on_event = True
        EventList.stop_event_number = number_events
        EventList.stop_event_name = stop_event_name
        if EventList.sim_entities.__contains__(EventList.stopper):
            EventList.sim_entities.remove(EventList.stopper)

    @staticmethod
    def reset():
        """
        Sets simtime to 0.0
        Clears event_list
        Calls reset() on all (persistent) SimEntityBase's
        Schedules run event on all that have them
        Clears event counts if is_stop_on_event
        """
        EventList.simtime = 0.0
        EventList.event_list.clear()
        for sim_entity in EventList.sim_entities:
            if sim_entity.persistent:
                sim_entity.reset()
                if hasattr(sim_entity, 'run'):
                    sim_entity.schedule('run', 0.0, priority=Priority.HIGHEST)
            else:
                EventList.sim_entities.remove(sim_entity)
        if EventList.is_stop_on_event:
            EventList.stop_event_count = 0
            EventList.event_counts.clear()
            EventList.event_counts[EventList.stop_event_name] = 0

    @staticmethod
    def schedule(sim_event):
        heappush(EventList.event_list, sim_event)

    @staticmethod
    def cancel(event_name, *args):
        for sim_event in EventList.event_list:
            if sim_event.cancelled:
                continue
            if  event_name == sim_event.event_name and args == sim_event.arguments:
                sim_event.cancelled = True
                break

    @staticmethod
    def dump():
        dump_string = ""
        dump_string += '*** Event List ***\n'
        queue_copy = EventList.event_list.copy()
        queue_copy.sort()
        if not queue_copy:
            dump_string += '    <Empty>\n'
        for event in queue_copy:
            if not event.cancelled and not EventList.ignore_on_dump.__contains__(event.event_name):
                dump_string += str(event) + '\n'
        return dump_string

    @staticmethod
    def start_simulation():
        EventList.running = True
        if EventList.verbose:
            print('Starting Simulation...')
            print(EventList.dump())
        while EventList.running and EventList.event_list:
            EventList.current_event = heappop(EventList.event_list)
            if EventList.current_event.cancelled:
                continue
            EventList.simtime = EventList.current_event.scheduled_time
            EventList.current_event.source.process_sim_event(EventList.current_event)
            if not EventList.event_counts.keys().__contains__(EventList.current_event.event_name):
                EventList.event_counts[EventList.current_event.event_name] = 1
            else:
                EventList.event_counts[EventList.current_event.event_name] +=  1
            if EventList.verbose and not EventList.ignore_on_dump.__contains__(EventList.current_event.event_name):
                print('CurrentEvent: ' + str(EventList.current_event) + ' [' + str(EventList.event_counts[EventList.current_event.event_name]) + ']')
                print(EventList.dump())
            if EventList.is_stop_on_event:
                if EventList.event_counts[EventList.stop_event_name] == EventList.stop_event_number:
                    EventList.stop_simulation()

    @staticmethod
    def stop_simulation():
        EventList.running = False

    @staticmethod
    def cold_reset():
        EventList.reset()
        EventList.sim_entities.clear()
        EventList.event_counts.clear()
        SimEntityBase.NEXT_ID = 1
        if not EventList.is_stop_on_event and EventList.stop_time > 0.0:
            EventList.stop_at_time(EventList.stop_time)

class Adapter:

    def __init__(self, source_event_name, target_event_name):
        self.source_event_name = source_event_name
        self.target_event_name = target_event_name
        self.source =None
        self.target = None

    def connect(self, source, target):
        self.source = source
        self.target = target
        self.source.add_sim_event_listener(self)

    def disconnect(self, source, target):
        self.source = None
        self.target = None

    def process_sim_event(self, simEvent):
        if simEvent.event_name == self.source_event_name:
            new_event = simEvent.copy()
            new_event.event_name = self.target_event_name
            self.target.process_sim_event(new_event)


class SimEntityBase:

    NEXT_ID = 1

    def __init__(self, **args):
        self.event_listeners = []
        self.state_change_listeners = []
        self.name = type(self).__name__
        self.id = SimEntityBase.NEXT_ID
        self.persistent = True
        EventList.sim_entities.append(self)
        SimEntityBase.NEXT_ID += 1

    def __repr__(self):
        return self.name + '.' + str(self.id)

    def reset(self):
        pass

    def process_sim_event(self, sim_event):
        method_name = sim_event.event_name
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            if (sim_event.arguments.__len__() > 0):
                method(*sim_event.arguments)
            else:
                method()
        if sim_event.source == self:
            self.notify_sim_event_listeners(sim_event)

    def add_sim_event_listener(self, sim_event_listener):
        if not sim_event_listener in self.event_listeners:
            self.event_listeners.append(sim_event_listener)

    def remove_sim_event_listener(self, sim_event_listener):
        self.event_listeners.remove(sim_event_listener)

    def add_state_change_listener(self, state_change_listener):
        if hasattr(state_change_listener, 'state_change'):
            if not state_change_listener in self.state_change_listeners:
                self.state_change_listeners.append(state_change_listener)

    def remove_state_change_listener(self, state_change_listener):
        self.state_change_listeners.remove(state_change_listener)

    def notify_state_change(self, state_name, state_value):
        state_change_event = StateChangeEvent(self, state_name, state_value)
        for state_change_listener in self.state_change_listeners:
            if hasattr(state_change_listener, 'state_change'):
                state_change_listener.state_change(state_change_event)

    def notify_indexed_state_change(self, index, state_name, state_value):
        state_change_event = IndexedStateChangeEvent(index, self, state_name, state_value)
        for state_change_listener in self.state_change_listeners:
            if hasattr(state_change_listener, 'state_change'):
                state_change_listener.state_change(state_change_event)

    def notify_sim_event_listeners(self, sim_event):
        if sim_event.event_name != 'run':
            for listener in self.event_listeners:
                listener.process_sim_event(sim_event)

    def schedule(self, event_name, delay, *args, **kwds):
        if delay < 0.0:
            raise ValueError('delay must be \u2265 0.0: {delay:.3f}'.format(delay=delay))
        event = SimEvent(self, event_name, EventList.simtime + delay, *args, **kwds)
        EventList.schedule(event)
        return event;

    def cancel(self, event_name, *arguments):
        EventList.cancel(event_name, *arguments)

    def describe(self):
        description = self.name
        for property in self.__dict__.keys():
            if not ['name', 'state_change_listeners', 'event_listeners'].__contains__(property):
                value = self.__dict__.get(property)
                description += '\n\t' + property + " = " + str(value)
        return description

class Stopper(SimEntityBase):
    def __init__(self):
        SimEntityBase.__init__(self)
        self.stop_event = None
        self.id = 0
        SimEntityBase.NEXT_ID -= 1;

    def run(self):
        self.stop_event = self.schedule('stop', EventList.stop_time, priority=Priority.LOWEST)

    def stop(self):
        EventList.event_list.clear()

class StateChangeEvent:
    def __init__(self, source, state_name, state_value):
        self.source = source
        self.name = state_name
        self.value = state_value

    def __repr__(self):
        return str(self.source) + '> ' + str(self.name) + ': ' + str(self.value)

class IndexedStateChangeEvent(StateChangeEvent):
    def __init__(self, index, source, state_name, state_value):
        StateChangeEvent.__init__(self, source, state_name, state_value)
        self.index = index

    def __repr__(self):
        return '{source}> {name}[{index:d}]: {value}'.\
            format(source=self.source, name=self.name, index=self.index, value=str(self.value))

class StateChangeListener(ABC):

    @abstractmethod
    def state_change(self, state_change_event):
        pass

class Entity:
    NEXT_ID = 1

    def __init__(self, name='Entity'):
        self.name=name
        self.id = Entity.NEXT_ID
        self.creation_time = EventList.simtime
        self.time_stamp = EventList.simtime
        self.stamp_time()
        Entity.NEXT_ID += 1

    def stamp_time(self):
        self.time_stamp = EventList.simtime

    def elapsed_time(self):
        return EventList.simtime - self.time_stamp

    def age(self):
        return EventList.simtime - self.creation_time

    def __eq__(self, other):
        if other == None:
            return False
        else:
            return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if self.time_stamp < other.time_stamp:
            return True
        elif self.time_stamp > other.time_stamp:
            return False
        else:
            return self.id < other.id

    def __gt__(self, other):
        return not self.lt(self, other)

    def __hash__(self):
        return hash((self.name, self.creation_time, self.id))

    def __repr__(self):
        return self.name + '.' + str(self.id) + ' [' + str(round(self.creation_time, 4)) + ', ' + str(round(self.time_stamp, 4)) + ']'
