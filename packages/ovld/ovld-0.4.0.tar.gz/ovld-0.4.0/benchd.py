import timeit
from collections import defaultdict


class Foo(dict):
    pass


d1 = {"a": 1}
d2 = Foo({"a": 1})
d3 = defaultdict(lambda: 3)
d3["a"] = 1


def f1():
    for i in range(100):
        d1["a"]


def f2():
    for i in range(100):
        d2["a"]


def f3():
    for i in range(100):
        d3["a"]


def f4():
    for i in range(100):
        try:
            d1["a"]
        except KeyError:
            pass


print(timeit.timeit(f1, number=1000))
print(timeit.timeit(f2, number=1000))
print(timeit.timeit(f3, number=1000))
print(timeit.timeit(f4, number=1000))
