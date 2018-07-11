from simkit.simkit import SimEvent, SimEntityBase, EventList
from heapq import heappush
from simkit.simkit import Priority

class TestSimEntity(SimEntityBase):

    def __init__(self, name='TestSimEntity'):
        SimEntityBase.__init__(self)
        self.count = 0

    def reset(self):
        self.count = 0

    def run(self):
        self.notifyStateChange("count", self.count)
        self.waitDelay('foo', 0.0)

    def foo(self):
        self.count += 1
        self.notifyStateChange('count', self.count)

if __name__=='__main__':
    source = TestSimEntity()
    name='aSimEvent'
    scheduled=42.0
    args=[]

    evt=SimEvent(source, name, scheduled, args)
    scheduled=21.5
    evt2=SimEvent(TestSimEntity('Foo'), name, scheduled, args, Priority.HIGH)
    evt3=SimEvent(source, 'anotherSimEvent', 21.5, [], Priority.LOW)
    evt4=SimEvent(TestSimEntity('bar'), 'anEvent', 10.0, [1.0, 'Two'])

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

    el = EventList()

    evt = source.schedule('Foo', 1.0)
    evt1 = SimEntityBase().schedule('bar', 2.0, [1])
    evt2 = SimEntityBase().schedule('boo', 2.0, [], priority=Priority.HIGH)

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

    print (getattr(source, 'processSimEvent'))
    method = getattr(source, 'processSimEvent')
    method(evt)
