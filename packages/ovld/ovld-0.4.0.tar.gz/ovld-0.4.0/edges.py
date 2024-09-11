from dataclasses import dataclass
from typing import Protocol, runtime_checkable

from ovld import Dataclass, ovld


@runtime_checkable
class SupportsRead(Protocol):
    def read(self, amount: int) -> bytes: ...


@runtime_checkable
class SupportsWrite(Protocol):
    def write(self, amount: int) -> bytes: ...


@dataclass
class Reader:
    def read(self):
        return 1

    def write(self):
        return 1


@dataclass
class Writer:
    def write(self):
        return 1


@ovld
def f(x: SupportsRead):
    return "yes"


@ovld
def f(x: SupportsWrite):
    return "yes"


# @ovld
# def f(x: Reader):
#     return "R" + f.next(x)


@ovld  # (priority=-1)
def f(x: Dataclass):
    return "DC"


@ovld
def f(x: int):
    return "w/e"


@ovld
def f(x):
    return "no"


# print(f(1))
print(f(Reader()))
# print(f(Writer()))
