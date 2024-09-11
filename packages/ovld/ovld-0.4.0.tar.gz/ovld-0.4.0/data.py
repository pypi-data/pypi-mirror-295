import json
import pickle
import sys
from pathlib import Path
from typing import Callable, Literal

import tomllib
import yaml
from jurigged.loop import loop

from ovld import call_next, ovld, recurse
from ovld.dependent import Dependent, ParametrizedDependentType

File = Dependent[Path, Path.is_file]


class FileType(ParametrizedDependentType):
    def default_bound(self, *_):
        return Path

    def check(self, f):
        return f.suffix == self.parameter


@ovld
def read(s: str):
    return recurse(Path(s))


@ovld
def read(f: File):
    return recurse(f.read_text(), format=f.suffix)


@ovld
def read(x: object, *, format: str | None = None, postprocess: Callable):
    if format is None:
        value = recurse(x)
    else:
        value = recurse(x, format=format)
    return postprocess(value)


@ovld
def read(channel: type(sys.stdin), *, format: str):
    return recurse(channel.read(), format=format)


@ovld
def read(f: File, *, format: Literal[".pickle"]):
    return pickle.load(f)


@ovld
def read(f: File, *, format: str):
    return recurse(f.read_text(), format=format)


@ovld
def read(s: str, *, format: Literal[".json"]):
    return json.loads(s)


@ovld
def read(s: str, *, format: Literal[".yaml"]):
    return yaml.safe_load(s)


@ovld
def read(s: str, *, format: Literal[".toml"]):
    return tomllib.loads(s)


@ovld
def read(xs: list):
    return [recurse(x) for x in xs]


@ovld(priority=-100)
def read(p: object, *, format: str = None):
    raise Exception(f"Could not read: {p}")


@read.variant(priority=100)
def read_only_here(f: File, *, format: str):
    if not f.absolute().is_relative_to("."):
        raise Exception("Can only read files in the current directory.")
    return call_next(f, format=format)


@loop(interface="rich")
def main():
    print(read(Path("../jurigged/pyproject.toml"), format=".toml"))
    print(read("world.yaml"))
    print(read(["world.yaml", "pyproject.toml"]))


if __name__ == "__main__":
    print(main)
    main()
