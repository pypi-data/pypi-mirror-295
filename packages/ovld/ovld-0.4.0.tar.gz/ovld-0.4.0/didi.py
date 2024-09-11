from multimethod import multimethod as dispatch
from plum import dispatch
from runtype import multidispatch as dispatch

from ovld import ovld as dispatch


@dispatch
def f(x: type[int]):
    return "ah"


@dispatch
def f(x: type[object]):
    return "something else"


@dispatch
def f(x: type[dict[str, object]]):
    return ("didi", x)


print(f(int))
print(f(str))
print(f(dict[str, int]))
print(f(dict[int, int]))
