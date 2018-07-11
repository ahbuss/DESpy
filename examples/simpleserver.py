from simkit.simkit import SimEntityBase
from simkit.simkit import Priority
from math import nan

class SimpleServer(SimEntityBase):

    def __init__(self, totalNumberServers, serviceTimeGenerator):
        SimEntityBase.__init__(self)
        self.totalNumberServers = totalNumberServers
        self.serviceTimeGenerator = serviceTimeGenerator
        self.numberInQueue = nan
        self.numberAvailableServers = nan
        self.numberServed = nan

    def reset(self):
        self.numberAvailableServers = self.totalNumberServers
        self.numberInQueue = 0
        self.numberServed = 0

    def run(self):
        self.notifyStateChange('numberAvailableServers', self.numberAvailableServers)
        self.notifyStateChange('numberInQueue', self.numberInQueue)
        self.notifyStateChange('numberServed', self.numberServed)

    def arrival(self):
        self.numberInQueue += 1
        self.notifyStateChange('numberInQueue', self.numberInQueue)

        if (self.numberAvailableServers > 0):
            self.schedule('startService', 0.0, priority=Priority.HIGH)

    def startService(self):
        self.numberInQueue -= 1
        self.notifyStateChange('numberInQueue', self.numberInQueue)

        self.numberAvailableServers -= 1
        self.notifyStateChange('numberAvailableServers', self.numberAvailableServers)

        self.schedule('endService', self.serviceTimeGenerator.generate())

    def endService(self):
        self.numberAvailableServers += 1
        self.notifyStateChange('numberAvailableServers', self.numberAvailableServers)

        self.numberServed += 1
        self.notifyStateChange('numberServed', self.numberServed)

        if self.numberInQueue > 0:
            self.schedule('startService', 0.0, priority=Priority.HIGH)


# if __name__=='__main__':
#     simpleServer = SimpleServer(None, None)
#     print(type(simpleServer).__name__)
