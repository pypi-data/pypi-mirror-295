from ovld import ovld

# @ovld
# def fact(n: Literal[0]):
#     return 1
# @ovld
# def fact(n: Dependent[int, lambda n: n > 0]):
#     return n * recurse(n - 1)
# print(fact(5))
# fact(-1)   # Error!
# @ovld
# def add(x: list, y: list):
#     return [recurse(a, b) for a, b in zip(x, y)]
# @ovld
# def add(x: tuple, y: tuple):
#     return tuple(recurse(a, b) for a, b in zip(x, y))
# @ovld
# def add(x: dict, y: dict):
#     return {k: recurse(v, y[k]) for k, v in x.items()}
# @ovld
# def add(x: object, y: object):
#     return x + y
# @add.variant
# def bad(self, x: object, y: object):
#     raise Exception("Bad.")
# add([[[1]]], [[[[2]]]])
# @ovld
# def f(cls: type[list[object]], xs: list):
#     return [recurse(cls.__args__[0], x) for x in xs]
# @ovld
# def f(cls: type[int], x: int):
#     return x * 2
# assert f(list[int], [1, 2, 3]) == [2, 4, 6]
# f(list[int], [1, "X", 3])  # type error
from ovld.types import Exactly, StrictSubclass


@ovld
def f(x: Exactly[BaseException]):
    return "=BaseException"


@ovld
def f(x: StrictSubclass[Exception]):
    return ">Exception"


assert f(TypeError()) == ">Exception"
assert f(BaseException()) == "=BaseException"

f(Exception())  # ERROR!
