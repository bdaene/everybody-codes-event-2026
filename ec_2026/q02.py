Test = list[tuple[int, int]]
Data = list[Test]


def parse(text: str) -> Data:
    tests = []
    for line in text.splitlines():
        test = []
        for a, op, b in line.split():
            test.append((int(a), int(b)) if op == "<" else (int(b), int(a)))
        tests.append(test)

    return tests


def get_order(test: Test) -> list[int]:
    """Topological order of the digits, from the (smaller, larger) pairs (Kahn's algorithm)."""
    digits = {digit for pair in test for digit in pair}
    smaller_than = {digit: set() for digit in digits}  # digit -> digits that must come after it
    larger_than = {digit: set() for digit in digits}  # digit -> digits that must come before it
    for smaller, larger in test:
        smaller_than[smaller].add(larger)
        larger_than[larger].add(smaller)

    ready = [digit for digit in digits if not smaller_than[digit]]
    order = []
    while ready:
        digit = ready.pop()
        order.append(digit)
        for other in larger_than[digit]:
            smaller_than[other].remove(digit)
            if not smaller_than[other]:
                ready.append(other)

    return order


def part1(data: Data) -> int:
    return sum(int("".join(map(str, get_order(test)))) for test in data)


part3 = part2 = part1
