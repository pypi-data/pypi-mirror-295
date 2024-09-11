from typing import Any

import torch
from torch import Tensor as T

from ovld import Dependent, ParametrizedDependentType, call_next, ovld


class Tensor(ParametrizedDependentType):
    def default_bound(self, *_):
        return T

    @property
    def shape(self):
        return [p for p in self.parameters if p is Any or isinstance(p, int)]

    @property
    def dtype(self):
        for p in self.parameters:
            if isinstance(p, torch.dtype):
                return p
        return Any

    def __lt__(self, other):
        if type(self) is not type(other):
            return False
        pairs = list(
            zip([self.dtype, *self.shape], [other.dtype, *other.shape])
        )
        return any(s1 is Any and s2 is not Any for s1, s2 in pairs) and not any(
            s2 for s1, s2 in pairs if s1 is not Any
        )

    def check(self, value):
        return (
            len(value.shape) == len(self.shape)
            and (self.dtype is Any or self.dtype is value.dtype)
            and all(
                s1 == s2
                for s1, s2 in zip(value.shape, self.shape)
                if s2 is not Any
            )
        )


def on_cpu(x):
    return x.device.type == "cpu"


@ovld(priority=1)
def convert(tensor: Dependent[T, on_cpu]):
    print("I'm on CPU")
    return call_next(tensor)


@ovld
def convert(t2d: Tensor[Any, Any]):
    return "A"


@ovld
def convert(t2d: Tensor[2, 2, torch.float64]):
    return "B"


@ovld
def convert(t2d: Tensor[2, 2]):
    return "C"


a = torch.zeros((2, 2))
print(convert(a))
