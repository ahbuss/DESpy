from simkit.rand import RandomVariate
from simkit.stats import SimpleStatsTally

if __name__ == '__main__':
    rv = RandomVariate.getInstance('Exponential', mean=1)
    print(rv)

    sum = 0.0
    n = 1000000
    for i in range(n):
        sum += rv.generate()
    # print(rv.generate())
    print(sum / n)

    print()
    rv.setSeed(2468)
    for i in range(1, 5):
        print(rv.generate())

        rv2 = RandomVariate.getInstance('Exponential', 'simkit.rand', mean=1.0 + i / 10)
        rv2.mean = 1.0 + i / 10
        print(rv2)

    # for module in modules:
    #     print(module)
    rv3 = RandomVariate.getInstance('Constant', 'simkit.rand', value=5.4);
    print(rv3)
    for i in range(4):
        print(rv3.generate())

    rv4 = RandomVariate.getInstance('Beta', alpha=2, beta=3)
    print(rv4)

    rv5 = RandomVariate.getInstance('Discrete', values=[1,2,3,4], frequencies=[10, 20, 30, 40])
    print(rv5)

    rv5 = RandomVariate.getInstance('Discrete', values=[4.0, 3.0, 2.0, 1.0], frequencies=[100, 200, 300, 400])
    print(rv5)

    rv6 = RandomVariate.getInstance('Poisson', mean=2.3)
    print(rv6)
    number = 1000000
    sst = SimpleStatsTally(str(rv6))
    for i in range(number):
        sst.newObservation(rv6.generate())
    print(sst)

    rv7 = RandomVariate.getInstance('Binomial', n=20, p=0.3)
    sst = SimpleStatsTally(str(rv7))
    for i in range(number):
        sst.newObservation(rv7.generate())
    print(sst)

    rv8 = RandomVariate.getInstance('Uniform',min=0.9, max=2.2)
    sst=SimpleStatsTally(str(rv8))
    for i in range(number):
        sst.newObservation(rv8.generate())
    print(sst)

    rv4.resetState()
    first = []
    for i in range(10):
        first.append(rv4.generate())

    second=[]
    rv4.resetState()
    for i in range(10):
        second.append(rv4.generate())

    print(first == second)