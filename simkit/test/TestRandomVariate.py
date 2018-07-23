from simkit.rand import RandomVariate
from simkit.stats import SimpleStatsTally

if __name__ == '__main__':
    rv = RandomVariate.instance('Exponential', mean=1)
    print(rv)

    sum = 0.0
    n = 1000000
    for i in range(n):
        sum += rv.generate()
    # print(rv.generate())
    print(sum / n)

    print()
    rv.seed(2468)
    for i in range(1, 5):
        print(rv.generate())

        rv2 = RandomVariate.instance('Exponential', 'simkit.rand', mean=1.0 + i / 10)
        rv2.mean = 1.0 + i / 10
        print(rv2)

    # for module in modules:
    #     print(module)
    rv3 = RandomVariate.instance('Constant', 'simkit.rand', value=5.4);
    print(rv3)
    for i in range(4):
        print(rv3.generate())

    rv4 = RandomVariate.instance('Beta', alpha=2, beta=3)
    print(rv4)

    rv4 = RandomVariate.instance('Beta', alpha=3, beta=4, scale=5)
    print(rv4)

    rv4 = RandomVariate.instance('Beta', alpha=3, beta=4, scale=5, shift=-3)
    print(rv4)

    rv4 = RandomVariate.instance('Beta', params={'alpha':1.2, 'beta':3.44})
    print(rv4)

    rv5 = RandomVariate.instance('Discrete', values=[1, 2, 3, 4], frequencies=[10, 20, 30, 40])
    print(rv5)

    rv5 = RandomVariate.instance('Discrete', values=[4.0, 3.0, 2.0, 1.0], frequencies=[100, 200, 300, 400])
    print(rv5)

    rv6 = RandomVariate.instance('Poisson', mean=2.3)
    print(rv6)
    number = 1000000
    sst = SimpleStatsTally(str(rv6))
    for i in range(number):
        sst.new_observation(rv6.generate())
    print(sst)

    rv7 = RandomVariate.instance('Binomial', n=20, p=0.3)
    sst = SimpleStatsTally(str(rv7))
    for i in range(number):
        sst.new_observation(rv7.generate())
    print(sst)

    rv8 = RandomVariate.instance('Uniform', min=0.9, max=2.2)
    sst=SimpleStatsTally(str(rv8))
    for i in range(number):
        sst.new_observation(rv8.generate())
    print(sst)

    rv4.reset()
    first = []
    for i in range(10):
        first.append(rv4.generate())

    second=[]
    rv4.reset()
    for i in range(10):
        second.append(rv4.generate())

    print(first == second)

    rv9 = RandomVariate.instance('Normal', mean=-2, stdev=4.5)
    print(rv9)

    for i in range(10):
        print(rv9.generate())