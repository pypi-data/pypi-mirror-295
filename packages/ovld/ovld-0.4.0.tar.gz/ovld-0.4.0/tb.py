from typing import Literal

from ovld.core import ovld


@ovld
def f(x: Literal["hello"]):
    return f(10)


@ovld
def f(x: int):
    breakpoint()
    return 2 * x


f("hello")
