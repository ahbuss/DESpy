from simkit import SimEntityBase
from simkit import EventList
from simkit import Priority

class TestCancelled(SimEntityBase):

    def doRun(self):
        self.waitDelay('A', 1.0, Priority.DEFAULT)
        self.waitDelay('B', 0.5, Priority.DEFAULT)
        self.waitDelay('C', 2.0, Priority.DEFAULT, 3)
        self.waitDelay('C', 1.5, Priority.DEFAULT, 2)
        self.waitDelay('D', 3.4, Priority.DEFAULT, 1, 2, 3)
        self.waitDelay('D', 3.4, Priority.HIGH, 1, 2, 4)

    def doB(self):
        print('In B!')
        self.interrupt('A')
        self.interrupt('C', 3)

    def doA(self):
        print('In A!')

    def doC(self, i):
        print('In C: i = ' + str(i))
        self.interrupt('D', 1, 2, 3)

    def doD(self, x, y, z):
        print('In D: args = (' + str(x) + ',' + str(y) + ',' + str(z) + ')')

if __name__=='__main__':
    test = TestCancelled()

    EventList.verbose = True

    EventList.reset()
    EventList.startSimulation()

