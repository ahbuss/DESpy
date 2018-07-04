import Simkit
from Simkit import SimEvent, SimEntityBase, EventList
from heapq import heappush, heappop
from Simkit import Priority

if __name__=='__main__':
    source = SimEntityBase()
    name='ASimEvent'
    scheduled=42.0
    args=[]

    evt=SimEvent(source, name, scheduled, args)
    scheduled=21.5
    evt2=SimEvent(SimEntityBase('Foo'), name, scheduled, args, Priority.HIGH)
    evt3=SimEvent(source, 'AnotherSimEvent', 21.5, [], Priority.LOW)
    evt4=SimEvent(SimEntityBase('Bar'), 'AnEvent', 10.0, [1.0, 'Two'])

    heap = []
    heappush(heap, evt)
    heappush(heap, evt2)
    heappush(heap, evt3)
    heappush(heap, evt4)

    copy = heap.copy()
    copy.sort()

    dump='Event List:'
    for e in copy:
        dump += '\n' + str(e)

    print(dump)

    el = Simkit.EventList()

    evt = source.waitDelay('Foo', 1.0)
    evt1 = SimEntityBase('Baz').waitDelay('Bar', 2.0, [1])
    evt2 = SimEntityBase('Foobar').waitDelay('Foo', 2.0, [], Priority.HIGH)

    print (EventList.dump())


    print (Priority.DEFAULT < Priority.HIGH)
    print (Priority.DEFAULT > Priority.HIGH)
    # print(evt1 < evt2)
    # print(evt1 > evt2)

    copy = EventList.eventList
    copy.sort()
    for e in copy:
        print(e)

    print(evt1.__gt__(evt2))
