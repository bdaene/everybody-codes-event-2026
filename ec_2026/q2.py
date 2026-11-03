from collections.abc import Iterable
from itertools import count
from pathlib import Path

Test = list[tuple[int, int]]
Data = list[Test]


def parse_data(path: Path) -> Data:
    tests = []
    for line in path.read_text().splitlines():
        test = []
        for check in line.split():
            a, o, b = check
            test.append((int(a), int(b)) if o == '<' else (int(b), int(a)))
        tests.append(test)

    return tests

def get_order(test: Test) -> list[int]:
    candidates = {a for a, b in test} | {b for a, b in test}
    graph = {a: set() for a in candidates}
    graph_ = {b : set() for b in candidates}
    for a, b in test:
        graph[a].add(b)
        graph_[b].add(a)
        candidates.discard(a)

    order = []
    while candidates:
        a = candidates.pop()
        order.append(a)
        for b in graph_[a]:
            deps = graph[b]
            deps.remove(a)
            if not deps:
                candidates.add(b)

    return order


def run(data: Data, part: int = 0) -> int:
    checksum = 0
    for test in data:
        order = get_order(test)
        number = 0
        for d in order:
            number *= 10
            number += d
        checksum += number

    return checksum


