import inspect
from collections import defaultdict


class ArgumentAnalyzer:
    def __init__(self):
        self.name_to_positions = defaultdict(set)
        self.position_to_names = defaultdict(set)
        self.counts = defaultdict(lambda: [0, 0])
        self.total = 0
        self.is_method = None

    def add(self, fn):
        sig = inspect.signature(fn)
        is_method = False
        for i, (name, param) in enumerate(sig.parameters.items()):
            if name == "self":
                assert i == 0
                is_method = True
                continue
            if param.kind is inspect._POSITIONAL_ONLY:
                cnt = self.counts[i]
                self.position_to_names[i].add(None)
            elif param.kind is inspect._POSITIONAL_OR_KEYWORD:
                cnt = self.counts[i]
                self.position_to_names[i].add(param.name)
                self.name_to_positions[param.name].add(i)
            elif param.kind is inspect._KEYWORD_ONLY:
                cnt = self.counts[param.name]
                self.name_to_positions[param.name].add(param.name)
            elif param.kind is inspect._VAR_POSITIONAL:
                raise TypeError("ovld does not support *args")
            elif param.kind is inspect._VAR_KEYWORD:
                raise TypeError("ovld does not support **kwargs")

            cnt[0] += 1 if param.default is inspect._empty else 0
            cnt[1] += 1

        self.total += 1

        if self.is_method is None:
            self.is_method = is_method
        elif self.is_method != is_method:
            raise TypeError(
                "Some, but not all registered methods define `self`. It should be all or none."
            )

    def compile(self):
        if any(
            len(pos) != 1
            for _name, pos in self.name_to_positions.items()
            if (name := _name) is not None
        ):
            raise TypeError(
                f"Argument {name} is found both in a positional and keyword setting."
            )
        npositional = 0
        positional = []
        for pos, names in sorted(self.position_to_names.items()):
            required, total = self.counts[pos]
            name = f"_ovld_arg{pos}"
            if len(names) == 1 and total == self.total:
                name = list(names)[0]
            else:
                npositional = pos + 1
            positional.append((name, required == self.total))

        keywords = []
        for key, (name,) in self.name_to_positions.items():
            if isinstance(name, int):
                pass  # ignore positional arguments
            else:
                assert key == name
                required, total = self.counts[key]
                keywords.append((name, required == self.total))

        return positional[:npositional], positional[npositional:], keywords


anal = ArgumentAnalyzer()


def foo(fn):
    anal.add(fn)


@foo
def f(x, y, *, zou):
    pass


@foo
def f(x, z, *, fax, coop):
    pass


def main():
    po, pn, kw = anal.compile()

    print(po)
    print(pn)
    print(kw)

    template = """
    def __DISPATCH__(self, {args}):
        KWARGS = {{}}
        {body}
        method = self.map[{lookup}]
        return method({posargs}, **KWARGS)
    """

    args = []
    body = [""]
    posargs = []
    lookup = []

    for k, necessary in po:
        txt = k
        if not necessary:
            txt += "=MISSING"
        args.append(txt)

    print(
        template.format(
            args=", ".join(args),
            posargs=", ".join(posargs),
            body="\n    ".join(body),
            lookup=", ".join(lookup),
        )
    )


if __name__ == "__main__":
    main()
