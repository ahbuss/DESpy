from simkit import SimEntityBase
from simkit import EventList
from simutil import SimpleStateChangeDumper

class Pinger(SimEntityBase):

    def __init__(self):
        SimEntityBase.__init__(self, 'Pinger')
        self.count = 0;

    def reset(self):
        self.count = 0

    def doRun(self):
        self.notifyStateChange("count", self.count)
        self.waitDelay('Ping', 1.1)

    def doPing(self):
        self.count = self.count + 1
        self.notifyStateChange('count', self.count)
        self.waitDelay('Ping', 1.2)

class Pinger2(SimEntityBase):

    def __init__(self, number=1):
        SimEntityBase.__init__(self, 'Pinger2')
        self.number = number

    def reset(self):
        pass

    def doRun(self):
        self.waitDelay('Init', 0.0, 0)

    def doInit(self, i):
        if i < self.number - 1:
            self.waitDelay('Init', 0.0, i + 1)

if __name__=='__main__':

    pinger = Pinger()
    dumper = SimpleStateChangeDumper()
    pinger.addStateChangeListener(dumper)

    pinger2 = Pinger2(4)

    EventList.verbose = True
    EventList.stopAtTime(5.0)

    EventList.reset()
    EventList.startSimulation()


