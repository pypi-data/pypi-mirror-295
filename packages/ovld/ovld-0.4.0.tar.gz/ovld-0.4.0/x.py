from ovld import ovld, recurse
from ovld.dependent import Dependent, Equals, StartsWith

recurse.next()


@ovld
def test(x: Dependent[int, Equals(0)]):
    return "zero"


@ovld
def test(x: Dependent[int, Equals(1)]):
    return "one"


@ovld
def test(x: Dependent[str, StartsWith("hell")]):
    return "H"


@ovld
def test(x: Dependent[str, StartsWith("hello")]):
    return "H"


@ovld
def test(x: int):
    return "yes"


@ovld
def test(x: str):
    return "yes"


@ovld
def test(x: object):
    return "done"


@ovld(priority=10)
def test(x: object):
    return "start"


test.display_resolution(13)
test.display_resolution(0)
test.display_resolution(1)
test.display_resolution("hello")
test.map.display_methods()
