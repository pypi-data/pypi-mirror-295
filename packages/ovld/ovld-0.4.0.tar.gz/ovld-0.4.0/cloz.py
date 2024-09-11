from ovld import ovld


def foo(dispatch, T, fallback):
    @dispatch
    def f(x: T):
        return x * 2

    @dispatch
    def f(x: object):
        return fallback

    return f


f1 = foo(ovld, int, "OK")
print(f1(1))
print(f1("x"))
print(f1(object()))

f2 = foo(ovld, str, "NONONO")
print(f1(1))
print(f1("x"))
print(f1(object()))
