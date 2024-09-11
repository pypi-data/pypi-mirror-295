from enum import Enum
from types import UnionType

from ovld import ovld
from ovld.core import OvldBase


class Poof[T]:
    pass


class Flax(OvldBase):
    @ovld
    def f(self, x: object, y: type[Poof[object]]):
        return 1234

    def f(self, frm: int, to: type[int]):
        return to(frm)

    def f(self, frm: float, to: type[float]):
        return to(frm)

    def f(self, frm: str, to: type[str]):
        return to(frm)

    def f(self, frm: str, to: type[Enum]):
        return to(frm)

    def f(self, frm: object, to: UnionType):
        for t in to.__args__:
            try:
                return self.deserialize(frm, t)
            except TypeError:
                continue
        else:
            return self.deserialize.next(frm, to)

    def f(self, frm: dict, to: type[Poof[object]]):
        model = self.model(to)
        if model is NotImplemented:
            return self.deserialize.next(frm, to)
        else:
            des = {
                k: self.deserialize(v, model.fields_by_name[k].type)
                for k, v in frm.items()
            }
            return model.builder(**des)

    def f(self, frm: dict, to: type[object]):
        model = self.model(to)
        if model is NotImplemented:
            return self.deserialize.next(frm, to)
        else:
            return self.deserialize(frm, model)

    # def f(self, frm: dict, typ: Model):
    #     des = {k: self.deserialize(v, typ.fields_by_name[k].type) for k, v in frm.items()}
    #     return typ.builder(**des)


@ovld
def f(x: object, y: type[Poof[object]]):
    return 12345


print(f(3, Poof[int]))
print(Flax().f(3, Poof[int]))


# print("=" * 80)
# print(compose_mro(list[int], {list[object]}, set()))

# print("=" * 80)
# print(compose_mro(Poof[int], {Poof[object]}, set()))
