from itertools import cycle
from pathlib import Path

Vote = tuple[int, int]
Data = list[Vote]


def parse_data(path: Path) -> Data:
    votes = []
    for line in path.read_text().splitlines():
        vote = tuple(map(int, line.strip().removeprefix('ISO-').removeprefix('ISO2-').split()))
        votes.append(vote)

    return votes


def get_value(vote: Vote) -> int:
    a, b = vote

    bases = []
    while a > 0:
        a, d = divmod(a, 10)
        bases.append(d)

    i, bases, value = 0, cycle(bases), 0
    while b:
        b, d = divmod(b, 10)
        value += d * next(bases) ** i
        i += 1

    return value


def check_vote(vote: Vote) -> int:
    a, b = vote
    value = get_value(vote)

    for c in reversed(range(value, b)):
        if get_value((a, c)) == value:
            return 0

    return value


def run(data: Data, part: int = 0) -> int:
    if part == 3:
        return sum(check_vote(vote) for vote in data)

    return sum(get_value(vote) for vote in data)
