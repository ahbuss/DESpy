from simkit.rand import RandomVariate
from simkit.rand import Discrete

rv = RandomVariate.getInstance('Discrete', values=[1,2,3,4,5], frequencies=[20, 30, 40, 50, 60])

print(rv)

counts={}

number = 1000000
for i in range(number):
    x = rv.generate()
    if counts.keys().__contains__(x):
        counts[x] = counts[x] + 1
    else:
        counts[x] = 1

print(counts)

for x in sorted(counts.keys()):
    counts[x] = counts[x] / number
    print('{x:d} = {p:.4f}'.format(x=x, p=counts[x]))

counts.clear()
rv = RandomVariate.getInstance('Discrete', values=['one', 'two', 'three', 'four', 'fiver'], frequencies=[20, 30, 40, 50, 60])
for i in range(number):
    x = rv.generate()
    if counts.keys().__contains__(x):
        counts[x] = counts[x] + 1
    else:
        counts[x] = 1

print(counts)

for x in sorted(counts.keys()):
    counts[x] = counts[x] / number
    print('{x:s} = {p:.4f}'.format(x=x, p=counts[x]))

counts.clear()
rv = RandomVariate.getInstance('DiscreteUniform', min=-3, max=5)
print(rv)
for i in range(number):
    x = rv.generate()
    if counts.keys().__contains__(x):
        counts[x] = counts[x] + 1
    else:
        counts[x] = 1

print(counts)

for x in sorted(counts.keys()):
    counts[x] = counts[x] / number
    print('{x:d} = {p:.4f}'.format(x=x, p=counts[x]))
