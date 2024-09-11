from ovld import ovld, recurse

# def g(n):
#     @ovld
#     def f(x: int):
#         return x

#     @ovld
#     def f(x: int, y: int):
#         return recurse(x) + y

#     @ovld
#     def f(x: int, y: int, z: int):
#         return recurse(x, y) + z + n

#     return f


@ovld
def f(x: int):
    return x


@ovld
def f(x: int, y: int):
    return recurse(x) + y


@ovld
def f(x: int, y: int, z: object):
    return recurse(x, y) + z


# def flax(x: int, y: int, z: object, *, w: int = 3):
#     return x + y + z


print(f(3, z=7))
