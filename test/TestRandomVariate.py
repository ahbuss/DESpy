from simkit.rand import RandomVariate

if __name__ == '__main__':
    rv = RandomVariate.getInstance('Exponential')

    rv.mean = 1
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

        rv2 = RandomVariate.getInstance('Exponential', 'rand', mean=1.0 + i / 10)
        rv2.mean = 1.0 + i / 10
    print(rv2)

    # for module in modules:
    #     print(module)
    rv3 = RandomVariate.getInstance('Constant', 'variates');
    rv3.value=4.5

    print(rv3)