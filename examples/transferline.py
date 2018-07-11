from simkit.simkit import SimEntityBase
from simkit.simkit import Priority
from simkit.simkit import Entity
from examples.arrivalprocess import ArrivalProcess
from math import nan
from heapq import heappush
from heapq import heappop

class Job(Entity):

    def __init__(self):
        Entity.__init__(self, 'Job')
        self.totalDelayInQueue = 0.0
        self.timeInSystem = 0.0

    def updateDelayInQueue(self):
        self.totalDelayInQueue += self.elapsedTime()

class JobCreator(ArrivalProcess):
    def __init__(self, interarrivalTimeGenerator):
        ArrivalProcess.__init__(self, interarrivalTimeGenerator)

    def arrival(self):
        ArrivalProcess.arrival(self)
        self.waitDelay('jobArrival', 0.0, Priority.DEFAULT, Job(), 0)

class TransferLine(SimEntityBase):
    def __init__(self, numberOfStations, numberMachines ,serviceTimes):
        SimEntityBase.__init__(self)
        self.numberStations = numberOfStations
        self.serviceTimes = serviceTimes
        self.numberMachines = numberMachines
        self.queue = []
        self.numberAvailableMachines = []
        self.validate()

    def validate(self):
        serviceTimesOK = len(self.serviceTimes) == self.numberStations
        numberMachinesOK = len(self.numberMachines) == self.numberStations
        if not serviceTimesOK or not numberMachinesOK:
            raise ValueError('{ns:d} stations specified but {st:d} service times and {nm:d} machines'.\
                             format(ns=self.numberStations, st=len(self.serviceTimes), nm=len(self.numberMachines)))

    def reset(self):
        self.queue.clear()
        self.numberAvailableMachines.clear()

    def run(self):
        if self.numberStations > 0:
            self.waitDelay('init', 0.0, Priority.DEFAULT, 0)

    def init(self, station):
        self.queue.append([])
        self.notifyIndexedStateChange(station, 'queue', self.queue[station])

        self.numberAvailableMachines.append(self.numberMachines[station])
        self.notifyIndexedStateChange(station, 'numberAvailableMachines', self.numberAvailableMachines[station])

        if station < self.numberStations - 1:
            self.waitDelay('init', 0.0, Priority.DEFAULT, station + 1)

    def arrival(self, job, station):
        job.stampTime()
        heappush(self.queue[station], job)
        self.notifyIndexedStateChange(station, 'queue', self.queue[station])

        if self.numberAvailableMachines[station] > 0:
            self.waitDelay('startProcessing', 0.0, Priority.HIGH, station)

    def startProcessing(self, station):
        job = heappop(self.queue[station])
        self.notifyIndexedStateChange(station, 'delayInQueue', job.elapsedTime())
        job.updateDelayInQueue()

        self.numberAvailableMachines[station] -= 1
        self.notifyIndexedStateChange(station, 'numberAvailableMachines', self.numberAvailableMachines[station])

        self.waitDelay('endProcessing', self.serviceTimes[station].generate(), Priority.DEFAULT, job, station)

    def endProcessing(self, job, station):
        self.numberAvailableMachines[station] += 1
        self.notifyIndexedStateChange(station, 'numberAvailableMachines', self.numberAvailableMachines[station])

        if len(self.queue[station]) > 0:
            self.waitDelay('startProcessing', 0.0, Priority.HIGH, station)

        if station < self.numberStations - 1:
            self.waitDelay('arrival', 0.0, Priority.HIGH, job, station + 1)

        if (station == self.numberStations - 1):
            self.waitDelay('jobComplete', 0.0, Priority.DEFAULT, job)

    def jobComplete(self, job):
        self.notifyStateChange('totalDelayInQueue', job.totalDelayInQueue)
        self.notifyStateChange('timeInSystem', job.age())