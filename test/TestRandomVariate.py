from rand import ExponentialVariate
from rand import RandomVariate

rv = ExponentialVariate(2.5)
print(rv)

sum = 0.0
n = 1000000
for i in range(n):
    sum += rv.generate()
    # print(rv.generate())
print(sum / n)

print('\n')

rv.setSeed(2468)
for i in range(5):
    print(rv.generate())

    rv2 = RandomVariate.getInstance('Exponential', 1.8)
    print(rv2)
