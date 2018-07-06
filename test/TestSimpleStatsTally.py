from stats import SimpleStatsTally
from rand import Exponential

sst = SimpleStatsTally()
print(sst)
for i in range(1,10):
    sst.newObservation(i)

print(sst)

sst.reset()
print(sst)
rv = Exponential(3.7)
number = 100000
for x in range(number):
    sst.newObservation(rv.generate())

print('expected: ' + str(rv.mean))
print(sst)
print(sst.mean)
