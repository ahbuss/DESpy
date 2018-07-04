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
        self.waitDelay('Ping', 1.1, [])

    def doPing(self):
        self.count = self.count + 1
        self.notifyStateChange('count', self.count)
        self.waitDelay('Ping', 1.2, [])

if __name__=='__main__':

    pinger = Pinger()
    dumper = SimpleStateChangeDumper()
    pinger.addStateChangeListener(dumper)

    EventList.verbose = True
    EventList.stopAtTime(5.0)

    EventList.reset()
    EventList.startSimulation()


