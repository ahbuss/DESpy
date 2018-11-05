from simkit.base import SimEntityBase     # (1)
from simkit.base import Entity
from math import nan

class ArrivalProcess(SimEntityBase):        # (2)

    def __init__(self, interarrival_time_generator):          # (3)
        SimEntityBase.__init__(self)
        self.interarrival_time_generator=interarrival_time_generator
        self.number_arrivals = nan

    def reset(self):                        # (4)
        SimEntityBase.reset(self)
        self.number_arrivals = 0

    def run(self):                          # (5)
        self.notify_state_change("number_arrivals", self.number_arrivals)

        self.schedule('arrival', self.interarrival_time_generator.generate())

    def arrival(self):                      # (6)
        self.number_arrivals += 1
        self.notify_state_change("number_arrivals", self.number_arrivals)

        self.schedule('arrival', self.interarrival_time_generator.generate())

class EntityCreator(ArrivalProcess):

    def __int__(self, generator):
        ArrivalProcess.__init__(self, generator)

    def arrival(self):
        ArrivalProcess.arrival(self)
        self.schedule('entity_arrival', 0.0, Entity())

class BatchArrivalProcess(ArrivalProcess):

    def __init__(self, interarrival_time_generator, batchGenerator):
        ArrivalProcess.__init__(self, interarrival_time_generator)
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
        self.notify_state_change('number_in_batch', self.numberInBatch)

        for i in range(self.numberInBatch):
            self.schedule('arrival1', 0.0)
        self.totalIndividualArrivals += self.numberInBatch
        self.notify_state_change('total_individual_arrivals', self.totalIndividualArrivals)

class StoppedArrivalProcess(ArrivalProcess):

    def __init__(self, interarrival_time_generator, stop_time):
        ArrivalProcess.__init__(self, interarrival_time_generator)
        self.stop_time = stop_time

    def run(self):
        ArrivalProcess.run(self)
        self.schedule('stop_arrivals', self.stop_time)

    def stop_arrivals(self):
        self.cancel('arrival')