from simkit.simkit import SimEntityBase
from simkit.simkit import EventList
from simkit.simkit import Priority

class TestCancelled(SimEntityBase):

    def run(self):
        self.waitDelay('q', 1.0, Priority.DEFAULT)
        self.waitDelay('b', 0.5, Priority.DEFAULT)
        self.waitDelay('c', 2.0, Priority.DEFAULT, 3)
        self.waitDelay('c', 1.5, Priority.DEFAULT, 2)
        self.waitDelay('d', 3.4, Priority.DEFAULT, 1, 2, 3)
        self.waitDelay('d', 3.4, Priority.HIGH, 1, 2, 4)

    def b(self):
        print('In b()!')
        self.interrupt('a')
        self.interrupt('c', 3)

    def a(self):
        print('In a()!')

    def c(self, i):
        print('In c(): i = ' + str(i))
        self.interrupt('d', 1, 2, 3)

    def d(self, x, y, z):
        print('In D: args = (' + str(x) + ',' + str(y) + ',' + str(z) + ')')

if __name__=='__main__':
    test = TestCancelled()

    EventList.verbose = True

    EventList.reset()
    EventList.startSimulation()

