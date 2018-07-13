from examples.arrivalprocess import ArrivalProcess
from simkit.rand import RandomVariate
from simkit.simkit import EventList
from simkit.simkit import SimEntityBase
from simkit.simkit import Priority

class Test(SimEntityBase):

    def run(self):
        self.schedule('init', 0.0, 0)

    def init(self, i):
        self.schedule('init', 0.0, i + 1)

if __name__=='__main__':

    # interarrivalTimeGenerator = RandomVariate.getInstance('Exponential', mean=3.0)
    # arrivalProcess = ArrivalProcess(interarrivalTimeGenerator)
    # print(arrivalProcess.describe())

    test = Test()

    EventList.stop_on_event(10, 'init')

    EventList.verbose = True
    EventList.reset()
    EventList.startSimulation()