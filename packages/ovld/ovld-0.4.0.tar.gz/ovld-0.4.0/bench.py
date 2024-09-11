import timeit

from multimethod import multimethod
from multipledispatch import dispatch
from plum import dispatch as plum

from ovld import ovld, recurse

# OVLD


@ovld
def smap(x: list, y: list):
    """One."""
    return [smap(a, b) for a, b in zip(x, y)]


@ovld
def smap(x: tuple, y: tuple):
    return tuple(smap(a, b) for a, b in zip(x, y))


@ovld
def smap(x: dict, y: dict):
    return {k: smap(v, y[k]) for k, v in x.items()}


@ovld
def smap(x: object, z: object):
    return x + z


# OVLD C


@ovld
def smap_c(x: list, y: list):
    """Two."""
    return [recurse(a, b) for a, b in zip(x, y)]


@ovld
def smap_c(x: tuple, y: tuple):
    return tuple(recurse(a, b) for a, b in zip(x, y))


@ovld
def smap_c(x: dict, y: dict):
    return {k: recurse(v, y[k]) for k, v in x.items()}


@ovld
def smap_c(x: object, y: object):
    return x + y


# multimethods


@multimethod
def smap_mm(x: list, y: list):
    """Three."""
    return [smap_mm(a, b) for a, b in zip(x, y)]


@multimethod
def smap_mm(x: tuple, y: tuple):
    return tuple(smap_mm(a, b) for a, b in zip(x, y))


@multimethod
def smap_mm(x: dict, y: dict):
    return {k: smap_mm(v, y[k]) for k, v in x.items()}


@multimethod
def smap_mm(x: object, y: object):
    return x + y


# multipledispatch


@dispatch(list, list)
def smap_md(x, y):
    """Four."""
    return [smap_md(a, b) for a, b in zip(x, y)]


@dispatch(tuple, tuple)
def smap_md(x, y):
    return tuple(smap_md(a, b) for a, b in zip(x, y))


@dispatch(dict, dict)
def smap_md(x, y):
    return {k: smap_md(v, y[k]) for k, v in x.items()}


@dispatch(object, object)
def smap_md(x, y):
    return x + y


# isinstance


def smap_ii(x, y):
    """Five."""
    if isinstance(x, dict) and isinstance(y, dict):
        return {k: smap_ii(v, y[k]) for k, v in x.items()}
    elif isinstance(x, tuple) and isinstance(y, tuple):
        return tuple(smap_ii(a, b) for a, b in zip(x, y))
    elif isinstance(x, list) and isinstance(y, list):
        return [smap_ii(a, b) for a, b in zip(x, y)]
    else:
        return x + y


# match statement


def smap_mh(x, y):
    """Six."""
    match (x, y):
        case ({}, {}):
            return {k: smap_mh(v, y[k]) for k, v in x.items()}
        case (tuple(), tuple()):
            return tuple(smap_mh(a, b) for a, b in zip(x, y))
        case ([*x], [*y]):
            return [smap_mh(a, b) for a, b in zip(x, y)]
        case _:
            return x + y


# plum


@plum
def smap_pl(x: list, y: list):
    """Three."""
    return [smap_pl(a, b) for a, b in zip(x, y)]


@plum
def smap_pl(x: tuple, y: tuple):
    return tuple(smap_pl(a, b) for a, b in zip(x, y))


@plum
def smap_pl(x: dict, y: dict):
    return {k: smap_pl(v, y[k]) for k, v in x.items()}


@plum
def smap_pl(x: object, y: object):
    return x + y


###


A = {"xs": list(range(50)), "ys": ("o", (6, 7))}
B = {"xs": list(range(10, 60)), "ys": ("x", (7, 6))}

results = {
    "smap": smap(A, B),
    "smap_mm": smap_mm(A, B),
    "smap_md": smap_md(A, B),
    "smap_pl": smap_pl(A, B),
    "smap_ii": smap_ii(A, B),
    "smap_mh": smap_mh(A, B),
    "smap_c": smap_c(A, B),
}

expected = results["smap"]

for k, v in results.items():
    assert v == expected, f"{k} failed"


# breakpoint()

print("smap_mm\t", 10 * timeit.timeit(lambda: smap_mm(A, B), number=10000))
print("smap_md\t", 10 * timeit.timeit(lambda: smap_md(A, B), number=10000))
print("smap_pl\t", 10 * timeit.timeit(lambda: smap_pl(A, B), number=10000))
print("smap_ov\t", 10 * timeit.timeit(lambda: smap(A, B), number=10000))
print("smap_c\t", 10 * timeit.timeit(lambda: smap_c(A, B), number=10000))
print("smap_ii\t", 10 * timeit.timeit(lambda: smap_ii(A, B), number=10000))
print("smap_mh\t", 10 * timeit.timeit(lambda: smap_mh(A, B), number=10000))
