from ovld.core import ovld

# @ovld(priority=1000)
# def f(x: object):
#     return "A"


# @ovld
# def f(x: Number):
#     return "B"


# @ovld
# def f(x: Dependent[int, lambda x: x < 0]):
#     return "C"


# @ovld
# def f(x: int):
#     return "D"


# @ovld
# def f(x: str):
#     return "E"


# @ovld(priority=-1)
# def f(x: object):
#     return "F"


# f.display_resolution(123)
# print("=" * 50)
# f.display_resolution("hello")


@ovld
def add(x: list, y: list):
    return [add(a, b) for a, b in zip(x, y)]


@ovld
def add(x: tuple, y: tuple):
    return tuple(add(a, b) for a, b in zip(x, y))


@ovld
def add(x: dict, y: dict):
    return {k: add(v, y[k]) for k, v in x.items()}


@ovld
def add(x: object, y: object):
    return x + y


add([[[1]]], [[[[2]]]])
