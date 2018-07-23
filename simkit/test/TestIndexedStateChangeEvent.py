from simkit.simkit import SimEntityBase
from simkit.simkit import EventList
from simkit.simkit import Priority
from simkit.simutil import SimpleStateChangeDumper

class TestIndexedStateChange(SimEntityBase):
    def __init__(self, number):
        SimEntityBase.__init__(self)
        self.number = number

    def run(self):
        self.schedule('init', 0.0,  0)

    def init(self, i):
        self.notify_indexed_state_change(i, 'foo', i)
        if i < self.number - 1:
            self.schedule('init', 0.0,  i+1)

if __name__=="__main__":
    test = TestIndexedStateChange(4)
    test.add_state_change_listener(SimpleStateChangeDumper())

    EventList.verbose = True

    EventList.reset()
    EventList.start_simulation()

