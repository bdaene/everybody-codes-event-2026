from itertools import cycle

Vote = tuple[int, int]
Data = list[Vote]


def parse(text: str) -> Data:
    votes = []
    for line in text.splitlines():
        vote = tuple(map(int, line.strip().removeprefix("ISO-").removeprefix("ISO2-").split()))
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


def part1(data: Data) -> int:
    return sum(get_value(vote) for vote in data)


part2 = part1


def part3(data: Data) -> int:
    return sum(check_vote(vote) for vote in data)
