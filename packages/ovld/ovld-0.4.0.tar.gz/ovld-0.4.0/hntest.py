from timeit import timeit

from plum import dispatch

from ovld import ovld as dispatch


def f1(x):
    match x:
        case str():
            return "string"
        case int():
            return "integer"


# from functools import singledispatch as dispatch


@dispatch
def f2(x: str):
    return "string"


@dispatch
def f2(x: int):
    return "integer"


test = [
    1,
    7,
    "5",
    "bob",
    1564813548,
    "Four score and seven years ago",
    456,
    "879",
    "I can't understand why my fingers messed that up",
    852,
    1234567890,
    "More of the same",
    "Spam spam spam",
    1,
    1,
    2,
    3,
    5,
    8,
    13,
    21,
    33,
    54,
    87,
    "Fizz",
    "Buzz",
]


def run(f, test):
    for one in test:
        f(one)


print(timeit(lambda: run(f1, test), number=10000))
print(timeit(lambda: run(f2, test), number=10000))
