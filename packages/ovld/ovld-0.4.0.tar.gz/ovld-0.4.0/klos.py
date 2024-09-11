from timeit import timeit


def g1(x):
    return x * 7


def f1(xs):
    return [g1(x) for x in xs]


def mkf():
    def g2(x):
        return x * 7

    def f2(xs):
        return [g2(x) for x in xs]

    return f2


f2 = mkf()
print(timeit(lambda: f2(list(range(100))), number=100000))
print(timeit(lambda: f1(list(range(100))), number=100000))
