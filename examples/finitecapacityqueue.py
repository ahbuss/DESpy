from simkit.simkit import SimEntityBase
from simkit.simkit import Priority
from math import nan

class FiniteCapacityQueue(SimEntityBase):

    def __init__(self, totalNumberServers, serviceTimeGenerator, queueCapacity):
        SimEntityBase.__init__(self)
        self.totalNumberServers = totalNumberServers
        self.serviceTimeGenerator = serviceTimeGenerator
        self.queueCapacity = queueCapacity
        self.numberInQueue = nan
        self.numberAvailableServers = nan
        self.numberBalks = nan
        self.numberPotentialCustomers = nan

        if (self.queueCapacity < 0):
            raise ValueError('queueCapacity must be \u2265 0: {cap:%d}'.format(cap=self.queueCapacity))

    def reset(self):
        SimEntityBase.reset(self)
        self.numberInQueue = 0
        self.numberAvailableServers = self.totalNumberServers
        self.numberBalks = 0
        self.numberPotentialCustomers = 0

    def run(self):
        self.notifyStateChange('numberInQueue', self.numberInQueue)
        self.notifyStateChange('numberAvailableServers', self.numberAvailableServers)
        self.notifyStateChange('numberBalks', self.numberBalks)
        self.notifyStateChange('numberPotentialCustomers', self.numberPotentialCustomers)

    def arrival(self):
        self.numberPotentialCustomers += 1
        self.notifyStateChange('numberPotentialCustomers', self.numberPotentialCustomers)

        if self.numberInQueue < self.queueCapacity or self.numberAvailableServers > 0:
            self.waitDelay('joinQueue', 0.0)

        if self.numberInQueue == self.queueCapacity and self.numberAvailableServers == 0:
            self.waitDelay('balk', 0.0)

    def balk(self):
        self.numberBalks += 1
        self.notifyStateChange('numberBalks', self.numberBalks)

    def joinQueue(self):
        self.numberInQueue += 1

        if self.numberAvailableServers > 0:
            self.waitDelay('startService', 0.0, Priority.HIGH)

    def startService(self):
        self.numberInQueue -= 1
        self.notifyStateChange('numberInQueue', self.numberInQueue)

        self.numberAvailableServers -= 1
        self.notifyStateChange('numberAvailableServers', self.numberAvailableServers)

        self.waitDelay('endService', self.serviceTimeGenerator.generate())

    def endService(self):
        self.numberAvailableServers += 1
        self.notifyStateChange('numberAvailableServers', self.numberAvailableServers)

        if self.numberInQueue > 0:
            self.waitDelay('startService', 0.0, Priority.HIGH)
