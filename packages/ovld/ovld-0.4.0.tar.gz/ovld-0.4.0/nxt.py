from ovld import OvldBase, ovld


class Boop(OvldBase):
    @ovld(priority=100)
    def f(self, x: object):
        return self.f.next(x) * 3

    def f(self, x: int):
        return x * 2


print(Boop().f(7))
