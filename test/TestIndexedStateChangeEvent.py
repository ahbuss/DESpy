from simkit.simkit import SimEntityBase
from simkit.simkit import EventList
from simkit.simkit import Priority
from simkit.simutil import SimpleStateChangeDumper

class TestIndexedStateChange(SimEntityBase):
    def __init__(self, number):
        SimEntityBase.__init__(self)
        self.number = number

    def run(self):
        self.waitDelay('init', 0.0, Priority.DEFAULT, 0)

    def init(self, i):
        self.notifyIndexedStateChange(i, 'foo', i)
        if i < self.number - 1:
            self.waitDelay('init', 0.0, Priority.DEFAULT, i+1)

if __name__=="__main__":
    test = TestIndexedStateChange(4)
    test.addStateChangeListener(SimpleStateChangeDumper())

    EventList.verbose = True

    EventList.reset()
    EventList.startSimulation()

