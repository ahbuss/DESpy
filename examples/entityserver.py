from simkit.simkit import SimEntityBase
from simkit.simkit import Priority
from math import nan
from heapq import heappush
from heapq import heappop

class EntityServer(SimEntityBase):

    def __init__(self, numberServers, generator):
        SimEntityBase.__init__(self)
        self.numberServers = numberServers
        self.generator = generator
        self.numberAvailableServers = nan
        self.queue = []
        self.delayInQueue = nan
        self.timeInSystem = nan

    @property
    def numberServers(self):
        return self.__numberServers

    @numberServers.setter
    def numberServers(self, numberServers):
        if numberServers <= 0:
            raise ValueError('numberServers must be > 0: ' + str(numberServers))
        self.__numberServers = numberServers

    def reset(self):
        self.numberAvailableServers = self.numberServers
        self.queue.clear()
        self.delayInQueue = nan
        self.timeInSystem = nan

    def run(self):
        self.notifyStateChange('numberAvailableServers', self.numberAvailableServers)
        self.notifyStateChange('queue', self.queue)

    def arrival(self, entity):
        entity.stampTime()
        heappush(self.queue, entity)
        self.notifyStateChange('queue', self.queue)
        self.notifyStateChange('numberInQueue', self.queue.__len__())

        if (self.numberAvailableServers > 0):
            self.waitDelay('startService', 0.0, Priority.HIGH)

    def startService(self):
        entity = heappop(self.queue)
        self.notifyStateChange('queue', self.queue)
        self.notifyStateChange('numberInQueue', self.queue.__len__())

        self.delayInQueue = entity.elapsedTime()
        self.notifyStateChange('delayInQueue', self.delayInQueue)

        self.numberAvailableServers -= 1
        self.notifyStateChange('numberAvailableServers', self.numberAvailableServers)

        self.waitDelay('endService', self.generator.generate(), Priority.DEFAULT, entity)

    def endService(self, entity):
        self.numberAvailableServers += 1
        self.notifyStateChange('numberAvailableServers', self.numberAvailableServers)

        self.timeInSystem = entity.elapsedTime()
        self.notifyStateChange('timeInSystem', self.timeInSystem)

        if self.queue.__len__() > 0:
            self.waitDelay('startService', 0.0, Priority.HIGH)