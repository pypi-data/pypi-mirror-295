from ovld import ovld, recurse
from ovld.core import OvldMC, extend_super


@ovld
def iterate_over_lists(xs: list):
    return [recurse(x) for x in xs]


@ovld
def iterate_over_dicts(xs: dict):
    return {k: recurse(v) for k, v in xs.items()}


@ovld(mixins=[iterate_over_lists, iterate_over_dicts])
def double(x):
    return x * 2


print(double([1, 2, 3]) == [2, 4, 6])
print(double({"x": 10, "y": 20}) == {"x": 20, "y": 40})


class IOL(metaclass=OvldMC):
    @ovld
    def __call__(self, xs: list):
        return [recurse(x) for x in xs]


class IOD(metaclass=OvldMC):
    @ovld
    def __call__(self, xs: dict):
        return {k: recurse(v) for k, v in xs.items()}


class Mul(IOL, IOD):
    def __init__(self, n):
        self.n = n

    @extend_super
    def __call__(self, x):
        return x * self.n


print(Mul(3)([1, 2, 3]))
print(Mul(3)({"x": 10, "y": 20}))
