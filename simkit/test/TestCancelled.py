from simkit.simkit import SimEntityBase
from simkit.simkit import EventList
from simkit.simkit import Priority

class TestCancelled(SimEntityBase):

    def run(self):
        self.schedule('q', 1.0)
        self.schedule('b', 0.5)
        self.schedule('c', 2.0, 3)
        self.schedule('c', 1.5, 2)
        self.schedule('d', 3.4, 1, 2, 3)
        self.schedule('d', 3.4, 1, 2, 4)

    def b(self):
        print('In b()!')
        self.cancel('a')
        self.cancel('c', 3)

    def a(self):
        print('In a()!')

    def c(self, i):
        print('In c(): i = ' + str(i))
        self.cancel('d', 1, 2, 3)

    def d(self, x, y, z):
        print('In D: args = (' + str(x) + ',' + str(y) + ',' + str(z) + ')')

if __name__=='__main__':
    test = TestCancelled()

    EventList.verbose = True

    EventList.reset()
    EventList.start_simulation()

