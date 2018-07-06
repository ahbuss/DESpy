from simkit import SimEntityBase
from simkit import Entity
from simkit import Priority
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

    def doRun(self):
        self.notifyStateChange('numberAvailableServers', self.numberAvailableServers)
        self.notifyStateChange('queue', self.queue)

    def doArrival(self, entity):
        entity.stampTime()
        heappush(self.queue, entity)
        self.notifyStateChange('queue', self.queue)
        self.notifyStateChange('numberInQueue', self.queue.__len__())

        if (self.numberAvailableServers > 0):
            self.waitDelay('StartService', 0.0, None, Priority.HIGH)

    def doStartService(self):
        entity = heappop(self.queue)
        self.notifyStateChange('queue', self.queue)
        self.notifyStateChange('numberInQueue', self.queue.__len__())

        self.notifyStateChange('delayInQueue', entity.elapsedTime())

        self.numberAvailableServers -= 1
        self.notifyStateChange('numberAvailableServers', self.numberAvailableServers)

        self.waitDelay('EndService', self.generator.generate(), entity)

    def doEndService(self, entity):
        self.numberAvailableServers += 1
        self.notifyStateChange('numberAvailableServers', self.numberAvailableServers)

        self.notifyStateChange('timeInSystem', entity.elapsedTime())

        if self.queue.__len__() > 0:
            self.waitDelay('StartService', 0.0, None, Priority.HIGH)