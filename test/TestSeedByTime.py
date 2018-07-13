from simkit.rand import Exponential
from datetime import datetime

rv = Exponential(mean=1.5)
print(rv)

number = 5

print('original:')
for i in range(number):
    print(rv.generate())

print('after resetState (should be identical:')
rv.reset()
for i in range(number):
    print(rv.generate())

print('after seed by clock (should be different each time:')
time = datetime.now().time()
print(time)
rv.seed(time)
for i in range(number):
    print(rv.generate())