import inspect


def f(x, y, /, z, *, quack):
    pass


print(inspect.getfullargspec(f))
print(sig := inspect.signature(f))

pa = sig.parameters

breakpoint()
