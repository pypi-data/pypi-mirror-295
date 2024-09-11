# # import dis

# # z = 10


# # def foo(x):
# #     def faf(y):
# #         return x + y + z

# #     return faf


# # fn = foo(4)

# # bytecode = dis.Bytecode(fn)
# # print("=" * 80)
# # for instr in bytecode:
# #     print(instr)

# # breakpoint()


# from wrapt import ObjectProxy

# from ovld import ovld, recurse


# class AnnotatedProxy(ObjectProxy):
#     def __init__(self, wrapped, **ann):
#         super().__init__(wrapped)
#         self._self_ann = ann

#     @property
#     def _(self):
#         return self._self_ann


# # @ovld(priority=10)
# # def f(x: object):
# #     return recurse.next(x)


# @ovld
# def f(xs: list):
#     return [recurse(x) for x in xs]


# @ovld
# def f(xs: dict):
#     return {recurse(k): recurse(v) for k, v in xs.items()}


# @ovld
# def f(x: str):
#     return x


# @ovld
# def f(x: int):
#     return x / 0


# # # f({"a": [[[[1, 2, 3]]]]})
# # # breakpoint()
# # res = f({"a": [[[[1, 2, 3]]]]})
# # print(res)

# # data = {"a": 2}
# # print(f(AnnotatedProxy(data, x=4)))


from ovld import call_next, ovld, recurse


@ovld(priority=10)
def f(x: object):
    return call_next(x)


@ovld
def f(xs: list):
    return [recurse(x) for x in xs]


@ovld
def f(xs: dict):
    return {recurse(k): recurse(v) for k, v in xs.items()}


@ovld
def f(x: str):
    return x


@ovld
def f(x: int):
    return x / 0


print(f([[1, 2]]))
