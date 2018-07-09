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

class BatchArrivalProcess(ArrivalProcess):

    def __init__(self, generator, batchGenerator):
        ArrivalProcess.__init__(self, generator)
        self.batchGenerator = batchGenerator
        self.totalIndividualArrivals = nan
        self.numberInBatch = nan

    def reset(self):
        ArrivalProcess.reset(self)
        self.totalIndividualArrivals = 0
        self.numberInBatch = nan

    def doArrival(self):
        ArrivalProcess.doArrival(self)

        self.numberInBatch = round(self.batchGenerator.generate())
        self.notifyStateChange('numberInBatch', self.numberInBatch)

        for i in range(self.numberInBatch):
            self.waitDelay('Arrival1', 0.0)
        self.totalIndividualArrivals += self.numberInBatch
        self.notifyStateChange('totalIndividualArrivals', self.totalIndividualArrivals)