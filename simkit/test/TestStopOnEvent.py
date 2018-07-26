from simkit.simkit import EventList
from simkit.simkit import SimEntityBase


class Test(SimEntityBase):

    def run(self):
        self.schedule('init', 0.0, 0)

    def init(self, i):
        self.schedule('init', 0.0, i + 1)

if __name__=='__main__':

    # interarrival_time_generator = RandomVariate.getInstance('Exponential', mean=3.0)
    # arrival_process = ArrivalProcess(interarrival_time_generator)
    # print(arrival_process.describe())

    test = Test()

    EventList.stop_on_event(10, 'init')

    EventList.verbose = True
    EventList.reset()
    EventList.start_simulation()