from simkit.simkit import SimEntityBase
from simkit.simkit import Entity
from simkit.simkit import Priority
from math import nan
from heapq import heappush
from heapq import  heappop

class RenegingCustomer(Entity):

    def __init__(self, renegeTime):
        Entity.__init__(self, 'RenegingCustomer')
        self.renegeTime = renegeTime

    def __repr__(self):
        return Entity.__repr__(self) + ' (' + str(round(self.renegeTime,4)) + ')'

class CustomerCreator(SimEntityBase):

    def __init__(self, interarrivaltimeGenerator, renegeTimeGenerator):
        SimEntityBase.__init__(self)
        self.interarrivaltimeGenerator = interarrivaltimeGenerator
        self.renegeTimeGenerator = renegeTimeGenerator

    def run(self):
        self.schedule('create', self.interarrivaltimeGenerator.generate())

    def create(self):
        customer = RenegingCustomer(self.renegeTimeGenerator.generate())
        self.schedule('arrival', 0.0, customer)
        self.schedule('create', self.interarrivaltimeGenerator.generate())

    def __repr__(self):
        return SimEntityBase.__repr__(self) + ' (' + str(self.interarrivaltimeGenerator) +', ' + str(self.renegeTimeGenerator) + ')'

class ServerWithReneges(SimEntityBase):

    def __init__(self, totalNumberServers, serviceTimeGenerator):
        SimEntityBase.__init__(self)
        self.totalNumberServers = totalNumberServers
        self.serviceTimeGenerator = serviceTimeGenerator
        self.queue = []
        self.numberAvailableServers = nan
        self.numberReneges = nan
        self.numberServed = nan

    def reset(self):
        self.queue.clear()
        self.numberAvailableServers = self.totalNumberServers
        self.numberReneges = 0
        self.numberServed = 0

    def run(self):
        self.notifyStateChange('numberAvailableServers', self.numberAvailableServers)
        self.notifyStateChange('queue', self.queue)
        self.notifyStateChange('numberReneges', self.numberReneges)
        self.notifyStateChange('numberServed', self.numberServed)

    def arrival(self, customer):
        customer.stampTime()
        heappush(self.queue, customer)
        self.notifyStateChange('queue', self.queue)

        if self.numberAvailableServers > 0:
            self.schedule('startService', 0.0, priority=Priority.HIGH)

        self.schedule('renege', customer.renegeTime, customer)

    def startService(self):

        customer = heappop(self.queue)
        self.cancel('renege', customer)

        self.notifyStateChange('delayInQueue', customer.elapsedTime())
        self.notifyStateChange('queue', self.queue)

        self.numberAvailableServers -= 1
        self.notifyStateChange('numberAvailableServers', self.numberAvailableServers)

        self.schedule('endService', self.serviceTimeGenerator.generate(), customer)

    def renege(self, customer):
        self.numberReneges += 1;
        self.notifyStateChange('numberReneges', self.numberReneges)

        self.notifyStateChange('delayInQueueReneged', customer.elapsedTime())

        self.queue.remove(customer)
        self.notifyStateChange('queue', self.queue)

    def endService(self, customer):
        self.notifyStateChange('timeInSystem', customer.elapsedTime())

        self.numberAvailableServers += 1
        self.notifyStateChange('numberAvailableServers', self.numberAvailableServers)

        if self.queue.__len__() > 0:
            self.schedule('startService', 0.0, priority=Priority.HIGH)

    @property
    def totalNumberServers(self):
        return self.__totalNumberServers

    @totalNumberServers.setter
    def totalNumberServers(self, totalNumberServers):
        if totalNumberServers <= 0:
            raise ValueError('totalNumberServers must be > 0: ' + str(totalNumberServers))
        self.__totalNumberServers = totalNumberServers


