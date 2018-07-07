from simkit.simkit import SimEntityBase
from math import nan

class ArrivalProcess(SimEntityBase):

    def __init__(self, generator):
        SimEntityBase.__init__(self)
        self.generator=generator
        self.numberArrivals = nan

    def reset(self):
        self.numberArrivals = 0

    def doRun(self):
        self.notifyStateChange("numberArrivals",self.numberArrivals)

        self.waitDelay('Arrival', self.generator.generate())

    def doArrival(self):
        self.numberArrivals += 1
        self.notifyStateChange("numberArrivals",self.numberArrivals)

        self.waitDelay('Arrival', self.generator.generate())

    # def __repr__(self):
    #     return 'ArrivalProcess: ' + str(self.generator);