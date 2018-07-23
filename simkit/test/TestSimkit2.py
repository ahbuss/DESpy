from simkit.simkit import SimEntityBase
from simkit.simkit import EventList
from simkit.simkit import Priority
from simkit.simutil import SimpleStateChangeDumper

class Pinger(SimEntityBase):

    def __init__(self):
        SimEntityBase.__init__(self)
        self.count = 0;

    def reset(self):
        self.count = 0

    def run(self):
        self.notify_state_change("count", self.count)
        self.schedule('ping', 1.1)

    def ping(self):
        self.count = self.count + 1
        self.notify_state_change('count', self.count)
        self.schedule('ping', 1.2)

class Pinger2(SimEntityBase):

    def __init__(self, number=1):
        SimEntityBase.__init__(self)
        self.number = number
        self.name='Pinger2'

    def reset(self):
        pass

    def run(self):
        self.schedule('init', 0.0, 0)

    def init(self, i):
        if i < self.number - 1:
            self.schedule('init', 0.0,  i + 1)

if __name__=='__main__':

    pinger = Pinger()
    dumper = SimpleStateChangeDumper()
    pinger.add_state_change_listener(dumper)

    pinger2 = Pinger2(4)

    EventList.verbose = True
    EventList.stop_at_time(5.0)

    EventList.reset()
    EventList.start_simulation()


