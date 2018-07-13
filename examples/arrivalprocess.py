from simkit.simkit import SimEntityBase
from simkit.simkit import Entity
from simkit.simkit import Priority
from math import nan

class ArrivalProcess(SimEntityBase):

    def __init__(self, generator):
        SimEntityBase.__init__(self)
        self.generator=generator
        self.number_arrivals = nan

    def reset(self):
        self.number_arrivals = 0

    def run(self):
        self.notifyStateChange("numberArrivals", self.number_arrivals)

        self.schedule('arrival', self.generator.generate())

    def arrival(self):
        self.number_arrivals += 1
        self.notifyStateChange("numberArrivals", self.number_arrivals)

        self.schedule('arrival', self.generator.generate())

class EntityCreator(ArrivalProcess):

    def __int__(self, generator):
        ArrivalProcess.__init__(self, generator)

    def arrival(self):
        ArrivalProcess.arrival(self)
        self.schedule('entityArrival', 0.0, Entity())

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

    def arrival(self):
        ArrivalProcess.arrival(self)

        self.numberInBatch = round(self.batchGenerator.generate())
        self.notifyStateChange('numberInBatch', self.numberInBatch)

        for i in range(self.numberInBatch):
            self.schedule('arrival1', 0.0)
        self.totalIndividualArrivals += self.numberInBatch
        self.notifyStateChange('totalIndividualArrivals', self.totalIndividualArrivals)