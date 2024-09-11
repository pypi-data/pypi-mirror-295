import json
from collections import defaultdict
from pathlib import Path

file = Path(".benchmarks/Darwin-CPython-3.12-64bit/0011_report.json")
data = json.loads(file.read_text())


grouped = defaultdict(lambda: defaultdict(list))
for bench in data["benchmarks"]:
    match bench["name"].split("_"):
        case (_, _, category, variant):
            bench["category"] = category
            bench["variant"] = variant
        case (_, _, category):
            bench["category"] = category
            bench["variant"] = "normal"
    grouped[bench["group"]][category].append(bench)

columns = [
    ["custom", "custom", None],
    ["ovld", "ovld", "https://github.com/breuleux/ovld"],
    ["plum", "plum", "https://github.com/beartype/plum"],
    ["multimethod", "multim", "https://github.com/coady/multimethod"],
    [
        "multipledispatch",
        "multid",
        "https://github.com/mrocklin/multipledispatch/",
    ],
    ["runtype", "runtype", "https://github.com/erezsh/runtype"],
    ["fastcore", "fastcore", "https://github.com/fastai/fastcore"],
    [
        "singledispatch",
        "sd",
        "https://docs.python.org/3/library/functools.html#functools.singledispatch",
    ],
]
bench_names = ["trivial", "add", "multer", "ast", "calc", "fib", "tweaknum"]


template = "https://github.com/breuleux/ovld/tree/master/benchmarks/test_{}.py"

# print("| Benchmark | custom | ovld | md | plum | mm | runtype | sd |")
headers = [f"[{title}]({lnk})" if lnk else title for _, title, lnk in columns]

print(f"| Benchmark | {' | '.join(headers)} |")
print("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")

for name in bench_names:
    group = grouped[name]
    best = min(
        min(bench["stats"]["median"] for bench in benches)
        for cat, benches in group.items()
        # if cat != "custom"
    )
    loc = template.format(name)
    line = [f"[{name}]({loc})"]
    for column, *_ in columns:
        benches = group.get(column, None)
        if not benches:
            line.append("x")
        else:
            value = min(bench["stats"]["median"] for bench in benches) / best
            line.append(f"{value:.2f}")

    print("|".join(["", *line, ""]))
