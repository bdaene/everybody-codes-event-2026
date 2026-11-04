from itertools import cycle

Vote = tuple[int, int]
Data = list[Vote]


def parse(text: str) -> Data:
    votes = []
    for line in text.splitlines():
        a, b = map(int, line.partition("-")[2].split())
        votes.append((a, b))

    return votes


def digits(n: int) -> list[int]:
    """Decimal digits of n, least significant first ([0] for 0)."""
    result = []
    while True:
        n, d = divmod(n, 10)
        result.append(d)
        if not n:
            return result


def get_weights(vote: Vote) -> tuple[list[int], list[int]]:
    a, b = vote
    b_digits = digits(b)
    weights = [base**i for i, base in zip(range(len(b_digits)), cycle(digits(a)))]
    return b_digits, weights


def get_value(vote: Vote) -> int:
    b_digits, weights = get_weights(vote)
    return sum(d * w for d, w in zip(b_digits, weights, strict=True))


def check_vote(vote: Vote) -> int:
    b_digits, weights = get_weights(vote)
    value = sum(d * w for d, w in zip(b_digits, weights, strict=True))

    # A smaller c keeps b's higher digits, has a smaller digit at some position and free lower digits.
    reachable, low = {0}, 0  # sums reachable by free lower digits, contribution of b's lower digits
    for d, w in zip(b_digits, weights, strict=True):
        if any(low + (d - c) * w in reachable for c in range(d)):
            return 0
        low += d * w
        reachable = {s + c * w for s in reachable for c in range(10) if s + c * w <= value}

    return value


def part1(data: Data) -> int:
    return sum(get_value(vote) for vote in data)


part2 = part1


def part3(data: Data) -> int:
    return sum(check_vote(vote) for vote in data)
