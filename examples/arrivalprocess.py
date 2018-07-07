from simkit.simkit import SimEntityBase
from simkit.simkit import Entity
from simkit.simkit import Priority
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

class EntityCreator(ArrivalProcess):

    def __int__(self, generator):
        ArrivalProcess.__init__(self, generator)

    def doArrival(self):
        ArrivalProcess.doArrival(self)
        self.waitDelay('EntityArrival', 0.0, Priority.DEFAULT, Entity())